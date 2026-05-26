#!/usr/bin/env python3
"""Generate micro-variants for each base transcript (4 per parent -> 144 variants)."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
BASE_PATH = FIXTURES / "demo_transcripts_three_scenarios.json"
OUT_PATH = FIXTURES / "demo_transcripts_three_scenarios_variants.json"

VARIANTS_PER_PARENT = 4

SUBJECTS = [
    ("李某", "男", 20, "大二"),
    ("王某", "女", 19, "大一"),
    ("张某", "男", 21, "大三"),
    ("赵某", "女", 22, "大四"),
]

# 姓名轮换：原笔录姓氏 -> 变体姓氏
NAME_CYCLE = ["李某", "王某", "张某", "赵某", "陈某", "刘某", "周某", "吴某"]

LOCATION_SWAPS = {
    "一食堂": ["二食堂", "三楼食堂", "教工餐厅"],
    "图书馆": ["南区图书馆", "北区阅览室", "图书馆四楼"],
    "宿舍302": ["宿舍415", "宿舍208", "宿舍517"],
    "东区篮球场": ["西区篮球场", "体育馆旁球场", "北区篮球场"],
    "体育馆": ["游泳馆更衣室", "综合馆更衣室", "训练馆"],
    "机房": ["计算机实验室", "信息楼机房", "实验中心机房"],
    "闲鱼": ["转转", "闲鱼", "闲鱼同城"],
    "QQ群": ["微信群", "QQ群", "贴吧私信"],
    "顺丰": ["圆通", "中通", "韵达"],
}

EXTRA_NOTES = {
    "fraud": [
        "变体：更换受害人姓名与年级，金额略浮动",
        "变体：转账时间前后错开1-2日，平台昵称不同",
        "变体：渠道表述改为同学代转/另一支付工具",
        "变体：证据保存位置不同（云端/另一部手机）",
    ],
    "theft": [
        "变体：更换受害人、案发楼层/区域",
        "变体：物品颜色品牌微调，时间改为相邻日期",
        "变体：监控/线索描述略不同",
        "变体：挂失/报备部门表述不同",
    ],
    "fight": [
        "变体：更换当事人姓名与宿舍号",
        "变体：伤情描述轻重略不同，时间错开",
        "变体：诉求从调解改为调宿/处分",
        "变体：见证/宿管介入细节不同",
    ],
}


def _next_name(used: str, index: int) -> str:
    for offset in range(len(NAME_CYCLE)):
        candidate = NAME_CYCLE[(index + offset) % len(NAME_CYCLE)]
        if candidate != used.split("，")[0]:
            return candidate
    return NAME_CYCLE[index % len(NAME_CYCLE)]


def _replace_surname(text: str, old_surname: str, new_surname: str) -> str:
    if not old_surname or old_surname == new_surname:
        return text
    return text.replace(old_surname[0], new_surname[0], 1).replace(old_surname, new_surname)


def _scale_amount(value: int | float, factor: float) -> int:
    if isinstance(value, float):
        return int(round(value * factor))
    return int(round(value * factor))


def _swap_token(text: str, key: str, options: list[str], variant_idx: int) -> str:
    if key not in text:
        return text
    choice = options[variant_idx % len(options)]
    return text.replace(key, choice, 1)


def _shift_dates(text: str, day_delta: int) -> str:
    def repl(match: re.Match[str]) -> str:
        month = int(match.group(1))
        day = int(match.group(2))
        day = max(1, min(28, day + day_delta))
        return f"{month}月{day}日"

    return re.sub(r"(\d{1,2})月(\d{1,2})日", repl, text)


def _replace_amounts_in_text(text: str, old_amt: int, new_amt: int) -> str:
    if old_amt == new_amt:
        return text
    text = text.replace(str(old_amt), str(new_amt))
    # 中文数字场景：五万 -> 略，仅处理阿拉伯数字
    return text


def mutate_transcript(base: dict, variant_idx: int) -> dict:
    """Create one micro-variant from a base transcript."""
    variant = copy.deepcopy(base)
    parent_id = base["id"]
    variant["parent_id"] = parent_id
    variant["variant_index"] = variant_idx + 1
    variant["id"] = f"{parent_id}-v{variant_idx + 1:02d}"
    variant["variant_type"] = "micro_diff"
    category = base["category"]

    old_subject = base.get("subject", "李某，男，20岁")
    old_name = old_subject.split("，")[0] if "，" in old_subject else "李某"
    sub = SUBJECTS[variant_idx % len(SUBJECTS)]
    new_name = _next_name(old_name, variant_idx + hash(parent_id) % 5)
    gender, age, grade = sub[1], sub[2] + (variant_idx % 2), sub[3]
    variant["subject"] = f"{new_name}，{gender}，{age}岁，某高校{grade}学生"

    day_shift = variant_idx - 1  # -1,0,1,2
    if base.get("incident_time"):
        variant["incident_time"] = _shift_dates(base["incident_time"], day_shift)

    slots = copy.deepcopy(base.get("expected_slots", {}))
    old_amount = slots.get("loss_amount")
    if isinstance(old_amount, (int, float)):
        factors = [1.0, 1.1, 0.92, 1.05]
        new_amount = _scale_amount(old_amount, factors[variant_idx % 4])
        slots["loss_amount"] = new_amount

    body = base["body"]
    summary = base["plain_summary"]
    title = base["title"]

    body = _replace_surname(body, old_name, new_name)
    summary = _replace_surname(summary, old_name, new_name)
    body = _shift_dates(body, day_shift)
    summary = _shift_dates(summary, day_shift)

    if isinstance(old_amount, (int, float)) and "loss_amount" in slots:
        body = _replace_amounts_in_text(body, old_amount, slots["loss_amount"])
        summary = _replace_amounts_in_text(summary, old_amount, slots["loss_amount"])

    for key, options in LOCATION_SWAPS.items():
        if key in body or key in summary:
            body = _swap_token(body, key, options, variant_idx)
            summary = _swap_token(summary, key, options, variant_idx)
            if key in str(slots.get("platform", "")):
                slots["platform"] = options[variant_idx % len(options)]
            if key in str(slots.get("lost_location", "")):
                slots["lost_location"] = _swap_token(
                    str(slots.get("lost_location", "")), key, options, variant_idx
                )
            if key in str(slots.get("time_location", "")):
                slots["time_location"] = _swap_token(
                    str(slots.get("time_location", "")), key, options, variant_idx
                )

    # 昵称/小特征差异
    nick_swaps = [("票务小王", "票务小李"), ("票务小王", "卖家阿杰"), ("票务小王", "黄牛小陈")]
    if variant_idx < len(nick_swaps) and "票务小王" in body:
        old_nick, new_nick = nick_swaps[variant_idx]
        body = body.replace(old_nick, new_nick)
        summary = summary.replace(old_nick, new_nick)

    evidence_phrases = [
        "聊天截图和转账记录",
        "微信聊天记录与支付凭证",
        "手机相册截图及银行通知",
        "云端备份的聊天与转账记录",
    ]
    if "evidence" in slots and category == "fraud":
        slots["evidence"] = evidence_phrases[variant_idx % len(evidence_phrases)]
        if "证据" in body:
            body = re.sub(
                r"答：有[^。\n]+[。]",
                f"答：有{slots['evidence']}。",
                body,
                count=1,
            )

    variant["body"] = body
    variant["plain_summary"] = summary
    if "变体" not in title:
        variant["title"] = f"{title}（变体{variant_idx + 1}）"
    else:
        variant["title"] = title

    variant["diff_notes"] = EXTRA_NOTES.get(category, ["微差变体"])[variant_idx % 4]
    variant["diff_dimensions"] = {
        "person": f"{old_name} -> {new_name}",
        "time_shift_days": day_shift,
        "amount_changed": isinstance(old_amount, (int, float)),
    }

    # 重算 missing / completeness
    req = {
        "telecom_fraud": ["fraud_method", "loss_amount", "transfer_channel", "evidence"],
        "property_loss": ["lost_item", "lost_time", "lost_location", "item_features"],
        "dorm_conflict": ["parties", "conflict_reason", "time_location", "expected_resolution"],
    }[base["scenario"]]
    missing = [f for f in req if not slots.get(f)]
    variant["expected_missing_fields"] = missing
    variant["expected_completeness"] = round(
        len([f for f in req if slots.get(f)]) / len(req), 2
    )

    if "parties" in slots:
        parties = str(slots["parties"])
        if old_name in parties or old_name[0] in parties:
            slots["parties"] = parties.replace(old_name, new_name).replace(
                old_name[0] + "某", new_name[0] + "某"
            )

    variant["expected_slots"] = slots
    return variant


def main() -> None:
    payload = json.loads(BASE_PATH.read_text(encoding="utf-8"))
    bases: list[dict] = payload["transcripts"]
    variants: list[dict] = []
    for base in bases:
        for idx in range(VARIANTS_PER_PARENT):
            variants.append(mutate_transcript(base, idx))

    out = {
        "meta": {
            "version": "1.0",
            "description": "三类笔录的微差变体：同一案情框架，不同人/时间/地点/金额等",
            "maintainer": "陆宣辰",
            "parent_file": "demo_transcripts_three_scenarios.json",
            "variants_per_parent": VARIANTS_PER_PARENT,
            "parent_count": len(bases),
            "total_variants": len(variants),
        },
        "variants": variants,
    }
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Parents: {len(bases)}, variants: {len(variants)} -> {OUT_PATH}")


if __name__ == "__main__":
    main()
