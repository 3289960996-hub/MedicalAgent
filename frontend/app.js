﻿const API_URL = "http://127.0.0.1:8000/chat";

const DEPARTMENT_LOCATIONS = {
    "急诊科": { floor: "1F", area: "急诊分诊区", room: "急诊楼 1F", description: "急诊楼 1F 急诊分诊区" },
    "发热门诊": { floor: "1F", area: "发热门诊区", room: "门诊楼 1F", description: "门诊楼 1F 发热门诊区" },
    "全科医学科": { floor: "2F", area: "A区", room: "201-205 诊室", description: "门诊楼 2F A区 201-205 诊室" },
    "儿科": { floor: "2F", area: "儿童诊区", room: "206-210 诊室", description: "门诊楼 2F 儿童诊区 206-210 诊室" },
    "口腔科": { floor: "2F", area: "D区", room: "211-216 诊室", description: "门诊楼 2F D区 211-216 诊室" },
    "肛肠科": { floor: "2F", area: "E区", room: "217-220 诊室", description: "门诊楼 2F E区 217-220 诊室" },
    "普外科": { floor: "2F", area: "F区", room: "221-224 诊室", description: "门诊楼 2F F区 221-224 诊室" },
    "呼吸内科": { floor: "3F", area: "B区", room: "301-306 诊室", description: "门诊楼 3F B区 301-306 诊室" },
    "消化内科": { floor: "3F", area: "C区", room: "307-312 诊室", description: "门诊楼 3F C区 307-312 诊室" },
    "耳鼻喉科": { floor: "3F", area: "D区", room: "313-318 诊室", description: "门诊楼 3F D区 313-318 诊室" },
    "眼科": { floor: "3F", area: "E区", room: "319-324 诊室", description: "门诊楼 3F E区 319-324 诊室" },
    "感染科/发热门诊": { floor: "1F", area: "发热门诊区", room: "门诊楼 1F 感染科/发热门诊", description: "门诊楼 1F 发热门诊区 感染科/发热门诊" },
    "感染科": { floor: "1F", area: "发热门诊区", room: "门诊楼 1F 感染科/发热门诊", description: "门诊楼 1F 发热门诊区 感染科/发热门诊" },
    "心内科": { floor: "4F", area: "A区", room: "401-406 诊室", description: "门诊楼 4F A区 401-406 诊室" },
    "神经内科": { floor: "4F", area: "B区", room: "407-412 诊室", description: "门诊楼 4F B区 407-412 诊室" },
    "内分泌科": { floor: "4F", area: "C区", room: "413-418 诊室", description: "门诊楼 4F C区 413-418 诊室" },
    "泌尿外科": { floor: "4F", area: "D区", room: "419-424 诊室", description: "门诊楼 4F D区 419-424 诊室" },
    "妇科": { floor: "4F", area: "E区", room: "425-430 诊室", description: "门诊楼 4F E区 425-430 诊室" },
    "乳腺外科": { floor: "4F", area: "F区", room: "431-434 诊室", description: "门诊楼 4F F区 431-434 诊室" },
    "骨科": { floor: "5F", area: "A区", room: "501-506 诊室", description: "门诊楼 5F A区 501-506 诊室" },
    "皮肤科": { floor: "5F", area: "C区", room: "507-512 诊室", description: "门诊楼 5F C区 507-512 诊室" },
    "风湿免疫科": { floor: "5F", area: "D区", room: "513-516 诊室", description: "门诊楼 5F D区 513-516 诊室" },
    "康复医学科": { floor: "5F", area: "康复治疗区", room: "517-520 诊室", description: "门诊楼 5F 康复治疗区 517-520 诊室" },
    "精神心理科": { floor: "5F", area: "E区", room: "521-524 诊室", description: "门诊楼 5F E区 521-524 诊室" },
    "导诊台": { floor: "1F", area: "门诊大厅", room: "门诊大厅", description: "门诊楼 1F 门诊大厅导诊台" },
    "全科": { floor: "2F", area: "A区", room: "201-205 诊室", description: "门诊楼 2F A区 201-205 诊室" },
    "全科/急诊": { floor: "1F", area: "急诊分诊区", room: "急诊楼 1F", description: "急诊楼 1F 急诊分诊区" },
    "急诊科/转人工": { floor: "1F", area: "急诊分诊区", room: "急诊楼 1F", description: "急诊楼 1F 急诊分诊区" },
    "全科医学科或导诊台": { floor: "2F", area: "A区", room: "201-205 诊室", description: "门诊楼 2F A区 201-205 诊室" }
};

