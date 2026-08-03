from collections import Counter
import json

def build_statistics(records):
    stats = {}
    for asset in records:
        candidate_fields = [
            asset.uniq_id,
            asset.equipment,
            asset.system,
            asset.manufacturer,
            asset.model
        ]

        asset_key = asset.uniq_id.strip()

        if (
            not asset_key
            or asset_key.lower() == "nan"
        ):
            continue

        for value in candidate_fields:

            value = str(value).strip()

            if value and value.lower() != "nan":

                asset_key = value

                break

        if not asset_key:
            continue

        print(
            "Grouping Asset:",
            asset_key
        )

        if asset_key not in stats:
            stats[asset_key] = {
                "count": 0,
                "manufacturer": Counter(),
                "model": Counter(),
                "os": Counter(),
                "firmware": Counter(),
                "sec_zone": Counter(),
                "suc": Counter(),
                "comm_protocols": Counter(),
                "is_neg_risk_count": 0,
                "has_ta_cert_count": 0,
            }
        asset_stats = stats[asset_key]
        asset_stats["count"] += 1
        if asset.manufacturer:
            asset_stats["manufacturer"][asset.manufacturer] += 1
        if asset.model:
            asset_stats["model"][asset.model] += 1
        if asset.os:
            asset_stats["os"][asset.os] += 1
        if asset.firmware:
            asset_stats["firmware"][asset.firmware] += 1
        if asset.sec_zone:
            asset_stats["sec_zone"][asset.sec_zone] += 1
        if asset.suc:
            asset_stats["suc"][asset.suc] += 1
        if asset.comm_protocols:
            asset_stats["comm_protocols"][asset.comm_protocols] += 1
        if asset.is_neg_risk:
            asset_stats["is_neg_risk_count"] += 1
        if asset.has_ta_cert:
            asset_stats["has_ta_cert_count"] += 1

    return stats

def save_statistics(stats, output_file):
    serialisable = {}
    for asset_type, values in stats.items():
        serialisable[asset_type] = {
            "count": values["count"],
            "manufacturer": dict(values["manufacturer"]),
            "model": dict(values["model"]),
            "os": dict(values["os"]),
            "firmware": dict(values["firmware"]),
            "sec_zone": dict(values["sec_zone"]),
            "suc": dict(values["suc"]),
            "comm_protocols": dict(values["comm_protocols"]),
            "is_neg_risk_count": values["is_neg_risk_count"],
            "has_ta_cert_count": values["has_ta_cert_count"],
        }
    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(serialisable, f, indent=2)