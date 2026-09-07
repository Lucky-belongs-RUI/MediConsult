import asyncio
import json
import sys
import openpyxl
from pathlib import Path
from typing import List, Dict, Any

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from app.config import settings
from app.services.aliyun_client import aliyun_client
from app.services.knowledge_graph.models import KnowledgeTriple, KnowledgeGraphRecord


TRIPLE_EXTRACTION_PROMPT = """你是一名知识图谱提取专家，负责提取数据中涉及到的三元组，严格按[(h,r,t),、、、、]格式输出，数据为{row_data}。"""


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


def parse_triples_result(content: str, category: str) -> List[KnowledgeTriple]:
    triples = []
    try:
        import re

        bracket_match = re.search(r'\[.*\]', content, re.DOTALL)
        if bracket_match:
            array_str = bracket_match.group()
            
            try:
                data = json.loads(array_str)
            except:
                pattern = r'\(([^,]+),([^,]+),([^)]+)\)'
                matches = re.findall(pattern, array_str)
                if matches:
                    data = [[m[0].strip(), m[1].strip(), m[2].strip()] for m in matches]
                else:
                    return triples
            
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, (list, tuple)) and len(item) >= 3:
                        triples.append(KnowledgeTriple(
                            subject=str(item[0]).strip(),
                            predicate=str(item[1]).strip(),
                            object=str(item[2]).strip(),
                            source=category,
                            category=category
                        ))
                    elif isinstance(item, dict):
                        triples.append(KnowledgeTriple(
                            subject=str(item.get("subject", item.get("h", ""))).strip(),
                            predicate=str(item.get("predicate", item.get("r", ""))).strip(),
                            object=str(item.get("object", item.get("t", ""))).strip(),
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


async def build_from_directory(data_dir: Path):
    xlsx_files = list(data_dir.rglob("*.xlsx"))
    
    if not xlsx_files:
        print(f"❌ 未找到Excel文件")
        return
    
    print(f"✅ 找到 {len(xlsx_files)} 个Excel文件\n")
    
    print("📋 可用的Excel文件:")
    for i, f in enumerate(xlsx_files):
        print(f"  [{i+1}] {f.name}")
    print(f"  [0] 全部构建")
    
    choice = input("\n请选择要构建的文件 (输入编号): ").strip()
    
    selected_files = []
    if choice == "0":
        selected_files = xlsx_files
    elif choice.isdigit() and 1 <= int(choice) <= len(xlsx_files):
        selected_files = [xlsx_files[int(choice) - 1]]
    else:
        print("❌ 无效选择")
        return
    
    all_records: List[KnowledgeGraphRecord] = []
    
    for file_path in selected_files:
        triples, category = build_from_excel(file_path)
        
        if triples:
            # 按文件名作为大类
            record = KnowledgeGraphRecord(
                disease_name=category,
                disease_info={"source": str(file_path), "row_count": len(triples)},
                triples=triples
            )
            all_records.append(record)
    
    output_file = data_dir / "knowledge_graph.json"
    
    payload = {
        "count": len(all_records),
        "total_triples": sum(len(r.triples) for r in all_records),
        "records": [r.as_dict() for r in all_records]
    }
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"\n" + "="*50)
    print(f"✅ 知识图谱构建完成!")
    print(f"   类别数量: {len(all_records)}")
    print(f"   三元组总数: {sum(len(r.triples) for r in all_records)}")
    print(f"   保存位置: {output_file}")
    print(f"="*50 + "\n")


async def main():
    print("\n" + "="*50)
    print("🏥 医学知识图谱构建工具 (Excel版)")
    print("="*50)
    
    if len(sys.argv) > 1:
        data_path = Path(sys.argv[1])
    else:
        data_path = settings.BASE_DIR / "data" / "test" / "yaopin"
        if not data_path.exists():
            data_path = settings.BASE_DIR / "data"
    
    if not data_path.exists():
        print(f"❌ 路径不存在: {data_path}")
        return
    
    if data_path.is_file() and data_path.suffix == ".xlsx":
        # 直接处理单个文件
        triples, category = build_from_excel(data_path)
        
        # 保存
        output_file = data_path.parent / "knowledge_graph.json"
        
        record = KnowledgeGraphRecord(
            disease_name=category,
            disease_info={"source": str(data_path)},
            triples=triples
        )
        
        payload = {
            "count": 1,
            "total_triples": len(triples),
            "records": [record.as_dict()]
        }
        
        output_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        
        print(f"\n✅ 完成! 保存到: {output_file}")
        
    else:
        # 处理目录
        await build_from_directory(data_path)


if __name__ == "__main__":
    asyncio.run(main())
