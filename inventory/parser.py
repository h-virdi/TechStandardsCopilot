import pandas as pd

from inventory.models import AssetRecord
from inventory.normaliser import (
    find_column,
    combine_columns,
    COLUMN_ALIASES
)

def load_workbook(file_path):
    return pd.read_excel(
        file_path, 
        sheet_name=None,
        header=None,
        engine="openpyxl"
    )

def detect_header_row(df):
    for row_idx in range(min(20, len(df))):
        row_text = " ".join(str(x)
                            for x in df.iloc[row_idx]).lower()
        if (
            "asset" in row_text
            or "system" in row_text
                ):
            return row_idx

    return 0

def flatten_headers(df, header_row):
    header1 = (df.iloc[header_row].fillna(method="ffill"))
    header2 = (df.iloc[header_row + 1].fillna(""))
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

    for _, row in data.iterrows():
        os_value = combine_columns(row, 
                                   ["OS Information (incl. firmware) OS Name",
                                    "OS Information (incl. firmware) Version Number"])

        