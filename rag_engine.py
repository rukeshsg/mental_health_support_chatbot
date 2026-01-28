from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


# ✅ Load knowledge and separate situation / response
def load_knowledge(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    raw_chunks = content.split("Situation:")
    situations = []
    responses = []

    for chunk in raw_chunks:
        if "Response:" in chunk:
            situation, response = chunk.split("Response:")
            situations.append(situation.strip())
            responses.append(response.strip())

    return situations, responses


# ✅ Create FAISS index using only situations
def create_faiss_index(situations):
    embeddings = model.encode(situations)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return index


# ✅ Search and return only the best response
def search(query, index, situations, responses, k=1):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    return [responses[i] for i in indices[0]]


# ✅ Load everything once when file runs
situations, responses = load_knowledge("mental_health_knowledge.txt")
index = create_faiss_index(situations)


# ✅ Testing block
if __name__ == "__main__":
    while True:
        user_input = input("Enter text: ")
        results = search(user_input, index, situations, responses)
        print("\nBest Response:\n", results[0])
        print()
