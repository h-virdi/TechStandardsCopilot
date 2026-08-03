from encodings.aliases import aliases
import json

from pandas import col

COLUMN_ALIASES = {
    "ship_sys": [
        "Ship functions and systems",
        "System Owner",
        "Asset Inventory System Owner"
    ],
    "system": [
        "System",
        "System Name or Identifier",
        "Maintaining Organization",
        "Asset Inventory System Name or Identifier",
        "Asset Inventory Maintaining Organization"
    ],
    "equipment": [
        "Equipment"
    ],
    "manufacturer": [
        "Brand/Manufacturer",
        "Manufacturer",
        "Hardware Manufacturer and Model",
        "Asset Inventory Hardware Manufacturer and Model"
    ],
    "model": [
        "Model and type",
        "Model",
        "Hardware Manufacturer and Model"
    ],
    "uniq_id": [
        "Unique ID",
        "Unique identifier",
        "ID",
        "Asset Inventory ID",
    ],
    "os": [
        "Operating system",
        "OS",
        "Operating System - (OS) Version and patch level included",
        "Asset Inventory OS Information (incl. firmware)"
    ],
    "firmware": [
        "Firmware version",
        "Firmware",
        "Firmware Version and patch level included"
    ],
    "app": [
        "Application version",
        "Application",
        "Application software and version"
    ],
    "sec_zone": [
        "Security zone",
        "Security Zone"
    ],
    "function": [
        "Function",
        "Function of the system",
        "Short description of functionality/purpose"
    ],
    "suc": [
        "Systems under consideration (SuC)",
        "Systems under consideration",
        "Connections to Systems under consideration (SuC)"
    ],
    "untrusted_network": [
        "Untrusted network connections",
        "Connections to or via untrusted network/Remote connection"
    ],
    "phy_interfaces": [
        "Physical interfaces",
        "Asset Inventory Physical Serial Port",
        "Asset Inventory Physical Network Port",
        "Asset Inventory Physical Fibre Port"
    ],
    "comm_protocols": [
        "Communication protocols",
        "Communication Protocols",
        "Supported communication protocols"
    ],
    "is_neg_risk": [
        "Negligible risk",
        "Negligible risk (separate risk assessment needed)"
    ],
    "has_ta_cert": [
        "TA certificate",
        "TA certificate (if applicable)",
        "Cyber security Type approval certificate"
    ]
}


def find_column(df, aliases):
    for col in df.columns:
        col_text = str(col).strip().lower()
        for alias in aliases:
            if alias.lower() in col_text:
                return col
    return None

def load_aliases():
    with open("data/asset_aliases.json",
              "r") as f:
        return json.load(f)

def normalise_asset_name(
        asset_name,
        aliases
):
    asset_name = asset_name.strip()
    for canonical, variants in aliases.items():
        if asset_name in variants:
            return canonical
    return asset_name

def combine_columns(row, columns):
    values = []
    for column in columns:
        value = str(
            row.get(column, "")
        ).strip()

        if value and value.lower() != "nan":
            values.append(value)
    return " ".join(values)

