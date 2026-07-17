export function renderLabAnalysisPage(state, escapeHtml, getAbnormalIndicators) {
    const report = state.labReport.result;
    const status = state.labReport.status || (report ? "complete" : "idle");
    const view = {
        report,
        status,
        statusLabel: status === "loading" ? "识别中" : status === "error" ? "识别失败" : report && !report.verified ? "待人工核对" : report ? "分析完成" : "等待上传",
        fileName: state.labReport.fileName || "",
        imageDataUrl: state.labReport.imageDataUrl || "",
        error: state.labReport.error || "",
        progress: Number(state.labReport.progress || 0),
        progressLabel: state.labReport.progressLabel || "正在准备分析…",
    };
    const preview = view.imageDataUrl ? `
        <div class="lab-analysis-preview">
            <img src="${escapeHtml(view.imageDataUrl)}" alt="已上传化验单预览">
            <div><strong>${escapeHtml(view.fileName || "已上传化验单")}</strong><small>${view.status === "loading" ? escapeHtml(view.progressLabel) : view.report ? `已识别 ${view.report.indicator_count || (view.report.indicators || []).length || 0} 项指标` : "等待重新上传"}</small></div>
        </div>
    ` : "";

    return `
        <div class="lab-analysis-page">
            <div class="lab-analysis-title">
                <div><p class="lab-analysis-eyebrow">LAB REPORT INTELLIGENCE</p><h1>化验单智能解读</h1><p>上传化验单后，系统自动识别指标与参考范围，判断异常并生成通俗、谨慎的辅助解释。</p></div>
                <span class="lab-analysis-privacy">隐私保护 · 原图仅用于本次识别</span>
            </div>
            <div class="lab-analysis-grid">
                <section class="lab-analysis-card lab-analysis-upload">
                    <div class="lab-analysis-card-head"><h2>上传报告</h2><span class="lab-analysis-step">第 1 步</span></div>
                    <div class="lab-analysis-dropzone">
                        <div class="lab-analysis-upload-icon">⇧</div>
                        <h3>${view.fileName ? "重新上传化验单" : "选择清晰的化验单图片"}</h3>
                        <p>建议上传完整、端正、无强反光的报告图片</p>
                        <button type="button" class="lab-analysis-upload-button" data-lab-page-action="upload">${view.fileName ? "重新选择" : "选择化验单"}</button>
                        <div class="lab-analysis-formats"><span>JPG</span><span>PNG</span><span>WebP</span><span class="planned">PDF · 规划中</span></div>
                        ${preview}
                    </div>
                    <div class="lab-analysis-hint"><b>!</b><span>医学报告可能包含敏感信息，上传前建议遮挡姓名、证件号和条形码。</span></div>
                    <div class="lab-analysis-types"><strong>支持的常见报告类型</strong><div class="lab-analysis-chips"><span>血常规</span><span>肝功能</span><span>肾功能</span><span>血脂</span><span>血糖</span><span>甲状腺</span><span>乙肝五项</span><span>其他检验</span></div></div>
                </section>
                ${renderReport(view, escapeHtml, getAbnormalIndicators)}
                <section class="lab-analysis-card lab-analysis-flow">
                    <div class="lab-analysis-flow-list">
                        <div class="lab-analysis-flow-item"><i>1</i><strong>上传报告</strong><small>图片文件</small></div>
                        <div class="lab-analysis-flow-item"><i>2</i><strong>OCR 识别</strong><small>提取指标信息</small></div>
                        <div class="lab-analysis-flow-item"><i>3</i><strong>异常判断</strong><small>升高 / 降低</small></div>
                        <div class="lab-analysis-flow-item"><i>4</i><strong>生成解读</strong><small>固定格式报告</small></div>
                    </div>
                    <div class="lab-analysis-flow-disclaimer"><strong>重要提示</strong><span>本分析仅用于辅助理解报告，不构成医疗诊断或治疗建议。</span></div>
                </section>
            </div>
        </div>
    `;
}