const FLOOR_ROOMS = {
    "1F": ["导诊台", "急诊科", "发热门诊", "感染科/发热门诊", "急诊分诊区"],
    "2F": ["全科医学科", "儿科", "口腔科", "肛肠科", "普外科"],
    "3F": ["呼吸内科", "消化内科", "耳鼻喉科", "眼科", "检查区"],
    "4F": ["心内科", "神经内科", "内分泌科", "泌尿外科", "妇科", "乳腺外科"],
    "5F": ["骨科", "皮肤科", "风湿免疫科", "康复医学科", "精神心理科"],
    "B1": ["停车区", "影像中心", "取药窗口", "后勤服务", "电梯厅"]
};

const state = {
    sessionId: createSessionId(),
    originalQuery: "",
    initialDepartment: "",
    currentBooking: null,
    result: null,
    awaitingFollowup: false,
    map: { department: "导诊台", location: DEPARTMENT_LOCATIONS["导诊台"], activeFloor: "1F" }
};

const questionInput = document.getElementById("question");
const charCount = document.getElementById("charCount");
const submitBtn = document.getElementById("submitBtn");
const clearBtn = document.getElementById("clearBtn");
const followupSubmitBtn = document.getElementById("followupSubmitBtn");
const questionList = document.getElementById("questionList");
const spinner = followupSubmitBtn.querySelector(".spinner");
const followupLabel = followupSubmitBtn.querySelector(".button-label");
const submitDefaultLabel = submitBtn.textContent;
const bookingModal = document.getElementById("bookingModal");
const bookingDetails = document.getElementById("bookingDetails");
const patientName = document.getElementById("patientName");
const toast = document.getElementById("toast");
const supplementCard = document.getElementById("supplementCard");
const finalResultContent = document.getElementById("finalResultContent");
const resultPending = document.getElementById("resultPending");
const floorList = document.getElementById("floorList");
const hospitalMap = document.getElementById("hospitalMap");
const diagnosisCard = document.getElementById("diagnosisCard");
const diagnosisTitle = document.getElementById("diagnosisTitle");
const diagnosisMeta = document.getElementById("diagnosisMeta");
const diagnosisText = document.getElementById("diagnosisText");

questionInput.addEventListener("input", updateCharCount);
questionInput.addEventListener("keydown", handleQuestionKeydown);
submitBtn.addEventListener("click", submitTriage);
clearBtn.addEventListener("click", clearTriage);
followupSubmitBtn.addEventListener("click", submitFollowup);
document.getElementById("reassessBtn").addEventListener("click", reassess);
document.getElementById("exportBtn").addEventListener("click", exportReport);
document.getElementById("locateDepartmentBtn").addEventListener("click", () => {
    document.querySelector(".map-card").scrollIntoView({ behavior: "smooth", block: "center" });
});
document.getElementById("doctorList").addEventListener("click", handleSlotClick);
document.getElementById("cancelBookingBtn").addEventListener("click", closeBooking);
document.getElementById("confirmBookingBtn").addEventListener("click", confirmBooking);
floorList.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-floor]");
    if (!button) return;
    state.map.activeFloor = button.dataset.floor;
    renderFloorPlan();
});
bookingModal.addEventListener("click", (event) => {
    if (event.target === bookingModal) closeBooking();
});
document.querySelectorAll(".quick-actions button").forEach((button) => {
    button.addEventListener("click", () => {
        if (button.textContent.includes("挂号")) {
            document.querySelector(".doctors-card").scrollIntoView({ behavior: "smooth", block: "center" });
            showToast("请选择医生和可预约时段。");
            return;
        }
        showToast(`${button.textContent.trim()}功能将在后续版本接入。`);
    });
});
document.querySelectorAll(".quick-replies button").forEach((button) => {
    button.addEventListener("click", () => {
        questionInput.value = button.textContent.trim();
        updateCharCount();
        questionInput.focus();
    });
});

selectQuestionOptions();
updateCharCount();
renderFloorPlan();

function createSessionId() {
    return `web_${Date.now()}_${Math.random().toString(16).slice(2)}`;
}

function updateCharCount() {
    charCount.textContent = `${questionInput.value.trim().length}/300`;
}

function handleQuestionKeydown(event) {
    if (event.key !== "Enter" || event.shiftKey || event.isComposing) return;
    event.preventDefault();
    if (submitBtn.disabled) return;
    submitTriage();
}

function selectQuestionOptions() {
    questionList.addEventListener("click", (event) => {
        const button = event.target.closest("button");
        if (!button) return;
        const fieldset = button.closest("fieldset");
        if (!fieldset) return;

        if (fieldset.dataset.selectMode === "multiple") {
            const selected = !button.classList.contains("selected");
            button.classList.toggle("selected", selected);
            button.setAttribute("aria-pressed", selected ? "true" : "false");
            return;
        }

        fieldset.querySelectorAll("button").forEach((item) => {
            const selected = item === button;
            item.classList.toggle("selected", selected);
            item.setAttribute("aria-pressed", selected ? "true" : "false");
        });
    });
}

