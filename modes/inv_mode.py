from pathlib import Path

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from inventory.parser import parse_inventory

from inventory.vector_store import (create_inventory_db, retrieve_assets, build_context_from_docs)

from inventory.taxonomy import get_taxonomy

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

def load_uploaded_inventory():
    uploads = Path("uploads")
    files = list(uploads.glob("*.xlsx"))
    if not files:
       raise Exception("No .xlsx inventory found.")
    inventory_file = files[0]
    print(f"Loading inventory from {inventory_file}")
    records = parse_inventory(inventory_file)
    print(f"Loaded {len(records)} records from inventory.")
    return records

def ask_inventory_question(question, inventory_db):
    docs = retrieve_assets(question, inventory_db, k=3)
    if not docs:
        return "No relevant assets found in the inventory."

    inv_context = build_context_from_docs(docs)
    prompt = f"""
You are analysing an OT asset inventory.

Inventory Context:
{inv_context}

Question:
{question}

Answer:
"""
    inputs = tokenizer(prompt, return_tensors="pt", max_length=2048, truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=250)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def run_mode_2():

    try:

        records = load_uploaded_inventory()

        inventory_db = create_inventory_db(
            records
        )

    except Exception as e:

        print(
            f"\nInventory Load Error: {e}"
        )

        return

    print(
        "\nAsset Inventory Analysis"
    )

    print(
        "Type 'exit' to quit."
    )

    while True:

        question = input(
            "\nInventory Question: "
        )

        if question.lower() == "exit":

            break

        try:

            answer = ask_inventory_question(
                question,
                inventory_db
            )

            print(
                "\n" + answer + "\n"
            )

        except Exception as e:

            print(
                f"\nError: {e}"
            )