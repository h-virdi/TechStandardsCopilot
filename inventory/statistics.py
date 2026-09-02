import json

with open("data/asset_statistics.json", encoding="utf-8") as f:
    STATS = json.load(f)

def validate_statistics(asset):
    findings = []
    key = (
        f"{asset.manufacturer}"
        f"|{asset.model}"
    )
    profle = STATS.get(key)
    if not profle:
        return findings
    return findings

