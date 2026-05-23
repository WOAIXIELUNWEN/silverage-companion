INTENT_PROMPT = """你是一个意图分类器，负责分析老年人用户的消息属于哪种类型。

请将用户消息分类为以下三种之一：
- chat: 日常闲聊、情感倾诉、问候寒暄、询问天气等
- health: 健康相关问题，如用药、症状、慢病管理、饮食养生、运动建议等
- emergency: 紧急求助信号，如摔倒、胸闷、呼吸困难、剧烈疼痛、意识模糊等

只回复一个单词：chat、health 或 emergency。

用户消息：{message}"""


def classify_sync(message: str) -> str:
    """Fast keyword-based classification as fallback when LLM is unavailable."""
    emergency_keywords = [
        "救命", "不行了", "摔倒", "摔倒了", "胸闷", "呼吸困难", "喘不过气",
        "晕倒", "晕了", "心脏", "心脏病", "中风", "动不了", "快不行了",
        "叫救护车", "120", "急救", "剧烈疼痛", "疼得受不了", "透不过气",
    ]
    health_keywords = [
        "吃药", "血压", "血糖", "头疼", "头晕", "失眠", "关节", "腰疼",
        "腿疼", "胃", "糖尿病", "高血压", "药", "怎么吃", "能不能吃",
        "饮食", "忌口", "运动", "锻炼", "养生", "保健品", "中药",
        "症状", "检查", "体检", "医院", "挂号", "手术",
    ]

    msg_lower = message.lower()
    for kw in emergency_keywords:
        if kw in msg_lower:
            return "emergency"
    for kw in health_keywords:
        if kw in msg_lower:
            return "health"
    return "chat"
