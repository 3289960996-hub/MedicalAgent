# MedicalAgent 项目文件说明

## 一、项目整体作用

MedicalAgent 是一个医疗导诊 Agent 项目。它不是正式诊断系统，而是根据用户描述的症状或就医问题，给出导诊参考、风险提示和模拟就医指引。

项目主要包含：

* 前端页面：用户输入病情、查看导诊结果、地图、医生和模拟挂号。
* FastAPI 后端：提供 `/chat`、`/build`、`/robot/chat` 等接口。
* LangGraph/医疗导诊流程：把业务拦截、风险分级、症状识别、科室推荐、追问、RAG、人工转接和最终回答串起来。
* RAG 知识库：读取 `data/docs/` 下的文档，构建和检索向量知识库。
* Qwen 大模型调用：通过 OpenAI 兼容接口调用 Qwen。
* 症状识别：把用户口语化描述转成症状、部位、特征等结构化信息。
* 科室推荐：根据规则和大模型兜底判断推荐科室。
* 风险等级：识别胸痛、呼吸困难、严重外伤等高风险情况。
* 一轮追问：信息不足时先补问关键问题，再继续导诊。
* 医生推荐：根据推荐科室返回模拟医生列表。
* 模拟挂号：前端提供演示性质的一键挂号弹窗。
* 医院地图指引：返回科室所在楼层、区域和路线，并在前端地图中高亮。

## 二、项目运行流程

简单理解，主流程是：

用户在前端输入病情
→ `frontend/app.js` 发送请求
→ `app.py` 的 `/chat` 接口接收
→ `medical_graph.py` / `graph.py` 执行导诊流程
→ 可能调用 `llm.py` / `rag/` / `tools/`
→ 返回科室、风险等级、地图、医生
→ 前端渲染结果

更细一点：

1. 用户打开 `frontend/index.html`，在页面输入症状或就医问题。
2. `frontend/app.js` 调用后端 `http://127.0.0.1:8000/chat`。
3. `app.py` 接收请求，并维护追问会话状态。
4. `app.py` 调用 `medical_graph.py` 中的 `run_medical_graph()`。
5. `medical_graph.py` 创建初始状态，并调用 `graph.py` 编译出的 LangGraph。
6. `graph.py` 依次经过业务拦截、风险分级、意图识别、症状标准化、科室推荐、地图、挂号流程、追问判断、RAG 检索、人工转接判断和回答生成。
7. 后端把结构化结果返回给前端。
8. `frontend/app.js` 渲染导诊结论、风险等级、科室、就诊指引、模拟楼层地图、医生列表和模拟挂号入口。

## 三、目录说明

| 目录 | 作用 | 是否核心 |
| --- | --- | --- |
| `frontend/` | 前端静态页面目录，包含页面结构、交互逻辑、样式、模拟地图和模拟挂号。 | 是 |
| `data/` | 数据目录，当前包含 RAG 原始文档 `data/docs/` 和医院地图数据 `data/hospital/hospital_map.json`。 | 是 |
| `rag/` | RAG 知识库相关代码，负责文本切分、向量库构建和向量检索。 | 是 |
| `scripts/` | 辅助脚本目录，当前有 UTF-8/乱码检查脚本。 | 否 |
| `tools/` | Agent 工具目录，包含风险分级、科室推荐、地图查询、追问、RAG 查询等工具函数。 | 是 |
| `docs/` | 项目说明文档目录，当前新增 `FILE_OVERVIEW.md` 用于解释项目文件结构。 | 否 |
| `vector_db/` | Chroma 向量数据库持久化目录，由 RAG 构建生成。未深入扫描具体内容。 | 是，运行数据 |
| `logs/` | 日志目录，可能用于记录运行日志或高风险导诊日志。未深入扫描具体内容。 | 否，运行数据 |
| `.venv/` | Python 虚拟环境目录，保存本地安装的依赖包。未深入扫描具体内容。 | 否 |
| `.langgraph_api/` | LangGraph 本地运行相关目录。未深入扫描具体内容。 | 否，运行环境 |
| `.agents/` | Agent 或开发工具相关目录。根据当前代码无法完全确认，疑似用于开发环境配置。 | 否 |
| `.git/` | Git 仓库内部目录。未深入扫描具体内容。 | 否 |
| `__pycache__/` | Python 自动生成的字节码缓存目录。未深入扫描具体内容。 | 否 |

