# crisis_module.py

def check_crisis_level(text: str) -> int:
    text = text.lower()

    # 🔴 Strong crisis triggers (direct self-harm intent)
    strong_triggers = [
        "kill myself",
        "end my life",
        "i want to die",
        "i don't want to live",
        "self harm",
        "hurt myself"
    ]

    # 🟠 Soft crisis triggers (dangerous wording but not direct action)
    soft_triggers = [
        "suicide",
        "ending it all",
        "better off dead"
    ]

    for word in strong_triggers:
        if word in text:
            return 2  # Strong crisis

    for word in soft_triggers:
        if word in text:
            return 1  # Soft crisis

    return 0  # No crisis


def strong_crisis_response() -> str:
    return (
        "I'm really sorry you're feeling this much pain right now. "
        "You don’t have to face this alone.\n\n"

        "Please reach out to someone you trust immediately or contact a crisis helpline:\n"
        "• India: AASRA +91 9820466726 | iCall +91 9152987821\n"
        "• USA: 988 (Suicide & Crisis Lifeline)\n"
        "• UK & Ireland: Samaritans 116 123\n\n"

        "If you feel you might act on these thoughts, please call your local emergency number right now.\n\n"
        "You matter, and help is available."
    )


def soft_crisis_response() -> str:
    return (
        "I can hear how overwhelmed you're feeling, and I'm really sorry you're going through this.\n\n"

        "It might help to talk to someone you trust or a mental health professional.\n"
        "If these thoughts start to feel stronger, please consider reaching out to a helpline:\n"
        "• India: AASRA +91 9820466726 | iCall +91 9152987821\n"
        "• USA: 988 (Suicide & Crisis Lifeline)\n"
        "• UK & Ireland: Samaritans 116 123\n\n"

        "You’re not alone, and support is available when you need it."
    )
