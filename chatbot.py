from utils import extract_references
from dotenv import load_dotenv
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from openai import OpenAI
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from inventory.parser import parse_inventory

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

CLASS_SOCIETIES = {
    "1": "DNV",
    "2": "ABS",
    "3": "Lloyd's Register",
    "4": "Bureau Veritas",
    "5": "RINA"
}

VESSEL_TYPES = {
    "1": "Tanker",
    "2": "Bulk Carrier",
    "3": "Container Ship",
    "4": "Offshore Support Vessel",
    "5": "Passenger Vessel",
    "6": "Gas Carrier",
    "7": "General Cargo Ship"
}

REGIONS = {
    "1": "Singapore",
    "2": "Norway",
    "3": "Liberia",
    "4": "Marshall Islands",
    "5": "Panama"
}

def get_menu_choice(prompt, options):
    while True:
        print(f"\n{prompt}")
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = input("\nOption: ").strip()
        if choice in options:
            return options[choice]
        print("Invalid selection. Please try again.")

def class_society_exists(class_society):
    results = db.get(include=["metadatas"])

    for metadata in results["metadatas"]:
        source = metadata.get("source", "").upper()
        if class_society.upper() in source:
            return True
    return False

def ask_question(question, vessel_context=None):
    seen_chunks = set()
    def add_unique(doc):
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
    

    # context = ""
    if vessel_context:
        vessel_context_text = f"""
        Region: {vessel_context['region']}
        Vessel Type: {vessel_context['vessel_type']}
        Classification Society: {vessel_context['classification_society']}
        """
    else:
        vessel_context_text = """
        General standards inquiry.
        No vessel-specific information supplied.
        """
    context = ""
    sources = set()
    references = set()

    for doc in docs:

        context += add_unique(doc)

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

Return a complete answer.

Vessel Information:
{vessel_context_text}

Standards Context:
{context}

Question:
{question}

Answer:

"""
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    outputs = model.generate(**inputs, max_new_tokens=250)
    # result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    source_text = "\n".join(f"- {s}" for s in sorted(sources))

    print(context)
    return answer + "\n\nSources:\n" + source_text

#to continue modifying
print("Technical Standards Copilot")
print("Type 'exit' to quit.\n")

print("Query Type:")
print("1. General Standards Inquiry")
print("2. Vessel-Specific Requirements")

query_type = ""

while query_type not in ["1", "2"]:
    query_type = input("\nOption: ").strip()

vessel_context = None

if query_type == "2":
    region = get_menu_choice("Select Region/Flag State:", REGIONS)
    vessel_type = get_menu_choice("Select Vessel Type:", VESSEL_TYPES)
    while True:
        class_society = get_menu_choice("Select Classification Society", CLASS_SOCIETIES)
        if class_society_exists(class_society):
            break
        else:
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