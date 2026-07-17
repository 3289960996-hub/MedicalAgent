export function formatRiskLabel(riskLevel) {
    const value = String(riskLevel || "").toLowerCase();
    if (value.includes("high") || value.includes("高")) return "高风险提示";
    if (value.includes("medium") || value.includes("中")) return "中等风险提示";
    return "低风险提示";
}

export function normalizeConfidenceValue(value) {
    const confidence = Number(value);
    if (!Number.isFinite(confidence)) return 0;
    return confidence > 1 ? confidence / 100 : confidence;
}

export function buildStructuredAnalysis(data, analysis, department) {
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
        { title: "到诊重点", text: doctorQuestions || "就诊时说明症状开始时间、持续时间、严重程度、是否加重、伴随症状和既往病史。" },
        { title: "就诊前准备", text: visitPreparation || buildVisitPreparation(department) },
        { title: "免责声明", text: "本系统仅提供导诊和健康科普参考，不能替代医生诊断。" },
    ];
}

export function getSelectableFollowups(data) {
    const source = data.followup_items || data.follow_up_items || [];
    if (!Array.isArray(source)) return [];
    return source
        .map((item) => ({
            question: String(item?.question || item?.text || "").trim(),
            options: Array.isArray(item?.options)
                ? item.options.map((option) => String(option).trim()).filter(Boolean).slice(0, 6)
                : [],
            multiple: item?.multiple === true || item?.multi_select === true || item?.select_mode === "multiple" || item?.type === "multiple",
        }))
        .filter((item) => item.question && item.options.length >= 2)
        .slice(0, 3);
}

export function isQwenUnavailableResponse(data) {
    const text = [data.answer, data.analysis, data.display_text, data.reason].filter(Boolean).join(" ");
    return /Qwen|LLM|大模型|API|Key|未返回可选择的追问|解析失败|未检测到/.test(text);
}

export function buildVisitPreparation(department) {
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
        "感染科/发热门诊": "记录体温峰值、发热天数、接触史、皮疹或咳嗽等伴随症状；就诊时按发热门诊流程分诊。",
    };
    return preparations[department] || `前往${department}前，重点整理与本次症状直接相关的时间、程度、诱因和伴随表现。`;
}

export function buildClinicalSummary(rawAnalysis, department, wasCorrected) {
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
        "消化内科": "结合患者腹痛、腹泻、恶心、呕吐、胃胀等表现，当前更偏向消化系统相关问题，建议由消化内科进一步评估。",
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

export function truncateSentences(text, maxSentences, maxLength) {
    const sentences = String(text || "").split(/[。！？!?]/).map((item) => item.trim()).filter(Boolean).slice(0, maxSentences);
    const merged = sentences.join("。") + (sentences.length ? "。" : "");
    return merged.length > maxLength ? `${merged.slice(0, maxLength)}...` : merged;
}

export function shortenText(text, maxLength) {
    const normalized = String(text || "暂未返回病情分析。").replace(/\s+/g, " ").trim();
    const firstSentence = normalized.split(/[。！!？?]/)[0];
    return firstSentence.length > maxLength ? `${firstSentence.slice(0, maxLength)}...` : firstSentence;
}

export function sanitizePatientText(value) {
    const text = String(value || "").replace(/\s+/g, " ").trim();
    if (!text) return "";
    if (/LLM|Qwen|解析失败|Expecting value|Traceback|Exception|API|Key|大模型调用失败|未检测到/.test(text)) return "";
    return text;
}
