# scripts/process_data.py

import sys
import json
from pathlib import Path
import re

# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from report_tools.word_groups import calculate_score_and_matches

def process_json_dir(input_dir: Path, output_csv: Path, label: str):
    """
    Load every JSON in input_dir, score & augment each entry,
    and write a filtered processed.csv to output_csv.
    """
    items = []
    if not input_dir.is_dir():
        # nothing to do
        print(f"  • No {label} JSON directory at {input_dir}, skipping.")
        return

    # gather every JSON under input_dir
    for raw_file in input_dir.glob("*.json"):
        try:
            data = json.loads(raw_file.read_text(encoding="utf8"))
            if isinstance(data, list):
                items.extend(data)
            else:
                print(f"   • warning: {raw_file.name} not a list, skipping")
        except json.JSONDecodeError:
            print(f"   • warning: could not parse {raw_file.name}, skipping")

    if not items:
        print(f"   • No records found in {input_dir}, skipping {label} processing.")
        return

    # Score & augment each item
    rows = []
    for item in items:
        title = item.get("course title") or item.get("title") or ""
        desc  = item.get("course description") or item.get("description") or ""
        score, kws, groups, freqs = calculate_score_and_matches(title, desc)
        item.update({
            "relevance_score":     score,
            "matched_keywords":    ";".join(kws),
            "matched_groups":      ";".join(groups),
            "keyword_frequencies": json.dumps(freqs, ensure_ascii=False)
        })
        cleaned = {}
        for k, v in item.items():
            key = k.strip().lower().replace(" ", "_")
            cleaned[key] = v
        rows.append(cleaned)

    # Build DataFrame and filter out zero‐score rows
    df = pd.DataFrame(rows)
    df = df[df["relevance_score"] > 0]

    for col in df.select_dtypes(include="object"):
        df[col] = (df[col]
            .fillna("")
            .map(lambda s: re.sub(r'\s{2,}', ' ', re.sub(r'[\n\r\t]{1,}', ' ', s)) if not (isinstance(s, float) or isinstance(s, list) or isinstance(s, dict)) else s)
        )

    output_dir = output_csv.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    if df.empty:
        print(f"   • filtered out everything for {label} → keeping old {output_csv.name} if any")
    else:
        df.to_csv(output_csv, index=False)
        print(f"   • Wrote {len(df)} records to {output_csv}")


def main():
    print("Processing raw JSON into processed CSVs")
    for category in ("priority", "non_priority"):
        base = PROJECT_ROOT / "schools" / category
        if not base.exists():
            continue

        for school in sorted(base.iterdir()):
            if not school.is_dir():
                continue

            print(f"\n== {category}/{school.name} ==")

            # 1) Web‐scrape output in raw_data → processed_data/processed.csv
            web_raw = school / "raw_data"
            web_out = school / "processed_data" / "processed.csv"
            process_json_dir(web_raw, web_out, label="web raw_data")

            # 2) PDF‐scrape output in pdfs/raw_data → pdfs/processed.csv
            pdf_raw = school / "pdfs" / "raw_data"
            pdf_out = school / "pdfs" / "processed.csv"
            process_json_dir(pdf_raw, pdf_out, label="pdfs/raw_data")

if __name__ == "__main__":
    main()
