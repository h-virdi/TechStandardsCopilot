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

def class_society_exists(class_society):
    results = db.get(include=["metadatas"])

    for metadata in results["metadatas"]:
        source = metadata.get("source", "").upper()
        if class_society.upper() in source:
            return True
    return False

def ask_question(question, vessel_context=None):
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
    vessel_context_text = f"""
    Region: {vessel_context['region']}
    Vessel Type: {vessel_context['vessel_type']}
    Classification Society: {vessel_context['classification_society']}
    """

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

Vessel Information:
{vessel_context_text}

Standards Context:
{context}

Question:
{question}

Answer:

"""
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=200)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    source_text = "\n".join(f"- {s}" for s in sources)

    print(context)
    return result + "\n\nSources:\n" + source_text
    def add_unique(context, doc):
        if doc.page_content not in seen_chunks:
            seen_chunks.add(doc.page_content)
            return doc.page_content + "\n\n"
        return ""
    search_query = question
    if vessel_context:
        search_query += f"""
        {vessel_context['vessel_type']} 
        {vessel_context['classification_society']}
        {vessel_context['region']}
        """
    docs = db.similarity_search(
        search_query,
        k=10
    )
    docs = sorted(docs, key=lambda d: len(d.page_content), reverse=True)
    if not docs:
        return "I could not find this information."
    

    context = ""
    if vessel_context:
        vessel_context_text = f"""
    Region: {vessel_context['region']}
    Vessel Type: {vessel_context['vessel_type']}
    Classification Society: {vessel_context['classification_society']}
    """
    else:
        vessel_context_text = "No vessel-specific information provided."
        

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


Answer using ONLY the standards context provided.

If vessel information is provided, use it to determine which requirements are applicable.

The answer requires identifying ALL relevant items.

Return a complete answer as a bullet list where appropriate.

Do NOT invent information.
Do NOT ignore relevant requirements.

Vessel Information:
{vessel_context_text}

Standards Context:
{context}

Question:
{question}

Answer:

"""
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=200)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    source_text = "\n".join(f"- {s}" for s in sources)

    # print(context)
    return result + "\n\nSources:\n" + source_text


print("Technical Standards Copilot")
print("Type 'exit' to quit.\n")

print("Query Type:")
print("1. General Standards Inquiry")
print("2. Vessel-Specific Requirements")

query_type = input("Select option: ")
vessel_context = None

if query_type == "2":
    class_society = input("Classification Society: ")

    vessel_context = {
        "region": input("Region/Flag State: "),
        "vessel_type": input("Vessel Type: "),
        "classification_society": class_society
    }
    if not class_society_exists(class_society):
        print(
            f"\nNo documents have been loaded for "
            f"{class_society}.\n"
            "Please choose a supported classification society."
        )

while True:

    question = input("Ask: ")

    if question.lower() == "exit":
        break

    try:

        answer = ask_question(question, vessel_context)
        print("\n" + answer + "\n")

    except Exception as e:

        print(f"\nError: {e}\n")