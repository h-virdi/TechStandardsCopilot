from numpy import rint
import pandas as pd

from inventory.models import AssetRecord
from inventory.normaliser import (
    find_column,
    combine_columns,
    COLUMN_ALIASES
)
from inventory.sheet_detector import (find_inventory_sheet, score_sheet)

def load_workbook(file_path):
    return pd.read_excel(
        file_path, 
        sheet_name=None,
        header=None,
        engine="openpyxl"
    )

def detect_header_row(df):

    required_keywords = [
        "id",
        "system owner",
        "component description"
    ]

    best_row = 0
    best_score = 0

    for row_idx in range(
        min(20, len(df))
    ):

        row_text = " ".join(
            str(x)
            for x in df.iloc[row_idx]
        ).lower()

        score = sum(
            1
            for keyword in required_keywords
            if keyword in row_text
        )

        if score > best_score:
            best_score = score
            best_row = row_idx

    return best_row

def flatten_headers(df, header_row):
    header1 = (df.iloc[header_row].ffill())
    if header_row + 1 < len(df):
        header2 = (df.iloc[header_row + 1].fillna(""))
    else:
        header2 = [""] * len(header1)
    headers = []

    for h1, h2 in zip(header1, header2):
        value = (f"{h1} {h2}".strip())
        headers.append(value)

    return headers

def parse_sheet(df, sheet_name):
    records = []
    header_row = detect_header_row(df)
    columns = flatten_headers(df, header_row)
    data = df.iloc[header_row + 2 :].copy()
    data.columns = columns
    id_col = find_column(data, COLUMN_ALIASES["uniq_id"])
    if id_col is None:
        return records
    ship_sys_col = find_column(data, COLUMN_ALIASES["ship_sys"])
    system_col = find_column(data, COLUMN_ALIASES["system"])
    equipment_col = find_column(data, COLUMN_ALIASES["equipment"])
    manufacturer_col = find_column(data, COLUMN_ALIASES["manufacturer"])
    model_col = find_column(data, COLUMN_ALIASES["model"])
    firmware_col = find_column(data, COLUMN_ALIASES["firmware"])
    app_col = find_column(data, COLUMN_ALIASES["app"])
    sec_zone_col = find_column(data, COLUMN_ALIASES["sec_zone"])
    function_col = find_column(data, COLUMN_ALIASES["function"])
    suc_col = find_column(data, COLUMN_ALIASES["suc"])
    untrusted_network_col = find_column(data, COLUMN_ALIASES["untrusted_network"])
    phy_interfaces_col = find_column(data, COLUMN_ALIASES["phy_interfaces"])
    comm_protocols_col = find_column(data, COLUMN_ALIASES["comm_protocols"])
    is_neg_risk_col = find_column(data, COLUMN_ALIASES["is_neg_risk"])
    has_ta_cert_col = find_column(data, COLUMN_ALIASES["has_ta_cert"])

    for _, row in data.iterrows():
        print(
            "ID:",
            row.get(id_col, ""),

            "| System:",
            row.get(system_col, ""),

            "| Manufacturer:",
            row.get(manufacturer_col, "")
)       
        print(row.index.tolist())

        os_name_col = find_column(
            data,
            [
                "OS Information (incl. firmware) OS Name",
                "OS Name"
            ]
        )

        os_version_col = find_column(
            data,
            [
                "OS Information (incl. firmware) Version Number",
                "Version Number"
            ]
        )

        os_value = combine_columns(
            row,
            [
                os_name_col,
                os_version_col
            ]
        )

        uniq_id = str(row.get(id_col, "")).strip()
        if (not uniq_id or uniq_id.lower() == "nan" or "<e.g." in uniq_id.lower() or uniq_id.lower() == "end of section."):
            continue

        manufacturer = str(
            row.get(manufacturer_col, "")
        ).strip()

        if (
            manufacturer.lower() == "nan"
            and uniq_id != ""
        ):
            continue

        if row.isna().all():
            continue

        if str(row.get(id_col, "")).strip() == "OmegaServer":

            print("OS NAME:",
                row.get(
                    "OS Information (incl. firmware) OS Name",
                    "NOT FOUND"
                ))

            print("OS VERSION:",
                row.get(
                    "OS Information (incl. firmware) Version Number",
                    "NOT FOUND"
                ))

        record = AssetRecord(
            ship_sys=str(row.get(ship_sys_col, "")),
            system=str(row.get(system_col, "")),
            equipment=str(row.get(equipment_col, "")),
            manufacturer=str(row.get(manufacturer_col, "")),
            model=str(row.get(model_col, "")),
            uniq_id=str(row.get(id_col, "")),
            os=os_value,
            firmware=str(row.get(firmware_col, "")),
            app=str(row.get(app_col, "")),
            sec_zone=str(row.get(sec_zone_col, "")),
            function=str(row.get(function_col, "")),
            suc=str(row.get(suc_col, "")),
            untrusted_network=str(row.get(untrusted_network_col, "")),
            phy_interfaces=str(row.get(phy_interfaces_col, "")),
            comm_protocols=str(row.get(comm_protocols_col, "")),
            is_neg_risk=bool(row.get(is_neg_risk_col, "")),
            has_ta_cert=bool(row.get(has_ta_cert_col, "")),
            source_sheet=sheet_name
        )

        records.append(record)

    return records

def parse_inventory(file_path):
    workbook = load_workbook(file_path)
    all_records = []

    inventory_sheets = find_inventory_sheet(workbook)
    for sheet_name in inventory_sheets:
        df = workbook[sheet_name]
        records = parse_sheet(df, sheet_name)
        print(f"{sheet_name}: {len(records)} records found.")
        all_records.extend(records)
    return all_records