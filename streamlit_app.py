import streamlit as st

from main import build_rag_system, ask_question
from processing.pdf_loader import load_pdf
from processing.chunking import create_chunks
from processing.embedding import get_embeddings
from retrieval.vector_store import create_faiss_index

# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="AI Document Assistant",
    layout="wide"
)

st.title("AI Document Assistant")


@st.cache_resource
def load_system():
    return build_rag_system()


default_chunks, default_index = load_system()

chunks = default_chunks
index = default_index

uploaded_files = st.file_uploader(
    "Upload Documents",
    type=["pdf"],
    accept_multiple_files=True,
    help="Upload one or more PDF files to chat with them."
)

if uploaded_files:

    all_text = ""

    with st.spinner("Processing documents..."):

        for pdf in uploaded_files:
            pdf_text = load_pdf(pdf)
            all_text += pdf_text + "\n"

        chunks = create_chunks(all_text)

        embeddings = get_embeddings(chunks)

        index = create_faiss_index(embeddings)

    st.success(
        f"Processed {len(uploaded_files)} document(s)"
    )

    with st.expander("Uploaded Documents"):

        for pdf in uploaded_files:
            st.write(f"• {pdf.name}")

# ----------------------------------
# Chat Memory
# ----------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------------
# Display Previous Messages
# ----------------------------------

for role, message in st.session_state.chat_history:

    if role == "You":

        with st.chat_message("user"):
            st.write(message)

    else:

        with st.chat_message("assistant"):
            st.write(message)

# ----------------------------------
# Chat Input
# ----------------------------------

user_input = st.chat_input(
    "Ask a question about your documents..."
)

# ----------------------------------
# Ask Question
# ----------------------------------

if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Thinking..."):

        answer = ask_question(
            user_input,
            chunks,
            index,
            st.session_state.chat_history
        )

    st.session_state.chat_history.append(
        ("You", user_input)
    )

    st.session_state.chat_history.append(
        ("Bot", answer)
    )

    with st.chat_message("assistant"):
        st.write(answer)