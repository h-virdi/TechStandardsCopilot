from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

INVENTORY_DB_FOLDER = "inv_vector_db"

embeddings = HuggingFaceEmbeddings()

def asset_to_text(asset):
    return f"""
Asset ID: {asset.uniq_id}
Ship System: {asset.ship_sys}
System: {asset.system}
Equipment: {asset.equipment}
Manufacturer: {asset.manufacturer}
Model: {asset.model}
OS: {asset.os}
Firmware: {asset.firmware}
Application: {asset.app}
Security Zone: {asset.sec_zone}
Function: {asset.function}
Suc: {asset.suc}
Untrusted Network: {asset.untrusted_network}
Physical Interfaces: {asset.phy_interfaces}
Communication Protocols: {asset.comm_protocols}
Negligible Risk: {asset.is_neg_risk}
Has TA Certification: {asset.has_ta_cert}
"""

def asset_to_document(asset):
    return Document(
        page_content=asset_to_text(asset),
        metadata={
            "asset_id": asset.uniq_id,
            "manufacturer": asset.manufacturer,
            "system": asset.system
        }
    )

def create_inventory_db(records):
    docs = [
        asset_to_document(asset) for asset in records
    ]
    db = Chroma.from_documents(docs, embeddings=embeddings, persist_directory=INVENTORY_DB_FOLDER)
    return db

def load_inventory_db():
    return Chroma(persist_directory=INVENTORY_DB_FOLDER, embedding_function=embeddings)

def retrieve_assets(question, inventory_db, k=3):
    return inventory_db.similarity_search(question, k=k)

def build_context_from_docs(docs):
    context = []
    for doc in docs:
        context.append(doc.page_content)
    return "\n\n".join(context)
