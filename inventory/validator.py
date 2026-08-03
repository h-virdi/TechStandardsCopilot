from inventory.history import (get_asset_profile, get_most_common)

def check_missing_fields(asset):
    findings = []
    if not asset.uniq_id:
        findings.append("Missing unique asset ID")

    if not asset.system:
        findings.append("Missing system name or identifier.")

    if not asset.manufacturer:
        findings.append("Missing manufacturer information.")

    if not asset.sec_zone:
        findings.append("Missing security zone information.")

    return findings

def check_historical_patterns(asset):
    findings = []
    profile = get_asset_profile(asset)
    if not profile:
        return findings

    expected_zone = get_most_common(profile.get("sec_zone", {}))
    if (expected_zone and asset.sec_zone and asset.sec_zone != expected_zone):
        findings.append(f"Security zone differs from "
                        f"historical norm "
                        f"({expected_zone}).")

    expected_suc = get_most_common(profile.get("suc", {}))
    if (expected_suc and asset.suc and asset.suc != expected_suc):
        findings.append(f"Systems under consideration (SuC) differs from "
                        f"historical norm "
                        f"({expected_suc}).")
    return findings

def validate_inventory(records):
    findings = []
    for asset in records:
        asset_findings = []
        asset_findings.extend(check_missing_fields(asset))
        asset_findings.extend(check_historical_patterns(asset))
        if asset_findings:
            findings.append({
                "asset": asset.equipment,
                "unique_id": asset.uniq_id,
                "findings": asset_findings
            })
    return findings
