from pathlib import Path
from inventory.parser import (parse_inventory)
from inventory.statistics_builder import (build_statistics, save_statistics)

records = []
inventory_dir = Path("historical_inventories")

for file in inventory_dir.glob("*.xlsx"):
    print(f"Processing {file.name}")
    records.extend(parse_inventory(str(file)))

stats = build_statistics(records)
save_statistics(stats, "data/asset_statistics.json")
print(f"Processed {len(records)} assets.")