from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional

from app.config import settings


class MedicalDataParser:

    FIELD_MAPPING = {
        "基本信息": ["disease_name", "english_name", "alias", "icd_code"],
        "概述": "summary",
        "病原": "pathogen",
        "病原学": "pathogen",
        "流行病学": "epidemiology",
        "临床表现": "clinical_manifestations",
        "实验室检查": "lab_examination",
        "诊断与鉴别诊断": "diagnosis",
        "诊断": "diagnosis",
        "治疗": "treatment",
        "预防": "prevention",
        "病因": "etiology",
    }
    
    def __init__(self, docs_dir: Optional[Path] = None):
        self.docs_dir = docs_dir or settings.docs_dir
    
    def parse_disease_file(self, file_path: Path) -> Dict:
        content = file_path.read_text(encoding="utf-8")
        return self.parse_disease_content(content)
    
    def parse_disease_content(self, content: str) -> Dict:
        clean_content = self._remove_html_tags(content)
        
        disease_name = self._extract_disease_name(clean_content)
        
        sections = self._extract_sections(clean_content)
        
        return {
            "disease_name": disease_name,
            "sections": sections,
            "full_text": clean_content
        }
    
    def _remove_html_tags(self, content: str) -> str:
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

        content = re.sub(r'<br\s*/?>', '\n', content, flags=re.IGNORECASE)
        content = re.sub(r'</p>', '\n\n', content, flags=re.IGNORECASE)
        content = re.sub(r'</div>', '\n', content, flags=re.IGNORECASE)
        content = re.sub(r'</h\d>', '\n', content, flags=re.IGNORECASE)
        content = re.sub(r'</li>', '\n', content, flags=re.IGNORECASE)
        
        content = re.sub(r'<[^>]+>', '', content)

        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r' {2,}', ' ', content)
        
        return content.strip()
    
    def _extract_disease_name(self, content: str) -> str:
        patterns = [
            r'^([^\n]{2,30})(?=\n|$)',  # 首行作为疾病名
            r'疾病名称[：:]\s*([^\n]+)',
            r'<li class="disease_name">([^<]+)</li>',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                name = match.group(1).strip()
                if name and len(name) > 1:
                    return name
        
        first_line = content.split('\n')[0].strip()
        return first_line[:50] if first_line else "未知疾病"
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        sections = {}
        
        section_titles = [
            "基本信息", "概述", "病原", "病原学", "流行病学",
            "临床表现", "实验室检查", "诊断与鉴别诊断", "诊断",
            "治疗", "预防", "病因", "发病机制", "并发症",
            "辅助检查", "鉴别诊断", "预后", "护理"
        ]
        
        title_pattern = '|'.join(re.escape(t) for t in section_titles)
        pattern = rf'(?:^|\n)({title_pattern})(?:[：:\s]*)([\s\S]*?)(?=(?:{title_pattern})(?:[：:\s])|$)'
        
        matches = re.finditer(pattern, content, re.MULTILINE)
        
        for match in matches:
            title = match.group(1).strip()
            content_text = match.group(2).strip()
            if title and content_text:
                key = self.FIELD_MAPPING.get(title, title)
                sections[key] = content_text[:2000]  # 限制长度
        
        return sections
    
    def extract_key_info(self, sections: Dict[str, str]) -> Dict[str, str]:
        key_info = {}
        
        if "etiology" in sections or "病原" in sections:
            key_info["etiology"] = sections.get("etiology", "")[:500]
        
        if "clinical_manifestations" in sections:
            text = sections["clinical_manifestations"]
            symptoms = self._extract_symptoms(text)
            key_info["symptoms"] = symptoms
        
        if "treatment" in sections:
            key_info["treatment"] = sections["treatment"][:500]
        
        if "prevention" in sections:
            key_info["prevention"] = sections["prevention"][:500]
        
        return key_info
    
    def _extract_symptoms(self, text: str) -> str:
        symptom_keywords = [
            "发热", "咳嗽", "头痛", "乏力", "全身酸痛", "畏寒", "高热",
            "鼻塞", "流涕", "咽痛", "干咳", "腹泻", "呕吐", "恶心",
            "胸闷", "气短", "呼吸困难", "腹痛", "皮疹", "瘙痒"
        ]
        
        found = []
        for symptom in symptom_keywords:
            if symptom in text:
                found.append(symptom)
        
        return "，".join(found) if found else ""


medical_parser = MedicalDataParser()
