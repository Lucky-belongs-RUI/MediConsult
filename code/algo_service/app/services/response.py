from __future__ import annotations

from typing import Any, Dict


SUCCESS_CODE = 200
ERROR_CODE = -1


def success(data: Any = None, msg: str = "success") -> Dict[str, Any]:
    return {"code": SUCCESS_CODE, "msg": msg, "data": data}


def error(msg: str, code: int = ERROR_CODE, data: Any = None) -> Dict[str, Any]:
    return {"code": code, "msg": msg, "data": data}