async function submitTriage() {
    if (state.awaitingFollowup) {
        await submitFollowup();
        return;
    }

    const question = questionInput.value.trim();
    if (!question) {
        showToast("请先输入患者主诉。");
        questionInput.focus();
        return;
    }

    state.sessionId = createSessionId();
    state.originalQuery = question;
    state.initialDepartment = "";
    document.getElementById("questionPreview").textContent = question;
    renderOptimisticFollowup(question);
    await requestTriage({
        question,
        original_query: question,
        followup_answer: "",
        initial_department: "",
        followup_done: false
    }, submitBtn);
}

async function submitFollowup() {
    const selectedAnswers = collectSelectedAnswers();
    const basicInfo = collectBasicInfo();
    const typedFollowup = questionInput.value.trim();
    const extraAnswer = state.awaitingFollowup && typedFollowup && typedFollowup !== state.originalQuery
        ? [`补充说明：${typedFollowup}`]
        : [];
    const followupAnswer = [...selectedAnswers, ...basicInfo, ...extraAnswer].join("；");
    if (!followupAnswer) {
        showToast("请至少选择一项追问答案或填写补充信息。");
        return;
    }

    await requestTriage({
        question: `${state.originalQuery}\n补充信息：${followupAnswer}`,
        original_query: state.originalQuery || questionInput.value.trim(),
        followup_answer: followupAnswer,
        initial_department: state.initialDepartment,
        followup_done: true
    }, followupSubmitBtn);
}

async function requestTriage(payload, activeButton) {
    setLoading(true, activeButton);
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ...payload, session_id: state.sessionId, client_type: "web" })
        });
        if (!response.ok) throw new Error(`服务返回 ${response.status}`);
        const data = await response.json();
        if (data.error) throw new Error(data.error);
        state.sessionId = data.session_id || state.sessionId;
        renderTriage(data);
        if (activeButton === followupSubmitBtn && data.need_followup !== true) {
            requestAnimationFrame(() => {
                diagnosisCard.scrollIntoView({ behavior: "smooth", block: "center" });
            });
        }
        return true;
    } catch (error) {
        showToast(`导诊请求失败：${error.message}`);
        return false;
    } finally {
        setLoading(false, activeButton);
    }
}

function setLoading(isLoading, activeButton) {
    submitBtn.disabled = isLoading;
    followupSubmitBtn.disabled = isLoading || supplementCard.classList.contains("is-submitted");
    [submitBtn, followupSubmitBtn].forEach((button) => button.classList.toggle("is-loading", isLoading && button === activeButton));
    spinner.hidden = !(isLoading && activeButton === followupSubmitBtn);
    followupLabel.textContent = isLoading && activeButton === followupSubmitBtn ? "加载中" : supplementCard.classList.contains("is-submitted") ? "补充信息已提交" : "提交补充信息";
    if (isLoading && activeButton === submitBtn) {
        submitBtn.replaceChildren(
            Object.assign(document.createElement("span"), { className: "spinner" }),
            document.createTextNode("加载中")
        );
    } else {
        submitBtn.textContent = state.awaitingFollowup ? "提交" : submitDefaultLabel;
    }
}

function renderTriage(data) {
    const resolved = resolveDepartment(data);
    const department =
        data.canonical_department ||
        data.recommended_department ||
        data.department ||
        resolved.department;
    const departmentLocation =
        normalizeDepartmentLocation(department, data.department_location || {});
    const rawAnalysis = data.analysis || data.answer || data.display_text || "系统暂未返回导诊说明。";
    const analysis = buildClinicalSummary(rawAnalysis, department, resolved.overridden);
    state.initialDepartment = department;

    const followups =
    data.followup_items ||
    data.follow_up_items ||
    data.followup_questions ||
    data.follow_up_questions ||
    [];
    if (data.need_followup === true) {
        state.awaitingFollowup = true;
        document.body.classList.remove("has-final-result");
        finalResultContent.hidden = true;
        resultPending.hidden = false;
        supplementCard.hidden = false;
        supplementCard.classList.remove("is-submitted");
        supplementCard.querySelectorAll("input, select").forEach((input) => { input.disabled = false; });
        diagnosisCard.hidden = true;
        resultPending.querySelector("strong").textContent = "已生成针对性追问";
        resultPending.querySelector("p").textContent = "请根据患者当前症状完成下方追问，并填写必要的补充信息后提交。";
        renderFollowupQuestions(followups);
        showToast("请完成追问并提交补充信息。", 3200);
        return;
    }

    state.awaitingFollowup = false;
    state.result = data;
    document.body.classList.add("has-final-result");
    finalResultContent.hidden = false;
    resultPending.hidden = true;
    supplementCard.hidden = false;
    supplementCard.classList.add("is-submitted");
    supplementCard.querySelectorAll("input, select").forEach((input) => { input.disabled = true; });
    renderDiagnosis(data, analysis, department);

    renderRisk(data.risk_level, analysis);
    renderDepartment(department, analysis, data.confidence);
    renderClinicalAnalysis(data, analysis, department, departmentLocation);
    renderNotes(data, analysis);
    renderDoctors(data.doctors || data.recommended_doctors || [], department);
    renderMap(department, departmentLocation);

    showToast("导诊结论已更新。", 2600);
}