## 四、根目录文件说明

| 文件 | 作用 | 主要内容 | 是否核心 |
| --- | --- | --- | --- |
| `.editorconfig` | 编辑器格式约定 | 指定 UTF-8、CRLF、文件末尾换行、去除行尾空格等规则。 | 否 |
| `.env` | 环境变量配置 | 配置 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`、LangSmith 相关变量。不要提交真实密钥。 | 是 |
| `.gitattributes` | Git 文本文件属性 | 为 `.py`、`.html`、`.css`、`.js`、`.json`、`.md`、`.txt`、`.toml` 等文件声明 UTF-8 工作区编码。 | 否 |
| `.gitignore` | Git 忽略规则 | 忽略 `__pycache__/`、构建产物、虚拟环境 `.venv` 等。 | 否 |
| `.python-version` | Python 版本提示 | 当前写的是 `3.12`，通常给 `uv`、`pyenv` 或类似工具使用。 | 是 |
| `agent.py` | 旧版或备用 Agent 主流程 | 使用 `planner.py` 和 `tools/` 手动编排导诊流程，并调用 `langchain_chains.py` 生成最终回答。当前 `app.py` 主流程实际调用的是 `medical_graph.py`。 | 是，可能是旧流程 |
| `app.py` | FastAPI 后端入口 | 定义接口、请求模型、会话追问状态、结果标准化和工具列表接口。 | 是 |
| `config.py` | 全局配置 | 读取 `.env`，设置 Qwen/OpenAI 兼容接口、RAG 文档目录、向量库目录和 embedding 模型名。 | 是 |
| `graph.py` | LangGraph 导诊流程核心 | 定义状态、节点函数、工具调用、条件路由和最终 `graph = builder.compile()`。 | 是 |
| `langchain_chains.py` | LangChain 链封装 | 封装 Qwen 调用、LangSmith tracing、最终回答链和追问链。 | 是 |
| `langgraph.json` | LangGraph 配置 | 指定依赖、图入口 `./graph.py:graph` 和环境变量文件 `.env`。 | 是 |
| `llm.py` | 大模型调用封装 | 初始化 OpenAI 客户端，调用 Qwen/OpenAI 兼容接口。 | 是 |
| `main.py` | 简单命令行入口 | 当前只打印 `Hello from medicalagent!`，不像主业务入口。 | 否 |
| `medical_graph.py` | 后端调用 LangGraph 的薄封装 | 构造初始状态，调用 `graph.invoke()`，补齐回答字段和追问字段。 | 是 |
| `planner.py` | 规则规划器 | 根据关键词判断意图，并给出要调用的工具列表。主要被 `agent.py` 使用。 | 是，可能是旧流程 |
| `prompt.py` | Prompt 模板 | 定义医疗导诊系统提示词和最终回答消息构造函数。 | 是 |
| `pyproject.toml` | Python 项目配置 | 项目名、版本、Python 要求 `>=3.12`，以及 `deepagents`、`langchain` 等依赖。 | 是 |
| `README.md` | 项目说明入口 | 当前文件为空，暂时没有项目介绍内容。 | 否 |
| `requirements.txt` | pip 依赖列表 | 包含 `fastapi`、`uvicorn`、`python-dotenv`、`openai`、`chromadb`、`sentence-transformers`、`pydantic`。 | 是 |
| `symptom_normalizer_tool.py` | 根目录症状标准化工具 | 调用 `llm.py`，要求大模型返回 JSON，把症状、部位、特征、持续时间、严重程度等结构化。`tools/` 下也有同名功能文件。 | 是 |
| `uv.lock` | uv 锁定文件 | 锁定依赖版本，便于复现 Python 环境。文件较大，通常不手动编辑。 | 是 |

说明：需求中提到的 `symptom_normalizer.py` 在当前根目录没有发现；当前实际存在的是 `symptom_normalizer_tool.py`，并且 `tools/` 目录下也有 `tools/symptom_normalizer_tool.py`。

## 五、核心文件重点解释

### `app.py`

1. 文件作用

`app.py` 是 FastAPI 后端入口，负责接收前端请求、调用导诊流程、维护追问会话，并把结果整理成前端容易使用的结构。

2. 主要函数/类

* `ChatRequest`：`/chat` 接口的请求体模型。
* `RobotChatRequest`：`/robot/chat` 接口的请求体模型。
* `normalize_chat_result()`：统一结果字段，比如风险等级、科室、医生、位置、追问字段。
* `home()`：根路径健康检查。
* `build()`：调用 RAG 构建函数，生成向量知识库。
* `chat()`：Web 主聊天接口。
* `robot_chat()`：机器人终端聊天接口。
* `get_tools()`：返回系统中登记的工具名称。

3. 和其他文件的关系

* 调用 `rag/build_vector_db.py` 的 `build_vector_db()`。
* 从 `graph.py` 导入科室规范化、医生模拟、风险等级规范化等辅助函数。
* 调用 `medical_graph.py` 的 `run_medical_graph()` 执行主流程。
* 被 `frontend/app.js` 通过 `/chat` 请求访问。

4. 初学者需要注意什么

先看 `/chat`，这是前后端连接的关键。`SESSION_STORE` 用来记录追问状态，所以同一轮追问需要携带 `session_id`。

### `graph.py`

1. 文件作用

`graph.py` 是当前导诊工作流核心。它用 LangGraph 定义状态、节点和节点之间的顺序。

2. 主要函数/类

* `MedicalAgentState`：整个图流转的状态字段定义。
* `get_func()`：动态导入工具函数，导入失败时返回 `None`。
* `canonicalize_department()`：把科室名称归一化。
* `normalize_risk_level()`：把风险等级统一为 `high`、`medium`、`low`。
* `normalize_confidence()`：统一置信度格式。
* `get_department_location()`：根据科室返回模拟位置。
* `build_visit_guide()`：生成就诊指引文本。
* `mock_doctors_by_department()`：返回模拟医生列表。
* `business_guard_node()`、`risk_triage_node()`、`llm_intent_node()`、`symptom_normalizer_node()`、`department_node()`、`hospital_map_node()`、`registration_node()`、`qwen_followup_node()`、`rag_node()`、`handoff_node()`、`answer_node()`：LangGraph 节点。
* `followup_router()`：决定是先追问还是继续 RAG/最终回答。
* `graph`：编译后的 LangGraph 实例。

3. 和其他文件的关系

* 动态调用 `tools/` 下的多个工具函数。
* 调用 `llm.py` 和 `prompt.py` 生成部分回答。
* 被 `medical_graph.py` 调用。
* 被 `langgraph.json` 指定为 LangGraph 图入口。

4. 初学者需要注意什么

可以把它当成“流程图代码”。先看底部 `builder.add_edge()`，理解节点顺序，再回头看每个节点做什么。当前文件里部分中文字符串在终端显示为乱码，但不影响理解代码结构。

### `medical_graph.py`

1. 文件作用

`medical_graph.py` 是 `app.py` 和 `graph.py` 之间的桥接层。它负责准备初始状态，然后调用 LangGraph。

2. 主要函数/类

* `run_medical_graph(question, client_type="web", session_state=None)`：执行一次导诊图调用，并补齐返回字段。

3. 和其他文件的关系

* 从 `graph.py` 导入编译好的 `graph`。
* 被 `app.py` 的 `/chat` 和 `/robot/chat` 调用。

4. 初学者需要注意什么

这个文件很短，适合作为理解后端主流程的入口。它展示了图执行前需要哪些状态字段。

### `frontend/index.html`

1. 文件作用

定义前端页面结构，包括输入区、快捷问题、追问区、结果区、风险和科室指标、地图、医生列表、模拟缴费和资料索引等区域。

2. 主要函数/类

HTML 文件没有函数，重点是元素 `id`，例如 `question`、`submitBtn`、`answer`、`risk`、`department`、`floorMap`、`doctorListLeft` 等。

3. 和其他文件的关系

* 引入 `frontend/style.css` 控制样式。
* 引入 `frontend/app.js` 处理交互和接口请求。

4. 初学者需要注意什么

读这个文件时重点看每个 `id`，因为 `app.js` 会通过这些 `id` 找到元素并更新页面。

### `frontend/app.js`

1. 文件作用

负责前端交互、请求后端、渲染导诊结果、管理追问模式、模拟楼层地图、医生卡片、模拟挂号、模拟缴费和本地资料索引。

2. 主要函数/类

* `sendQuestion()`：提交首轮问题。
* `sendFollowup()`：提交追问补充信息。
* `requestChat()`：调用后端 `/chat`。
* `renderResult()`：渲染后端返回的结果。
* `renderMetrics()`：渲染风险等级、科室和置信度。
* `renderLocation()`：渲染科室位置。
* `renderRegistration()`：渲染挂号和就诊指引。
* `renderFloorMap()`：渲染模拟楼层地图。
* `renderFollowups()`：显示追问问题和补充输入框。
* `renderDoctors()`、`openBookingModal()`：显示医生并模拟挂号。
* `renderPayment()`、`saveRecordIndex()`、`renderRecords()`：演示缴费和资料索引。

3. 和其他文件的关系

* 调用 `app.py` 的 `/chat` 接口。
* 操作 `index.html` 中定义的元素。
* 依赖 `style.css` 中的类名呈现界面。

4. 初学者需要注意什么

`API_URL` 写死为 `http://127.0.0.1:8000/chat`，所以本地后端需要运行在 8000 端口。这个文件里很多数据是前端模拟数据，不等于真实医院系统。

