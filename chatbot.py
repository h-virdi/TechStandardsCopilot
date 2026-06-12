from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from openai import OpenAI

load_dotenv()

client = OpenAI()

DB_FOLDER = "vector_db"

embeddings = HuggingFaceEmbeddings()

db = Chroma(
    persist_directory=DB_FOLDER,
    embedding_function=embeddings
)

SYSTEM_PROMPT = """
You are a cybersecurity standards assistant.

Rules:

1. Answer ONLY using the retrieved context.
2. Do not invent information.
3. If the answer is not in the context, say:
   "I could not find this information in the loaded standards."
4. Always cite the source documents.
"""


def ask_question(question):

    docs = db.similarity_search(
        question,
        k=5
    )

    context = ""

    sources = set()

    for doc in docs:

        context += doc.page_content + "\n\n"

        if "source" in doc.metadata:
            sources.add(doc.metadata["source"])

    prompt = f"""
Context:

{context}

Question:

{question}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    source_text = "\n".join(
        f"- {source}" for source in sources
    )

    return f"""
{answer}

Sources:
{source_text}
"""


print("Cybersecurity Standards Chatbot")
print("Type 'exit' to quit.\n")

while True:

    question = input("Ask: ")

    if question.lower() == "exit":
        break

    try:

        answer = ask_question(question)

        print("\n" + answer + "\n")

    except Exception as e:

        print(f"\nError: {e}\n")