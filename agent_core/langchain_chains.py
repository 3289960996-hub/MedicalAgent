from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

import os

from agent_core.llm import call_llm
from agent_core.prompt import MEDICAL_SYSTEM_PROMPT


def configure_langsmith_tracing() -> None:
    api_key = os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY")
    project = os.getenv("LANGSMITH_PROJECT") or os.getenv("LANGCHAIN_PROJECT") or "MedicalAgent-LangGraph"

    if not api_key:
        return

    os.environ.setdefault("LANGSMITH_API_KEY", api_key)
    os.environ.setdefault("LANGCHAIN_API_KEY", api_key)
    os.environ.setdefault("LANGSMITH_TRACING", "true")
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGSMITH_PROJECT", project)
    os.environ.setdefault("LANGCHAIN_PROJECT", project)


configure_langsmith_tracing()


def _message_to_dict(message) -> dict:
    role = getattr(message, "type", "human")
    if role == "human":
        role = "user"
    elif role == "ai":
        role = "assistant"

    return {
        "role": role,
        "content": message.content
    }


def _call_qwen_with_prompt(prompt_value) -> str:
    messages = [
        _message_to_dict(message)
        for message in prompt_value.to_messages()
    ]
    return call_llm(messages)


qwen_llm = RunnableLambda(_call_qwen_with_prompt)


final_answer_prompt = ChatPromptTemplate.from_messages([
    ("system", MEDICAL_SYSTEM_PROMPT),
    (
        "user",
        """
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
5. 不要诊断疾病。
6. 不要开药。
7. 最后必须提醒：本系统仅提供导诊和健康科普参考，不能替代医生诊断。
"""
    )
])

qwen_followup_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
你是医院智能导诊问诊助手。

你的任务：
根据患者当前描述，判断为了完成导诊还缺少哪些关键信息，并生成最必要的追问问题。

核心原则：
1. 必须根据患者的具体病情动态生成追问。
2. 不允许使用固定模板套所有症状。
3. 不允许所有患者都问同一套问题。
4. 每个追问都必须和当前主诉直接相关。
5. 已经在患者描述中出现的信息，不要重复追问。
6. 每次最多追问 3 个问题。
7. 如果信息已经足够推荐科室，need_followup 必须为 false。
8. 如果已追问次数 >= 1，need_followup 必须为 false。
9. 不能诊断疾病。
10. 不能开药。
11. 不能给治疗方案。
12. 必须严格返回 JSON，不要输出 Markdown，不要输出解释文字。

你生成追问时，应优先考虑这些导诊关键信息：
- 症状持续时间
- 症状部位
- 症状严重程度
- 是否持续加重
- 伴随症状
- 是否存在急诊红旗信号
- 是否有外伤
- 是否有过敏或接触史
- 是否有用药史
- 是否有既往病史
- 是否影响呼吸、吞咽、意识、行走、活动能力等重要功能

注意：
你不能机械地把上面的所有项目都问一遍。
你必须根据患者当前症状，选择最影响导诊判断的 1 到 3 个问题。

导诊科室判断要求：
- 咽喉、鼻部、耳部相关不适，优先考虑耳鼻喉科。
- 皮肤瘙痒、红疹、过敏、水疱等，优先考虑皮肤科。
- 牙疼、牙龈肿、口腔疼痛等，优先考虑口腔科。
- 眼红、眼痛、视力下降、畏光等，优先考虑眼科。
- 咳嗽、咳痰、胸闷、气短等，优先考虑呼吸内科。
- 腹痛、腹泻、恶心、呕吐、胃胀等，优先考虑消化内科。
- 摔伤、扭伤、骨折、关节痛、活动受限等，优先考虑骨科。
- 痔疮、肛门疼、肛门瘙痒、便血、肛裂、肛周肿痛等，优先考虑肛肠科。
- 伤口、体表包块、疝气、脓肿、皮下肿块、外科换药等，优先考虑普外科。
- 尿痛、尿频、尿急、血尿、排尿困难、尿不尽等，优先考虑泌尿外科。
- 月经不调、痛经、白带异常、阴道出血、外阴瘙痒等，优先考虑妇科。
- 儿童、孩子、小孩、宝宝、婴儿、幼儿相关症状，优先考虑儿科。
- 头痛、头晕、眩晕、手脚麻木、肢体无力、说话不清、面瘫、抽搐等，优先考虑神经内科。
- 胸痛、胸闷、心慌、心悸、心跳快、血压高等，优先考虑心内科。
- 糖尿病、血糖高、甲亢、甲减、甲状腺、肥胖、多饮多尿等，优先考虑内分泌科。
- 关节肿痛、多关节痛、晨僵、风湿、类风湿、痛风、尿酸高等，优先考虑风湿免疫科。
- 术后康复、运动康复、腰腿康复、偏瘫康复、功能恢复等，优先考虑康复医学科。
- 焦虑、抑郁、失眠、情绪低落、压力大、睡不着等，优先考虑精神心理科。
- 持续高热、发热伴皮疹、疑似传染病、近期接触感染患者等，优先考虑感染科/发热门诊。
- 乳房疼、乳房肿块、乳头溢液、乳腺结节、乳房红肿等，优先考虑乳腺外科。
- 高热、呼吸困难、意识异常、大量出血、剧烈胸痛、严重外伤、迅速加重等，优先考虑急诊或转人工。

