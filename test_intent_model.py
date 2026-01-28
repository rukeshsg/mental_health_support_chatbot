import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

# Load model and labels
model = tf.keras.models.load_model("intent_model.h5")
labels = np.load("label_classes.npy", allow_pickle=True)

# Load USE
use = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

while True:
    text = input("Enter text: ")

    embedding = use([text])[0].numpy().reshape(1, -1)
    prediction = model.predict(embedding)

    intent_index = np.argmax(prediction)
    confidence = np.max(prediction)
    intent = labels[intent_index]


    print("Intent:", intent)
    print("Confidence:", confidence)

    if confidence < 0.95:
        print("⚠️ Send to RAG")
    else:
        print("✅ Direct response")

