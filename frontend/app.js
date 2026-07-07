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
    "B1": ["停车区", "影像中心", "服务窗口", "后勤服务", "电梯厅"]
};

const FLOOR_MAP_IMAGES = {
    "1F": "assets/maps/floor-1.png",
    "2F": "assets/maps/floor-2.png",
    "3F": "assets/maps/floor-3.png",
    "4F": "assets/maps/floor-4.png",
    "5F": "assets/maps/floor-5.png"
};

const MAP_TARGET_POINTS = {
    "导诊台": { x: 42, y: 78 },
    "急诊科": { x: 16, y: 24 },
    "发热门诊": { x: 48, y: 24 },
    "全科医学科": { x: 18, y: 26 },
    "儿科": { x: 50, y: 26 },
    "口腔科": { x: 78, y: 28 },
    "肛肠科": { x: 25, y: 72 },
    "普外科": { x: 75, y: 72 },
    "呼吸内科": { x: 18, y: 26 },
    "消化内科": { x: 47, y: 26 },
    "耳鼻喉科": { x: 78, y: 26 },
    "眼科": { x: 78, y: 72 },
    "心内科": { x: 17, y: 24 },
    "神经内科": { x: 35, y: 24 },
    "内分泌科": { x: 55, y: 24 },
    "泌尿外科": { x: 79, y: 25 },
    "妇科": { x: 80, y: 52 },
    "乳腺外科": { x: 80, y: 76 },
    "骨科": { x: 18, y: 25 },
    "皮肤科": { x: 48, y: 25 },
    "风湿免疫科": { x: 78, y: 25 },
    "康复医学科": { x: 48, y: 72 },
    "精神心理科": { x: 78, y: 72 },
    "感染科/发热门诊": { x: 48, y: 24 },
    "感染科": { x: 48, y: 24 }
};

const state = {
    sessionId: createSessionId(),
    originalQuery: "",
    initialDepartment: "",
    currentBooking: null,
    result: null,
    awaitingFollowup: false,
    records: { filter: "全部", query: "", selectedId: "neuro-headache" },
    plans: { selectedId: "plan-neuro", draftDate: "2026-07-01" },
    orders: { filter: "全部", query: "", selectedId: "order-ent-1" },
    currentRecordId: "",
    lastFollowupAnswer: "",
    map: { department: "导诊台", location: DEPARTMENT_LOCATIONS["导诊台"], activeFloor: "1F" }
};

const PATIENTS = [
    { name: "张先生", gender: "男", age: 32, phone: "158****8806", tag: "默认就诊人", note: "近期无特殊慢病记录", height: 175, weight: 72, bloodType: "AB", allergy: "阿莫西林", history: "无", remark: "无" },
    { name: "李女士", gender: "女", age: 29, phone: "136****2218", tag: "家人", note: "青霉素过敏史", height: 164, weight: 55, bloodType: "O", allergy: "青霉素", history: "无", remark: "近期睡眠不足" },
    { name: "王小朋友", gender: "男", age: 8, phone: "158****8806", tag: "儿童", note: "儿童就诊建议监护人陪同", height: 128, weight: 27, bloodType: "A", allergy: "暂无", history: "无", remark: "儿童就诊需监护人陪同" }
];

let activePatient = PATIENTS[0];

const SAVED_RECORDS_KEY = "medicalAgent.consultationRecords.v1";

const DEFAULT_CONSULTATION_RECORDS = [
    {
        id: "neuro-headache",
        department: "神经内科",
        risk: "中风险",
        symptom: "头痛加重",
        time: "今天 10:15",
        fullTime: "2026年7月1日 10:15",
        duration: "约3分钟",
        status: "已完成",
        confidence: "65%",
        transcript: [
            "头痛加重",
            "头痛是否伴随肢体无力或麻木、发热、颈部僵硬、畏光等情况？患者补充：目前没有这些表现。"
        ],
        analysis: "建议前往神经内科进行面诊评估。就诊时重点说明头痛开始时间、持续时间、疼痛性质、是否加重，以及是否伴随发热、呕吐、肢体无力或意识异常。"
    },
    {
        id: "ent-nausea",
        department: "耳鼻喉科",
        risk: "低风险",
        symptom: "坐地铁突然特别恶心，中午吃了碗粉汤",
        time: "6月30日",
        fullTime: "2026年6月30日 09:40",
        duration: "约4分钟",
        status: "已完成",
        confidence: "72%",
        transcript: [
            "坐地铁突然特别恶心，中午吃了碗粉汤",
            "补充：无明显胸痛、呼吸困难或持续高热，活动后不适减轻。"
        ],
        analysis: "建议先到耳鼻喉科或全科门诊评估。就诊时说明恶心出现的场景、是否伴随眩晕耳鸣、是否呕吐、近期饮食和睡眠情况。"
    },
    {
        id: "emergency-headache",
        department: "急诊科",
        risk: "高风险",
        symptom: "头痛加重",
        time: "6月30日",
        fullTime: "2026年6月30日 18:20",
        duration: "约2分钟",
        status: "已完成",
        confidence: "81%",
        transcript: [
            "头痛突然加重",
            "补充：疼痛强烈且出现明显不适，需要优先排除急性风险信号。"
        ],
        analysis: "当前记录存在较高风险提示，建议优先到急诊科或请人工导诊确认。若出现意识异常、肢体无力、喷射样呕吐、持续高热或颈部僵硬，应立即急诊。"
    },
    {
        id: "pediatric-abnormal",
        department: "儿科",
        risk: "中风险",
        symptom: "我感觉我的脚趾头会说话，而且我感觉我的后背不见了",
        time: "6月30日",
        fullTime: "2026年6月30日 15:05",
        duration: "约5分钟",
        status: "已完成",
        confidence: "58%",
        transcript: [
            "我感觉我的脚趾头会说话，而且我感觉我的后背不见了",
            "补充：儿童就诊建议监护人陪同，并完整说明症状发生前后的状态变化。"
        ],
        analysis: "建议由儿科先做面诊评估，必要时由医生判断是否转相关专科。就诊时由监护人说明症状出现时间、意识状态、睡眠、近期用药和是否有外伤。"
    }
];

let CONSULTATION_RECORDS = loadSavedConsultationRecords();

function patientRecordKey(patient = activePatient) {
    return patient?.name || "默认就诊人";
}

function defaultRecordsForPatient(patient = activePatient) {
    if (patientRecordKey(patient) !== "张先生") return [];
    return DEFAULT_CONSULTATION_RECORDS.map((record) => ({ ...record, patientName: "张先生", source: "default" }));
}

function readRecordStore() {
    try {
        return JSON.parse(localStorage.getItem(SAVED_RECORDS_KEY) || "{}") || {};
    } catch {
        return {};
    }
}

function writeRecordStore(store) {
    localStorage.setItem(SAVED_RECORDS_KEY, JSON.stringify(store));
}

function loadSavedConsultationRecords(patient = activePatient) {
    const key = patientRecordKey(patient);
    const saved = readRecordStore()[key];
    if (Array.isArray(saved)) return saved;
    return defaultRecordsForPatient(patient);
}

function persistCurrentPatientRecords() {
    const store = readRecordStore();
    store[patientRecordKey()] = CONSULTATION_RECORDS;
    writeRecordStore(store);
}

function refreshCurrentPatientRecords() {
    CONSULTATION_RECORDS = loadSavedConsultationRecords(activePatient);
    state.records.selectedId = CONSULTATION_RECORDS[0]?.id || "";
}

const VISIT_PLANS = [
    { id: "plan-neuro", time: "09:00", date: "2026-07-01", type: "门诊", department: "神经内科", title: "神经内科门诊评估", location: "门诊楼 4F B区 407-412 诊室", note: "结合患者当前描述，建议由神经内科进一步评估", status: "待处理" },
    { id: "plan-ent-order", time: "09:30", date: "2026-07-01", type: "复诊", department: "耳鼻喉科", title: "耳鼻喉科就诊", location: "门诊楼 3F D区 313-318 诊室", note: "张华华 · 订单号：MA70683036", status: "待处理" },
    { id: "plan-ent-check", time: "10:30", date: "2026-07-01", type: "门诊", department: "耳鼻喉科", title: "耳鼻喉科门诊评估", location: "门诊楼 3F D区 313-318 诊室", note: "症状呈活动诱发，前庭相关特征较明显，建议携带近期检查资料", status: "待处理" },
    { id: "plan-emergency", time: "14:00", date: "2026-07-01", type: "急诊", department: "急诊科", title: "急诊科门诊评估", location: "急诊楼 1F 急诊分诊区", note: "如出现高热、意识异常或剧烈疼痛，应优先急诊", status: "待处理" }
];

const REGISTER_ORDERS = [
    { id: "order-ent-1", patientName: "张先生", status: "已预约", code: "MA70683036", department: "耳鼻喉科", doctor: "张伟华", time: "09:00", location: "门诊楼 3F D区 313-318 诊室", fee: "已支付", source: "喉咙痛伴鼻塞问诊" },
    { id: "order-ent-2", patientName: "张先生", status: "已取消", code: "MA70682876", department: "耳鼻喉科", doctor: "陈明远", time: "10:30", location: "门诊楼 3F D区 313-318 诊室", fee: "已退回", source: "用户取消" },
    { id: "order-digestive", patientName: "张先生", status: "已完成", code: "MA70682532", department: "消化内科", doctor: "李医生", time: "14:00", location: "门诊楼 3F C区 307-312 诊室", fee: "25元", source: "腹痛腹泻导诊" },
    { id: "order-child-ent", patientName: "王小朋友", status: "已预约", code: "MA70683036", department: "耳鼻喉科", doctor: "张伟华", time: "09:00", location: "门诊楼 3F D区 313-318 诊室", fee: "已支付", source: "喉咙痛伴鼻塞问诊" },
    { id: "order-child-pay", patientName: "王小朋友", status: "待支付", code: "MA70681708", department: "儿科", doctor: "周童", time: "15:30", location: "门诊楼 2F 儿童诊区 206-210 诊室", fee: "25元", source: "儿童发热问诊" }
];

