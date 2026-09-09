import json
import openpyxl
from pathlib import Path
from typing import List, Dict, Any


from app.config import settings
from app.services.aliyun_client import aliyun_client
from app.services.knowledge_graph.models import KnowledgeTriple, KnowledgeGraphRecord


TRIPLE_EXTRACTION_PROMPT = """请从给定数据中提取医学知识三元组（实体-关系-实体），严格按JSON数组格式输出，数组中每个三元组是一个包含三个字符串的小数组。示例输出：
[["高血压","属于","慢性疾病"],["高血压","常见症状","头晕"],["低盐饮食","可改善","高血压"]]
只输出该JSON数组本身，不要输出任何解释、前后缀或代码块标记。待提取的数据如下：
{row_data}"""


def extract_triples_from_row(row_data: str, category: str) -> List[KnowledgeTriple]:
    triples = []
    
    if not aliyun_client.is_configured():
        print(f"  ⚠️ 阿里云API未配置")
        return triples
    
    try:
        messages = [
            {"role": "system", "content": "你是一个知识图谱提取专家"},
            {"role": "user", "content": TRIPLE_EXTRACTION_PROMPT.format(row_data=row_data)}
        ]
        
        result, _ = aliyun_client.chat(
            messages=messages,
            model=settings.aliyun_model,
            temperature=0.3
        )
        
        triples = parse_triples_result(result, category)
        
        return triples
        
    except Exception as e:
        print(f"  ❌ LLM调用失败: {e}")
        return triples


def _clean_entity(value: str) -> str:
    """去除实体/关系两端的中英文引号与空白"""
    return value.strip(' "\'“”‘’')


def parse_triples_result(content: str, category: str) -> List[KnowledgeTriple]:
    triples = []
    try:
        import re

        bracket_match = re.search(r'\[.*\]', content, re.DOTALL)
        if bracket_match:
            array_str = bracket_match.group()
            
            try:
                data = json.loads(array_str)
            except (json.JSONDecodeError, ValueError):
                # 兜底：匹配 (h,r,t) 或 (h, r, t) 形式，支持引号包裹的含逗号字段
                pattern = r'\(\s*["\']?([^"\',\)]+)["\']?\s*,\s*["\']?([^"\',\)]+)["\']?\s*,\s*["\']?([^"\']+?)["\']?\s*\)'
                matches = re.findall(pattern, array_str)
                if matches:
                    data = [[m[0].strip(), m[1].strip(), m[2].strip()] for m in matches]
                else:
                    return triples
            
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, (list, tuple)) and len(item) >= 3:
                        triples.append(KnowledgeTriple(
                            subject=_clean_entity(str(item[0])),
                            predicate=_clean_entity(str(item[1])),
                            object=_clean_entity(str(item[2])),
                            source=category,
                            category=category
                        ))
                    elif isinstance(item, dict):
                        triples.append(KnowledgeTriple(
                            subject=_clean_entity(str(item.get("subject", item.get("h", "")))),
                            predicate=_clean_entity(str(item.get("predicate", item.get("r", "")))),
                            object=_clean_entity(str(item.get("object", item.get("t", "")))),
                            source=category,
                            category=category
                        ))
        
    except Exception as e:
        print(f"  ⚠️ 解析失败: {e}")
    
    return triples


def build_from_excel(file_path: Path):
    print(f"\n📂 正在读取文件: {file_path.name}")
    
    try:
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        sheet = workbook.active
        
        headers = []
        for cell in sheet[1]:
            headers.append(str(cell.value) if cell.value else "")
        
        print(f"   表头: {headers}")
        print(f"   总行数: {sheet.max_row - 1}")
        
    except Exception as e:
        print(f"❌ 读取Excel失败: {e}")
        return None, None
    
    category_name = file_path.stem
    
    all_triples: List[KnowledgeTriple] = []
    
    llm_outputs: List[Dict[str, Any]] = []
    
    print(f"\n🚀 开始构建知识图谱 (共 {sheet.max_row - 1} 行)...")
    
    for row_idx in range(2, sheet.max_row + 1):
        row_data_list = []
        for col_idx in range(1, len(headers) + 1):
            cell = sheet.cell(row=row_idx, column=col_idx)
            value = cell.value
            if value is not None:
                row_data_list.append(str(value))
        
        if not row_data_list:
            continue
        
        row_text = " | ".join([f"{headers[i]}: {row_data_list[i]}" for i in range(len(row_data_list))])
        
        print(f"\n[{row_idx-1}/{sheet.max_row-1}] 处理行数据: {row_text[:80]}...")
        
        triples = extract_triples_from_row(row_text, category_name)
        
        llm_outputs.append({
            "row_index": row_idx,
            "row_data": row_text,
            "triples_count": len(triples)
        })
        
        all_triples.extend(triples)
        
        print(f"   ✅ 提取到 {len(triples)} 个三元组")
    
    log_file = file_path.parent / f"{file_path.stem}_llm_output.json"
    log_data = {
        "file": str(file_path),
        "category": category_name,
        "total_rows": sheet.max_row - 1,
        "total_triples": len(all_triples),
        "outputs": llm_outputs
    }
    log_file.write_text(json.dumps(log_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📝 LLM输出日志已保存: {log_file}")
    
    return all_triples, category_name


