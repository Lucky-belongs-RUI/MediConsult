from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import settings
@dataclass
class DocumentPayload:
    object_key: str
    file_name: str
    summary: Dict[str, str]


class DocumentBuilder:
    def __init__(self, docs_dir: Optional[Path] = None) -> None:
        self.docs_dir = docs_dir or settings.docs_dir
        self.docs_dir.mkdir(parents=True, exist_ok=True)

    def _write_document(self, content: str, prefix: str) -> DocumentPayload:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        object_key = f"{prefix}-{timestamp}.md"
        file_path = self.docs_dir / object_key
        file_path.write_text(content, encoding="utf-8")
        return DocumentPayload(object_key=object_key, file_name=object_key, summary={})

    def build_case_document(self, case: Dict[str, Any]) -> DocumentPayload:
        content = ["# 病例档案\n"]
        content.append(f"## 基本信息\n- 标题：{case.get('title','未命名病例')}\n- 科室：{case.get('categoryName','未指定')}\n")
        content.append("## 病情描述\n")
        content.append(case.get("description", "暂无描述") + "\n")
        if case.get("tags"):
            content.append(f"## 关键词\n{case['tags']}\n")
        extra_data = case.get("extraData")
        if isinstance(extra_data, (dict, list)):
            content.append("## 额外信息\n")
            content.append(json.dumps(extra_data, ensure_ascii=False, indent=2) + "\n")
        payload = self._write_document("\n".join(content), prefix=f"case-{case.get('id','unknown')}")
        payload.summary = {
            "title": case.get("title", "未命名病例"),
            "category": case.get("categoryName", "未指定"),
        }
        return payload

    def build_chat_document(self, session: Dict[str, Any], messages: List[Dict[str, Any]]) -> DocumentPayload:
        content = ["# 问诊对话记录\n"]
        content.append(f"## 会话信息\n- 会话ID：{session.get('id','未知')}\n- 会话名：{session.get('sessionName','未命名')}\n")
        content.append("## 对话明细\n")
        for message in messages:
            role = "患者" if message.get("role") == "user" else "AI医生"
            content.append(f"- **{role}**：{message.get('content','')}\n")
        payload = self._write_document("\n".join(content), prefix=f"session-{session.get('id','unknown')}")
        payload.summary = {
            "sessionName": session.get("sessionName", "未命名会话"),
            "messageCount": str(len(messages)),
        }
        return payload


document_builder = DocumentBuilder()