const FEATURE_DATA = {
    "问诊记录": {
        title: "问诊记录",
        desc: "查看最近的模拟问诊记录和导诊结论。",
        items: ["2026-07-06 皮肤瘙痒与红疹：建议皮肤科", "2026-07-04 咽喉疼痛：建议耳鼻喉科", "2026-07-02 腹痛腹泻：建议消化内科"]
    },
    "就诊计划": {
        title: "就诊计划",
        desc: "整理待就诊事项、预约时间和到院准备。",
        items: ["今日 14:30 皮肤科普通门诊", "到院前准备过敏史和历史检查报告", "如症状加重，优先转急诊或人工导诊"]
    },
    "检查检验": {
        title: "检查检验",
        desc: "展示检查检验入口和常用报告状态。",
        items: ["血常规：暂无新报告", "过敏原检测：可按医生建议预约", "影像检查：暂无待查看结果"]
    },
    "我的订单": {
        title: "我的订单",
        desc: "查看模拟挂号、缴费和预约订单。",
        items: ["挂号订单：暂无待支付", "检查预约：暂无记录", "缴费记录：演示环境暂未接入支付"]
    },
    "健康档案": {
        title: "健康档案",
        desc: "汇总就诊人基础信息、过敏史、既往史和就诊摘要。",
        items: ["基础信息：男，32岁", "过敏史：暂无记录", "既往病史：暂无特殊记录", "就诊提醒：详情请咨询医生，系统只提供导诊建议"]
    },
    "预约挂号": {
        title: "预约挂号",
        desc: "根据导诊结果选择科室和医生号源。",
        items: ["完成导诊后可在右侧医生号源中选择时间", "未完成导诊时可先选择全科医学科", "本项目为演示流程，不会产生真实订单"]
    },
    "院内地图": {
        title: "院内地图",
        desc: "查看推荐科室位置和楼层导航。",
        items: ["1F：导诊台、急诊科、发热门诊", "3F：呼吸内科、消化内科、耳鼻喉科", "5F：骨科、皮肤科、康复医学科"]
    },
    "报告查询": {
        title: "报告查询",
        desc: "模拟查看检查检验报告。",
        items: ["暂无新报告", "完成检查后可在此查看报告摘要", "异常结果需由医生结合病情解释"]
    },
    "在线支付": {
        title: "在线支付",
        desc: "模拟缴费入口。",
        items: ["当前没有待支付订单", "真实支付能力未接入", "后续可对接医院支付系统或第三方支付网关"]
    },
    "常见问题": {
        title: "常见问题",
        desc: "整理导诊流程、风险提示和演示系统说明。",
        items: ["AI 导诊只能作为就诊参考，不能替代医生诊断", "出现胸痛、呼吸困难、意识异常等高危症状应优先急诊", "提交主诉后先完成追问，再查看科室、路线和号源建议"]
    }
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
document.querySelector(".app-nav").addEventListener("click", handleNavigation);
document.querySelector(".patient-card button").addEventListener("click", openPatientSwitcher);
document.querySelector(".header-tools").addEventListener("click", (event) => {
    if (event.target.closest("div") || event.target.closest(".user-badge")) openPatientSwitcher();
    if (event.target.closest("button")?.textContent.includes("帮助")) showFeaturePage("常见问题");
});
document.querySelector(".faq-button").addEventListener("click", () => showFeaturePage("常见问题"));
floorList.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-floor]");
    if (!button) return;
    state.map.activeFloor = button.dataset.floor;
    renderFloorPlan();
});
bookingModal.addEventListener("click", (event) => {
    if (event.target === bookingModal) closeBooking();
});
document.querySelectorAll(".dock-action").forEach((button) => {
    button.addEventListener("click", () => {
        const label = button.querySelector("strong")?.textContent.trim() || button.textContent.trim();
        if (label.includes("挂号")) {
            document.querySelector(".doctors-card").scrollIntoView({ behavior: "smooth", block: "center" });
            showFeaturePage("预约挂号");
            return;
        }
        if (label.includes("地图")) {
            showFeaturePage("院内地图");
            return;
        }
        showFeaturePage(label);
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
syncPatientView();

function handleNavigation(event) {
    const link = event.target.closest("a");
    if (!link) return;
    event.preventDefault();

    document.querySelectorAll(".app-nav a").forEach((item) => item.classList.toggle("active", item === link));
    const label = link.textContent.replace(/[▣▤□♧▧▱]/g, "").trim();

    if (label === "智能问诊") {
        showConsultationPage();
        document.getElementById("consultation").scrollIntoView({ behavior: "smooth" });
        return;
    }

    showFeaturePage(label);
}

function ensureFeaturePage() {
    let page = document.getElementById("moduleWorkspace");
    if (page) return page;

    page = document.createElement("section");
    page.id = "moduleWorkspace";
    page.className = "module-workspace";
    page.hidden = true;
    document.querySelector(".app-header").after(page);
    return page;
}

function showConsultationPage() {
    const page = ensureFeaturePage();
    page.hidden = true;
    document.querySelector(".consultation-layout").hidden = false;
    document.querySelector(".service-dock").hidden = false;
}

function showFeaturePage(label) {
    const config = getFeaturePageConfig(normalizeModuleLabel(label));
    const page = ensureFeaturePage();

    document.querySelector(".consultation-layout").hidden = true;
    document.querySelector(".service-dock").hidden = true;

    page.innerHTML =
        config.type === "archive" ? renderArchiveModule() :
        config.type === "records" ? renderRecordsModule() :
        config.type === "plans" ? renderPlansModule() :
        config.type === "orders" ? renderOrdersModule("全部") :
        config.type === "map" ? renderMapModule() :
        renderStandardModule(config);
    attachModuleHandlers(page, config);
    page.hidden = false;
}

function normalizeModuleLabel(label) {
    if (label.includes("订单")) return "挂号订单";
    if (label.includes("档案")) return "患者档案";
    if (label.includes("挂号")) return "预约挂号";
    if (label.includes("地图")) return "院内地图";
    if (label.includes("报告")) return "报告查询";
    if (label.includes("支付")) return "在线支付";
    return label;
}

function renderStandardModule(config) {
    const actions = config.actions
        ? `<div class="module-shortcuts">${config.actions.map((item) => `<button type="button">${item}</button>`).join("")}</div>`
        : "";
    return `
        <div class="module-layout">
            <aside class="module-side">
                <div class="module-title">
                    <span>${config.kicker}</span>
                    <h1>${config.title}</h1>
                    <p>${config.desc}</p>
                </div>
                <div class="module-stats">
                    ${config.stats.map((item) => `<article><strong>${item.value}</strong><span>${item.label}</span></article>`).join("")}
                </div>
                <div class="module-filter">
                    ${config.filters.map((item, index) => `<button type="button" class="${index === 0 ? "active" : ""}">${item}</button>`).join("")}
                </div>
                ${actions}
            </aside>
            <section class="module-main">
                <div class="module-toolbar">
                    <div>
                        <h2>${config.mainTitle}</h2>
                        <p>${config.mainDesc}</p>
                    </div>
                    <button type="button">${config.primaryAction}</button>
                </div>
                <div class="module-list">
                    ${config.records.map((item) => `
                        <article class="module-record ${item.highlight ? "highlight" : ""}">
                            <time>${item.time}</time>
                            <div>
                                <h3>${item.title}</h3>
                                <p>${item.desc}</p>
                                <div>${item.tags.map((tag) => `<span>${tag}</span>`).join("")}</div>
                            </div>
                            <em>${item.status}</em>
                        </article>
                    `).join("")}
                </div>
            </section>
            <aside class="module-insight">
                <h2>${config.insightTitle}</h2>
                <div class="insight-card strong">
                    <strong>${config.focus.title}</strong>
                    <p>${config.focus.text}</p>
                </div>
                ${config.insights.map((item) => `
                    <div class="insight-card">
                        <span>${item.label}</span>
                        <p>${item.text}</p>
                    </div>
                `).join("")}
            </aside>
        </div>
    `;
}

function renderArchiveModule() {
    const surname = activePatient.name.slice(0, 1);
    const bmi = calculateBmi(activePatient.height, activePatient.weight);
    const events = [
        { time: "今天 10:15", title: "智能问诊", desc: "神经内科 · 头痛加重" },
        { time: "今天 10:15", title: "就诊计划", desc: "神经内科门诊评估 · 待办" },
        { time: "今天 09:51", title: "就诊计划", desc: "耳鼻喉科就诊 · 待办" },
        { time: "今天 09:51", title: "挂号订单", desc: "耳鼻喉科 · 已取消" },
        { time: "6月30日", title: "智能问诊", desc: "呼吸内科 · 咳嗽鼻塞" }
    ];

    return `
        <div class="archive-layout">
            <aside class="archive-profile">
                <section class="archive-card patient-identity">
                    <div class="archive-avatar">${surname}</div>
                    <div><h2>${activePatient.name}</h2><p>${activePatient.gender} · ${activePatient.age}岁</p></div>
                    <button type="button">切换就诊人</button>
                </section>
                <section class="archive-card">
                    <div class="archive-progress"><strong>100%</strong><span>档案完整度</span></div>
                    <div class="progress-bar"><i style="width:100%"></i></div>
                </section>
                <section class="archive-card archive-tags">
                    <span>过敏史：阿莫西林</span>
                    <span>既往病史：无</span>
                    <span>过敏史已记录</span>
                </section>
                <section class="archive-card archive-stats">
                    <h3>档案统计</h3>
                    <div><strong>8</strong><span>问诊</span></div>
                    <div><strong>8</strong><span>订单</span></div>
                    <div><strong>8</strong><span>计划</span></div>
                </section>
                <section class="archive-card archive-actions">
                    <h3>快捷操作</h3>
                    <button type="button">查看问诊记录</button>
                    <button type="button">查看挂号订单</button>
                    <button type="button">查看就诊计划</button>
                </section>
                <button class="archive-export" type="button">导出档案摘要</button>
            </aside>
            <section class="archive-main">
                <div class="archive-header">
                    <div><h1>患者档案</h1><p>按当前就诊人独立保存健康资料，并汇总问诊、订单与计划。</p></div>
                    <button type="button" data-archive-action="save">保存档案</button>
                </div>
                <div class="archive-kpis">
                    <article><span>BMI</span><strong id="archiveBmiValue">${bmi.value}</strong><small id="archiveBmiStatus">${bmi.status}</small></article>
                    <article><span>最近风险</span><strong>高风险 3 次</strong><small>今天 10:15</small></article>
                    <article><span>最近挂号</span><strong>耳鼻喉科</strong><small>张华华 · 已预约</small></article>
                    <article><span>下一计划</span><strong>神经内科门诊...</strong><small>09:00</small></article>
                </div>
                <section class="archive-form-card">
                    <h2>基础信息</h2>
                    <div class="archive-form-grid">
                        <label>身高 cm<input type="number" min="40" max="230" step="1" data-archive-field="height" value="${escapeHtml(activePatient.height)}"></label>
                        <label>体重 kg<input type="number" min="2" max="250" step="0.1" data-archive-field="weight" value="${escapeHtml(activePatient.weight)}"></label>
                        <label>血型<input data-archive-field="bloodType" value="${escapeHtml(activePatient.bloodType)}"></label>
                        <label>联系电话<input data-archive-field="phone" value="${escapeHtml(activePatient.phone)}"></label>
                    </div>
                </section>
                <section class="archive-form-card">
                    <h2>健康资料</h2>
                    <div class="archive-form-grid">
                        <label>过敏史<input data-archive-field="allergy" value="${escapeHtml(activePatient.allergy)}"></label>
                        <label>既往病史<input data-archive-field="history" value="${escapeHtml(activePatient.history)}"></label>
                        <label class="wide">就诊备注<input data-archive-field="remark" value="${escapeHtml(activePatient.remark)}"></label>
                    </div>
                </section>
                <section class="archive-form-card">
                    <h2>最近问诊摘要</h2>
                    <div class="archive-summary-list">
                        <article><strong>头痛加重</strong><span>神经内科 · 中等风险 · 今天 10:15</span></article>
                        <article><strong>喉咙痛伴鼻塞</strong><span>耳鼻喉科 · 低风险 · 今天 09:51</span></article>
                        <article><strong>咳嗽两天</strong><span>呼吸内科 · 低风险 · 6月30日</span></article>
                    </div>
                </section>
            </section>
            <aside class="archive-events">
                <h2>健康事件</h2>
                ${events.map((event) => `
                    <article>
                        <time>${event.time}</time>
                        <strong>${event.title}</strong>
                        <p>${event.desc}</p>
                    </article>
                `).join("")}
            </aside>
        </div>
    `;
}

function calculateBmi(heightCm, weightKg) {
    const height = Number(heightCm);
    const weight = Number(weightKg);
    if (!Number.isFinite(height) || !Number.isFinite(weight) || height <= 0 || weight <= 0) {
        return { value: "--", status: "请填写身高体重" };
    }
    const bmi = weight / ((height / 100) ** 2);
    const value = bmi.toFixed(1);
    const status = bmi < 18.5 ? "偏瘦" : bmi < 24 ? "正常" : bmi < 28 ? "超重" : "肥胖";
    return { value, status };
}

function updateArchiveBmi(page) {
    const bmi = calculateBmi(activePatient.height, activePatient.weight);
    const value = page.querySelector("#archiveBmiValue");
    const status = page.querySelector("#archiveBmiStatus");
    if (value) value.textContent = bmi.value;
    if (status) status.textContent = bmi.status;
}

function formatRecordTime(date = new Date()) {
    const now = new Date();
    const sameDay = date.toDateString() === now.toDateString();
    const time = `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
    return sameDay ? `今天 ${time}` : `${date.getMonth() + 1}月${date.getDate()}日`;
}

function formatRecordFullTime(date = new Date()) {
    return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
}

function normalizeRiskText(risk) {
    const value = String(risk || "").toLowerCase();
    if (value.includes("high") || value.includes("高")) return "高风险";
    if (value.includes("medium") || value.includes("中")) return "中风险";
    return "低风险";
}

function startSavedConsultationRecord(question) {
    const now = new Date();
    const record = {
        id: `record-${Date.now()}`,
        patientName: activePatient.name,
        department: "待分析",
        risk: "低风险",
        symptom: question,
        time: formatRecordTime(now),
        fullTime: formatRecordFullTime(now),
        duration: "进行中",
        status: "分析中",
        confidence: "--",
        transcript: [question],
        analysis: "已提交主诉，正在生成追问或导诊建议。"
    };
    CONSULTATION_RECORDS = [record, ...CONSULTATION_RECORDS.filter((item) => item.id !== record.id)];
    state.currentRecordId = record.id;
    state.records.selectedId = record.id;
    persistCurrentPatientRecords();
}

function updateSavedConsultationRecord(data, status, extra = {}) {
    if (!state.currentRecordId) return;
    const index = CONSULTATION_RECORDS.findIndex((record) => record.id === state.currentRecordId);
    if (index < 0) return;
    const department = data.canonical_department || data.recommended_department || data.department || CONSULTATION_RECORDS[index].department || "待分析";
    const analysis = data.analysis || data.answer || data.display_text || CONSULTATION_RECORDS[index].analysis;
    const transcript = [state.originalQuery || CONSULTATION_RECORDS[index].symptom];
    if (state.lastFollowupAnswer) transcript.push(`补充信息：${state.lastFollowupAnswer}`);
    CONSULTATION_RECORDS[index] = {
        ...CONSULTATION_RECORDS[index],
        patientName: activePatient.name,
        department,
        risk: normalizeRiskText(data.risk_level),
        status,
        duration: status === "已完成" ? "约3分钟" : "进行中",
        confidence: data.confidence ? `${Math.round(Number(data.confidence) * 100)}%` : CONSULTATION_RECORDS[index].confidence,
        transcript,
        analysis,
        ...extra
    };
    state.records.selectedId = state.currentRecordId;
    persistCurrentPatientRecords();
}

function renderRecordsModule(filter = state.records.filter, selectedId = state.records.selectedId, query = state.records.query) {
    state.records.filter = filter;
    state.records.query = query;
    const records = getFilteredConsultationRecords(filter, query);
    const selected = records.find((record) => record.id === selectedId) || records[0] || null;
    state.records.selectedId = selected?.id || "";

    return `
        <div class="records-layout">
            <aside class="records-side">
                <div class="module-title compact"><h1>问诊记录</h1><span>${records.length}</span></div>
                <div class="records-stats"><article><strong>${CONSULTATION_RECORDS.length}</strong><span>总问诊次数</span></article><article><strong>${records.length}</strong><span>当前筛选</span></article></div>
                <input class="module-search" placeholder="搜索症状、科室..." value="${escapeHtml(query)}">
                <div class="pill-filter" data-record-filter>${["全部", "高风险", "中风险", "低风险"].map((item) => `<button type="button" class="${item === filter ? "active" : ""}" data-record-risk="${item}">${item}</button>`).join("")}</div>
                <div class="records-list">
                    ${records.length ? records.map((record) => renderRecordListItem(record, selected?.id)).join("") : renderRecordsEmptyState(filter, query)}
                </div>
            </aside>
            ${selected ? renderRecordDetail(selected) : renderRecordEmptyDetail()}
        </div>
    `;
}

function getFilteredConsultationRecords(filter, query) {
    const keyword = String(query || "").trim().toLowerCase();
    return CONSULTATION_RECORDS.filter((record) => {
        const matchRisk = filter === "全部" || record.risk === filter;
        const haystack = [record.department, record.risk, record.symptom, record.status, record.analysis].join(" ").toLowerCase();
        return matchRisk && (!keyword || haystack.includes(keyword));
    });
}

function renderRecordListItem(record, selectedId) {
    return `
        <article class="${record.id === selectedId ? "active" : ""}" data-record-id="${record.id}" tabindex="0">
            <strong>${escapeHtml(record.department)}</strong>
            <em class="${riskClass(record.risk)}">${escapeHtml(record.risk)}</em>
            <p>${escapeHtml(record.symptom)}</p>
            <small>${escapeHtml(record.time)}</small>
            <span>${escapeHtml(record.status)}</span>
        </article>
    `;
}

function renderRecordDetail(record) {
    return `
        <section class="records-detail">
            <div class="detail-header">
                <div><h1>${escapeHtml(record.symptom)} · ${escapeHtml(record.department)}</h1><p>问诊时间：${escapeHtml(record.fullTime)} · 问诊时长：${escapeHtml(record.duration)}</p></div>
                <div><button type="button">重新问诊</button><button type="button" class="ghost">导出报告</button><button type="button" class="danger">删除</button></div>
            </div>
            <section class="detail-card">
                <h2>基本信息</h2>
                <div class="info-grid six">
                    <article><span>姓名</span><strong>${escapeHtml(activePatient.name)}</strong></article><article><span>年龄</span><strong>${activePatient.age}岁</strong></article><article><span>性别</span><strong>${escapeHtml(activePatient.gender)}</strong></article>
                    <article><span>风险等级</span><strong class="${riskDetailClass(record.risk)}">${escapeHtml(record.risk)}</strong></article><article><span>推荐科室</span><strong>${escapeHtml(record.department)}</strong></article><article><span>置信度</span><strong>${escapeHtml(record.confidence)}</strong></article>
                </div>
            </section>
            <section class="detail-card">
                <h2>问诊过程</h2>
                <div class="chat-transcript">
                    ${record.transcript.map((item) => `<div><span>${activePatient.name.slice(0, 1)}</span><p>${escapeHtml(item)}</p></div>`).join("")}
                    <div class="assistant"><span>●</span><p>${escapeHtml(record.analysis)}</p></div>
                </div>
            </section>
            <section class="detail-card">
                <h2>病情分析与导诊建议</h2>
                <p>${escapeHtml(record.analysis)}</p>
            </section>
        </section>
    `;
}

function renderRecordsEmptyState(filter, query) {
    const queryText = query ? `“${escapeHtml(query)}”` : "";
    return `<div class="records-empty">没有找到${escapeHtml(filter)}${queryText}相关问诊记录。</div>`;
}

function renderRecordEmptyDetail() {
    return `
        <section class="records-detail empty-detail">
            <div class="detail-header"><div><h1>暂无匹配记录</h1><p>请切换风险筛选或调整搜索条件。</p></div></div>
        </section>
    `;
}

function riskClass(risk) {
    if (risk === "高风险") return "high";
    if (risk === "低风险") return "low";
    return "";
}

function riskDetailClass(risk) {
    if (risk === "高风险") return "tag-high";
    if (risk === "低风险") return "tag-low";
    return "tag-warn";
}

function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

function renderPlansModule() {
    const selected = getSelectedPlan();
    const pendingCount = VISIT_PLANS.filter((plan) => plan.status !== "已完成").length;
    const doneCount = VISIT_PLANS.filter((plan) => plan.status === "已完成").length;
    return `
        <div class="plan-layout">
            <aside class="plan-side">
                <div class="module-title compact"><h1>就诊计划</h1><span>${escapeHtml(activePatient.name)}</span></div>
                <div class="calendar-card"><strong>${String(new Date(state.plans.draftDate).getDate()).padStart(2, "0")}</strong><span>2026年7月</span><small>今日计划与待办</small></div>
                <div class="records-stats three"><article><strong>${VISIT_PLANS.length}</strong><span>今日待办</span></article><article><strong>${pendingCount}</strong><span>待处理</span></article><article><strong>${doneCount}</strong><span>已完成</span></article></div>
                <section class="quick-plan">
                    <h2>新增计划</h2>
                    <label>计划名称<input data-plan-input="title" placeholder="如：复诊、检查、缴费"></label>
                    <div><label>日期<input type="date" data-plan-input="date" value="${state.plans.draftDate}"></label><label>时间<input type="time" data-plan-input="time" value="09:00"></label></div>
                    <div><label>类型<select data-plan-input="type"><option>门诊</option><option>复诊</option><option>检查</option><option>缴费</option><option>急诊</option></select></label><label>科室<select data-plan-input="department">${Object.keys(DEPARTMENT_LOCATIONS).filter((name) => !name.includes("/") && name !== "导诊台").map((name) => `<option>${escapeHtml(name)}</option>`).join("")}</select></label></div>
                    <label>地点<input data-plan-input="location" placeholder="留空则按科室自动匹配"></label>
                    <button type="button" data-plan-action="save">保存计划</button>
                </section>
            </aside>
            <section class="plan-main">
                <div class="detail-header"><div><h1>今日就诊计划</h1><p>${escapeHtml(activePatient.name)} · ${escapeHtml(activePatient.gender)} · ${activePatient.age}岁</p></div><button type="button" data-plan-action="from-record">从最近问诊生成</button></div>
                <div class="plan-list">
                    ${VISIT_PLANS.map((plan) => renderPlanItem(plan, selected?.id)).join("")}
                </div>
            </section>
            <aside class="plan-insight">
                ${renderPlanInsight(selected)}
            </aside>
        </div>
    `;
}

function getSelectedPlan() {
    return VISIT_PLANS.find((plan) => plan.id === state.plans.selectedId) || VISIT_PLANS[0] || null;
}

function renderPlanItem(plan, selectedId) {
    return `
        <article class="${plan.id === selectedId ? "active" : ""} ${plan.status === "已完成" ? "is-done" : ""}" data-plan-id="${plan.id}">
            <time>${escapeHtml(plan.time)}</time>
            <div>
                <h2>${escapeHtml(plan.title)}</h2>
                <strong>${escapeHtml(plan.location)}</strong>
                <p>${escapeHtml(plan.note)}</p>
                <button type="button" data-plan-action="navigate" data-plan-id="${plan.id}">导航</button>
                <button type="button" data-plan-action="done" data-plan-id="${plan.id}">${plan.status === "已完成" ? "恢复待办" : "标记完成"}</button>
                <button type="button" class="danger" data-plan-action="delete" data-plan-id="${plan.id}">删除</button>
            </div>
            <em>${escapeHtml(plan.status)}</em>
        </article>
    `;
}

function renderPlanInsight(plan) {
    if (!plan) {
        return `<section><h2>下一步建议</h2><p>暂无计划。请在左侧新增计划，或从最近问诊生成。</p></section>`;
    }
    const location = normalizeDepartmentLocation(plan.department, DEPARTMENT_LOCATIONS[plan.department] || {});
    const image = FLOOR_MAP_IMAGES[location.floor] || FLOOR_MAP_IMAGES["1F"];
    const point = MAP_TARGET_POINTS[plan.department] || MAP_TARGET_POINTS[location.area] || MAP_TARGET_POINTS["导诊台"];
    return `
        <section><h2>下一步建议</h2><p>当前选中：${escapeHtml(plan.time)} ${escapeHtml(plan.title)}</p><p>建议提前到达：${escapeHtml(plan.location)}</p><p>点击“导航”会按该计划的科室定位，不再沿用其他问诊结果。</p></section>
        <section><h2>模拟导航</h2><div class="mini-route image-route"><img src="${image}" alt="${escapeHtml(location.floor)} 门诊楼平面图"><b style="left:${point.x}%;top:${point.y}%">${escapeHtml(plan.department)}</b></div><div class="route-meta"><span>起点<br><strong>门诊大厅</strong></span><span>终点<br><strong>${escapeHtml(location.description || plan.location)}</strong></span><span>预计<br><strong>约${location.floor === "1F" ? "3" : "8"}分钟</strong></span></div></section>
    `;
}

function renderOrdersModule(filter = state.orders.filter, selectedId = state.orders.selectedId, query = state.orders.query) {
    state.orders.filter = filter;
    state.orders.query = query;
    const orders = getFilteredOrders(filter, query);
    const active = orders.find((order) => order.id === selectedId) || orders[0] || null;
    state.orders.selectedId = active?.id || "";
    const patientOrders = getCurrentPatientOrders();
    const pendingPay = patientOrders.filter((order) => order.status === "待支付").length;
    const booked = patientOrders.filter((order) => order.status === "已预约").length;
    return `
        <div class="orders-layout">
            <aside class="orders-side">
                <div class="module-title compact"><h1>挂号订单</h1><span>${orders.length}</span></div>
                <input class="module-search" placeholder="搜索科室、医生、订单号..." value="${escapeHtml(query)}">
                <div class="pill-filter">${["全部", "待支付", "已预约", "已完成", "已取消"].map((item) => `<button type="button" class="${item === filter ? "active" : ""}" data-order-filter="${item}">${item}</button>`).join("")}</div>
                <div class="records-stats"><article><strong>${pendingPay}</strong><span>待支付</span></article><article><strong>${booked}</strong><span>已预约</span></article></div>
                <section class="order-source"><h2>订单来源</h2><p>确认模拟挂号后会自动生成订单，并同步加入当前就诊人的就诊计划。</p></section>
            </aside>
            <section class="orders-main">
                <div class="detail-header"><div><h1>当前就诊人订单</h1><p>${escapeHtml(activePatient.name)} · ${escapeHtml(activePatient.gender)} · ${activePatient.age}岁</p></div><button type="button" data-order-action="from-record">从最近问诊生成</button></div>
                <div class="order-list">${orders.length ? orders.map((order) => renderOrderItem(order, active?.id)).join("") : `<div class="records-empty">没有找到匹配订单。</div>`}</div>
            </section>
            ${active ? renderOrderDetail(active) : renderOrderEmptyDetail()}
        </div>
    `;
}

function getFilteredOrders(filter, query) {
    const keyword = String(query || "").trim().toLowerCase();
    return getCurrentPatientOrders().filter((order) => {
        const matchStatus = filter === "全部" || order.status === filter;
        const haystack = [order.code, order.department, order.doctor, order.status, order.source].join(" ").toLowerCase();
        return matchStatus && (!keyword || haystack.includes(keyword));
    });
}

function getCurrentPatientOrders() {
    return REGISTER_ORDERS.filter((order) => order.patientName === activePatient.name);
}

function renderOrderItem(order, selectedId) {
    const canPay = order.status === "待支付";
    const canCancel = order.status === "待支付" || order.status === "已预约";
    const canPlan = (order.status === "已预约" || order.status === "已完成") && !orderExistsInPlans(order);
    return `
        <article class="${order.id === selectedId ? "active" : ""}" data-order-id="${order.id}">
            <div><h2>${escapeHtml(order.department)}</h2><p>${escapeHtml(order.doctor)} · ${escapeHtml(order.time)} · ${escapeHtml(order.source)}</p><small>${escapeHtml(order.code)}</small></div>
            <em>${escapeHtml(order.status)}</em>
            <strong>${escapeHtml(order.fee)}</strong>
            <div>
                ${canPay ? `<button type="button" data-order-action="pay" data-order-id="${order.id}">支付</button>` : ""}
                <button type="button" data-order-action="route" data-order-id="${order.id}">路线</button>
                ${canPlan ? `<button type="button" data-order-action="plan" data-order-id="${order.id}">加入计划</button>` : ""}
                ${canCancel ? `<button type="button" class="danger" data-order-action="cancel" data-order-id="${order.id}">取消</button>` : ""}
            </div>
        </article>
    `;
}

function renderOrderDetail(order) {
    const voucher = order.status === "已取消" ? "已取消" : order.status === "待支付" ? "待支付" : order.code.replace("MA706", "");
    return `
        <aside class="order-detail">
            <h1>${escapeHtml(order.department)} · ${escapeHtml(order.doctor)}</h1><p>订单号：${escapeHtml(order.code)}</p><span class="order-status">${escapeHtml(order.status)}</span>
            <div class="fake-qr"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            <strong class="visit-code">${escapeHtml(voucher)}</strong><p>${order.status === "已预约" || order.status === "已完成" ? "就诊凭证<br>到院后可凭此码模拟签到" : "该订单当前不可签到"}</p>
            <section class="detail-card compact-card"><h2>就诊信息</h2><div class="info-grid two"><article><span>就诊人</span><strong>${escapeHtml(activePatient.name)}</strong></article><article><span>科室</span><strong>${escapeHtml(order.department)}</strong></article><article><span>医生</span><strong>${escapeHtml(order.doctor)}</strong></article><article><span>时间</span><strong>${escapeHtml(order.time)}</strong></article><article><span>位置</span><strong>${escapeHtml(order.location)}</strong></article><article><span>费用</span><strong>${escapeHtml(order.fee)}</strong></article></div></section>
            <section class="detail-card compact-card"><h2>订单进度</h2><ol class="order-progress">${renderOrderProgress(order)}</ol></section>
        </aside>
    `;
}

function renderOrderProgress(order) {
    if (order.status === "待支付") {
        return "<li>已提交</li><li>待支付</li><li>支付后生成就诊凭证</li>";
    }
    if (order.status === "已预约") {
        return "<li>已提交</li><li>已支付</li><li>已预约</li>";
    }
    if (order.status === "已完成") {
        return "<li>已提交</li><li>已预约</li><li>已完成就诊</li>";
    }
    if (order.status === "已取消") {
        return "<li>已提交</li><li>已取消</li><li>不可签到</li>";
    }
    return `<li>${escapeHtml(order.status)}</li>`;
}

function orderExistsInPlans(order) {
    return VISIT_PLANS.some((plan) => plan.note?.includes(order.code) && plan.department === order.department);
}

function renderOrderEmptyDetail() {
    return `<aside class="order-detail"><h1>暂无订单</h1><p>请切换筛选条件，或从最近问诊生成订单。</p></aside>`;
}

function renderMapModule(floor = state.map.activeFloor || "1F") {
    const mapState = buildMapViewState(floor);
    return `
        <div class="map-module-layout">
            <aside class="map-module-side">
                <div class="module-title compact"><h1>院内地图</h1><span>${mapState.floor}</span></div>
                <p class="map-module-desc">查看门诊楼真实楼层平面图，按推荐科室定位路线。</p>
                <div class="map-floor-tabs">
                    ${Object.keys(FLOOR_MAP_IMAGES).map((item) => `<button type="button" data-map-floor="${item}" class="${item === mapState.floor ? "active" : ""}">${item}</button>`).join("")}
                </div>
                <section class="route-card">
                    <h2>推荐路线</h2>
                    <p>起点：门诊大厅导诊台</p>
                    <p>终点：${mapState.department} · ${mapState.location.room || mapState.location.area}</p>
                    <p>预计：约 ${mapState.floor === "1F" ? "3" : "8"} 分钟</p>
                </section>
                <section class="route-card">
                    <h2>楼层科室</h2>
                    <div class="map-room-list">${(FLOOR_ROOMS[mapState.floor] || []).map((room) => `<span>${room}</span>`).join("")}</div>
                </section>
            </aside>
            <section class="map-module-main">
                <div class="map-toolbar">
                    <div><h1>${mapState.floor} 门诊楼平面图</h1><p>${mapState.location.description || "请到导诊台确认具体诊室位置。"}</p></div>
                    <button type="button" data-map-action="locate">定位推荐科室</button>
                </div>
                <div class="full-map-frame">
                    <img src="${mapState.image}" alt="${mapState.floor} 门诊楼平面图">
                    ${mapState.showMarker ? `<span class="full-map-marker" style="left:${mapState.point.x}%;top:${mapState.point.y}%">${mapState.department}</span>` : ""}
                </div>
            </section>
            <aside class="map-module-info">
                <h2>导航信息</h2>
                <article><span>推荐科室</span><strong>${mapState.department}</strong></article>
                <article><span>楼层</span><strong>${mapState.location.floor}</strong></article>
                <article><span>诊室</span><strong>${mapState.location.room || "--"}</strong></article>
                <article><span>区域</span><strong>${mapState.location.area || "--"}</strong></article>
                <button type="button" data-map-action="back-consult">返回问诊</button>
            </aside>
        </div>
    `;
}

function buildMapViewState(floor) {
    const department = state.map.department || state.initialDepartment || "导诊台";
    const location = normalizeDepartmentLocation(department, state.map.location || {});
    const activeFloor = FLOOR_MAP_IMAGES[floor] ? floor : (location.floor || "1F");
    return {
        department,
        location,
        floor: activeFloor,
        image: FLOOR_MAP_IMAGES[activeFloor] || FLOOR_MAP_IMAGES["1F"],
        point: MAP_TARGET_POINTS[department] || MAP_TARGET_POINTS[location.area] || MAP_TARGET_POINTS["导诊台"],
        showMarker: activeFloor === location.floor
    };
}

function attachModuleHandlers(page, config) {
    page.onclick = (event) => {
        const recordCard = event.target.closest("[data-record-id]");
        if (recordCard && !event.target.closest("button")) {
            state.records.selectedId = recordCard.dataset.recordId;
            page.innerHTML = renderRecordsModule(state.records.filter, state.records.selectedId, state.records.query);
            attachModuleHandlers(page, { type: "records" });
            return;
        }

        const planCard = event.target.closest("[data-plan-id]");
        if (planCard && !event.target.closest("button")) {
            state.plans.selectedId = planCard.dataset.planId;
            page.innerHTML = renderPlansModule();
            attachModuleHandlers(page, { type: "plans" });
            return;
        }

        const orderCard = event.target.closest("[data-order-id]");
        if (orderCard && !event.target.closest("button")) {
            state.orders.selectedId = orderCard.dataset.orderId;
            page.innerHTML = renderOrdersModule(state.orders.filter, state.orders.selectedId, state.orders.query);
            attachModuleHandlers(page, { type: "orders" });
            return;
        }

        const button = event.target.closest("button");
        if (!button) return;
        const label = button.textContent.trim();

        if (button.dataset.mapFloor) {
            state.map.activeFloor = button.dataset.mapFloor;
            page.innerHTML = renderMapModule(button.dataset.mapFloor);
            attachModuleHandlers(page, { type: "map" });
            return;
        }
        if (button.dataset.mapAction === "back-consult") {
            showConsultationPage();
            document.querySelectorAll(".app-nav a").forEach((item, index) => item.classList.toggle("active", index === 0));
            return;
        }
        if (button.dataset.mapAction === "locate") {
            const targetFloor = state.map.location?.floor || "1F";
            state.map.activeFloor = targetFloor;
            page.innerHTML = renderMapModule(targetFloor);
            attachModuleHandlers(page, { type: "map" });
            showToast("已定位到推荐科室所在楼层。");
            return;
        }

        if (button.dataset.planAction) {
            handlePlanAction(page, button);
            return;
        }

        if (button.dataset.orderAction) {
            handleOrderAction(page, button);
            return;
        }

        if (button.dataset.archiveAction === "save") {
            showToast(`已保存${activePatient.name}的档案，BMI ${calculateBmi(activePatient.height, activePatient.weight).value}。`);
            return;
        }

        if (button.dataset.orderFilter) {
            state.orders.filter = button.dataset.orderFilter;
            state.orders.selectedId = "";
            page.innerHTML = renderOrdersModule(state.orders.filter, "", state.orders.query);
            attachModuleHandlers(page, { type: "orders" });
            showToast(`已筛选${state.orders.filter}订单。`);
            return;
        }

        if (button.closest(".module-filter")) {
            applyStandardModuleFilter(page, button);
            return;
        }

        if (button.dataset.recordRisk) {
            state.records.filter = button.dataset.recordRisk;
            state.records.selectedId = "";
            page.innerHTML = renderRecordsModule(state.records.filter, "", state.records.query);
            attachModuleHandlers(page, { type: "records" });
            showToast(`已筛选${state.records.filter}记录。`);
            return;
        }

        if (label === "全部" || label === "待支付" || label === "已预约" || label === "已完成" || label === "已取消") {
            if (button.closest(".orders-side")) {
                page.innerHTML = renderOrdersModule(label);
                attachModuleHandlers(page, { type: "orders" });
                showToast(`已筛选${label}订单。`);
                return;
            }
            button.closest(".pill-filter")?.querySelectorAll("button").forEach((item) => item.classList.toggle("active", item === button));
            showToast(`已切换到${label}视图。`);
            return;
        }
        if (label.includes("切换就诊人")) {
            openPatientSwitcher();
            return;
        }
        if (label.includes("查看问诊")) return openModuleFromButton("问诊记录");
        if (label.includes("查看挂号")) return openModuleFromButton("挂号订单");
        if (label.includes("查看就诊")) return openModuleFromButton("就诊计划");
        if (label.includes("导航") || label.includes("路线")) {
            showFeaturePage("院内地图");
            showToast("已打开院内地图。");
            return;
        }
        if (label.includes("加入计划")) {
            showFeaturePage("就诊计划");
            showToast("已加入当前就诊计划。");
            return;
        }
        if (label.includes("标记完成")) {
            const row = button.closest("article");
            if (row) {
                row.classList.add("is-done");
                const status = row.querySelector("em");
                if (status) status.textContent = "已完成";
            }
            showToast("计划已标记完成。");
            return;
        }
        if (label.includes("删除")) {
            const row = button.closest("article");
            if (row) row.remove();
            showToast("已从当前列表移除。");
            return;
        }
        if (label.includes("取消")) {
            const row = button.closest("article");
            const status = row?.querySelector("em");
            if (status) status.textContent = "已取消";
            showToast("订单已取消。");
            return;
        }
        if (label.includes("支付")) {
            const row = button.closest("article");
            const status = row?.querySelector("em");
            if (status) status.textContent = "已预约";
            showToast("模拟支付完成，订单已预约。");
            return;
        }
        if (label.includes("保存")) {
            showToast("已保存当前信息。");
            return;
        }
        if (label.includes("导出")) {
            showToast("已生成模拟导出文件。");
            return;
        }
        if (label.includes("重新问诊") || label.includes("从最近问诊生成")) {
            showConsultationPage();
            questionInput.focus();
            showToast("已回到智能问诊。");
        }
    };

    page.oninput = (event) => {
        if (event.target.matches(".records-side .module-search")) {
            state.records.query = event.target.value;
            page.innerHTML = renderRecordsModule(state.records.filter, state.records.selectedId, state.records.query);
            attachModuleHandlers(page, { type: "records" });
            const search = page.querySelector(".records-side .module-search");
            if (search) {
                search.focus();
                search.setSelectionRange(search.value.length, search.value.length);
            }
            return;
        }
        if (event.target.matches(".orders-side .module-search")) {
            state.orders.query = event.target.value;
            page.innerHTML = renderOrdersModule(state.orders.filter, state.orders.selectedId, state.orders.query);
            attachModuleHandlers(page, { type: "orders" });
            const search = page.querySelector(".orders-side .module-search");
            if (search) {
                search.focus();
                search.setSelectionRange(search.value.length, search.value.length);
            }
            return;
        }
        if (event.target.matches("[data-archive-field]")) {
            const field = event.target.dataset.archiveField;
            const value = event.target.value;
            activePatient[field] = field === "height" || field === "weight" ? Number(value) : value;
            if (field === "height" || field === "weight") updateArchiveBmi(page);
            return;
        }
        if (event.target.matches('[data-plan-input="date"]')) {
            state.plans.draftDate = event.target.value || state.plans.draftDate;
        }
    };
}

function applyStandardModuleFilter(page, button) {
    const label = button.textContent.trim();
    button.closest(".module-filter")?.querySelectorAll("button").forEach((item) => item.classList.toggle("active", item === button));
    const records = [...page.querySelectorAll(".module-record")];
    let visible = 0;
    records.forEach((record) => {
        const text = record.textContent.replace(/\s+/g, " ");
        const matched = label === "全部" || text.includes(label) || (label === "待处理" && /待|建议|预留/.test(text));
        record.hidden = !matched;
        if (matched) visible += 1;
    });
    let empty = page.querySelector(".module-empty");
    if (!empty) {
        empty = document.createElement("div");
        empty.className = "records-empty module-empty";
        empty.textContent = "当前筛选下暂无内容。";
        page.querySelector(".module-list")?.appendChild(empty);
    }
    empty.hidden = visible > 0;
    showToast(`已筛选${label}内容。`);
}

function handlePlanAction(page, button) {
    const action = button.dataset.planAction;
    const planId = button.dataset.planId;
    const plan = VISIT_PLANS.find((item) => item.id === planId);

    if (action === "save") {
        savePlanFromForm(page);
        return;
    }
    if (action === "from-record") {
        createPlanFromSelectedRecord(page);
        return;
    }
    if (!plan) return;

    state.plans.selectedId = plan.id;
    if (action === "navigate") {
        openPlanNavigation(plan);
        return;
    }
    if (action === "done") {
        plan.status = plan.status === "已完成" ? "待处理" : "已完成";
        page.innerHTML = renderPlansModule();
        attachModuleHandlers(page, { type: "plans" });
        showToast(plan.status === "已完成" ? "计划已标记完成。" : "计划已恢复为待处理。");
        return;
    }
    if (action === "delete") {
        const index = VISIT_PLANS.findIndex((item) => item.id === plan.id);
        if (index >= 0) VISIT_PLANS.splice(index, 1);
        state.plans.selectedId = VISIT_PLANS[index]?.id || VISIT_PLANS[index - 1]?.id || VISIT_PLANS[0]?.id || "";
        page.innerHTML = renderPlansModule();
        attachModuleHandlers(page, { type: "plans" });
        showToast("计划已删除。");
    }
}

function savePlanFromForm(page) {
    const read = (name) => page.querySelector(`[data-plan-input="${name}"]`)?.value.trim() || "";
    const department = read("department") || "全科医学科";
    const location = read("location") || normalizeDepartmentLocation(department, DEPARTMENT_LOCATIONS[department] || {}).description || "到院后请到导诊台确认";
    const title = read("title") || `${department}${read("type") || "门诊"}计划`;
    const time = read("time") || "09:00";
    const date = read("date") || state.plans.draftDate;
    const plan = {
        id: `plan-${Date.now()}`,
        title,
        time,
        date,
        type: read("type") || "门诊",
        department,
        location,
        note: "手动新增计划。可点击导航查看对应科室楼层位置。",
        status: "待处理"
    };
    VISIT_PLANS.unshift(plan);
    state.plans.selectedId = plan.id;
    state.plans.draftDate = date;
    page.innerHTML = renderPlansModule();
    attachModuleHandlers(page, { type: "plans" });
    showToast("已新增就诊计划。");
}

function createPlanFromSelectedRecord(page) {
    const record = CONSULTATION_RECORDS.find((item) => item.id === state.records.selectedId) || CONSULTATION_RECORDS[0];
    if (!record) return;
    const location = normalizeDepartmentLocation(record.department, DEPARTMENT_LOCATIONS[record.department] || {});
    const plan = {
        id: `plan-record-${Date.now()}`,
        title: `${record.department}门诊评估`,
        time: "09:00",
        date: state.plans.draftDate,
        type: "门诊",
        department: record.department,
        location: location.description || "到院后请到导诊台确认",
        note: `由问诊记录生成：${record.symptom}`,
        status: "待处理"
    };
    VISIT_PLANS.unshift(plan);
    state.plans.selectedId = plan.id;
    page.innerHTML = renderPlansModule();
    attachModuleHandlers(page, { type: "plans" });
    showToast("已从最近问诊生成就诊计划。");
}

function openPlanNavigation(plan) {
    const location = normalizeDepartmentLocation(plan.department, DEPARTMENT_LOCATIONS[plan.department] || {});
    state.map.department = plan.department;
    state.map.location = location;
    state.map.activeFloor = location.floor || "1F";
    showFeaturePage("院内地图");
    showToast(`已导航到${plan.department}。`);
}

function handleOrderAction(page, button) {
    const action = button.dataset.orderAction;
    if (action === "from-record") {
        createOrderFromSelectedRecord(page);
        return;
    }
    const order = REGISTER_ORDERS.find((item) => item.id === button.dataset.orderId);
    if (!order) return;
    state.orders.selectedId = order.id;

    if (action === "pay") {
        if (order.status !== "待支付") {
            showToast("当前订单不需要支付。");
            return;
        }
        order.status = "已预约";
        order.fee = "已支付";
        rerenderOrders(page);
        showToast("模拟支付完成，订单已变为已预约。");
        return;
    }
    if (action === "cancel") {
        if (order.status !== "待支付" && order.status !== "已预约") {
            showToast("当前订单不能取消。");
            return;
        }
        order.status = "已取消";
        order.fee = order.fee === "已支付" ? "已退回" : "无需支付";
        rerenderOrders(page);
        showToast("订单已取消。");
        return;
    }
    if (action === "route") {
        const location = normalizeDepartmentLocation(order.department, DEPARTMENT_LOCATIONS[order.department] || {});
        state.map.department = order.department;
        state.map.location = location;
        state.map.activeFloor = location.floor || "1F";
        showFeaturePage("院内地图");
        showToast(`已打开${order.department}路线。`);
        return;
    }
    if (action === "plan") {
        if (orderExistsInPlans(order)) {
            showToast("该订单已在就诊计划中。");
            return;
        }
        const location = normalizeDepartmentLocation(order.department, DEPARTMENT_LOCATIONS[order.department] || {});
        const plan = {
            id: `plan-order-${Date.now()}`,
            title: `${order.department}就诊`,
            time: order.time || "09:00",
            date: state.plans.draftDate,
            type: "门诊",
            department: order.department,
            location: location.description || order.location,
            note: `${order.doctor} · 订单号：${order.code}`,
            status: "待处理"
        };
        VISIT_PLANS.unshift(plan);
        state.plans.selectedId = plan.id;
        showFeaturePage("就诊计划");
        showToast("订单已加入就诊计划。");
    }
}

function rerenderOrders(page) {
    page.innerHTML = renderOrdersModule(state.orders.filter, state.orders.selectedId, state.orders.query);
    attachModuleHandlers(page, { type: "orders" });
}

function createOrderFromSelectedRecord(page) {
    const record = CONSULTATION_RECORDS.find((item) => item.id === state.records.selectedId) || CONSULTATION_RECORDS[0];
    if (!record) return;
    const location = normalizeDepartmentLocation(record.department, DEPARTMENT_LOCATIONS[record.department] || {});
    const order = {
        id: `order-record-${Date.now()}`,
        patientName: activePatient.name,
        status: "待支付",
        code: `MA${String(Date.now()).slice(-8)}`,
        department: record.department,
        doctor: "待分配医生",
        time: "待确认",
        location: location.description || "到院后请到导诊台确认",
        fee: "待确认",
        source: record.symptom
    };
    REGISTER_ORDERS.unshift(order);
    state.orders.selectedId = order.id;
    state.orders.filter = "全部";
    rerenderOrders(page);
    showToast("已从最近问诊生成待支付订单。");
}

function openModuleFromButton(label) {
    const target = normalizeModuleLabel(label);
    showFeaturePage(target);
    document.querySelectorAll(".app-nav a").forEach((item) => {
        const text = item.textContent.trim();
        item.classList.toggle("active", text.includes(target) || target.includes(text.replace(/[▣▤□▧▱]/g, "").trim()));
    });
}

function getFeaturePageConfig(label) {
    const common = FEATURE_DATA[label] || { title: label, desc: "功能模块", items: [] };
    const pages = {
        "问诊记录": {
            type: "records",
            kicker: "历史记录",
            title: "问诊记录",
            desc: "按时间查看患者问诊过程、追问结果和导诊结论。",
            stats: [{ value: "30", label: "累计问诊" }, { value: "5", label: "本周新增" }, { value: "2", label: "需复核" }],
            filters: ["全部", "待复核", "已完成", "高风险"],
            mainTitle: "最近问诊",
            mainDesc: "点击记录可查看主诉、追问、科室建议和风险提示。",
            primaryAction: "导出记录",
            records: [
                { time: "09:40", title: "皮肤瘙痒并出现红疹", desc: "主诉：晨起后皮肤发痒，局部红疹。建议皮肤科评估。", tags: ["皮肤科", "低风险"], status: "已完成", highlight: true },
                { time: "昨天", title: "咽喉疼痛伴鼻塞", desc: "结合咽痛、鼻塞和轻度咳嗽，建议耳鼻喉科或全科。", tags: ["耳鼻喉科", "追问完成"], status: "已完成" },
                { time: "07-02", title: "腹痛腹泻", desc: "记录腹痛位置、腹泻次数和饮食诱因，建议消化内科。", tags: ["消化内科"], status: "已归档" }
            ],
            insightTitle: "下一步建议",
            focus: { title: "复核提醒", text: "若问诊中出现持续高热、胸痛、呼吸困难等高危信号，应转急诊或人工导诊。" },
            insights: [{ label: "质量检查", text: "2 条记录缺少持续时间信息。" }, { label: "患者沟通", text: "建议补充既往病史和过敏史。" }]
        },
        "就诊计划": {
            type: "plans",
            kicker: "计划安排",
            title: "就诊计划",
            desc: "管理预约、到院准备、科室路线和候诊提醒。",
            stats: [{ value: "3", label: "待办事项" }, { value: "1", label: "今日预约" }, { value: "0", label: "逾期" }],
            filters: ["今日", "本周", "待准备", "已完成"],
            mainTitle: "待执行计划",
            mainDesc: "围绕导诊结论生成就医前准备和到院流程。",
            primaryAction: "新增计划",
            records: [
                { time: "今日 14:30", title: "皮肤科普通门诊", desc: "携带过敏史、历史检查报告；到 5F C区候诊。", tags: ["已预约", "5F"], status: "待就诊", highlight: true },
                { time: "就诊前", title: "整理症状变化", desc: "记录红疹范围、瘙痒程度、是否接触新食物或环境刺激。", tags: ["准备事项"], status: "待完成" },
                { time: "到院后", title: "导诊台确认路线", desc: "如症状加重，优先咨询导诊台是否需要急诊。", tags: ["院内导航"], status: "待执行" }
            ],
            insightTitle: "计划提醒",
            focus: { title: "今日重点", text: "请提前 20 分钟到院取号，携带身份证或医保凭证。" },
            insights: [{ label: "路线", text: "推荐路线：门诊大厅 → 电梯 → 5F C区。" }, { label: "材料", text: "建议带上过敏史和历史检查报告。" }]
        },
        "检查检验": {
            kicker: "报告中心",
            title: "检查检验",
            desc: "管理检查预约、报告状态和结果提醒。",
            stats: [{ value: "0", label: "新报告" }, { value: "2", label: "可预约" }, { value: "1", label: "建议复查" }],
            filters: ["全部", "检查", "检验", "异常提醒"],
            mainTitle: "检查检验项目",
            mainDesc: "展示医生建议的检查项目和报告查询状态。",
            primaryAction: "上传报告",
            records: [
                { time: "建议", title: "过敏原检测", desc: "皮肤反复瘙痒或红疹时，可按医生建议进一步检查。", tags: ["可预约", "皮肤科"], status: "建议项", highlight: true },
                { time: "暂无", title: "血常规", desc: "当前没有新报告；如伴发热可咨询医生是否需要检查。", tags: ["检验"], status: "无新报告" },
                { time: "历史", title: "胸部影像", desc: "暂无待查看影像结果。", tags: ["影像"], status: "已归档" }
            ],
            insightTitle: "报告提醒",
            focus: { title: "异常解读", text: "报告结果需结合症状和医生面诊判断，系统仅作信息整理。" },
            insights: [{ label: "上传入口", text: "后续可接入报告 OCR 和异常指标摘要。" }, { label: "安全提示", text: "报告解释请结合医生面诊意见。" }]
        },
        "挂号订单": {
            type: "orders",
            kicker: "订单管理",
            title: "挂号订单",
            desc: "查看预约挂号、取消记录和候诊信息。",
            stats: [{ value: "1", label: "进行中" }, { value: "0", label: "待支付" }, { value: "4", label: "历史订单" }],
            filters: ["全部", "已预约", "已取消", "已完成"],
            mainTitle: "挂号订单",
            mainDesc: "按就诊人展示挂号科室、医生、时间和订单状态。",
            primaryAction: "刷新订单",
            records: [
                { time: "今天 09:51", title: "耳鼻喉科普通门诊", desc: "张先生 · 张华华医生 · 09:00 · 门诊楼 3F D区。", tags: ["已预约", "普通门诊"], status: "待就诊", highlight: true },
                { time: "今天 09:51", title: "耳鼻喉科普通门诊", desc: "张先生 · 陈明远医生 · 10:30 · 用户取消。", tags: ["已取消"], status: "已取消" },
                { time: "07-02", title: "消化内科咨询", desc: "腹痛腹泻导诊后的模拟挂号记录。", tags: ["历史订单"], status: "已完成" }
            ],
            insightTitle: "订单提示",
            focus: { title: "候诊提醒", text: "请提前 20 分钟到院取号，携带身份证或医保凭证。" },
            insights: [{ label: "退改规则", text: "真实系统需展示医院号源退改规则。" }, { label: "凭证", text: "可扩展电子就诊凭证和二维码。" }]
        },
        "患者档案": { type: "archive", title: "患者档案" }
        ,
        "院内地图": { type: "map", title: "院内地图" }
    };

    return pages[label] || {
        kicker: "功能模块",
        title: common.title || label,
        desc: common.desc || "该功能模块已预留入口。",
        stats: [{ value: "—", label: "暂无数据" }, { value: "0", label: "待处理" }, { value: "0", label: "提醒" }],
        filters: ["全部", "待处理", "已完成"],
        mainTitle: common.title || label,
        mainDesc: common.desc || "",
        primaryAction: "刷新",
        records: (common.items || []).map((item, index) => ({ time: `0${index + 1}`, title: item, desc: "后续可继续接入真实业务数据。", tags: ["演示"], status: "预留" })),
        insightTitle: "模块说明",
        focus: { title: "当前状态", text: "该模块已恢复页面入口，后续可继续扩展数据和接口。" },
        insights: []
    };
}

function openPatientSwitcher() {
    let modal = document.getElementById("patientSwitcher");
    if (!modal) {
        modal = document.createElement("div");
        modal.id = "patientSwitcher";
        modal.className = "modal patient-switcher";
        modal.hidden = true;
        modal.innerHTML = `
            <div class="modal-content patient-switcher-content" role="dialog" aria-modal="true" aria-labelledby="patientSwitcherTitle">
                <h2 id="patientSwitcherTitle">切换就诊人</h2>
                <p>选择后会同步到左侧卡片、顶部信息和挂号确认。</p>
                <div class="patient-list" id="patientList"></div>
                <div class="modal-actions">
                    <button type="button" id="closePatientSwitcherBtn">取消</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        document.getElementById("closePatientSwitcherBtn").addEventListener("click", closePatientSwitcher);
        modal.addEventListener("click", (event) => {
            if (event.target === modal) closePatientSwitcher();
        });
    }

    const list = document.getElementById("patientList");
    list.replaceChildren();
    PATIENTS.forEach((patient) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = `patient-option${patient.name === activePatient.name ? " active" : ""}`;
        button.innerHTML = `<strong></strong><span></span><small></small>`;
        button.querySelector("strong").textContent = patient.name;
        button.querySelector("span").textContent = `${patient.gender} · ${patient.age}岁 · ${patient.tag}`;
        button.querySelector("small").textContent = patient.note;
        button.addEventListener("click", () => {
            activePatient = patient;
            refreshCurrentPatientRecords();
            syncPatientView();
            refreshOpenPatientScopedModule();
            closePatientSwitcher();
            showToast(`已切换为${patient.name}。`);
        });
        list.appendChild(button);
    });
    modal.hidden = false;
}

function closePatientSwitcher() {
    const modal = document.getElementById("patientSwitcher");
    if (modal) modal.hidden = true;
}

function syncPatientView() {
    const surname = activePatient.name.slice(0, 1);
    document.querySelector(".patient-card strong").replaceChildren(
        document.createTextNode(`${activePatient.name} `),
        Object.assign(document.createElement("button"), { type: "button", textContent: "切换" })
    );
    document.querySelector(".patient-card small").textContent = `${activePatient.gender} · ${activePatient.age}岁`;
    document.querySelector(".patient-card button").addEventListener("click", openPatientSwitcher);
    document.querySelector(".user-badge").textContent = surname;
    document.querySelector(".user-avatar").textContent = surname;
    const headerName = document.querySelector(".header-tools strong");
    if (headerName) headerName.textContent = activePatient.name;
    const headerHint = document.querySelector(".header-tools small");
    if (headerHint) headerHint.textContent = "切换患者";
    patientName.value = activePatient.name;
}

function refreshOpenPatientScopedModule() {
    const page = document.getElementById("moduleWorkspace");
    if (!page || page.hidden) return;
    if (page.querySelector(".records-layout")) {
        state.records.filter = "全部";
        state.records.query = "";
        page.innerHTML = renderRecordsModule("全部", state.records.selectedId, "");
        attachModuleHandlers(page, { type: "records" });
        return;
    }
    if (page.querySelector(".archive-layout")) {
        page.innerHTML = renderArchiveModule();
        attachModuleHandlers(page, { type: "archive" });
        return;
    }
    if (page.querySelector(".plan-layout")) {
        page.innerHTML = renderPlansModule();
        attachModuleHandlers(page, { type: "plans" });
        return;
    }
    if (page.querySelector(".orders-layout")) {
        page.innerHTML = renderOrdersModule();
        attachModuleHandlers(page, { type: "orders" });
    }
}

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
    state.lastFollowupAnswer = "";
    startSavedConsultationRecord(question);
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
    const followupAnswer = selectedAnswers.join("；");
    if (!followupAnswer) {
        showToast("请先选择 AI 追问给出的选项。");
        return;
    }

    state.lastFollowupAnswer = followupAnswer;
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
    followupLabel.textContent = isLoading && activeButton === followupSubmitBtn ? "加载中" : supplementCard.classList.contains("is-submitted") ? "追问选项已提交" : "提交追问选项";
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

    const followups = getSelectableFollowups(data);
    const qwenUnavailable = !data.followup_done && data.need_followup !== true && !followups.length && isQwenUnavailableResponse(data);
    if (qwenUnavailable) {
        updateSavedConsultationRecord(data, "待补充", {
            department: "待补充",
            analysis: data.answer || data.display_text || "当前主诉信息不足，请补充具体不适后再评估。"
        });
        state.awaitingFollowup = false;
        document.body.classList.remove("has-final-result");
        finalResultContent.hidden = true;
        resultPending.hidden = false;
        supplementCard.hidden = true;
        diagnosisCard.hidden = true;
        resultPending.querySelector("strong").textContent = "Qwen 暂未返回追问选项";
        resultPending.querySelector("p").textContent = "请先配置 LLM_API_KEY，系统才能根据病情生成可选择的 AI 追问选项。";
        questionList.innerHTML = `
            <p class="question-empty">
                Qwen 未返回可选择的追问选项。配置 Qwen 后，请重新提交主诉生成追问。
            </p>
        `;
        document.getElementById("followupState").textContent = "等待 Qwen 配置";
        showToast("Qwen 未返回追问选项，请检查模型配置。", 3200);
        return;
    }
    if (data.need_followup === true && followups.length > 0) {
        updateSavedConsultationRecord(data, "待补充", {
            transcript: [state.originalQuery, `AI追问：${followups.map((item) => item.question).join("；")}`],
            analysis: "已生成针对性追问，等待患者选择补充信息。"
        });
        state.awaitingFollowup = true;
        document.body.classList.remove("has-final-result");
        finalResultContent.hidden = true;
        resultPending.hidden = false;
        supplementCard.hidden = false;
        supplementCard.classList.remove("is-submitted");
        diagnosisCard.hidden = true;
        resultPending.querySelector("strong").textContent = "已生成针对性追问";
        resultPending.querySelector("p").textContent = "请根据患者当前症状选择 AI 追问选项，提交后系统再进行病情分析和诊室建议。";
        renderFollowupQuestions(followups);
        showToast("请完成追问并提交补充信息。", 3200);
        return;
    }

    state.awaitingFollowup = false;
    state.result = data;
    updateSavedConsultationRecord(data, "已完成");
    document.body.classList.add("has-final-result");
    finalResultContent.hidden = false;
    resultPending.hidden = true;
    supplementCard.hidden = true;
    supplementCard.classList.add("is-submitted");
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
    const base = sanitizePatientText(analysis || data.analysis || data.answer || "");
    const reason = sanitizePatientText(data.reason || "");
    const departmentReason = sanitizePatientText(data.department_reason || "");
    const patientExplanation = sanitizePatientText(data.patient_explanation || "");
    const urgencyAdvice = sanitizePatientText(data.urgency_advice || "");
    const possibleConditions = Array.isArray(data.possible_conditions)
        ? data.possible_conditions.filter(Boolean).join("、")
        : "";
    const doctorQuestions = Array.isArray(data.doctor_questions)
        ? data.doctor_questions.filter(Boolean).join("；")
        : "";
    const visitPreparation = Array.isArray(data.visit_preparation)
        ? data.visit_preparation.filter(Boolean).join("；")
        : "";

    return [
        { title: "病情概括", text: data.symptom_summary || shortenText(base, 120) || "暂未返回症状概括。" },
        { title: "可能方向", text: patientExplanation || possibleConditions || "需要结合医生面诊和必要检查进一步判断。" },
        { title: "推荐诊室", text: departmentReason || reason || `结合当前描述，建议先到${department}评估。详情请咨询医生。` },
        { title: "风险提示", text: urgencyAdvice || riskText },
        { title: "到诊重点", text: doctorQuestions || `就诊时说明症状开始时间、持续时间、严重程度、是否加重、伴随症状和既往病史。` },
        { title: "就诊前准备", text: visitPreparation || buildVisitPreparation(department) },
        { title: "免责声明", text: "本系统仅提供导诊和健康科普参考，不能替代医生诊断。" }
    ];
}

function getSelectableFollowups(data) {
    const source = data.followup_items || data.follow_up_items || [];
    if (!Array.isArray(source)) return [];
    return source
        .map((item) => ({
            question: String(item?.question || item?.text || "").trim(),
            options: Array.isArray(item?.options)
                ? item.options.map((option) => String(option).trim()).filter(Boolean).slice(0, 6)
                : [],
            multiple: item?.multiple === true || item?.multi_select === true || item?.select_mode === "multiple" || item?.type === "multiple"
        }))
        .filter((item) => item.question && item.options.length >= 2)
        .slice(0, 3);
}

function isQwenUnavailableResponse(data) {
    const text = [
        data.answer,
        data.analysis,
        data.display_text,
        data.reason
    ].filter(Boolean).join(" ");
    return /Qwen|LLM|大模型|API|Key|未返回可选择的追问|解析失败|未检测到/.test(text);
}

function buildVisitPreparation(department) {
    const preparations = {
        "肛肠科": "就诊前记录便血颜色和次数、肛门疼痛或肿痛持续时间、排便习惯变化。",
        "泌尿外科": "记录尿频尿急尿痛出现时间、是否血尿、饮水和排尿情况；就诊前尽量保留近期尿检或相关检查结果。",
        "妇科": "记录末次月经时间、出血量或白带变化、是否腹痛；如有妊娠可能或既往妇科病史请主动说明。",
        "儿科": "准备体温记录、精神状态、进食饮水、大小便情况；儿童就诊建议监护人陪同。",
        "心内科": "记录胸闷心慌发作时间、持续多久、是否活动后加重；如有血压或心率记录请带上。",
        "神经内科": "记录头晕头痛或麻木无力的开始时间、持续时间、是否单侧、是否伴说话不清或面瘫。",
        "内分泌科": "携带近期血糖、甲状腺功能或体重变化记录；说明饮食和多饮多尿情况。",
        "风湿免疫科": "记录关节肿痛部位、晨僵时长、是否反复发作；如有尿酸、炎症指标或影像检查可带上。",
        "精神心理科": "记录睡眠、情绪变化持续时间、压力来源和是否影响工作生活。",
        "感染科/发热门诊": "记录体温峰值、发热天数、接触史、皮疹或咳嗽等伴随症状；就诊时按发热门诊流程分诊。"
    };
    return preparations[department] || `前往${department}前，重点整理与本次症状直接相关的时间、程度、诱因和伴随表现。`;
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
    supplementCard.hidden = true;
    supplementCard.classList.remove("is-submitted");
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
2. 建议携带既往病史、过敏史和历史检查报告等信息就诊。
3. 如果症状持续加重，或出现高热、呼吸困难、意识异常、大量出血、剧烈胸痛等情况，应及时前往急诊或联系医护人员。
4. 本系统仅提供导诊和健康科普参考，不能替代医生诊断。`;
    }

    return `${fallback}

判断依据：
1. 系统根据患者主诉和补充信息判断主要症状方向。
2. 当前未发现足以直接改变推荐科室的强证据。
3. 若存在发热、明显肿胀、活动受限、呼吸困难、症状迅速加重等情况，需要提高风险等级并尽快就医。

就诊建议：
建议前往${department}进行面诊评估。就诊时可向医生说明症状开始时间、持续时间、疼痛或不适程度、是否加重、是否伴随其他症状、是否接触过特殊诱因。

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
建议就诊时向医生说明症状持续时间、严重程度、是否加重、是否伴随发热或其他不适，以及既往病史、过敏史和历史检查报告。`;
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
                Qwen 暂未返回可选择的追问选项，请检查后端 Qwen 配置后重新提交主诉。
            </p>
        `;
        document.getElementById("followupState").textContent = "等待 Qwen 选项";
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

        if (options.length === 0) {
            const empty = document.createElement("p");
            empty.className = "question-empty";
            empty.textContent = "Qwen 未返回此问题的选项，请重新提交主诉生成追问。";
            fieldset.appendChild(empty);
        }

        options.slice(0, 6).forEach((label) => {
            const button = document.createElement("button");
            button.type = "button";
            button.textContent = label;
            fieldset.appendChild(button);
        });

        questionList.appendChild(fieldset);
    });

    document.getElementById("followupState").textContent = "请选择选项";
}

