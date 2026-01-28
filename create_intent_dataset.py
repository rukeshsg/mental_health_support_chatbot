import pandas as pd
from datasets import load_dataset

dataset = load_dataset("dair-ai/emotion")

# HF label numbers:
# 0 = sadness
# 1 = joy
# 2 = love
# 3 = anger
# 4 = fear
# 5 = surprise

label_mapping = {
    0: "depression",   # sadness
    1: "normal",       # joy
    2: "normal",       # love
    3: "anger",        # anger
    4: "anxiety",      # fear
    5: "normal"        # surprise
}

texts = []
intents = []

for split in ["train", "validation", "test"]:
    for example in dataset[split]:
        label_num = example["label"]
        mapped_intent = label_mapping.get(label_num, None)
        if mapped_intent:
            texts.append(example["text"])
            intents.append(mapped_intent)

df = pd.DataFrame({"text": texts, "intent": intents})

# Add custom samples
custom_data = [
    ("Hi", "greeting"),
    ("Hello", "greeting"),
    ("Hey there", "greeting"),
    ("I feel stressed about exams", "stress"),
    ("Too much work is making me tired", "stress"),
    ("I feel very lonely", "loneliness"),
    ("Nobody understands me", "loneliness"),
    ("I feel isolated from everyone", "loneliness")
]

custom_df = pd.DataFrame(custom_data, columns=["text", "intent"])
df = pd.concat([df, custom_df], ignore_index=True)

df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("intent_data.csv", index=False)

print("intent_data.csv created successfully!")
print("Total rows:", len(df))
