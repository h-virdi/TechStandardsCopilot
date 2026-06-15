from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re


def load_pdf(filepath):

    reader = PdfReader(filepath)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def split_text(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_text(text)

def normalise_whitespace(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def fix_line_breaks(text):
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\n+', ' ', text)
    return text

def remove_noise(text):
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'[|•©®™]', '', text)
    return text


def fix_punctuation(text):
    text = re.sub(r'\s([.,!?])', r'\1', text) 
    text = re.sub(r'([.,!?])([^\s])', r'\1 \2', text)
    return text

def remove_repeated_lines(text):
    lines = text.split('. ')
    seen = set()
    cleaned = []

    for line in lines:
        if line not in seen:
            cleaned.append(line)
            seen.add(line)

    return '. '.join(cleaned)

def clean_ocr_text(text):
    text = fix_line_breaks(text)
    text = remove_noise(text)
    text = normalise_whitespace(text)
    text = fix_punctuation(text)
    return text
