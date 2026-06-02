"""Full CaseState fixtures for presentation-grade document generation."""

from app.core.state import CaseState

SHOWCASE_CASES: dict[str, CaseState] = {
    "property_loss": CaseState(
        case_id="showcase-loss-library-2026",
        user_text=(
            "那个……警官你好，我就是，嗯，昨天下午吧，大概三四点钟的样子，"
            "我在图书馆三楼那个自习室自习，然后手机放桌上了，"
            "我去接了个水回来就发现没了，反正就是一个黑色的 iPhone，"
            "带透明壳的，里面还有支付宝、微信和校园卡绑定的，"
            "我现在真的很慌，也不知道是被偷了还是我自己掉了，"
            "那个自习室好像有监控，但是我还没去问保卫处……"
        ),
        scenario="property_loss",
        emotion="anxious",
        risk_level="high",
        completeness_score=0.82,
        slots={
            "reporter_name": "李同学",
            "reporter_contact": "13912345678",
            "lost_item": "手机（iPhone）",
            "lost_time": "2026年5月29日 15:00 左右",
            "lost_location": "图书馆三楼自习室",
            "item_features": "黑色机身、透明手机壳",
            "item_value": 6500,
            "suspected_theft": True,
            "account_or_id_risk": True,
            "possible_clues": "自习室可能有监控，尚未联系保卫处",
            "evidence": ["尚未调取监控"],
        },
        missing_fields=["ownership_proof"],
        evidence_checklist=["购买凭证待补充", "监控录像待保卫处调取"],
        key_facts=["遗失：黑色 iPhone", "地点：图书馆三楼自习室", "支付/校园账户存在风险"],
        knowledge_snippets=[
            "先确认最后使用手机的时间与位置，联系图书馆保卫部门申请调取监控。",
            "若绑定支付宝、微信或校园卡，建议立即挂失并修改相关密码。",
            "保留购买凭证、序列号或包装盒照片，便于证明权属。",
        ],
        next_action="ask_followup",
        next_question="是否有购买发票、序列号或包装盒照片可证明手机权属？",
        police_summary=(
            "报案人李同学反映5月29日下午在图书馆三楼自习室遗失黑色 iPhone，"
            "怀疑被盗；手机绑定支付与校园账户，存在证件与资金安全风险。"
            "建议优先调取监控、挂失关联账户，并补充权属证明。"
        ),
        suggested_next_steps=[
            "联系图书馆保卫处调取监控",
            "挂失校园卡与第三方支付账户",
            "补充购买凭证或序列号",
        ],
        extracted_addresses=["图书馆三楼自习室"],
    ),
    "telecom_fraud": CaseState(
        case_id="showcase-fraud-xianyu-2026",
        user_text=(
            "唉警官，我，那个，我这两天在闲鱼上买演唱会票嘛，嗯，"
            "对方让我先微信转480，我转了，然后他又说要保证金200，我又转了，"
            "现在还在催我继续打钱，我真的怕了，聊天记录和截图我都有……"
        ),
        scenario="telecom_fraud",
        emotion="fearful",
        risk_level="high",
        completeness_score=0.68,
        slots={
            "reporter_name": "陈同学",
            "reporter_contact": "13600001111",
            "fraud_method": "购票诈骗",
            "platform": "闲鱼",
            "loss_amount": 680,
            "transfer_channel": "微信",
            "incident_time": "2026年5月28–29日",
            "incident_location": "闲鱼平台（线上）",
            "still_transferring": True,
            "still_contacting": True,
            "evidence": ["聊天记录", "转账截图"],
        },
        missing_fields=["recipient_account", "recipient_name"],
        evidence_checklist=["聊天记录", "转账截图", "对方账号待补充"],
        key_facts=["损失合计约680元", "仍在被催促转账", "渠道：微信/闲鱼"],
        knowledge_snippets=[
            "立即停止一切转账与扫码操作，保存聊天记录、转账凭证与对方账号。",
            "可向平台投诉并同步公安报案，避免二次损失。",
        ],
        next_action="handoff_human",
        next_question="请先停止转账。对方收款微信号或账号是什么？是否还能联系到对方？",
        police_summary=(
            "报案人陈同学反映通过闲鱼购买演唱会门票遭诈骗，已微信转账合计约680元，"
            "对方仍催促继续转账；已保留聊天记录与转账截图。建议止付并立即人工介入。"
        ),
        suggested_next_steps=["停止转账", "固定对方账号", "平台投诉", "转人工处置"],
    ),
    "personal_safety_threat": CaseState(
        case_id="showcase-threat-dormgate-2026",
        user_text=(
            "警官救命，嗯，就是，我室友在外面堵我，说要打我，"
            "我现在在宿舍区北门这边，不敢回去，怎么办啊，之前也骂过我几次了……"
        ),
        scenario="personal_safety_threat",
        emotion="fearful",
        risk_level="high",
        completeness_score=0.7,
        slots={
            "reporter_name": "王同学",
            "reporter_contact": "13700002222",
            "threat_type": "口头人身威胁",
            "suspect_info": "室友，男性，常穿灰色外套",
            "current_location": "宿舍区北门附近",
            "danger_level": "较高",
            "ongoing_threat": True,
            "current_danger": True,
            "prior_incidents": "此前多次辱骂",
            "evidence": ["目击同学联系方式"],
        },
        missing_fields=["immediate_need"],
        evidence_checklist=["目击证人", "威胁录音/短信待补充"],
        key_facts=["威胁可能持续", "报案人当前不敢回宿舍", "位置：宿舍区北门"],
        knowledge_snippets=[
            "人身安全威胁优先确保报案人处于安全环境，必要时安排陪同或转人工处置。",
            "建议保留威胁信息、证人证言，并评估是否需要现场处置。",
        ],
        next_action="handoff_human",
        next_question="你现在是否处于安全位置？对方是否仍在附近？是否需要安排民警到场？",
        police_summary=(
            "报案人王同学反映遭室友口头人身威胁并被堵截，当前在宿舍区北门附近，"
            "不敢返回宿舍，威胁可能持续。建议优先保障人身安全并安排民警介入。"
        ),
        suggested_next_steps=["确认安全位置", "联系值班民警", "固定威胁证据"],
        extracted_addresses=["宿舍区北门"],
    ),
    "dorm_conflict": CaseState(
        case_id="showcase-dorm-noise-2026",
        user_text=(
            "那个，警官，我们宿舍吧，反正就是隔壁床那个同学，"
            "老是半夜打游戏还外放，我说他他就骂我，昨天晚上还推了我一下，"
            "我也没敢还手，就想调解一下……"
        ),
        scenario="dorm_conflict",
        emotion="anxious",
        risk_level="medium",
        completeness_score=0.76,
        slots={
            "reporter_name": "赵同学",
            "reporter_contact": "13500003333",
            "parties": "同宿舍两名同学",
            "dorm_location": "6号楼 312 宿舍",
            "incident_time": "2026年5月29日 夜间",
            "conflict_reason": "作息与噪音矛盾",
            "physical_conflict": True,
            "threat": False,
            "expected_resolution": "调解与宿舍管理介入",
            "witnesses_or_evidence": "同宿舍其他同学可作证",
        },
        missing_fields=["injuries_or_property_damage"],
        key_facts=["存在推搡", "起因：夜间游戏外放", "诉求：调解"],
        knowledge_snippets=[
            "宿舍矛盾优先了解双方陈述，评估是否存在持续骚扰或肢体冲突升级风险。",
            "可联系辅导员、宿管共同调解，必要时记录证据。",
        ],
        next_action="ask_followup",
        next_question="推搡是否造成受伤或财物损坏？是否愿意由宿管老师现场调解？",
        police_summary=(
            "报案人赵同学反映与同宿舍同学因夜间游戏噪音发生冲突，"
            "昨日夜间被对方推搡，希望调解处理；需进一步核实受伤情况与证人。"
        ),
        suggested_next_steps=["联系宿管/辅导员", "询问同宿舍证人", "评估是否升级处置"],
        extracted_addresses=["6号楼312宿舍"],
    ),
}
