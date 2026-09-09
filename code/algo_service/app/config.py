from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_FILE = BASE_DIR / "config.env"


def _load_env_file(file_path: Path) -> None:
    if not file_path.exists():
        return
    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


CONFIG_FILE = Path(os.getenv("ALGO_CONFIG_FILE", DEFAULT_CONFIG_FILE))
_load_env_file(CONFIG_FILE)


DATA_DIR = Path(os.getenv("ALGO_DATA_DIR", BASE_DIR / "data"))
DOCS_DIR = Path(os.getenv("ALGO_DOCS_DIR", DATA_DIR / "docs"))
FILE_STORAGE_ROOT = Path(os.getenv("FILE_STORAGE_ROOT", DATA_DIR / "files"))
VECTOR_INDEX_FILE = Path(os.getenv("ALGO_VECTOR_INDEX", DATA_DIR / "vector_index.json"))
SPRINGBOOT_API_BASE = os.getenv("SPRINGBOOT_API_BASE", "http://localhost:8090/api")
FILE_SERVICE_BASE = os.getenv("FILE_SERVICE_BASE", "http://localhost:5000")
ALIYUN_API_BASE = os.getenv("ALIYUN_API_BASE", "https://open.bigmodel.cn/api/paas/v4")
ALIYUN_API_KEY = os.getenv("ALIYUN_API_KEY")
ALIYUN_MODEL = os.getenv("ALIYUN_MODEL", "glm-4-flash")


def _load_timeout(env_key: str, default: float) -> float:
    value = os.getenv(env_key)
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


ALIYUN_TIMEOUT = _load_timeout("ALIYUN_TIMEOUT", 30.0)


for folder in {DATA_DIR, DOCS_DIR, FILE_STORAGE_ROOT}:
    folder.mkdir(parents=True, exist_ok=True)


@dataclass(slots=True)
class Settings:
    app_name: str = "Medical Consultation Algorithm Service"
    springboot_api_base: str = SPRINGBOOT_API_BASE.rstrip("/")
    file_service_base: str = FILE_SERVICE_BASE.rstrip("/")
    vector_index_file: Path = VECTOR_INDEX_FILE
    docs_dir: Path = DOCS_DIR
    data_dir: Path = DATA_DIR
    file_storage_root: Path = FILE_STORAGE_ROOT
    aliyun_api_base: str = ALIYUN_API_BASE.rstrip("/")
    aliyun_api_key: Optional[str] = ALIYUN_API_KEY
    aliyun_model: str = ALIYUN_MODEL
    aliyun_timeout: float = ALIYUN_TIMEOUT
    BASE_DIR: Path = BASE_DIR


settings = Settings()
