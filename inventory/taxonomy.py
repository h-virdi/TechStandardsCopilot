import json
from pathlib import Path

TAXONOMY_FILE = Path("data/taxonomy.json")

if TAXONOMY_FILE.exists():
    with open(TAXONOMY_FILE, "r", encoding="utf-8") as f:
        TAXONOMY = json.load(f)
else:
    TAXONOMY = {}


def get_taxonomy(
    comp_desc
):
    if not comp_desc:
        return {}
    return TAXONOMY.get(comp_desc, {})

def get_category(comp_desc):
    taxonomy_entry = get_taxonomy(comp_desc)
    return taxonomy_entry.get("category", "Unknown")

def get_ship_system(comp_desc):
    taxonomy_entry = get_taxonomy(comp_desc)
    return taxonomy_entry.get("ship_system", "Unknown")

def get_subcategory(comp_desc):
    taxonomy_entry = get_taxonomy(comp_desc)
    return taxonomy_entry.get("subcategory", "Unknown")