import json
from pathlib import Path

RULES_FILE = Path("data/rules.json")

if RULES_FILE.exists():
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        RULES = json.load(f)
else:
    RULES = {
        "required fields": [],
        "recommended fields": [],
    }

def validate_asset(asset):
    findings = []
    required_fields = RULES.get("required fields", [])
    for field in required_fields:
        value = getattr(asset, field, None)
        value = str(value).strip()
        if (not value or value.lower() == "nan"):
            findings.append({"severity": "HIGH", "finding": f"Missing {field}", "reason": f"{field} is required."})
    return findings