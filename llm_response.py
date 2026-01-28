import requests

OPENROUTER_API_KEY = "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"


def generate_reply(user_text, intent, rag_context, recent_intents):
    history_summary = ", ".join(recent_intents[-5:]) if recent_intents else "No recent emotional pattern."

    short_triggers = ["hi", "hii", "hello", "hey", "yo"]

    if intent in ["greeting", "normal"] and user_text.lower().strip() in short_triggers:
        style_rule = "Reply very casually in 5–8 words. Friendly. No questions."
    elif intent in ["greeting", "normal"]:
        style_rule = "Reply shortly and casually in one sentence."
    else:
        style_rule = "Give a warm, empathetic, supportive reply in 2–3 sentences."

    prompt = f"""
You are a compassionate mental health support assistant.

{style_rule}

User recent emotional pattern: {history_summary}
Current detected emotion: {intent}

Helpful support context:
{rag_context}

User message:
{user_text}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
    )

    return response.json()["choices"][0]["message"]["content"].strip()
