import numpy as np

def retrieve_chunks(query, model, index, chunks, k=3):
    # convert query to embedding
    query_embedding = model.encode([query])
    
    # search in FAISS
    distances, indices = index.search(np.array(query_embedding).astype("float32"), k)
    
    # get relevant chunks
    results = [chunks[i] for i in indices[0]]
    
    return results