function renderReport(view, escapeHtml, getAbnormalIndicators) {
    const report = view.report || {};
    const indicators = Array.isArray(report.indicators) ? report.indicators : [];
    if (view.report && !report.verified) {
        const rows = indicators.map((item) => `
            <div class="lab-analysis-abnormal-row">
                <span>${escapeHtml(item.name || "未命名指标")}</span>
                <strong>${escapeHtml(item.result || "--")} ${escapeHtml(item.unit || "")}</strong>
                <span>${escapeHtml(item.reference_range || "参考范围待核对")}</span>
                <em>${Math.round(Number(item.confidence || 0) * 100)}%</em>
            </div>
        `).join("");
        return `
            <section class="lab-analysis-card lab-analysis-report">
                <div class="lab-analysis-report-head"><div><h2>识别结果待核对</h2><p>${escapeHtml(view.fileName || "化验单")}</p></div><span class="lab-analysis-report-status">待人工核对</span></div>
                <div class="lab-analysis-report-body">
                    <div class="lab-analysis-overview"><div><span>识别类型</span><strong>${escapeHtml(report.report_type || "化验单")}</strong></div><div><span>图片质量</span><strong>${escapeHtml(report.image_quality === "partial" ? "部分可读" : "清晰")}</strong></div></div>
                    <section class="lab-analysis-section abnormal"><h3><span class="lab-analysis-number">2</span>待核对指标</h3><div class="lab-analysis-abnormal-list">${rows}</div></section>
                    <section class="lab-analysis-section"><h3><span class="lab-analysis-number">3</span>安全提示</h3><p>系统尚未生成医学分析。请对照原图逐项核对项目、结果、单位和参考范围；确认后才会生成解读。</p>${report.quality_reason ? `<p>${escapeHtml(report.quality_reason)}</p>` : ""}</section>
                </div>
                <div class="lab-analysis-report-actions">
                    <button type="button" data-lab-page-action="view-image">查看原图</button>
                    <button type="button" class="primary" data-lab-page-action="review">核对识别数据</button>
                </div>
            </section>
        `;
    }

    const abnormal = getAbnormalIndicators(report);
    const reportType = report.report_type || "尚未识别";
    const sampleInfo = typeof report.sample_info === "string" ? report.sample_info : report.sample_type || "未提供";
    const interpretation = polishAnalysisText(report.interpretation || report.abnormal_summary || "上传化验单后，系统将在这里解释异常指标的可能意义。");
    const comprehensive = report.report?.comprehensive_analysis || {};
    const mainAbnormalities = polishAnalysisText(comprehensive.main_abnormalities || report.abnormal_summary || (abnormal.length ? `本次共识别 ${indicators.length} 项指标，其中 ${abnormal.length} 项需要关注。具体意义需结合症状、病史和医生面诊综合判断。` : "识别完成后将在这里汇总主要异常和建议关注方向。"));
    const possibleSystems = (Array.isArray(comprehensive.possible_systems) ? comprehensive.possible_systems : (Array.isArray(report.possible_systems) ? report.possible_systems : [])).map(polishAnalysisText);
    const possibleDirections = (Array.isArray(comprehensive.possible_directions) ? comprehensive.possible_directions : (Array.isArray(report.possible_directions) ? report.possible_directions : [])).map(polishAnalysisText);
    const riskLevel = comprehensive.risk_level || report.risk_level || (abnormal.length ? "建议关注" : "正常");
    const suggestedChecks = (Array.isArray(comprehensive.suggested_checks) ? comprehensive.suggested_checks : (Array.isArray(report.suggested_checks) ? report.suggested_checks : (Array.isArray(report.recommendations) ? report.recommendations : []))).map(polishAnalysisText);
    const comprehensiveHtml = `
        <p><strong>报告结论：</strong>${escapeHtml(mainAbnormalities)}</p>
        <p><strong>关注系统：</strong>${escapeHtml(possibleSystems.length ? possibleSystems.join("、") : "需要结合具体指标进一步判断")}</p>
        <p><strong>关注方向：</strong>${escapeHtml(possibleDirections.length ? possibleDirections.join("；") : "需要结合其他指标、症状和病史判断")}</p>
        <p><strong>风险等级：</strong>${escapeHtml(riskLevel)}</p>
        <p><strong>复核建议：</strong>${escapeHtml(suggestedChecks.length ? suggestedChecks.join("；") : "建议结合检查目的咨询医生")}</p>
    `;
    const recommendations = Array.isArray(report.recommendations) && report.recommendations.length
        ? report.recommendations.map(polishAnalysisText)
        : ["识别完成后，将根据异常指标给出进一步检查和就医关注方向。"];
    const statusClass = view.status === "loading" ? "loading" : view.status === "error" ? "error" : "";
    const abnormalHtml = abnormal.length ? abnormal.slice(0, 8).map((item) => `
        <div class="lab-analysis-abnormal-row"><span>${escapeHtml(item.name || "未命名指标")}</span><strong>${escapeHtml(item.result || "--")} ${escapeHtml(item.unit || "")}</strong><span>${escapeHtml(item.reference_range || "参考范围未知")}</span><em>${escapeHtml(statusLabel(item.status))}</em></div>
    `).join("") : `<span class="lab-analysis-empty">${view.status === "loading" ? "正在提取报告中的检验指标…" : view.status === "error" ? escapeHtml(view.error || "识别失败，请重新上传。") : "尚未识别到异常指标。"}</span>`;
    const explanationHtml = abnormal.length ? abnormal.slice(0, 5).map((item) => `<p><strong>${escapeHtml(item.name || "该指标")}</strong>：${escapeHtml(polishAnalysisText(item.explanation || `该指标${statusLabel(item.status)}，可能提示相关生理状态发生变化，需结合其他指标和临床情况理解。`))}</p>`).join("") : `<p>${escapeHtml(interpretation)}</p>`;
    const progressHtml = view.status === "loading" ? `
        <div class="lab-analysis-progress" role="status" aria-live="polite">
            <div class="lab-analysis-progress-head">
                <strong data-lab-progress-label>${escapeHtml(view.progressLabel)}</strong>
                <span data-lab-progress-value>${Math.round(view.progress)}%</span>
            </div>
            <div class="lab-analysis-progress-track" aria-hidden="true">
                <i data-lab-progress-fill style="width:${Math.round(view.progress)}%"></i>
            </div>
            <small>正在调用多模态识别和医学知识库，通常需要几十秒，请勿关闭页面。</small>
        </div>
    ` : "";

    return `
        <section class="lab-analysis-card lab-analysis-report">
            <div class="lab-analysis-report-head"><div><h2>智能分析报告</h2><p>${escapeHtml(view.fileName || "上传报告后自动生成")}</p></div><span class="lab-analysis-report-status ${statusClass}">${escapeHtml(view.statusLabel)}</span></div>
            ${progressHtml}
            <div class="lab-analysis-report-body">
                <div class="lab-analysis-overview"><div><span>1. 检查类型</span><strong>${escapeHtml(reportType)}</strong></div><div><span>样本信息</span><strong>${escapeHtml(sampleInfo)}</strong></div></div>
                <section class="lab-analysis-section abnormal"><h3><span class="lab-analysis-number">2</span>异常指标</h3><div class="lab-analysis-abnormal-list">${abnormalHtml}</div></section>
                <section class="lab-analysis-section"><h3><span class="lab-analysis-number">3</span>重点指标解读</h3>${explanationHtml}</section>
                <section class="lab-analysis-section"><h3><span class="lab-analysis-number">4</span>综合分析</h3>${comprehensiveHtml}</section>
                <section class="lab-analysis-section"><h3><span class="lab-analysis-number">5</span>后续建议</h3><ul>${recommendations.slice(0, 5).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></section>
                <div class="lab-analysis-disclaimer">6. 本分析仅用于辅助理解报告，不构成医疗诊断或治疗建议。</div>
            </div>
            <div class="lab-analysis-report-actions">
                ${view.imageDataUrl ? `<button type="button" data-lab-page-action="view-image">查看原图</button>` : ""}
                ${view.report ? `<button type="button" class="primary" data-lab-page-action="continue">结合症状继续问诊</button>` : ""}
            </div>
        </section>
    `;
}

function statusLabel(status) {
    const value = String(status || "unknown").toLowerCase();
    if (value === "high" || value === "critical") return "升高";
    if (value === "low") return "降低";
    if (value === "normal") return "正常";
    return "需要复核";
}

function polishAnalysisText(value) {
    return String(value ?? "")
        .replace(/(可能提示)(?:\s*可能提示)+/g, "$1")
        .replace(/可能提示\s*可能(?:提示)?/g, "可能提示")
        .replace(/可能\s*可能/g, "可能");
}
