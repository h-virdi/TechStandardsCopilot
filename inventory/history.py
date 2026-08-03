import json

def load_statistics():
    with open("data/asset_statistics.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_asset_profile(asset):
    stats = load_statistics()
    asset_key = asset.equipment
    return stats.get(asset_key)

def get_most_common(counter_dict):
    if not counter_dict:
        return None
    return max(counter_dict, key=counter_dict.get)