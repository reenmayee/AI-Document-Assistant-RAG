from processing.chunking import create_chunks
from processing.embedding import get_embeddings, model
from retrieval.vector_store import create_faiss_index
from retrieval.retriever import retrieve_chunks
from llm.generator import generate_answer


def build_rag_system():
    return [], None


def ask_question(query, chunks, index, chat_history):

    conversation = ""

    for role, message in chat_history[-10:]:
        conversation += f"{role}: {message}\n"

    if index is None or len(chunks) == 0:

        return generate_answer(
            query=query,
            context="",
            conversation=conversation
        )

    summary_keywords = [
        "summary",
        "summarize",
        "analyse",
        "analyze",
        "resume review",
        "review my resume",
        "tell me about the document",
        "explain the document"
    ]

    if any(word in query.lower() for word in summary_keywords):

        context = " ".join(chunks[:20])

    else:

        results = retrieve_chunks(
            query,
            model,
            index,
            chunks,
            k=8
        )

        context = " ".join(results)

    answer = generate_answer(
        query=query,
        context=context,
        conversation=conversation
    )

    return answer


if __name__ == "__main__":

    chunks, index = build_rag_system()

    chat_history = []

    print("RAG System Ready!")

    while True:

        query = input("\nYou: ")

        if query.lower() == "exit":
            break

        answer = ask_question(
            query,
            chunks,
            index,
            chat_history
        )

        print("\nBot:", answer)

        chat_history.append(("You", query))
        chat_history.append(("Bot", answer))
