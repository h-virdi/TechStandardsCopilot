COLUMN_MAPPING = {
    "ship_sys": [
        "Ship functions and systems"
    ],
    "system": [
        "System"
    ],
    "equipment": [
        "Equipment",
    ],
    "manufacturer": [
        "Brand/Manufacturer"
        "Manufacturer"
    ],
    "model": [
        "Model and type",
        "Model"
    ],
    "uniq_id": [
        "Unique ID",
        "Unique identifier"
    ],
    "os": [
        "Operating system",
        "OS",
        "Operating System - (OS) Version and patch level included"
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
    for column in df.columns:
        if str(column).strip() in aliases:
            return column
    return None