import streamlit as st
from openai import OpenAI

api_key = st.secrets["GROQ_API_KEY"]

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

def generate_answer(query, context, conversation):

    prompt = f"""
You are an intelligent AI assistant.

IMPORTANT RULES:

1. Use the document context whenever available.
2. Treat uploaded documents as the primary source of truth.
3. Never ask the user to upload a document if context already exists.
4. Use conversation history when relevant.
5. Be concise unless detailed explanation is requested.
6. If translation is requested, return ONLY the translation.
7. If summarizing a document, cover:

   * Overview
   * Skills
   * Experience
   * Projects
   * Education
   * Achievements
   * Improvements

8. If information is missing from context, answer normally.

---

## Conversation History

{conversation}

---

## Document Context

{context}

---

## User Question

{query}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1000
    )

    return response.choices[0].message.content
