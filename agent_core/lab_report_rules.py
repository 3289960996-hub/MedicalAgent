import re
from typing import Any


VALID_STATUSES = {"high", "low", "normal", "critical", "unknown"}
ABNORMAL_STATUSES = {"high", "low", "critical"}
_NUMBER = r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)"
_RANGE_PATTERN = re.compile(rf"^\s*({_NUMBER})\s*(?:-|~|～|—|–|至)\s*({_NUMBER})\s*$")
_LIMIT_PATTERN = re.compile(rf"^\s*(<=|>=|<|>|≤|≥)\s*({_NUMBER})")


def apply_indicator_rules(indicators: list[dict[str, Any]], *, allow_confirmed_status: bool = False) -> list[dict[str, Any]]:
    return [apply_indicator_rule(item, allow_confirmed_status=allow_confirmed_status) for item in indicators]


def apply_indicator_rule(indicator: dict[str, Any], *, allow_confirmed_status: bool = False) -> dict[str, Any]:
    item = dict(indicator)
    status, source = _determine_status(item)

    if status == "unknown" and allow_confirmed_status:
        confirmed = str(item.get("status") or "unknown").lower()
        if confirmed in VALID_STATUSES:
            status, source = confirmed, "manual_review"

    item["status"] = status
    item["status_source"] = source
    item["abnormal_direction"] = _direction(status, item)
    return item


def _determine_status(indicator: dict[str, Any]) -> tuple[str, str]:
    explicit = _explicit_status(indicator)
    if explicit:
        return explicit, "source_flag"

    result_text = str(indicator.get("result") or "").strip()
    reference = str(indicator.get("reference_range") or "").strip()
    qualitative = _qualitative_status(result_text, reference)
    if qualitative:
        return qualitative, "reference_range"

    value = _coerce_number(indicator.get("value"))
    if value is None:
        value = _extract_first_number(result_text)
    if value is None or not reference:
        return "unknown", "unresolved"

    normalized_reference = reference.replace(",", "").strip()
    range_match = _RANGE_PATTERN.match(normalized_reference)
    if range_match:
        lower, upper = float(range_match.group(1)), float(range_match.group(2))
        if lower > upper:
            lower, upper = upper, lower
        return ("low", "reference_range") if value < lower else ("high", "reference_range") if value > upper else ("normal", "reference_range")

    limit_match = _LIMIT_PATTERN.match(normalized_reference)
    if limit_match:
        operator, bound = limit_match.group(1), float(limit_match.group(2))
        if operator in {"<", "≤", "<="}:
            normal = value < bound if operator == "<" else value <= bound
            return ("normal", "reference_range") if normal else ("high", "reference_range")
        normal = value > bound if operator == ">" else value >= bound
        return ("normal", "reference_range") if normal else ("low", "reference_range")

    return "unknown", "unresolved"


def _explicit_status(indicator: dict[str, Any]) -> str | None:
    text = " ".join([
        str(indicator.get("source_flag") or ""),
        str(indicator.get("result") or ""),
    ]).strip().lower()
    if re.search(r"危急|critical|危重", text):
        return "critical"
    if re.search(r"(?:^|\s)(?:h|high)(?:$|\s)|↑|升高|偏高", text):
        return "high"
    if re.search(r"(?:^|\s)(?:l|low)(?:$|\s)|↓|降低|偏低", text):
        return "low"
    return None


def _qualitative_status(result: str, reference: str) -> str | None:
    result_text = result.strip().lower()
    reference_text = reference.strip().lower()
    negative_tokens = ("阴性", "negative", "未检出")
    positive_tokens = ("阳性", "positive", "检出")
    reference_negative = any(token in reference_text for token in negative_tokens)
    reference_positive = any(token in reference_text for token in positive_tokens)
    result_negative = any(token in result_text for token in negative_tokens)
    result_positive = any(token in result_text for token in positive_tokens)
    if reference_negative and (result_negative or result_positive):
        return "normal" if result_negative and not result_positive else "high"
    if reference_positive and (result_negative or result_positive):
        return "normal" if result_positive else "low"
    return None


def _coerce_number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def _extract_first_number(text: str) -> float | None:
    match = re.search(_NUMBER, text.replace(",", ""))
    return float(match.group(0)) if match else None


def _direction(status: str, indicator: dict[str, Any]) -> str:
    if status == "high":
        result = str(indicator.get("result") or "")
        return "阳性" if "阳性" in result else "升高"
    if status == "low":
        return "降低"
    if status == "critical":
        return "危急"
    if status == "normal":
        return "正常"
    return "需要复核"