重要：
如果患者描述很简单，比如“嗓子疼”“牙疼”“皮肤痒”，不要直接给最终结论，应优先追问影响导诊和风险判断的关键信息。
如果患者已经描述了持续时间、伴随症状、严重程度和危险信号情况，可以不再追问。

返回 JSON 格式必须严格如下：
{{
  "need_followup": true/false,
  "follow_up_questions": [],
  "follow_up_items": [
    {{
      "question": "动态追问问题",
      "options": ["动态选项1", "选项2", "选项3", "选项4"]
    }}
  ],
  "preliminary_department": "",
  "risk_level": "low/medium/high",
  "reason": ""
}}
"""
    ),
    (
        "user",
        """
患者描述：
{question}

上一轮缺失信息：
{previous_missing}

上一轮初步判断：
{previous_result}

已追问次数：
{followup_count}

请根据患者当前描述，动态判断还缺少哪些导诊关键信息。

要求：
1. 追问必须针对当前病情。
2. 不要使用固定模板。
3. 不要重复患者已经说过的信息。
4. 最多追问 3 个问题。
5. 如果已追问次数 >= 1，need_followup 必须为 false。
6. 必须严格返回 JSON。
"""
    )
])

triage_analysis_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
你是医院智能导诊病情分析助手。

任务：
根据患者具体病情语义进行导诊分析，推荐合适科室、风险等级、可能方向和必要追问。

严格要求：
1. 根据患者具体描述分析，不靠固定关键词模板。
2. 只能使用“可能”“疑似”“建议”等不确定表达，不能确诊。
3. 不能开药。
4. 不能给治疗方案。
5. 每次最多追问 3 个问题。
6. 追问问题和选项必须根据病情动态生成。
7. 严格返回 JSON，不要 Markdown，不要解释文字。
8. 如果存在呼吸困难、意识异常、大量出血、剧烈胸痛、严重外伤、持续高热、迅速加重、无法行走、明显畸形，应标记 high，并建议急诊科/转人工。

可用标准科室包括：
急诊科、发热门诊、全科医学科、儿科、口腔科、肛肠科、普外科、呼吸内科、消化内科、耳鼻喉科、眼科、感染科/发热门诊、心内科、神经内科、内分泌科、泌尿外科、妇科、乳腺外科、骨科、皮肤科、风湿免疫科、康复医学科、精神心理科。

返回 JSON 格式必须严格如下：
{{
  "symptom_summary": "",
  "possible_conditions": [],
  "recommended_department": "",
  "canonical_department": "",
  "risk_level": "low/medium/high",
  "confidence": 0.0,
  "red_flags": [],
  "reason": "",
  "need_followup": true/false,
  "follow_up_items": [
    {{
      "question": "",
      "options": []
    }}
  ]
}}
"""
    ),
    (
        "user",
        """
患者描述：
{question}

已追问次数：
{followup_count}

上一轮初步判断：
{previous_result}

请返回严格 JSON。若已追问次数 >= 1，need_followup 必须为 false。
"""
    )
])


final_answer_chain = final_answer_prompt | qwen_llm | StrOutputParser()
qwen_followup_chain = qwen_followup_prompt | qwen_llm | StrOutputParser()
triage_analysis_chain = triage_analysis_prompt | qwen_llm | StrOutputParser()
qwen_messages_chain = RunnableLambda(call_llm) | StrOutputParser()


def run_final_answer_chain(
    question: str,
    plan: dict,
    tool_results: list,
    rag_context: str
) -> str:
    return final_answer_chain.invoke({
        "question": question,
        "plan": plan,
        "tool_results": tool_results,
        "rag_context": rag_context
    })


def run_qwen_followup_chain(
    question: str,
    previous_missing: list,
    previous_result: dict,
    followup_count: int
) -> str:
    return qwen_followup_chain.invoke({
        "question": question,
        "previous_missing": previous_missing,
        "previous_result": previous_result,
        "followup_count": followup_count
    })


def run_triage_analysis_chain(
    question: str,
    followup_count: int = 0,
    previous_result: dict | None = None
) -> str:
    return triage_analysis_chain.invoke({
        "question": question,
        "followup_count": followup_count,
        "previous_result": previous_result or {}
    })


def run_messages_chain(messages: list[dict]) -> str:
    return qwen_messages_chain.invoke(messages)
