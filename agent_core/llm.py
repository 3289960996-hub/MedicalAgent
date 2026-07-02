from openai import OpenAI
from agent_core.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, check_config

check_config()

client = OpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL
)


def call_llm(messages: list[dict], temperature: float = 0.3) -> str:
    """
    调用 Qwen / 阿里云百炼 OpenAI 兼容接口。
    """
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=temperature
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"大模型调用失败：{str(e)}"
