import os

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from utils import load_pdf, split_text

load_dotenv()

PDF_FOLDER = "standards"
DB_FOLDER = "vector_db"

all_chunks = []
all_metadatas = []

print("Loading PDFs...")

for filename in os.listdir(PDF_FOLDER):

    if not filename.endswith(".pdf"):
        continue

    filepath = os.path.join(PDF_FOLDER, filename)

    print(f"Processing {filename}")

    text = load_pdf(filepath)

    chunks = split_text(text)

    for i, chunk in enumerate(chunks):

        all_chunks.append(chunk)

        all_metadatas.append(
            {
                "source": filename,
                "chunk": i
            }
        )

print(f"Total chunks: {len(all_chunks)}")

embeddings = HuggingFaceEmbeddings()

db = Chroma.from_texts(
    texts=all_chunks,
    embedding=embeddings,
    metadatas=all_metadatas,
    persist_directory=DB_FOLDER
)

print("Vector database created.")