### `frontend/style.css`

1. 文件作用

控制页面视觉样式、布局、响应式适配、按钮、卡片、地图、医生列表、弹窗和动画。

2. 主要函数/类

CSS 没有函数，重点类名包括 `page-shell`、`hero-panel`、`main-grid`、`panel`、`result-card`、`floor-map`、`doctor-card`、`toast-overlay` 等。

3. 和其他文件的关系

* 被 `frontend/index.html` 引入。
* 类名与 `frontend/app.js` 动态创建的元素配合。

4. 初学者需要注意什么

如果页面显示异常，优先检查 `index.html` 的结构和 `app.js` 生成的类名是否与这里一致。

### `config.py`

1. 文件作用

集中读取环境变量和项目路径配置。

2. 主要函数/类

* `check_config()`：检查 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL` 是否存在。
* 常量：`LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`、`DOCS_DIR`、`VECTOR_DB_DIR`、`EMBEDDING_MODEL_NAME`。

3. 和其他文件的关系

* 被 `llm.py` 读取大模型配置。
* 被 `rag/build_vector_db.py`、`rag/retriever.py` 读取文档目录、向量库目录和 embedding 模型。

4. 初学者需要注意什么

没有正确配置 `.env` 时，大模型调用会失败。`check_config()` 会在 `llm.py` 导入时执行。

### `llm.py`

1. 文件作用

封装 Qwen/OpenAI 兼容接口调用。

2. 主要函数/类

* `client = OpenAI(...)`：使用 `.env` 中的 API Key 和 Base URL 初始化客户端。
* `call_llm(messages, temperature=0.3)`：发送 messages，返回模型输出文本。

3. 和其他文件的关系

* 读取 `config.py`。
* 被 `prompt.py`、`langchain_chains.py`、多个 `tools/` 文件和症状标准化工具间接或直接使用。

4. 初学者需要注意什么

这个文件只负责“怎么调用模型”，不负责“问模型什么”。提示词主要在 `prompt.py`、`langchain_chains.py` 和部分工具文件中。

### `langchain_chains.py`

1. 文件作用

用 LangChain 把 prompt 和 Qwen 调用包装成可复用链，并可选启用 LangSmith tracing。

2. 主要函数/类

* `configure_langsmith_tracing()`：根据环境变量开启 LangSmith。
* `_message_to_dict()`：把 LangChain message 转成 OpenAI messages 格式。
* `_call_qwen_with_prompt()`：把 ChatPromptTemplate 的结果发送给 Qwen。
* `run_final_answer_chain()`：生成最终回答。
* `run_qwen_followup_chain()`：生成追问 JSON。
* `run_messages_chain()`：直接调用 messages 链。

3. 和其他文件的关系

* 调用 `llm.py` 的 `call_llm()`。
* 使用 `prompt.py` 的 `MEDICAL_SYSTEM_PROMPT`。
* 被 `agent.py` 使用；当前 `graph.py` 中主要直接调用工具和 `llm.py`。

4. 初学者需要注意什么

这是“LangChain 写法”的封装，与 `graph.py` 的 LangGraph 流程不是同一层概念。LangChain 负责单个链，LangGraph 负责编排多个节点。

### `planner.py`

1. 文件作用

根据用户问题中的关键词，决定意图和推荐调用哪些工具。

2. 主要函数/类

* `make_plan(question)`：返回 `intent`、`tools` 和 `reason`。

3. 和其他文件的关系

* 主要被 `agent.py` 调用。
* 当前 FastAPI 主流程通过 `medical_graph.py` 走 `graph.py`，不直接依赖 `planner.py`。

4. 初学者需要注意什么

它更像旧版或备用的规则规划器。阅读时不要把它和 `graph.py` 的节点流程混淆。

### `prompt.py`

1. 文件作用

存放医疗导诊系统提示词和最终回答 prompt 构造函数。

2. 主要函数/类

* `MEDICAL_SYSTEM_PROMPT`：系统角色和安全边界，例如不能诊断、不能开药、不能替代医生。
* `build_final_prompt()`：把用户问题、决策结果、工具结果、RAG 内容拼成大模型 messages。

3. 和其他文件的关系

* 被 `graph.py` 和 `langchain_chains.py` 使用。
* 最终通过 `llm.py` 调用模型。

4. 初学者需要注意什么

医疗类项目最重要的是安全边界。这里的 prompt 明确要求只做导诊参考，不做疾病诊断和治疗方案。

### `symptom_normalizer_tool.py`

1. 文件作用

把用户口语化症状描述标准化为结构化 JSON。

2. 主要函数/类

* `clean_json_text()`：清理模型可能返回的 Markdown 代码块。
* `symptom_normalizer_tool(question)`：调用大模型提取症状、身体部位、症状特征、持续时间、严重程度、科室方向和风险信号。

3. 和其他文件的关系

* 调用 `llm.py` 的 `call_llm()`。
* `tools/symptom_normalizer_tool.py` 中也有同类功能，`graph.py` 实际动态加载的是 `tools.symptom_normalizer_tool`。

4. 初学者需要注意什么

这个工具只做信息提取，不应该输出诊断结论。当前项目存在根目录和 `tools/` 目录两个相似文件，阅读时以 `graph.py` 实际导入路径为准。

### `rag/build_vector_db.py`

1. 文件作用

构建 RAG 向量知识库。

2. 主要函数/类

* `get_embedding_model()`：懒加载 embedding 模型。
* `get_clean_collection()`：删除旧 collection 后创建新的 `medical_docs` collection。
* `build_vector_db()`：读取 `data/docs/` 下的 `.txt` 文件，切片、向量化并写入 Chroma。

3. 和其他文件的关系

* 使用 `config.py` 的 `DOCS_DIR`、`VECTOR_DB_DIR`、`EMBEDDING_MODEL_NAME`。
* 使用 `rag/splitter.py` 的 `split_text()`。
* 被 `app.py` 的 `/build` 接口调用。
* 生成的数据被 `rag/retriever.py` 和 `tools/medical_rag_tool.py` 使用。

4. 初学者需要注意什么

修改 `data/docs/` 后通常需要重新构建向量库。`vector_db/` 是生成目录，不建议手动改。

### `requirements.txt`

1. 文件作用

记录使用 `pip install -r requirements.txt` 时需要安装的主要依赖。

2. 主要内容

包含 FastAPI、Uvicorn、dotenv、OpenAI SDK、ChromaDB、sentence-transformers 和 Pydantic。

3. 和其他文件的关系

* `app.py` 依赖 FastAPI/Pydantic。
* `llm.py` 依赖 OpenAI SDK。
* `rag/` 依赖 ChromaDB 和 sentence-transformers。

4. 初学者需要注意什么

`requirements.txt` 和 `pyproject.toml` 同时存在，依赖列表不完全相同。实际运行时要看项目采用的是 pip 还是 uv。

### `pyproject.toml`

1. 文件作用

Python 项目元数据和 uv/现代 Python 工具的依赖配置。

2. 主要内容

项目名 `medicalagent`，版本 `0.1.0`，Python 版本要求 `>=3.12`，依赖包含 `deepagents` 和 `langchain`。

3. 和其他文件的关系

* 与 `uv.lock` 配合锁定依赖。
* 与 `.python-version` 的 Python 3.12 保持一致。

4. 初学者需要注意什么

如果用 uv 管理环境，应关注 `pyproject.toml` 和 `uv.lock`；如果用 pip，应关注 `requirements.txt`。

## 六、配置文件说明

| 文件 | 负责内容 | 初学者说明 |
| --- | --- | --- |
| `.env` | 环境变量 | 保存模型 API Key、模型地址、模型名、LangSmith 配置等。不要在文档或日志中暴露真实密钥。 |
| `config.py` | Python 内部配置 | 把 `.env` 读入 Python 变量，并定义 RAG 文档目录、向量库目录、embedding 模型名。 |
| `requirements.txt` | pip 依赖管理 | 适合用 `pip install -r requirements.txt` 安装后端运行依赖。 |
| `pyproject.toml` | 项目元数据和现代依赖管理 | 适合 uv 等工具读取，当前声明 Python `>=3.12` 和部分依赖。 |
| `uv.lock` | uv 依赖锁文件 | 锁定具体依赖版本，帮助不同机器安装一致环境。通常不手动编辑。 |
| `.python-version` | Python 版本 | 当前为 `3.12`。 |
| `langgraph.json` | LangGraph 配置 | 告诉 LangGraph 图入口是 `./graph.py:graph`，环境变量来自 `.env`。 |

## 七、前端文件说明

| 文件 | 作用 |
| --- | --- |
| `frontend/index.html` | 页面结构。定义输入框、按钮、结果卡片、风险指标、科室位置、追问区、地图区、医生区、模拟缴费和资料索引区。 |
| `frontend/app.js` | 前端交互、请求后端、渲染结果。还包含模拟楼层地图、医生列表、模拟挂号弹窗、本地资料索引和模拟缴费逻辑。 |
| `frontend/style.css` | 页面样式。控制整体布局、颜色、卡片、按钮、地图、医生卡片、弹窗、动画和移动端适配。 |
| `frontend/concept-dark-tech.html` | 概念展示/备用页面，不一定是当前主流程文件。 |
| `frontend/concept-cyber-medical.html` | 概念展示/备用页面，不一定是当前主流程文件。 |
| `frontend/concept-glass-tech.html` | 概念展示/备用页面，不一定是当前主流程文件。 |

当前主流程页面是 `frontend/index.html`，主交互脚本是 `frontend/app.js`。

## 八、临时文件说明

当前没有发现根目录下典型的 `_fix_xxx.py`、`fix_xxx.py`、`backup` 文件。

发现一个辅助检查脚本：

| 文件 | 标记 | 说明 |
| --- | --- | --- |
| `scripts/check_utf8.py` | 辅助检查脚本 | 用于检查项目文本文件是否是 UTF-8，以及是否包含疑似乱码字符。不是主业务流程必须文件。 |

另外，`main.py` 当前只打印一行示例文本，更像项目模板入口，不是 FastAPI 或 LangGraph 主流程入口。

## 九、初学者阅读顺序

推荐按下面顺序阅读：

1. `README.md`
2. `frontend/index.html`
3. `frontend/app.js`
4. `app.py`
5. `medical_graph.py`
6. `graph.py`
7. `llm.py`
8. `rag/build_vector_db.py`
9. `config.py`

补充建议：

* 如果想理解前端如何显示结果，再看 `frontend/style.css`。
* 如果想理解科室推荐、风险分级、地图、追问等能力，再看 `tools/` 下对应文件。
* 如果想理解知识库来源，再看 `data/docs/` 和 `rag/retriever.py`。
* 如果想理解旧版或备用流程，再看 `agent.py` 和 `planner.py`。

## 十、不要胡编

以下是根据当前代码能确认或不能完全确认的点：

* 当前主后端入口可以确认是 `app.py`，前端请求 `/chat`。
* 当前 LangGraph 图入口可以确认是 `graph.py` 中的 `graph`，并被 `langgraph.json` 指向。
* 当前 `medical_graph.py` 可以确认是 `app.py` 调用 LangGraph 的桥接文件。
* `agent.py` 根据当前代码无法完全确认是否仍被运行入口使用，疑似旧版或备用 Agent 编排流程。
* `planner.py` 根据当前代码无法完全确认是否仍在主流程中使用，当前主要被 `agent.py` 使用。
* `.agents/` 根据当前代码无法完全确认，疑似开发工具或 Agent 配置目录。
* `.langgraph_api/` 根据目录名判断是 LangGraph 本地 API 运行目录，但未深入扫描具体内容。
* `logs/` 未深入扫描具体内容，疑似保存运行日志或高风险记录。
* `vector_db/` 未深入扫描具体内容，根据 RAG 代码可确认是 Chroma 向量库持久化目录。
* 当前没有发现 `symptom_normalizer.py`，只有 `symptom_normalizer_tool.py` 和 `tools/symptom_normalizer_tool.py`。

## 附：`tools/` 目录主要文件快速说明

| 文件 | 作用 |
| --- | --- |
| `tools/business_guard_tool.py` | 业务拦截，避免回答真实号源、诊断、开药等不适合系统处理的问题。 |
| `tools/risk_triage_tool.py` | 风险分级，识别高风险症状并给出处理建议。 |
| `tools/llm_intent_tool.py` | 调用大模型识别用户意图、症状、身体部位、风险和是否需要转人工。 |
| `tools/symptom_normalizer_tool.py` | 症状标准化，把口语化描述转成结构化字段。 |
| `tools/department_router_tool.py` | 基于规则做科室推荐。 |
| `tools/department_llm_classifier_tool.py` | 当规则无法确定时，调用大模型兜底推荐科室。 |
| `tools/hospital_map_tool.py` | 读取 `data/hospital/hospital_map.json`，返回科室位置和路线。 |
| `tools/registration_guide_tool.py` | 生成模拟挂号/就诊流程。 |
| `tools/qwen_followup_tool.py` | 调用 Qwen 判断是否需要追问，以及生成追问问题。 |
| `tools/medical_rag_tool.py` | 调用 RAG 检索，把知识库片段整理成上下文。 |
| `tools/human_handoff_tool.py` | 判断是否建议人工转接。 |
| `tools/high_risk_log_tool.py` | 高风险情况记录工具，可能写入日志。 |
| `tools/robot_response_tool.py` | 把回答整理成机器人展示和播报文本。 |
| `tools/lab_report_tool.py` | 体检/检验指标解释相关工具。 |
| `tools/slot_check_tool.py` | 检查信息是否完整，不完整时给出追问问题。 |
| `tools/visit_prepare_tool.py` | 给出就诊准备建议。 |
| `tools/__init__.py` | Python 包初始化文件。 |
| `tools/_init_.py` | 名称类似初始化文件，但不是标准的 `__init__.py`；根据当前代码无法完全确认用途。 |

## 附：`rag/` 和 `data/` 目录快速说明

| 文件 | 作用 |
| --- | --- |
| `rag/build_vector_db.py` | 构建 Chroma 向量库。 |
| `rag/retriever.py` | 查询 Chroma 向量库，返回最相关文档片段。 |
| `rag/splitter.py` | 把长文本切成较短片段。 |
| `rag/__init__.py` | Python 包初始化文件。 |
| `data/docs/科室说明.txt` | RAG 原始知识文档，提供科室说明。 |
| `data/docs/就诊流程.txt` | RAG 原始知识文档，提供就诊流程说明。 |
| `data/docs/医疗安全规则.txt` | RAG 原始知识文档，提供安全边界和风险提示规则。 |
| `data/docs/体检指标说明.txt` | RAG 原始知识文档，提供体检指标说明。 |
| `data/hospital/hospital_map.json` | 模拟医院科室位置和路线数据。 |
