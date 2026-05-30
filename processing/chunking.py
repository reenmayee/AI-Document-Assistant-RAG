import nltk

def create_chunks(text, chunk_size=3):
    sentences = nltk.sent_tokenize(text)
    
    chunks = []
    
    for i in range(0, len(sentences), chunk_size):
        chunk = " ".join(sentences[i:i+chunk_size])
        chunks.append(chunk)
    
    return chunks