function renderRisk(value, analysis) {
    const risk = String(value || "low").toLowerCase();
    const label = risk.includes("high") || risk.includes("高") ? "高风险" : risk.includes("medium") || risk.includes("中") ? "中等风险" : "低风险";
    document.getElementById("riskLevel").textContent = label;
    const summary = label === "高风险"
        ? "存在需优先就医或人工确认的风险信号。"
        : label === "中等风险"
            ? "建议尽快门诊评估，留意症状变化。"
            : "暂未发现明显高危信号，可按门诊流程评估。";
    document.getElementById("riskDescription").textContent = summary;
    document.querySelector(".risk-summary").classList.toggle("high-risk", label === "高风险");
}

function renderDepartment(department, analysis, confidence) {
    const target = document.getElementById("departmentName");
    target.replaceChildren(document.createTextNode(department + " "));
    const tag = document.createElement("span");
    tag.textContent = normalizeConfidenceValue(confidence) < 0.5 ? "建议人工复核" : "优先推荐";
    target.appendChild(tag);
    document.getElementById("departmentReason").textContent = "";
}

function renderDiagnosis(data, analysis, department) {
    diagnosisCard.hidden = false;
    diagnosisTitle.textContent = "病情分析与导诊建议";
    diagnosisMeta.textContent = `${department} · ${formatRiskLabel(data.risk_level)}`;
    diagnosisText.replaceChildren();

    buildStructuredAnalysis(data, analysis, department).forEach((item) => {
        const block = document.createElement("section");
        block.className = "diagnosis-section";
        const title = document.createElement("h3");
        title.textContent = item.title;
        const content = document.createElement("p");
        content.textContent = item.text;
        block.append(title, content);
        diagnosisText.appendChild(block);
    });
}

function formatRiskLabel(riskLevel) {
    const value = String(riskLevel || "").toLowerCase();
    if (value.includes("high") || value.includes("高")) return "高风险提示";
    if (value.includes("medium") || value.includes("中")) return "中等风险提示";
    return "低风险提示";
}

function normalizeConfidenceValue(value) {
    const confidence = Number(value);
    if (!Number.isFinite(confidence)) return 0;
    return confidence > 1 ? confidence / 100 : confidence;
}

function buildStructuredAnalysis(data, analysis, department) {
    const risk = String(data.risk_level || "").toLowerCase();
    const riskText = risk.includes("high") || risk.includes("高")
        ? "当前存在较高风险信号，建议优先就医或请人工导诊确认。"
        : risk.includes("medium") || risk.includes("中")
            ? "当前为中等风险，建议尽快安排门诊评估，并观察是否加重。"
            : "当前暂未发现明显高危信号，如症状加重仍需及时就医。";
    const base = String(analysis || data.analysis || data.answer || "").replace(/\s+/g, " ").trim();
    const possibleConditions = Array.isArray(data.possible_conditions)
        ? data.possible_conditions.filter(Boolean).join("、")
        : "";

    return [
        { title: "病情概括", text: data.symptom_summary || shortenText(base, 120) || "暂未返回症状概括。" },
        { title: "可能方向", text: possibleConditions || "需结合补充信息和医生面诊进一步判断。" },
        { title: "推荐依据", text: data.reason || shortenText(base, 160) || `结合当前症状方向，建议先到${department}评估。` },
        { title: "风险提示", text: riskText },
        { title: "就诊建议", text: `建议前往${department}，就诊时说明症状开始时间、持续时间、严重程度、伴随症状和既往病史。` },
        { title: "就诊前准备", text: buildVisitPreparation(department) },
        { title: "免责声明", text: "本系统仅提供导诊和健康科普参考，不能替代医生诊断。" }
    ];
}

