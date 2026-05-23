SAFETY_PROMPT = """你是内容安全审核员。请检查以下AI助手的回复是否适合老年人阅读。

检查项目：
1. 是否包含医疗诊断或处方建议（不允许）
2. 是否推荐了具体药品品牌（不允许）
3. 是否包含可能引起恐慌的内容（不允许）
4. 是否包含不尊重老年人的用语（不允许）
5. 语言是否足够简单清晰

如果回复完全合规，请原样返回回复内容。
如果有问题，请修改为合规版本后返回。不要输出任何解释，只输出最终回复。

待审核回复：
{response}"""


def basic_filter(text: str) -> str:
    """Quick local filter to strip obviously problematic patterns."""
    import re

    # Strip any "我建议你服用xxx药" patterns — too prescriptive
    text = re.sub(r"建议你?[购买服用]+\S+药", "建议咨询医生后再用药", text)
    # Replace dosage numbers
    text = re.sub(r"(\d+)(片|粒|颗|毫克|mg|ml)", r"\1\2（请遵医嘱）", text)

    return text
