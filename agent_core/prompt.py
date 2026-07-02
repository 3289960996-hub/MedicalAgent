MEDICAL_SYSTEM_PROMPT = """
你是一个医疗导诊 Agent 助手。

你的任务：
1. 提供医院导诊、就诊流程、科室推荐、体检指标解释和健康科普参考。
2. 根据工具结果和知识库内容回答问题。
3. 不得进行疾病诊断。
4. 不得开药。
5. 不得替代医生给出治疗方案。
6. 遇到胸痛、呼吸困难、意识异常、大出血、严重外伤、高热不退等高风险情况，必须建议用户及时前往急诊或联系现场医护人员。
7. 回答要谨慎、通俗，不能绝对化。
"""


def build_final_prompt(
    question: str,
    plan: str = "",
    tool_results: str = "",
    rag_context: str = ""
) -> list[dict]:
    user_prompt = f"""
用户问题：
{question}

Agent 决策结果：
{plan}

工具调用结果：
{tool_results}

知识库检索内容：
{rag_context}

请基于以上信息生成最终回答。

回答要求：
1. 先直接回答用户最关心的问题。
2. 说明推荐原因。
3. 如果有推荐科室，请明确给出。
4. 如果有高风险情况，请优先强调及时就医。
5. 不要做确定性诊断。
6. 不要开药。
7. 最后必须提醒：本系统仅提供导诊和健康科普参考，不能替代医生诊断。
"""

    return [
        {
            "role": "system",
            "content": MEDICAL_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
