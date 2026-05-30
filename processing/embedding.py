from sentence_transformers import SentenceTransformer

# load model ONCE (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(chunks):
    embeddings = model.encode(chunks)
    return embeddings