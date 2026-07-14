from pydoc import doc
from unittest import result
from weakref import ref
from utils import extract_references
from click import prompt
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from openai import OpenAI
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

load_dotenv()

# client = OpenAI()

DB_FOLDER = "vector_db"
MAX_REFERENCES = 5

embeddings = HuggingFaceEmbeddings()

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

db = Chroma(
    persist_directory=DB_FOLDER,
    embedding_function=embeddings
)

# SYSTEM_PROMPT = """

# Answer using ONLY the context.

# If the answer refers to sections (e.g., 3.1.2), explain what those sections contain.

# Answer using ONLY the context.

# Provide a clear and complete answer.

# If the answer is not in the context, say:
# "I could not find this information in the loaded standards."

# Always cite the source

# """


def ask_question(question):
    seen_chunks = set()
    def add_unique(context, doc):
        if doc.page_content not in seen_chunks:
            seen_chunks.add(doc.page_content)
            return doc.page_content + "\n\n"
        return ""
    docs = db.similarity_search(
        question,
        k=10
    )
    docs = sorted(docs, key=lambda d: len(d.page_content), reverse=True)
    if not docs:
        return "I could not find this information."
    

    context = ""

    sources = set()
    references = set()

    for doc in docs:

        context += add_unique(context, doc)

        if "source" in doc.metadata:
            sources.add(doc.metadata["source"])

        refs = extract_references(doc.page_content)
        references.update(refs)

    for ref in list(references)[:MAX_REFERENCES]:
        
        more_docs = db.similarity_search(ref, k=2)

        for doc in more_docs:
            context += add_unique(context, doc)

    prompt = f"""


Answer using ONLY the context below.

The answer requires identifying ALL relevant items.

Return a COMPLETE list.
Return the answer as a bullet list.

Do NOT return only partial items.
Do NOT ignore any variants.

Context:
{context}

Question:
{question}

Answer:

"""
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=200)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    source_text = "\n".join(f"- {s}" for s in sources)

    # response = client.chat.completions.create(
    #     model="gpt-4.1",
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": SYSTEM_PROMPT
    #         },
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # )

    print(context)
    return result + "\n\nSources:\n" + source_text


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