function buildVisitPreparation(department) {
    const preparations = {
        "肛肠科": "就诊前记录便血颜色和次数、肛门疼痛或肿痛持续时间、排便习惯变化；如方便可带近期用药信息。",
        "泌尿外科": "记录尿频尿急尿痛出现时间、是否血尿、饮水和排尿情况；就诊前尽量保留近期尿检或相关检查结果。",
        "妇科": "记录末次月经时间、出血量或白带变化、是否腹痛；如有妊娠可能或既往妇科病史请主动说明。",
        "儿科": "准备体温记录、精神状态、进食饮水、大小便情况和近期用药；儿童就诊建议监护人陪同。",
        "心内科": "记录胸闷心慌发作时间、持续多久、是否活动后加重；如有血压或心率记录请带上。",
        "神经内科": "记录头晕头痛或麻木无力的开始时间、持续时间、是否单侧、是否伴说话不清或面瘫。",
        "内分泌科": "携带近期血糖、甲状腺功能或体重变化记录；说明用药、饮食和多饮多尿情况。",
        "风湿免疫科": "记录关节肿痛部位、晨僵时长、是否反复发作；如有尿酸、炎症指标或影像检查可带上。",
        "精神心理科": "记录睡眠、情绪变化持续时间、压力来源和是否影响工作生活；如正在服药请带药名。",
        "感染科/发热门诊": "记录体温峰值、发热天数、接触史、皮疹或咳嗽等伴随症状；就诊时按发热门诊流程分诊。"
    };
    return preparations[department] || `前往${department}前，重点整理与本次症状直接相关的时间、程度、诱因、伴随表现和近期用药。`;
}

function resolveDepartment(data) {
    const modelDepartment =
        data.canonical_department ||
        data.recommended_department ||
        data.department ||
        "";

    if (modelDepartment && DEPARTMENT_LOCATIONS[modelDepartment]) {
        return {
            department: modelDepartment,
            overridden: false
        };
    }

    return {
        department: "全科",
        overridden: false
    };
}

function renderOptimisticFollowup(question) {
    document.body.classList.remove("has-final-result");
    finalResultContent.hidden = true;
    resultPending.hidden = false;
    supplementCard.hidden = false;
    supplementCard.classList.remove("is-submitted");
    supplementCard.querySelectorAll("input, select").forEach((input) => { input.disabled = false; });
    diagnosisCard.hidden = true;
    resultPending.querySelector("strong").textContent = "AI 正在分析病情";
    resultPending.querySelector("p").textContent = "系统正在根据患者主诉生成针对性追问，请稍候。";

    document.getElementById("followupState").textContent = "AI 分析中";

    questionList.innerHTML = `
        <p class="question-empty">
            AI 正在根据当前病情判断需要补充哪些关键信息...
        </p>
    `;
}

