from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


DB_FOLDER = "vector_db"
embeddings = HuggingFaceEmbeddings()

db = Chroma(
    persist_directory=DB_FOLDER,
    embedding_function=embeddings
)
def debug_retrieval(query):
    docs = db.similarity_search(query, k=7)

    for doc in docs:
        print("-----")
        print(doc.page_content)
        print(doc.metadata)


query = "What are the different types of cybersecurity notations?"

debug_retrieval(query)
