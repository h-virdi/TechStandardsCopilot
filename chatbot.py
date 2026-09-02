from modes.standards_mode import run_mode_1
from modes.inv_mode import run_mode_2
from modes.sec_doc_mode import run_mode_3
from modes.req_mode import run_mode_4


def main():

    print("\nTechnical Standards Copilot\n")

    print("Select Mode:")
    print("1. Technical Standards Copilot")
    print("2. Asset Inventory Analysis")
    print("3. Secondary Document Analysis")
    print("4. Asset Inventory Requirement Extraction")

    mode = ""

    while mode not in ["1", "2", "3", "4"]:
        mode = input("\nOption: ").strip()

    if mode == "1":
        run_mode_1()

    elif mode == "2":
        run_mode_2()

    elif mode == "3":
        run_mode_3()
        
    elif mode == "4":
        run_mode_4()


if __name__ == "__main__":
    main()