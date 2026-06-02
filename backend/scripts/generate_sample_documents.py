"""Generate sample pre-acceptance documents for fraud, property loss, and safety threat."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from app.core.state import CaseState
from app.modules.document_generator import GENERATED_DIR, generate_pre_acceptance_document

SAMPLES: list[CaseState] = [
    CaseState(
        case_id="sample-telecom-fraud",
        user_text="我在闲鱼买演唱会票被骗了，微信转了480元，对方把我拉黑了，有聊天记录和转账截图。",
        scenario="telecom_fraud",
        risk_level="medium",
        completeness_score=0.75,
        slots={
            "reporter_name": "张同学",
            "reporter_contact": "13800138000",
            "incident_time": "2026-05-28 晚间",
            "incident_location": "闲鱼平台（线上）",
            "fraud_method": "购票诈骗",
            "loss_amount": 480,
            "transfer_channel": "微信",
            "platform": "闲鱼",
            "evidence": ["聊天记录", "转账截图"],
            "still_contacting": False,
        },
        missing_fields=["recipient_account"],
        evidence_checklist=["聊天记录", "转账截图"],
        knowledge_snippets=[
            "立即停止继续转账，保存聊天记录、转账凭证与对方账号信息。",
            "可通过平台投诉与公安报案并行固定证据。",
        ],
        next_action="ask_followup",
        next_question="对方收款微信号或账号是否还能找到？",
        police_summary=(
            "报案人反映通过闲鱼购买演唱会门票遭诈骗，已微信转账480元，"
            "对方拉黑；已保留聊天记录与转账截图，建议固定电子证据并补充收款账号。"
        ),
        suggested_next_steps=["保存聊天记录与转账截图", "补充对方收款账号", "向平台投诉并报案"],
    ),
    CaseState(
        case_id="sample-property-loss",
        user_text="昨天下午在图书馆自习室丢了手机，是黑色 iPhone，有手机壳。",
        scenario="property_loss",
        risk_level="low",
        completeness_score=0.82,
        slots={
            "reporter_name": "李同学",
            "reporter_contact": "13900139000",
            "lost_item": "手机",
            "lost_time": "2026-05-29 15:00 左右",
            "lost_location": "图书馆三楼自习室",
            "item_features": "黑色 iPhone，带透明手机壳",
            "item_value": 6000,
            "suspected_theft": True,
            "account_or_id_risk": True,
            "possible_clues": "自习室可能有监控",
        },
        missing_fields=["ownership_proof"],
        evidence_checklist=["购买发票（待补充）", "监控线索待调取"],
        knowledge_snippets=[
            "先确认最后使用时间与活动轨迹，联系图书馆保卫部门调取监控。",
            "若含支付与校园账户，建议同步挂失相关账号。",
        ],
        next_action="ask_followup",
        next_question="是否有购买凭证或序列号可证明权属？",
        police_summary=(
            "报案人称5月29日下午在图书馆三楼自习室遗失黑色 iPhone，"
            "怀疑被盗，证件/账户存在风险，建议调取监控并补充权属证明。"
        ),
        suggested_next_steps=["联系图书馆保卫调取监控", "挂失校园卡与支付账户", "补充购买凭证"],
        extracted_addresses=["图书馆三楼自习室"],
    ),
    CaseState(
        case_id="sample-safety-threat",
        user_text="有人在宿舍楼下堵我，说下次见我要打我，我现在很害怕，不敢回宿舍。",
        scenario="personal_safety_threat",
        risk_level="high",
        completeness_score=0.65,
        slots={
            "reporter_name": "王同学",
            "reporter_contact": "13700137000",
            "threat_type": "口头人身威胁",
            "suspect_info": "同院系男生，穿灰色外套",
            "current_location": "宿舍区北门附近",
            "danger_level": "较高",
            "ongoing_threat": True,
            "current_danger": True,
            "evidence": ["目击同学联系方式"],
        },
        missing_fields=["prior_incidents"],
        evidence_checklist=["目击证人", "威胁短信/录音（待补充）"],
        knowledge_snippets=[
            "人身安全威胁优先确保报案人处于安全环境，必要时安排陪同或转人工处置。",
            "建议保留威胁信息、证人证言，并评估是否需要现场处置。",
        ],
        next_action="handoff_human",
        next_question="你现在是否处于安全位置？对方是否仍在附近？",
        police_summary=(
            "报案人反映遭他人口头人身威胁，威胁可能持续，当前存在即时安全风险，"
            "建议优先保障人身安全并安排民警介入。"
        ),
        suggested_next_steps=["确认报案人当前安全位置", "联系值班民警现场处置", "固定威胁证据与证人"],
    ),
]


def main() -> None:
    out_dir = GENERATED_DIR / "samples"
    out_dir.mkdir(parents=True, exist_ok=True)
    for state in SAMPLES:
        path, name = generate_pre_acceptance_document(state, output_dir=out_dir)
        print(f"{state.scenario}: {name} -> {path}")


if __name__ == "__main__":
    main()
