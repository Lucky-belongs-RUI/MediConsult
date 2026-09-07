from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional

from app.config import settings
from app.services.aliyun_client import AliyunLLMClientError, aliyun_client
from app.services.knowledge_graph.models import KnowledgeGraphRecord, KnowledgeTriple
from app.services.knowledge_graph.parser import medical_parser
from app.services.knowledge_graph.store import knowledge_graph_store


logger = logging.getLogger(__name__)


TRIPLE_EXTRACTION_PROMPT = """你是一个医学知识图谱专家。请从以下医学文本中提取知识图谱三元组。

要求：
1. 三元组格式：(主体, 关系, 客体)
2. 关系类型包括：属于、症状、治疗、预防、诊断、并发、病因、传播、检查
3. 只提取确定的知识，不要编造
4. 输出JSON格式的数组

医学文本：
{medical_text}

请提取最多20个最重要的三元组，输出格式：
[
  {{"subject": "主体", "predicate": "关系", "object": "客体", "category": "类别"}},
  ...
]

只输出JSON数组，不要其他内容。
"""


CORE_KNOWLEDGE_PROMPT = """你是一个医学专家。请从以下疾病信息中提取核心知识，包括：
1. 疾病名称和ICD编码
2. 主要症状
3. 主要病因
4. 常用治疗方法
5. 预防措施
6. 诊断方法

疾病信息：
{disease_info}

请用简洁的医学语言总结，每项不超过100字。
"""


class TripleGenerator:

    def __init__(self):
        self.parser = medical_parser
        self.store = knowledge_graph_store
    
    def generate_from_file(self, file_path: Path) -> Optional[KnowledgeGraphRecord]:
        try:
            parsed = self.parser.parse_disease_file(file_path)
            
            disease_name = parsed.get("disease_name", file_path.stem)
            sections = parsed.get("sections", {})
            
            core_info = self._extract_core_info(sections)
            
            triples = self._extract_triples_with_llm(core_info, disease_name)
            
            if not triples:
                triples = self._extract_triples_with_rules(sections, disease_name)
            
            return KnowledgeGraphRecord(
                disease_name=disease_name,
                disease_info=core_info,
                triples=triples
            )
            
        except Exception as e:
            logger.error(f"从文件生成知识图谱失败: {file_path}, 错误: {e}")
            return None
    
    def _extract_core_info(self, sections: Dict[str, str]) -> Dict[str, str]:
        core = {}
        
        if "summary" in sections:
            core["概述"] = sections["summary"][:500]
        
        if "etiology" in sections:
            core["病因"] = sections["etiology"][:300]
        elif "pathogen" in sections:
            core["病因"] = sections["pathogen"][:300]
        
        if "clinical_manifestations" in sections:
            core["临床表现"] = sections["clinical_manifestations"][:500]
        
        if "treatment" in sections:
            core["治疗"] = sections["treatment"][:500]
        
        if "prevention" in sections:
            core["预防"] = sections["prevention"][:300]
        
        if "diagnosis" in sections:
            core["诊断"] = sections["diagnosis"][:300]
        
        if "epidemiology" in sections:
            core["流行病学"] = sections["epidemiology"][:300]
        
        return core
    
    def _extract_triples_with_llm(self, core_info: Dict[str, str], disease_name: str) -> List[KnowledgeTriple]:
        if not aliyun_client.is_configured():
            return []
        
        try:
            medical_text = f"疾病名称: {disease_name}\n\n"
            for key, value in core_info.items():
                medical_text += f"【{key}】\n{value}\n\n"
            
            messages = [
                {"role": "system", "content": "你是一个医学知识图谱专家，擅长从医学文本中提取结构化的知识三元组。"},
                {"role": "user", "content": TRIPLE_EXTRACTION_PROMPT.format(medical_text=medical_text)}
            ]
            
            content, _ = aliyun_client.chat(
                messages=messages,
                model=settings.aliyun_model,
                temperature=0.3
            )
            
            triples = self._parse_llm_response(content, disease_name)
            logger.info(f"从LLM提取到 {len(triples)} 个三元组")
            return triples
            
        except AliyunLLMClientError as e:
            logger.warning(f"LLM提取三元组失败: {e}")
            return []
        except Exception as e:
            logger.error(f"提取三元组时发生错误: {e}")
            return []
    
    def _parse_llm_response(self, content: str, source: str) -> List[KnowledgeTriple]:
        import json

        triples = []
        
        try:
            start = content.find('[')
            end = content.rfind(']') + 1
            
            if start >= 0 and end > start:
                json_str = content[start:end]
                data = json.loads(json_str)
                
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            triple = KnowledgeTriple(
                                subject=item.get("subject", "").strip(),
                                predicate=item.get("predicate", "").strip(),
                                object=item.get("object", "").strip(),
                                source=source,
                                category=item.get("category", "其他")
                            )
                            if triple.subject and triple.predicate and triple.object:
                                triples.append(triple)
        except Exception as e:
            logger.warning(f"解析LLM响应失败: {e}")
        
        return triples
    
    def _extract_triples_with_rules(self, sections: Dict[str, str], disease_name: str) -> List[KnowledgeTriple]:
        triples = []
        
        if "summary" in sections:
            summary = sections["summary"][:200]
            triples.append(KnowledgeTriple(
                subject=disease_name,
                predicate="定义",
                object=summary[:50],
                source=disease_name,
                category="概述"
            ))
        
        if "etiology" in sections or "pathogen" in sections:
            etext = (sections.get("etiology", "") or sections.get("pathogen", ""))[:100]
            if etext:
                triples.append(KnowledgeTriple(
                    subject=disease_name,
                    predicate="病因",
                    object=etext,
                    source=disease_name,
                    category="病因"
                ))
        
        if "clinical_manifestations" in sections:
            symptoms_text = sections["clinical_manifestations"][:200]
            symptom_keywords = ["发热", "咳嗽", "头痛", "乏力", "呕吐", "腹泻", "胸闷", "呼吸困难"]
            for kw in symptom_keywords:
                if kw in symptoms_text:
                    triples.append(KnowledgeTriple(
                        subject=disease_name,
                        predicate="症状",
                        object=kw,
                        source=disease_name,
                        category="症状"
                    ))
        
        if "treatment" in sections:
            treatment = sections["treatment"][:100]
            triples.append(KnowledgeTriple(
                subject=disease_name,
                predicate="治疗",
                object=treatment,
                source=disease_name,
                category="治疗"
            ))
        
        if "prevention" in sections:
            prevention = sections["prevention"][:100]
            triples.append(KnowledgeTriple(
                subject=disease_name,
                predicate="预防",
                object=prevention,
                source=disease_name,
                category="预防"
            ))
        
        return triples
    
    def build_knowledge_graph(self, data_dir: Path) -> Dict[str, any]:
        disease_files = list(data_dir.rglob("*.txt"))
        
        if not disease_files:
            medical_data_dir = settings.BASE_DIR / "data" / "医疗大模型预训练医疗知识数据集样例"
            if medical_data_dir.exists():
                disease_files = list(medical_data_dir.rglob("*.txt"))
        
        if not disease_files:
            return {
                "success": False,
                "message": "未找到医学知识文件"
            }
        
        records = []
        for file_path in disease_files:
            record = self.generate_from_file(file_path)
            if record:
                records.append(record)
        
        self.store.save(records)
        
        return {
            "success": True,
            "disease_count": len(records),
            "triple_count": sum(len(r.triples) for r in records)
        }
    


triple_generator = TripleGenerator()
