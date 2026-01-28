import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

# Load dataset
data = pd.read_csv("intent_data.csv")

texts = data['text'].astype(str).values
labels = data['intent'].values

# Encode labels
le = LabelEncoder()
labels_encoded = le.fit_transform(labels)
labels_categorical = to_categorical(labels_encoded)

print("Loading Universal Sentence Encoder...")
use = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

print("Generating embeddings (this takes time)...")
embeddings = np.array([use([text])[0].numpy() for text in texts])

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    embeddings, labels_categorical, test_size=0.2, random_state=42
)

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(256, activation='relu', input_shape=(512,)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(len(le.classes_), activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print("Training model...")
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Save
model.save("intent_model.h5")
np.save("label_classes.npy", le.classes_)

print("Model saved successfully!")
