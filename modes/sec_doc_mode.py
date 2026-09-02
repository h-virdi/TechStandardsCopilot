from pathlib import Path


def run_mode_3():

    print("\nSecondary Document Analysis")
    print("Type 'exit' to quit.\n")

    docs_folder = Path("uploads/docs")

    if not docs_folder.exists():

        print(
            "\nNo uploads/docs folder found."
        )

        return

    supported_files = []

    supported_files.extend(
        docs_folder.glob("*.pdf")
    )

    supported_files.extend(
        docs_folder.glob("*.docx")
    )

    if not supported_files:

        print(
            "\nNo supported documents found."
        )

        return

    print("\nDocuments Found:")

    for file in supported_files:

        print(
            f"- {file.name}"
        )

    print(
        "\nFuture capability:"
    )

    print(
        "- Vendor manual analysis"
    )

    print(
        "- Assessment report analysis"
    )

    print(
        "- Network diagram analysis"
    )

    print(
        "- Architecture document analysis"
    )

    while True:

        question = input(
            "\nDocument Question: "
        )

        if (
            question.lower() == "exit"
        ):
            break

        print(
            "\nDocument analysis is not yet implemented."
        )