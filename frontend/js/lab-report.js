const LAB_ANALYZE_URL = "http://127.0.0.1:8000/lab-report/analyze";
const LAB_INTERPRET_URL = "http://127.0.0.1:8000/lab-report/interpret";
const ALLOWED_IMAGE_TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);
const MAX_IMAGE_BYTES = 8 * 1024 * 1024;

export function createLabReportController({
    state,
    refreshWorkspace,
    showToast,
    showTriageResultPane,
    showConsultationPage,
    updateCharCount,
}) {
    const labReportPreview = document.getElementById("labReportPreview");
    const labReportCard = document.getElementById("labReportCard");
    const labReviewModal = document.getElementById("labReviewModal");
    const labImageModal = document.getElementById("labImageModal");
    const questionInput = document.getElementById("question");
    let progressTimer = null;

    function setProgress(progress, label) {
        const value = Math.max(0, Math.min(100, Math.round(progress)));
        state.labReport.progress = value;
        state.labReport.progressLabel = label;

        const fill = document.querySelector("[data-lab-progress-fill]");
        const valueNode = document.querySelector("[data-lab-progress-value]");
        const labelNode = document.querySelector("[data-lab-progress-label]");
        if (fill) fill.style.width = `${value}%`;
        if (valueNode) valueNode.textContent = `${value}%`;
        if (labelNode) labelNode.textContent = label;

        const legacyMeta = document.getElementById("labReportMeta");
        if (legacyMeta && state.labReport.status === "loading") legacyMeta.textContent = label;
    }

    function stopProgress() {
        if (!progressTimer) return;
        window.clearInterval(progressTimer);
        progressTimer = null;
    }

    function startProgress() {
        stopProgress();
        const startedAt = Date.now();
        setProgress(6, "正在上传图片…");
        progressTimer = window.setInterval(() => {
            const elapsed = (Date.now() - startedAt) / 1000;
            if (elapsed < 2) {
                setProgress(6 + elapsed * 6, "正在上传图片…");
            } else if (elapsed < 7) {
                setProgress(20 + (elapsed - 2) * 5, "正在识别化验单指标…");
            } else if (elapsed < 10) {
                setProgress(47 + (elapsed - 7) * 5, "正在判断指标异常…");
            } else if (elapsed < 14) {
                setProgress(64 + (elapsed - 10) * 3, "正在检索医学知识库…");
            } else {
                setProgress(Math.min(92, 78 + (elapsed - 14) * 0.7), "正在生成辅助解释…");
            }
        }, 600);
    }

    async function handleUpload(event) {
        const file = event.target.files?.[0];
        event.target.value = "";
        if (!file) return;
        if (!ALLOWED_IMAGE_TYPES.has(file.type)) {
            showToast("仅支持 JPG、PNG 或 WebP 化验单图片。", 3200);
            return;
        }
        if (file.size > MAX_IMAGE_BYTES) {
            showToast("化验单图片不能超过 8MB。", 3200);
            return;
        }

        try {
            const imageDataUrl = await readFileAsDataUrl(file);
            state.labReport = { imageDataUrl, fileName: file.name, result: null, status: "loading", error: "", progress: 6, progressLabel: "正在上传图片…" };
            labReportPreview.src = imageDataUrl;
            document.getElementById("labImageLarge").src = imageDataUrl;
            renderLoading();
            startProgress();

            const result = await requestJson(LAB_ANALYZE_URL, { image_data_url: imageDataUrl });
            stopProgress();
            setProgress(100, "识别完成，等待核对");
            state.labReport.result = result;
            state.labReport.status = "review";
            renderReport(result);
            showToast("化验单识别完成，请先核对数据；核对前不会生成分析。", 4200);
        } catch (error) {
            stopProgress();
            renderError(error.message || "化验单识别失败，请稍后重试。");
            showToast(error.message || "化验单识别失败。", 3600);
        }
    }

    function readFileAsDataUrl(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(String(reader.result || ""));
            reader.onerror = () => reject(new Error("无法读取图片文件。"));
            reader.readAsDataURL(file);
        });
    }

    async function requestJson(url, body) {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });
        let payload = {};
        try {
            payload = await response.json();
        } catch (_) {
            throw new Error("后端未返回有效数据。请确认服务已启动。");
        }
        if (!response.ok) throw new Error(payload.detail || payload.error || `请求失败（${response.status}）`);
        return payload;
    }

    function renderLoading() {
        state.labReport.status = "loading";
        state.labReport.error = "";
        labReportCard.hidden = false;
        document.getElementById("labReportTitle").textContent = state.labReport.fileName || "化验单";
        document.getElementById("labReportMeta").textContent = "正在识别图片中的检验指标…";
        const status = document.getElementById("labReportStatus");
        status.textContent = "识别中";
        status.className = "lab-status loading";
        document.getElementById("labMetricPreview").innerHTML = '<div class="lab-empty-metrics">多模态模型正在读取报告，请稍候…</div>';
        document.getElementById("reviewLabDataBtn").disabled = true;
        refreshWorkspace();
    }

    function renderError(message) {
        stopProgress();
        state.labReport.status = "error";
        state.labReport.error = message;
        const status = document.getElementById("labReportStatus");
        status.textContent = "识别失败";
        status.className = "lab-status error";
        document.getElementById("labReportMeta").textContent = message;
        document.getElementById("labMetricPreview").innerHTML = '<div class="lab-empty-metrics">请检查图片清晰度或模型配置后重新上传。</div>';
        document.getElementById("reviewLabDataBtn").disabled = true;
        refreshWorkspace();
    }

    function renderReport(result) {
        stopProgress();
        state.labReport.progress = 100;
        state.labReport.progressLabel = result.verified ? "分析完成" : "识别完成，等待核对";
        state.labReport.status = result.verified ? "complete" : "review";
        state.labReport.error = "";
        document.getElementById("labReportTitle").textContent = result.report_type || "化验单";
        const verifiedText = result.verified ? " · 已人工核对" : "";
        document.getElementById("labReportMeta").textContent = `已识别 ${result.indicator_count || 0} 项指标 · ${result.abnormal_count || 0} 项异常${verifiedText}`;
        const status = document.getElementById("labReportStatus");
        status.textContent = result.verified ? "已核对" : "待核对";
        status.className = "lab-status";
        document.getElementById("reviewLabDataBtn").disabled = false;

        const preview = document.getElementById("labMetricPreview");
        preview.replaceChildren();
        const abnormal = getAbnormalIndicators(result).slice(0, 3);
        const rows = abnormal.length ? abnormal : (result.indicators || []).slice(0, 3);
        if (!rows.length) {
            const empty = document.createElement("div");
            empty.className = "lab-empty-metrics";
            empty.textContent = "未识别到可核对的检验指标，请上传更清晰的图片。";
            preview.appendChild(empty);
            refreshWorkspace();
            return;
        }
        rows.forEach((item) => {
            const row = document.createElement("div");
            row.className = "lab-metric-row";
            const name = document.createElement("span");
            name.textContent = item.name;
            const value = document.createElement("strong");
            value.textContent = `${item.result || "--"} ${statusArrow(item.status)}`.trim();
            const unit = document.createElement("small");
            unit.textContent = item.unit || "";
            row.append(name, value, unit);
            preview.appendChild(row);
        });
        refreshWorkspace();
    }

    function getAbnormalIndicators(result) {
        return (result?.indicators || []).filter((item) => ["high", "low", "critical"].includes(item.status));
    }

    function statusArrow(status) {
        if (status === "high") return "↑";
        if (status === "low") return "↓";
        if (status === "critical") return "!";
        return "";
    }

    function openReview() {
        const indicators = state.labReport.result?.indicators || [];
        if (!indicators.length) {
            showToast("当前没有可核对的识别数据。");
            return;
        }
        const rows = document.getElementById("labReviewRows");
        rows.replaceChildren();
        indicators.forEach((indicator, index) => {
            const row = document.createElement("tr");
            row.dataset.index = String(index);
            if (Number(indicator.confidence || 0) < 0.75) row.className = "low-confidence";
            ["name", "result", "unit", "reference_range"].forEach((field) => {
                const cell = document.createElement("td");
                const input = document.createElement("input");
                input.dataset.field = field;
                input.value = indicator[field] || "";
                input.maxLength = field === "name" ? 100 : 50;
                cell.appendChild(input);
                row.appendChild(cell);
            });
            const statusCell = document.createElement("td");
            const select = document.createElement("select");
            select.dataset.field = "status";
            [["normal", "正常"], ["high", "偏高"], ["low", "偏低"], ["critical", "危急"], ["unknown", "不确定"]].forEach(([value, label]) => {
                const option = document.createElement("option");
                option.value = value;
                option.textContent = label;
                option.selected = indicator.status === value;
                select.appendChild(option);
            });
            statusCell.appendChild(select);
            row.appendChild(statusCell);
            rows.appendChild(row);
        });
        labReviewModal.hidden = false;
    }

    function closeReview() {
        labReviewModal.hidden = true;
    }

    async function confirmReview() {
        const button = document.getElementById("confirmLabReviewBtn");
        const indicators = [...document.querySelectorAll("#labReviewRows tr")].map((row, index) => {
            const original = state.labReport.result.indicators[index] || {};
            const data = { ...original, confidence: 1 };
            row.querySelectorAll("input,select").forEach((control) => { data[control.dataset.field] = control.value.trim(); });
            const numericValue = Number.parseFloat(data.result);
            data.value = Number.isFinite(numericValue) ? numericValue : null;
            return data;
        }).filter((item) => item.name);
        if (!indicators.length) {
            showToast("请至少保留一项检验指标。");
            return;
        }
        button.disabled = true;
        button.textContent = "重新分析中…";
        try {
            const result = await requestJson(LAB_INTERPRET_URL, {
                report_type: state.labReport.result.report_type || "化验单",
                indicators,
            });
            state.labReport.result = result;
            renderReport(result);
            closeReview();
            showToast("已使用核对后的数据重新生成解读。", 3000);
        } catch (error) {
            showToast(error.message || "重新分析失败。", 3600);
        } finally {
            button.disabled = false;
            button.textContent = "确认无误并重新分析";
        }
    }

    function openImage() {
        if (!state.labReport.imageDataUrl) return;
        labImageModal.hidden = false;
    }

    function closeImage() {
        labImageModal.hidden = true;
    }

    function continueConsultation() {
        const result = state.labReport.result;
        if (!result) return;
        if (!result.verified) {
            showToast("请先对照原图核对识别数据，确认后才能结合报告继续问诊。", 3600);
            openReview();
            return;
        }
        const abnormalNames = getAbnormalIndicators(result).slice(0, 5).map((item) => item.name).join("、");
        questionInput.value = abnormalNames
            ? `我的化验单提示${abnormalNames}异常，同时有以下症状：`
            : "我已经上传并核对化验单，同时有以下症状：";
        updateCharCount();
        showConsultationPage();
        document.querySelectorAll(".app-nav a").forEach((item, index) => item.classList.toggle("active", index === 0));
        showTriageResultPane();
        questionInput.focus();
        showToast("请补充当前症状后发送，系统会结合化验单信息继续问诊。", 3600);
    }

    return {
        closeImage,
        closeReview,
        confirmReview,
        continueConsultation,
        getAbnormalIndicators,
        handleUpload,
        openImage,
        openReview,
    };
}
