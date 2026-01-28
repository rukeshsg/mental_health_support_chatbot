from crisis_module import check_crisis_level, strong_crisis_response, soft_crisis_response
from logger import save_intent, get_recent_intents
from rag_engine import search, situations, responses, index

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from llm_response import generate_reply


# ✅ Load label classes
label_classes = np.load("label_classes.npy", allow_pickle=True)

# ✅ Load Universal Sentence Encoder
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


# ✅ Rebuild same model architecture used during training
intent_model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(512,)),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(len(label_classes), activation='softmax')
])

# ✅ Load only weights (fixes your error)
intent_model.load_weights("intent_model.h5")


# 🔮 Intent prediction function
def predict_intent(text):
    embedding = embed([text])
    prediction = intent_model.predict(embedding)
    confidence = np.max(prediction)
    intent = label_classes[np.argmax(prediction)]
    return intent, confidence


# 🧠 Main chatbot function
def chatbot(user_text):
    # 🔴 Step 1 — Crisis check
    crisis_level = check_crisis_level(user_text)

    if crisis_level == 2:
        return strong_crisis_response()

    elif crisis_level == 1:
        return soft_crisis_response()

    # 🧠 Step 2 — Intent detection
    intent, confidence = predict_intent(user_text)

    # 📝 Step 3 — Save intent to logger
    save_intent(intent)

    # 📚 Step 4 — Read emotional pattern
    recent_intents = get_recent_intents()

    # 🧩 Step 5 — Decide RAG or direct
    if confidence < 0.95:
        rag_context = search(user_text, index, situations, responses)[0]
    else:
        rag_context = ""

    reply = generate_reply(user_text, intent, rag_context, recent_intents)
    return reply



# 🧪 Testing block
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        reply = chatbot(user_input)
        print("Bot:", reply)
