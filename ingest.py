import os
import pytesseract
import shutil

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from utils import load_pdf, split_text, clean_ocr_text

from pdf2image import convert_from_path

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\HARVIR\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

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

    # text = load_pdf(filepath)
    images = convert_from_path(filepath, dpi=300, poppler_path=r"C:\Users\HARVIR\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin")
    text = ""

    for i, img in enumerate(images):
        t = pytesseract.image_to_string(img, config="--oem 3 --psm 6")
        text += f"\n--- Page {i+1} ---\n"
        text += t

    text = clean_ocr_text(text)
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
shutil.rmtree(DB_FOLDER, ignore_errors=True)
db = Chroma.from_texts(
    texts=all_chunks,
    embedding=embeddings,
    metadatas=all_metadatas,
    persist_directory=DB_FOLDER
)

print("Vector database created.")