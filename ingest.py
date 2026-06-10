from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Loading pdfs
reader = PdfReader("CCS_Cybersec_guidelines.pdf")
text = ""
for page in reader.pages:
  text += page.extract_text()
print(text[:1000])
