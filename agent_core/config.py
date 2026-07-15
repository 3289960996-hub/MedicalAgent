import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]

load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "project_config" / ".env", override=True)

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen-plus")
LLM_VISION_MODEL = os.getenv("LLM_VISION_MODEL", "qwen3.7-plus")

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "medical_agent")

DOCS_DIR = "data/docs"
VECTOR_DB_DIR = "vector_db"

EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5"


def check_config():
    if not LLM_API_KEY:
        raise ValueError("未检测到 LLM_API_KEY,请在 .env 文件中配置百炼 API Key。")

    if not LLM_BASE_URL:
        raise ValueError("未检测到 LLM_BASE_URL,请在 .env 文件中配置 Qwen base_url。")

    if not LLM_MODEL:
        raise ValueError("未检测到 LLM_MODEL,请在 .env 文件中配置模型名称。")
