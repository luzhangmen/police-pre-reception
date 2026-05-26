"""Extract physical location phrases from user text and structured slots."""

from __future__ import annotations

import re

LOCATION_SLOT_KEYS = (
    "incident_location",
    "lost_location",
    "dorm_location",
    "current_location",
    "time_location",
)

_ONLINE_ONLY_MARKERS = (
    "线上",
    "网络",
    "平台",
    "微信",
    "qq",
    "闲鱼",
    "咸鱼",
    "淘宝",
    "抖音",
    "unknown",
    "online",
    "ticket platform",
    "转账",
)

_CAMPUS_PLACE_SUFFIX = (
    "食堂",
    "图书馆",
    "宿舍",
    "教学楼",
    "体育馆",
    "操场",
    "球场",
    "篮球场",
    "实验室",
    "机房",
    "自习室",
    "洗澡间",
    "更衣室",
    "快递",
    "校门",
    "校区",
    "学院",
    "活动室",
    "琴房",
    "超市",
    "游泳馆",
    "大排档",
    "车间",
    "讨论室",
    "羽毛球馆",
)

_ADDRESS_PATTERN = re.compile(
    r"[\u4e00-\u9fff]{1,12}(?:省|市|自治区|区|县|镇|乡|村|路|街|道|巷|号|楼|栋|室|层|楼)"
    r"[\u4e00-\u9fff0-9A-Za-z\-·]*"
)

_CAMPUS_PATTERN = re.compile(
    r"(?:[东南西北一二三四五六七八九十]?[\u4e00-\u9fff]{0,8}(?:"
    + "|".join(re.escape(suffix) for suffix in _CAMPUS_PLACE_SUFFIX)
    + r"))(?:[\u4e00-\u9fff0-9A-Za-z\-·]{0,12})?"
)


def _is_online_only(value: str) -> bool:
    lowered = value.lower().strip()
    if not lowered:
        return True
    if "/" in lowered:
        parts = [part.strip() for part in lowered.split("/") if part.strip()]
        if parts and all(_is_online_only(part) for part in parts):
            return True
    markers_hit = sum(1 for marker in _ONLINE_ONLY_MARKERS if marker in lowered)
    has_place_hint = any(suffix in value for suffix in _CAMPUS_PLACE_SUFFIX)
    has_admin_division = any(token in value for token in ("省", "市", "区", "县", "路", "街", "号", "楼"))
    if has_place_hint or has_admin_division:
        return False
    return markers_hit >= 1 and len(lowered) < 40


def _clean_fragment(fragment: str) -> str:
    text = fragment.strip(" ，,。；;：:（）()\"'")
    text = re.sub(r"^(?:在|于|到|去|位于|发生在|地点[是为]?)", "", text)
    text = re.sub(r"\d{1,2}月\d{1,2}日.*?(?:，|,)", "", text)
    text = re.sub(r"\d{1,2}:\d{2}", "", text)
    text = re.sub(r"\d{1,2}时\d{0,2}分?", "", text)
    text = re.sub(r"\s+", "", text)
    return text.strip(" ，,。；;")


def _split_time_location(value: str) -> list[str]:
    parts: list[str] = []
    for chunk in re.split(r"[，,；;]", value):
        chunk = _clean_fragment(chunk)
        if not chunk:
            continue
        if any(token in chunk for token in ("月", "日", "时", "许", "凌晨", "晚上", "中午", "下午")):
            if any(suffix in chunk for suffix in _CAMPUS_PLACE_SUFFIX + ("宿舍", "教室", "楼", "区", "馆")):
                parts.append(chunk)
            continue
        parts.append(chunk)
    return parts


def extract_addresses(text: str, slots: dict | None = None, *, max_items: int = 3) -> list[str]:
    """Return deduplicated physical location strings, most specific first."""
    slots = slots or {}
    candidates: list[str] = []

    for key in LOCATION_SLOT_KEYS:
        raw = slots.get(key)
        if raw is None:
            continue
        value = str(raw).strip()
        if not value or _is_online_only(value):
            continue
        if key == "time_location":
            candidates.extend(_split_time_location(value))
        else:
            for part in re.split(r"[／/|]", value):
                cleaned = _clean_fragment(part)
                if cleaned and not _is_online_only(cleaned):
                    candidates.append(cleaned)
        continue

    for match in _ADDRESS_PATTERN.finditer(text):
        candidates.append(_clean_fragment(match.group(0)))

    for match in _CAMPUS_PATTERN.finditer(text):
        candidates.append(_clean_fragment(match.group(0)))

    deduped: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        if len(item) < 2:
            continue
        key = item.casefold()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    return deduped[:max_items]
