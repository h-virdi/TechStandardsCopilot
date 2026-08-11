def score_sheet(df, sheet_name):
    score = 0
    sheet_name = str(sheet_name).lower()

    positive_sheet_keywords = [
        "asset",
        "inventory",
        "ot",
        "system",
        "ics"
        ]

    negative_sheet_keywords = [
        "summary",
        "index",
        "table of contents",
        "toc",
        "cover",
        "title",
        "appendix",
        "info",
        "instructions",
        "introduction",
        "general",
        "readme"
    ]

    for keyword in positive_sheet_keywords:
        if keyword in sheet_name:
            score += 10

    for keyword in negative_sheet_keywords:
        if keyword in sheet_name:
            score -= 20

    inventory_keywords = [
        "equipment",
        "manufacturer",
        "model",
        "unique",
        "security",
        "firmware",
        "network",
        "protocol"
        ]

    rows_to_check = min(10, len(df))
    for row_idx in range(rows_to_check):
        row_text = " ".join(str(x)
                            for x in df.iloc[row_idx]).lower()
        for keyword in inventory_keywords:
            if keyword in row_text:
                score += 5

    return score

def find_inventory_sheet(workbook):
    best_sheet = None
    best_score = -999

    for sheet_name, df in workbook.items():
        score = score_sheet(df, sheet_name)
        # print(f"Sheet: {sheet_name}, Score: {score}")
        if score > best_score:
            best_score = score
            best_sheet = sheet_name

    return [best_sheet]