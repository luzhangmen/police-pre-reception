import json
import os

from app.core.state import CaseState, NextAction
from app.services.llm_client import call_llm_json


_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "followup.md")

with open(_PROMPT_PATH, "r", encoding="utf-8") as f:
    _SYSTEM_PROMPT = f.read()

FIELD_QUESTIONS: dict[str, dict[str, str]] = {
    "telecom_fraud": {
        "reporter_name": "请问你的姓名或登记称呼是什么？",
        "reporter_contact": "请留下一个方便联系你的手机号或联系方式。",
        "incident_time": "这件事大概发生在什么时间？",
        "incident_location": "这件事发生在线上哪个平台或线下什么地点？",
        "fraud_method": "你方便说一下对方是用什么方式骗你的，比如买卖交易、刷单、冒充熟人还是其他情况吗？",
        "loss_amount": "目前大概损失了多少钱？如果有多次转账，也可以先说总金额。",
        "transfer_time": "你是什么时候转账或付款的？",
        "transfer_channel": "钱是通过什么方式转出的，比如微信、支付宝、银行卡或平台担保交易？",
        "recipient_account": "你是否知道对方的收款账号或平台账号？",
        "recipient_name": "你是否知道收款账户对应的姓名或昵称？",
        "suspect_contact_info": "你是否还知道对方的手机号、微信、QQ、平台昵称或其他联系方式？",
        "evidence": "你现在是否还保留聊天记录、转账截图、订单信息或对方账号？",
    },
    "property_loss": {
        "reporter_name": "请问你的姓名或登记称呼是什么？",
        "reporter_contact": "请留下一个方便联系你的手机号或联系方式。",
        "lost_item": "你丢失的具体是什么物品？",
        "lost_time": "你最后一次确认物品还在是什么时间，大概什么时候发现丢失的？",
        "lost_location": "物品大概是在什么地点丢失的？",
        "item_features": "这个物品有什么明显特征，比如颜色、品牌、外观、卡号后四位或保护壳？",
        "item_value": "这个物品大概价值多少钱，或者当时购买价格是多少？",
        "ownership_proof": "你是否有能证明物品属于你的记录，比如照片、购买记录、序列号或校园账户记录？",
        "suspected_theft": "你觉得更像是自己遗失，还是有被盗的迹象？",
        "account_or_id_risk": "丢失物品里是否涉及身份证、银行卡、校园卡、手机账号等需要挂失的内容？",
    },
    "dorm_conflict": {
        "reporter_name": "请问你的姓名或登记称呼是什么？",
        "reporter_contact": "请留下一个方便联系你的手机号或联系方式。",
        "parties": "这次冲突主要涉及谁和谁？",
        "dorm_location": "冲突发生在哪栋宿舍、哪个房间或附近位置？",
        "incident_time": "冲突大概发生在什么时间？",
        "conflict_reason": "冲突主要是因为什么事情引起的？",
        "incident_description": "你能简单说一下事情经过吗？",
        "current_status": "现在冲突是否还在继续？",
        "safety_risk": "目前有没有威胁、堵门、推搡、打架或其他安全风险？",
        "injuries_or_property_damage": "有没有人员受伤或物品损坏？",
        "witnesses_or_evidence": "有没有同学、宿管看到，或者聊天记录、照片、视频等证据？",
        "expected_resolution": "你希望这件事接下来怎么处理，比如调解、制止骚扰或联系辅导员？",
    },
    "personal_safety_threat": {
        "reporter_name": "请问你的姓名或登记称呼是什么？",
        "reporter_contact": "请留下一个方便联系你的手机号或联系方式。",
        "threat_type": "对方具体做了什么让你感到危险，比如跟踪、威胁、骚扰或堵截？",
        "current_location": "你现在在哪里，身边是否有同学、老师或保安可以帮助你？",
        "incident_time": "威胁或骚扰大概发生在什么时间？",
        "incident_location": "威胁或骚扰发生在什么地点？",
        "suspect_info": "对方是谁，你是否认识对方，或者知道对方的姓名、联系方式、外貌特征？",
        "relationship_to_suspect": "你和对方是什么关系，比如同学、室友、前任、陌生人？",
        "threat_content": "对方具体说了什么或做了什么？",
        "current_danger": "危险现在是否正在发生，你目前是否已经到安全位置？",
        "injury_status": "你或者其他人有没有受伤？",
        "evidence": "你是否保留了聊天记录、录音、监控线索或其他证据？",
        "witnesses": "现场有没有目击者或可以帮你作证的人？",
        "immediate_need": "你现在最需要的帮助是什么，比如联系安保、报警、找老师或转人工？",
    },
}

GUIDANCE_MESSAGES = {
    "telecom_fraud": "关键信息已经基本齐了，请先保存聊天记录、转账凭证、平台订单和对方账号，避免继续转账。",
    "property_loss": "关键信息已经基本齐了，请先保留物品特征、丢失时间地点和可能线索，涉及证件或银行卡时尽快挂失。",
    "dorm_conflict": "关键信息已经基本齐了，请先避免继续激化冲突，并保留聊天记录、现场情况或宿管辅导员沟通记录。",
    "personal_safety_threat": "关键信息已经基本齐了，请优先确保自己在安全位置，并保留威胁、跟踪或骚扰证据。",
    "unknown": "请再补充一句，这件事更像诈骗、财物遗失、宿舍冲突，还是人身安全威胁？",
}


def decide_next_action(state: CaseState) -> NextAction:
    if state.risk_level == "high":
        return "handoff_human"
    if state.scenario == "unknown":
        return "ask_followup"
    if state.missing_fields:
        return "ask_followup"
    return "give_guidance"


def generate_next_question(state: CaseState) -> str:
    result = call_llm_json(
        user_prompt=json.dumps(state.model_dump(), ensure_ascii=False),
        system_prompt=_SYSTEM_PROMPT,
    )
    if result and isinstance(result.get("next_question"), str):
        return result["next_question"]
    return _fallback_question(state)


def _fallback_question(state: CaseState) -> str:
    if state.next_action == "handoff_human":
        if state.scenario == "personal_safety_threat":
            return "请先确认你现在是否安全、具体位置在哪里；如果正在受到现实危险，请立即联系现场安保或拨打 110。"
        return "这个情况风险较高，我会建议转人工处理。请先补充你现在是否安全，以及是否还在继续发生。"
    if state.scenario == "unknown":
        return GUIDANCE_MESSAGES["unknown"]
    if state.missing_fields:
        first_missing = state.missing_fields[0]
        return FIELD_QUESTIONS.get(state.scenario, {}).get(
            first_missing,
            f"请再补充：{first_missing}。",
        )
    return GUIDANCE_MESSAGES.get(state.scenario, GUIDANCE_MESSAGES["unknown"])
