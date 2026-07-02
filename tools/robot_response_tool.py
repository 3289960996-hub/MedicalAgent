def robot_response_tool(answer: str) -> dict:
    """
    机器人输出适配工具。
    机器人播报文本要短，屏幕展示文本可以更完整。
    """

    speak_text = answer.strip()

    if len(speak_text) > 120:
        speak_text = speak_text[:120] + "..."

    return {
        "speak_text": speak_text,
        "display_text": answer
    }