function buildClinicalSummary(rawAnalysis, department, wasCorrected) {
    const clean = String(rawAnalysis || "")
        .replace(/[*#`]/g, "")
        .replace(/\s+/g, " ")
        .trim();

    const departmentFocus = {
        "呼吸内科": "结合患者咳嗽、咳痰、发热、胸闷或气促等表现，当前更偏向呼吸系统相关问题，建议由呼吸内科进一步评估。",
        "皮肤科": "结合患者皮肤瘙痒、红疹、皮肤发红、接触史或过敏相关表现，当前更偏向皮肤相关问题，建议由皮肤科进一步评估。",
        "耳鼻喉科": "结合患者咽喉疼痛、鼻部不适、耳部症状或声音嘶哑等表现，当前更偏向耳鼻喉相关问题，建议由耳鼻喉科进一步评估。",
        "骨科": "结合患者疼痛部位、活动受限、外伤史、关节或肌肉骨骼相关表现，当前更偏向骨科相关问题，建议由骨科进一步评估。",
        "口腔科": "结合患者牙痛、牙龈肿胀、口腔疼痛或面部肿胀等表现，当前更偏向口腔科相关问题，建议由口腔科进一步评估。",
        "眼科": "结合患者眼红、眼痛、视力变化、流泪或畏光等表现，当前更偏向眼科相关问题，建议由眼科进一步评估。",
        "消化内科": "结合患者腹痛、腹泻、恶心、呕吐、胃胀等表现，当前更偏向消化系统相关问题，建议由消化内科进一步评估。"
    };

    const fallback = departmentFocus[department] || `结合患者当前描述，建议由${department}进一步评估。`;

    if (clean && clean.length >= 80 && !wasCorrected) {
        return `${clean}

综合导诊建议：
1. 当前推荐科室为：${department}。
2. 建议携带既往病史、过敏史、近期用药情况等信息就诊。
3. 如果症状持续加重，或出现高热、呼吸困难、意识异常、大量出血、剧烈胸痛等情况，应及时前往急诊或联系医护人员。
4. 本系统仅提供导诊和健康科普参考，不能替代医生诊断。`;
    }

    return `${fallback}

判断依据：
1. 系统根据患者主诉和补充信息判断主要症状方向。
2. 当前未发现足以直接改变推荐科室的强证据。
3. 若存在发热、明显肿胀、活动受限、呼吸困难、症状迅速加重等情况，需要提高风险等级并尽快就医。

就诊建议：
建议前往${department}进行面诊评估。就诊时可向医生说明症状开始时间、持续时间、疼痛或不适程度、是否加重、是否伴随其他症状、近期是否用药或接触过特殊诱因。

安全提醒：
以上分析仅作导诊参考，不能替代医生诊断。`;
}

function truncateSentences(text, maxSentences, maxLength) {
    const sentences = String(text || "").split(/[。！？!?]/).map((item) => item.trim()).filter(Boolean).slice(0, maxSentences);
    const merged = sentences.join("。") + (sentences.length ? "。" : "");
    return merged.length > maxLength ? `${merged.slice(0, maxLength)}...` : merged;
}

function renderClinicalAnalysis(data, analysis, department, departmentLocation) {
    const location = normalizeDepartmentLocation(department, departmentLocation);
    const floor = location.floor || "--";
    const area = location.area || "";
    const room = location.room || "";
    const description = location.description || [floor, area, room].filter(Boolean).join(" ");

    document.getElementById("analysisTitle").textContent = `${department} · ${floor}`;
    document.getElementById("analysisSummary").textContent = description || "请到导诊台确认具体诊室位置。";

    const confidence = Number(data.confidence);
    const text = Number.isFinite(confidence) && confidence > 0
        ? `${Math.round((confidence <= 1 ? confidence : confidence / 100) * 100)}%`
        : "--";

    document.getElementById("confidenceText").textContent = `置信度：${text}`;
}

function buildDetailedAnalysisText(data, analysis) {
    const department =
        data.canonical_department ||
        data.recommended_department ||
        data.department ||
        state.initialDepartment ||
        "推荐科室";

    const risk = String(data.risk_level || "").toLowerCase();

    const riskText = risk.includes("high") || risk.includes("高")
        ? "当前风险等级偏高，建议尽快就医或转人工确认。"
        : risk.includes("medium") || risk.includes("中")
            ? "当前属于中等风险，建议尽快安排门诊评估。"
            : "当前暂未发现明显高危信号，可按普通门诊流程就诊。";

    const base = String(analysis || data.analysis || data.answer || "")
        .replace(/\s+/g, " ")
        .trim();

    return `${base || `系统根据患者主诉和补充信息，初步建议前往${department}就诊。`}

补充说明：
${riskText}
建议就诊时向医生说明症状持续时间、严重程度、是否加重、是否伴随发热或其他不适，以及既往病史、过敏史和近期用药情况。`;
}
function shortenText(text, maxLength) {
    const normalized = String(text || "暂未返回病情分析。").replace(/\s+/g, " ").trim();
    const firstSentence = normalized.split(/[。！!？?]/)[0];
    return firstSentence.length > maxLength ? `${firstSentence.slice(0, maxLength)}...` : firstSentence;
}

function renderNotes(data, analysis) {
    const content = data.visit_guide || data.guide || analysis;
    const notes = String(content).split(/\n|。/).map((item) => item.trim()).filter(Boolean).slice(0, 3);
    const list = document.getElementById("notesList");
    list.innerHTML = "";
    (notes.length ? notes : ["如症状加重或出现急性不适，请及时就医。"]).forEach((note) => {
        const item = document.createElement("li");
        item.textContent = note;
        list.appendChild(item);
    });
    document.getElementById("analysisText").textContent = "本建议仅供参考，不能替代医生诊断。如有不适，请及时就医。";
}

function renderFollowupQuestions(items) {
    questionList.innerHTML = "";

    const rawItems = Array.isArray(items) && items.length ? items : [];

    if (!rawItems.length) {
        questionList.innerHTML = `
            <p class="question-empty">
                AI 暂未返回追问信息，请补充症状持续时间、严重程度和伴随症状。
            </p>
        `;
        document.getElementById("followupState").textContent = "请补充信息";
        return;
    }

    rawItems.slice(0, 3).forEach((item, index) => {
        const questionText = typeof item === "string"
            ? item
            : item.question || item.text || `请补充第 ${index + 1} 项信息`;

        const options = typeof item === "object" && Array.isArray(item.options)
            ? item.options
            : [];
        const isMultiple = typeof item === "object" && (
            item.multiple === true ||
            item.multi_select === true ||
            item.select_mode === "multiple" ||
            item.type === "multiple"
        ) || /多选|可多选|可复选|复选/.test(questionText);

        const fieldset = document.createElement("fieldset");
        fieldset.dataset.question = questionText;
        fieldset.dataset.selectMode = isMultiple ? "multiple" : "single";

        const legend = document.createElement("legend");
        legend.textContent = questionText;
        fieldset.appendChild(legend);

        if (options.length > 0) {
            options.slice(0, 5).forEach((label) => {
                const button = document.createElement("button");
                button.type = "button";
                button.textContent = label;
                fieldset.appendChild(button);
            });
        } else {
            const input = document.createElement("input");
            input.type = "text";
            input.className = "followup-free-input";
            input.placeholder = "请根据实际情况补充";
            fieldset.appendChild(input);
        }

        questionList.appendChild(fieldset);
    });

    document.getElementById("followupState").textContent = "请补充信息";
}

function collectSelectedAnswers() {
    return [...questionList.querySelectorAll("fieldset")].flatMap((fieldset) => {
        const selectedButtons = [...fieldset.querySelectorAll("button.selected")];
        if (selectedButtons.length) {
            const selectedText = selectedButtons.map((button) => button.textContent.trim()).join("、");
            return [`${fieldset.dataset.question}${selectedText}`];
        }

        const input = fieldset.querySelector(".followup-free-input");
        const value = input && input.value.trim();
        return value ? [`${fieldset.dataset.question}${value}`] : [];
    });
}

function collectBasicInfo() {
    return [...document.querySelectorAll(".mini-form label")].flatMap((label) => {
        const name = label.childNodes[0].textContent.trim();
        const input = label.querySelector("input, select");
        const value = input && input.value.trim();
        return value && value !== "请选择" ? [`${name}：${value}`] : [];
    });
}

function renderDoctors(doctors, department) {
    const list = document.getElementById("doctorList");
    list.innerHTML = "";
    const fallback = [
        { name: "李医生", title: "主任医师", specialty: `${department}常见病诊疗`, type: "专家门诊", slots: ["10:30", "14:30", "15:30"] },
        { name: "张医生", title: "副主任医师", specialty: `${department}相关疾病`, type: "普通门诊", slots: ["09:00", "11:00", "16:00"] },
        { name: "陈医生", title: "主治医师", specialty: "常见病诊疗", type: "普通门诊", slots: ["09:30", "13:30", "16:30"] }
    ];
    (doctors.length ? doctors : fallback).slice(0, 3).forEach((doctor, index) => {
        const name = doctor.name || fallback[index].name;
        const title = doctor.title || doctor.level || fallback[index].title;
        const specialty = doctor.specialty || doctor.description || fallback[index].specialty;
        const slots = Array.isArray(doctor.slots) ? doctor.slots : Array.isArray(doctor.available_slots) ? doctor.available_slots : fallback[index].slots;
        const row = document.createElement("div");
        row.className = "doctor-row";
        row.innerHTML = `<div class="doctor-avatar"></div><div><b></b><p></p></div><div class="slots"></div>`;
        row.querySelector(".doctor-avatar").textContent = name.slice(0, 1);
        const heading = row.querySelector("b");
        heading.append(document.createTextNode(`${name}　`));
        const titleEl = document.createElement("small");
        titleEl.textContent = title;
        heading.appendChild(titleEl);
        const tag = document.createElement("em");
        tag.textContent = doctor.type || fallback[index].type;
        heading.appendChild(tag);
        row.querySelector("p").textContent = `擅长：${specialty}`;
        const slotBox = row.querySelector(".slots");
        slots.slice(0, 3).forEach((time) => {
            const button = document.createElement("button");
            button.type = "button";
            button.textContent = time;
            button.dataset.doctor = name;
            button.dataset.time = time;
            button.dataset.department = department;
            button.disabled = doctor.available === false;
            slotBox.appendChild(button);
        });
        list.appendChild(row);
    });
}

function renderMap(department, location) {
    const finalDepartment = department || "导诊台";
    const finalLocation = normalizeDepartmentLocation(finalDepartment, location);

    state.map = {
        department: finalDepartment,
        location: finalLocation,
        activeFloor: finalLocation.floor || "1F"
    };

    renderFloorPlan();
}

function normalizeDepartmentLocation(department, location) {
    const fallback = DEPARTMENT_LOCATIONS[department] || DEPARTMENT_LOCATIONS["导诊台"] || {};
    const source = DEPARTMENT_LOCATIONS[department] || (Object.keys(location || {}).length ? location : fallback);
    const floor = normalizeFloor(source.floor || source.building || fallback.floor || "");
    return {
        floor: floor || fallback.floor || "1F",
        area: source.area || fallback.area || "",
        room: source.room || source.clinic || source.route || fallback.room || "",
        description: source.description || source.route || fallback.description || ""
    };
}

function normalizeFloor(value) {
    const text = String(value || "");
    const matched = text.match(/(?:F\s*([1-5])|([1-5])\s*(?:F|楼))/i);
    if (matched) return `${matched[1] || matched[2]}F`;
    const cnMatched = text.match(/([一二三四五])楼/);
    if (cnMatched) return `${"一二三四五".indexOf(cnMatched[1]) + 1}F`;
    return text === "B1" ? "B1" : "";
}

function renderFloorPlan() {
    const { department, location, activeFloor } = state.map;
    document.querySelectorAll(".floor-list button").forEach((button) => {
        button.classList.toggle("active", button.dataset.floor === activeFloor);
    });
    hospitalMap.replaceChildren();
    const rooms = FLOOR_ROOMS[activeFloor] || [];
    hospitalMap.classList.toggle("has-six-rooms", rooms.length >= 6);
    rooms.forEach((roomName, index) => {
        const room = document.createElement("span");
        room.className = `map-room map-room-${index + 1}${roomName === department || roomName === location.area ? " is-target" : ""}`;
        room.textContent = roomName;
        hospitalMap.appendChild(room);
    });
    if (activeFloor === location.floor) {
        const target = document.createElement("span");
        target.className = "map-target";
        target.id = "mapTarget";
        target.replaceChildren(document.createTextNode(department));
        const small = document.createElement("small");
        small.textContent = `${location.floor} · ${location.room}`;
        target.appendChild(small);
        hospitalMap.appendChild(target);
    }
    const entrance = document.createElement("span");
    entrance.className = "map-entrance";
    entrance.innerHTML = "↑<small>入口</small>";
    hospitalMap.appendChild(entrance);
    document.getElementById("locationSummary").textContent = `推荐位置：${location.description}`;
}

function handleSlotClick(event) {
    const button = event.target.closest(".slots button");
    if (!button || button.disabled) return;
    state.currentBooking = { doctor: button.dataset.doctor, time: button.dataset.time, department: button.dataset.department || state.initialDepartment };
    bookingDetails.textContent = `${state.currentBooking.department} · ${state.currentBooking.doctor} · ${state.currentBooking.time}`;
    bookingModal.hidden = false;
    patientName.focus();
}

function closeBooking() {
    bookingModal.hidden = true;
    state.currentBooking = null;
}

function confirmBooking() {
    const name = patientName.value.trim() || "患者";
    if (!state.currentBooking) return;
    showToast(`已为${name}提交${state.currentBooking.doctor} ${state.currentBooking.time}的模拟挂号。`, 4000);
    closeBooking();
}

function reassess() {
    if (!state.originalQuery) {
        questionInput.focus();
        showToast("请输入患者主诉后再评估。");
        return;
    }
    submitTriage();
}

function exportReport() {
    if (!state.result) {
        showToast("请先完成一次导诊。");
        return;
    }
    const department = state.result.canonical_department || state.result.department || "全科";
    const content = [
        "智能导诊报告",
        `患者主诉：${state.originalQuery}`,
        `推荐科室：${department}`,
        `风险等级：${state.result.risk_level || "暂无"}`,
        `导诊结论：${state.result.analysis || state.result.answer || "暂无"}`
    ].join("\n");
    const url = URL.createObjectURL(new Blob([content], { type: "text/plain;charset=utf-8" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = "智能导诊报告.txt";
    link.click();
    URL.revokeObjectURL(url);
    showToast("导诊报告已导出。", 2200);
}

function clearTriage() {
    questionInput.value = "";
    state.sessionId = createSessionId();
    state.originalQuery = "";
    state.initialDepartment = "";
    state.result = null;
    state.awaitingFollowup = false;
    document.body.classList.remove("has-final-result");
    finalResultContent.hidden = true;
    resultPending.hidden = false;
    supplementCard.hidden = true;
    supplementCard.classList.remove("is-submitted");
    supplementCard.querySelectorAll("input, select").forEach((input) => { input.disabled = false; });
    diagnosisCard.hidden = true;
    resultPending.querySelector("strong").textContent = "等待患者补充信息";
    resultPending.querySelector("p").textContent = "提交主诉后，系统会先结合病情生成追问；完成补充后再给出导诊结论、科室与院内路线。";
    questionList.innerHTML = '<p class="question-empty">请先填写患者主诉，系统将根据病情生成针对性追问。</p>';
    document.getElementById("questionPreview").textContent = "请在下方描述患者当前的不适症状。";
    updateCharCount();
    questionList.querySelectorAll("button.selected").forEach((button) => button.classList.remove("selected"));
    questionInput.focus();
    showToast("已清空本次导诊内容。", 1800);
}

function showToast(message, duration = 2800) {
    toast.textContent = message;
    toast.hidden = false;
    window.clearTimeout(showToast.timer);
    showToast.timer = window.setTimeout(() => { toast.hidden = true; }, duration);
}