function sanitizePatientText(value) {
    const text = String(value || "").replace(/\s+/g, " ").trim();
    if (!text) return "";
    if (/LLM|Qwen|解析失败|Expecting value|Traceback|Exception|API|Key|大模型调用失败|未检测到/.test(text)) {
        return "";
    }
    return text;
}

function collectSelectedAnswers() {
    return [...questionList.querySelectorAll("fieldset")].flatMap((fieldset) => {
        const selectedButtons = [...fieldset.querySelectorAll("button.selected")];
        if (selectedButtons.length) {
            const selectedText = selectedButtons.map((button) => button.textContent.trim()).join("、");
            return [`${fieldset.dataset.question}：${selectedText}`];
        }
        return [];
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
    hospitalMap.classList.remove("has-six-rooms");
    hospitalMap.classList.add("has-image-map");
    const image = document.createElement("img");
    image.className = "floor-map-image";
    image.src = FLOOR_MAP_IMAGES[activeFloor] || FLOOR_MAP_IMAGES["1F"];
    image.alt = `${activeFloor} 门诊楼平面图`;
    hospitalMap.appendChild(image);
    if (activeFloor === location.floor) {
        const target = document.createElement("span");
        target.className = "map-target";
        target.id = "mapTarget";
        const point = MAP_TARGET_POINTS[department] || MAP_TARGET_POINTS[location.area] || MAP_TARGET_POINTS["导诊台"];
        target.style.left = `${point.x}%`;
        target.style.top = `${point.y}%`;
        target.replaceChildren(document.createTextNode(department));
        const small = document.createElement("small");
        small.textContent = `${location.floor} · ${location.room}`;
        target.appendChild(small);
        hospitalMap.appendChild(target);
    }
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
