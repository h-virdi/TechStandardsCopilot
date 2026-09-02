from pathlib import Path



def run_mode_4():

    print(
        "\nAsset Inventory Requirement Extraction"
    )

    print(
        "Type 'exit' to quit.\n"
    )

    rules_folder = Path(
        "Inventory Rules"
    )

    if not rules_folder.exists():

        print(
            "\nNo inventory rules folder found."
        )

        return

    pdfs = list(
        rules_folder.glob("*.pdf")
    )
    print(f"\nDetected {len(pdfs)} rule documents.")
    while True:
        question = input("\nRequirement Question: ")
        if question.lower() == "exit":
            break
        print("Not implemented yet")