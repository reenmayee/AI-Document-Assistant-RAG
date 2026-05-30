import numpy as np

def retrieve_chunks(query, model, index, chunks, k=3):
    
    query_embedding = model.encode([query])
    
    distances, indices = index.search(np.array(query_embedding).astype("float32"), k)
    
    results = [chunks[i] for i in indices[0]]
    
    return results
