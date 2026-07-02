# MedicalAgent

基于大模型的智能分诊与就医路径推荐系统。项目面向学习、课程设计和实习展示场景，围绕用户的症状描述，完成意图识别、风险分级、科室推荐、动态追问、就医路径推荐、报告解读和人工转接判断。

本项目保留现有 LangGraph/Agent 流程，通过 FastAPI 提供后端接口，并提供静态前端页面用于演示完整导诊链路。

## 技术栈

- Python 3.12
- FastAPI / Uvicorn
- LangGraph / LangChain
- OpenAI 兼容接口，用于调用 Qwen 等大模型
- ChromaDB / sentence-transformers，用于本地医学知识库检索
- SQLAlchemy / PyMySQL，用于可选的科室位置等结构化数据
- HTML / CSS / JavaScript，用于前端演示页面

## 核心功能

- 症状输入与意图识别：识别用户输入中的症状、部位、持续时间和就医诉求。
- 风险等级判断：根据胸痛、呼吸困难、意识异常、大量出血等高危信号给出 high / medium / low 风险等级。
- 科室推荐：结合规则、LLM 分析和兜底逻辑推荐合适科室。
- 动态追问：当症状信息不足时，生成一轮关键追问，补齐导诊所需信息。
- 就医路径推荐：返回科室位置、楼层区域、挂号流程和就诊准备建议。
- 报告智能解读：对体检或检验报告相关问题给出指标解释和就医建议方向。
- 人工转接判断：识别高风险、低置信度或超出系统能力边界的问题，建议人工导诊或现场医护介入。

## 系统流程

1. 用户在前端或命令行输入症状描述。
2. FastAPI `/chat` 接口接收请求并维护会话状态。
3. `agent_core.medical_graph.run_medical_graph()` 初始化导诊状态。
4. LangGraph 按节点执行：业务边界判断 -> 风险分级 -> 症状/意图分析 -> 科室推荐 -> 院内位置查询 -> 挂号流程生成 -> 动态追问判断。
5. 若信息不足，系统返回追问问题；若信息足够，继续执行 RAG 检索、人工转接判断和最终回答生成。
6. 前端或命令行展示风险等级、推荐科室、就医路径、参考依据和免责声明。

## 架构图

```mermaid
flowchart TD
    A[用户症状输入] --> B[FastAPI /chat]
    B --> C[LangGraph MedicalAgentState]
    C --> D[业务边界判断]
    D --> E[风险等级判断]
    E --> F[症状与意图分析]
    F --> G[科室推荐]
    G --> H[院内位置与挂号流程]
    H --> I{是否需要追问}
    I -- 是 --> J[返回动态追问]
    I -- 否 --> K[RAG 知识库检索]
    K --> L[人工转接判断]
    L --> M[生成导诊建议]
    M --> N[前端/命令行展示]
```

## 目录结构

```text
MedicalAgent/
├── agent_core/          # LangGraph 流程、LLM 调用、提示词和结果结构
├── backend/             # FastAPI 后端入口
├── data/                # 医学知识文档和模拟医院地图数据
├── docs/                # 项目文档和报告
├── frontend/            # 静态前端演示页面
├── rag/                 # RAG 文档切分、向量库构建和检索
├── scripts/             # 辅助脚本和检查脚本
├── tools/               # 风险分级、科室推荐、追问、RAG、人工转接等工具
├── app.py               # 后端兼容入口，导出 backend.app
├── graph.py             # LangGraph 兼容入口，导出 agent_core.graph
├── main.py              # 最小命令行 demo 入口
├── medical_graph.py     # 导诊流程兼容入口
├── requirements.txt     # pip 依赖列表
└── langgraph.json       # LangGraph 本地运行配置
```

## 安装方式

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

如需调用大模型，请在 `project_config/.env` 或根目录 `.env` 中配置：

```env
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus
```

## 运行方式

运行命令行最小 demo：

```bash
python main.py "我发烧咳嗽两天了，应该挂什么科？"
```

启动后端服务：

```bash
uvicorn backend.app:app --reload
```

访问接口文档：

```text
http://127.0.0.1:8000/docs
```

前端页面位于 `frontend/index.html`。启动后端后，可直接用浏览器打开该文件进行演示。

如需重建本地 RAG 向量库，可在服务启动后请求：

```bash
curl -X POST http://127.0.0.1:8000/build
```

运行单元测试：

```bash
python -m pytest -q
```

使用 Docker 启动后端：

```bash
docker compose up --build
```

启动后访问：

```text
http://127.0.0.1:8000/docs
```

## 示例输入输出

可以直接运行内置 demo：

```bash
python main.py --case all
```

### 示例一：普通感冒/咳嗽类低风险

输入：

```text
我咳嗽两天了，有点流鼻涕，没有胸痛，也没有呼吸困难，应该挂什么科？
```

示例输出：

```json
{
  "risk_level": "low",
  "recommended_department": "呼吸内科",
  "need_followup": true,
  "follow_up_questions": [
    "症状持续多久了？是否伴随发热、胸闷、呼吸困难或基础疾病？"
  ]
}
```

### 示例二：胃痛/发热类中风险

输入：

```text
我胃痛持续三天了，今天还有点发热和恶心，应该去哪个科？
```

示例输出：

```json
{
  "risk_level": "medium",
  "recommended_department": "消化内科",
  "need_followup": true,
  "visit_guide": "建议携带身份证、医保卡和既往检查资料，按医院挂号流程前往对应科室。"
}
```

### 示例三：胸痛/呼吸困难类高风险

输入：

```text
我突然胸痛，喘不上气，还有明显呼吸困难，现在应该怎么办？
```

示例输出：

```json
{
  "risk_level": "high",
  "recommended_department": "急诊科",
  "need_followup": false,
  "answer": "根据当前描述，建议优先考虑急诊科。该结果仅作为导诊参考。"
}
```

说明：默认 `main.py` 使用轻量规则 demo，便于无 API Key 时快速展示；使用 `--full-agent` 会调用现有 LangGraph Agent 全流程，实际输出会受到规则、模型返回、知识库和本地配置影响。

## RAG 引用来源

完整 Agent 流程会保留 RAG 检索来源字段，便于前端或命令行展示回答参考依据：

```json
{
  "sources": ["科室说明.txt", "就诊流程.txt"],
  "source_details": [
    {
      "source": "科室说明.txt",
      "content": "呼吸内科主要处理咳嗽、发热、气促等呼吸系统相关问题..."
    }
  ]
}
```

这些字段来自 `rag/` 和 `tools/medical_rag_tool.py`，用于说明导诊建议参考了哪些本地知识文档。

## 后续优化方向

- 接入报告 OCR，支持上传图片或 PDF 报告。
- 建设医学知识库 RAG，提高回答可追溯性和稳定性。
- 完善前端页面和多轮会话体验。
- 增加 Docker 部署脚本，降低环境配置成本。
- 补充单元测试和回归测试，覆盖高风险分诊、科室推荐、追问逻辑等关键路径。
- 优化编码和日志规范，提升开源可读性。

## 免责声明

本项目仅用于学习研究和工程实践展示，不能替代医生诊断、治疗建议或真实医院分诊结果。若出现胸痛、呼吸困难、意识异常、大量出血、严重外伤等高风险症状，请立即联系急救服务或前往急诊。
