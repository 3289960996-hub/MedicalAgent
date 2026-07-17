export const PATIENTS = [
    { name: "张先生", gender: "男", age: 32, phone: "158****8806", tag: "默认就诊人", note: "近期无特殊慢病记录", height: 175, weight: 72, bloodType: "AB", allergy: "阿莫西林", history: "无", remark: "无" },
    { name: "李女士", gender: "女", age: 29, phone: "136****2218", tag: "家人", note: "青霉素过敏史", height: 164, weight: 55, bloodType: "O", allergy: "青霉素", history: "无", remark: "近期睡眠不足" },
    { name: "王小朋友", gender: "男", age: 8, phone: "158****8806", tag: "儿童", note: "儿童就诊建议监护人陪同", height: 128, weight: 27, bloodType: "A", allergy: "暂无", history: "无", remark: "儿童就诊需监护人陪同" },
];

export const DEFAULT_CONSULTATION_RECORDS = [
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
            "头痛是否伴随肢体无力或麻木、发热、颈部僵硬、畏光等情况？患者补充：目前没有这些表现。",
        ],
        analysis: "建议前往神经内科进行面诊评估。就诊时重点说明头痛开始时间、持续时间、疼痛性质、是否加重，以及是否伴随发热、呕吐、肢体无力或意识异常。",
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
            "补充：无明显胸痛、呼吸困难或持续高热，活动后不适减轻。",
        ],
        analysis: "建议先到耳鼻喉科或全科门诊评估。就诊时说明恶心出现的场景、是否伴随眩晕耳鸣、是否呕吐、近期饮食和睡眠情况。",
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
            "补充：疼痛强烈且出现明显不适，需要优先排除急性风险信号。",
        ],
        analysis: "当前记录存在较高风险提示，建议优先到急诊科或请人工导诊确认。若出现意识异常、肢体无力、喷射样呕吐、持续高热或颈部僵硬，应立即急诊。",
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
            "补充：儿童就诊建议监护人陪同，并完整说明症状发生前后的状态变化。",
        ],
        analysis: "建议由儿科先做面诊评估，必要时由医生判断是否转相关专科。就诊时由监护人说明症状出现时间、意识状态、睡眠、近期用药和是否有外伤。",
    },
];

export const VISIT_PLANS = [
    { id: "plan-neuro", time: "09:00", date: "2026-07-01", type: "门诊", department: "神经内科", title: "神经内科门诊评估", location: "门诊楼 4F B区 407-412 诊室", note: "结合患者当前描述，建议由神经内科进一步评估", status: "待处理" },
    { id: "plan-ent-order", time: "09:30", date: "2026-07-01", type: "复诊", department: "耳鼻喉科", title: "耳鼻喉科就诊", location: "门诊楼 3F D区 313-318 诊室", note: "张华华 · 订单号：MA70683036", status: "待处理" },
    { id: "plan-ent-check", time: "10:30", date: "2026-07-01", type: "门诊", department: "耳鼻喉科", title: "耳鼻喉科门诊评估", location: "门诊楼 3F D区 313-318 诊室", note: "症状呈活动诱发，前庭相关特征较明显，建议携带近期检查资料", status: "待处理" },
    { id: "plan-emergency", time: "14:00", date: "2026-07-01", type: "急诊", department: "急诊科", title: "急诊科门诊评估", location: "急诊楼 1F 急诊分诊区", note: "如出现高热、意识异常或剧烈疼痛，应优先急诊", status: "待处理" },
];

export const REGISTER_ORDERS = [
    { id: "order-ent-1", patientName: "张先生", status: "已预约", code: "MA70683036", department: "耳鼻喉科", doctor: "张伟华", time: "09:00", location: "门诊楼 3F D区 313-318 诊室", fee: "已支付", source: "喉咙痛伴鼻塞问诊" },
    { id: "order-ent-2", patientName: "张先生", status: "已取消", code: "MA70682876", department: "耳鼻喉科", doctor: "陈明远", time: "10:30", location: "门诊楼 3F D区 313-318 诊室", fee: "已退回", source: "用户取消" },
    { id: "order-digestive", patientName: "张先生", status: "已完成", code: "MA70682532", department: "消化内科", doctor: "李医生", time: "14:00", location: "门诊楼 3F C区 307-312 诊室", fee: "25元", source: "腹痛腹泻导诊" },
    { id: "order-child-ent", patientName: "王小朋友", status: "已预约", code: "MA70683036", department: "耳鼻喉科", doctor: "张伟华", time: "09:00", location: "门诊楼 3F D区 313-318 诊室", fee: "已支付", source: "喉咙痛伴鼻塞问诊" },
    { id: "order-child-pay", patientName: "王小朋友", status: "待支付", code: "MA70681708", department: "儿科", doctor: "周童", time: "15:30", location: "门诊楼 2F 儿童诊区 206-210 诊室", fee: "25元", source: "儿童发热问诊" },
];

export const FEATURE_DATA = {
    "问诊记录": { title: "问诊记录", desc: "查看最近的模拟问诊记录和导诊结论。", items: ["2026-07-06 皮肤瘙痒与红疹：建议皮肤科", "2026-07-04 咽喉疼痛：建议耳鼻喉科", "2026-07-02 腹痛腹泻：建议消化内科"] },
    "就诊计划": { title: "就诊计划", desc: "整理待就诊事项、预约时间和到院准备。", items: ["今日 14:30 皮肤科普通门诊", "到院前准备过敏史和历史检查报告", "如症状加重，优先转急诊或人工导诊"] },
    "检查检验": { title: "检查检验", desc: "展示检查检验入口和常用报告状态。", items: ["血常规：暂无新报告", "过敏原检测：可按医生建议预约", "影像检查：暂无待查看结果"] },
    "我的订单": { title: "我的订单", desc: "查看模拟挂号、缴费和预约订单。", items: ["挂号订单：暂无待支付", "检查预约：暂无记录", "缴费记录：演示环境暂未接入支付"] },
    "健康档案": { title: "健康档案", desc: "汇总就诊人基础信息、过敏史、既往史和就诊摘要。", items: ["基础信息：男，32岁", "过敏史：暂无记录", "既往病史：暂无特殊记录", "就诊提醒：详情请咨询医生，系统只提供导诊建议"] },
    "预约挂号": { title: "预约挂号", desc: "根据导诊结果选择科室和医生号源。", items: ["完成导诊后可在右侧医生号源中选择时间", "未完成导诊时可先选择全科医学科", "本项目为演示流程，不会产生真实订单"] },
    "院内地图": { title: "院内地图", desc: "查看推荐科室位置和楼层导航。", items: ["1F：导诊台、急诊科、发热门诊", "3F：呼吸内科、消化内科、耳鼻喉科", "5F：骨科、皮肤科、康复医学科"] },
    "报告查询": { title: "报告查询", desc: "模拟查看检查检验报告。", items: ["暂无新报告", "完成检查后可在此查看报告摘要", "异常结果需由医生结合病情解释"] },
    "在线支付": { title: "在线支付", desc: "模拟缴费入口。", items: ["当前没有待支付订单", "真实支付能力未接入", "后续可对接医院支付系统或第三方支付网关"] },
    "常见问题": { title: "常见问题", desc: "整理导诊流程、风险提示和演示系统说明。", items: ["AI 导诊只能作为就诊参考，不能替代医生诊断", "出现胸痛、呼吸困难、意识异常等高危症状应优先急诊", "提交主诉后先完成追问，再查看科室、路线和号源建议"] },
};
