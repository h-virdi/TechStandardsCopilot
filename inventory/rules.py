import json
from pathlib import Path

RULES_FILE = Path("data/DNV_rules.json")

if RULES_FILE.exists():
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        RULES = json.load(f)
else:
    RULES = {
        "required_fields": [],
        "recommended_fields": [],
    }

FIELD_MAPPING = {
    "ship functions and systems": "ship_sys",
    "equipment": "equipment",
    "manufacturer": "manufacturer",
    "model": "model",
    "os": "os",
    "firmware": "firmware",
    "application": "app",
    "security zone": "sec_zone",
    "purpose": "function",
    "connections to suc": "suc",
    "connections to untrusted networks": "untrusted_network",
    "physical interfaces": "phy_interfaces",
    "communication protocols": "comm_protocols",
    "negligible risk": "is_neg_risk",
    "unique identifier": "uniq_id"
}


def validate_asset(asset):
    findings = []
    required_fields = RULES.get("required_fields", [])
    for field in required_fields:
        attr_name = FIELD_MAPPING.get(field.lower())
        if not attr_name:
            continue
        value = getattr(asset, attr_name, None)
        value = str(value).strip()
        if (not value or value.lower() == "nan"):
            findings.append({"severity": "HIGH", "finding": f"Missing {field}", "reason": f"{field} is required."})
    return findings