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

def process_school(school_dir: Path):
    raw_dir = school_dir / "raw_data"
    out_dir = school_dir / "processed_data"
    out_dir.mkdir(parents=True, exist_ok=True)

    # gather every JSON under raw_data
    items = []
    for raw_file in raw_dir.glob("*.json"):
        try:
            data = json.loads(raw_file.read_text(encoding="utf8"))
            if isinstance(data, list):
                items.extend(data)
            else:
                print(f"   • warning: {raw_file.name} not a list, skipping")
        except json.JSONDecodeError:
            print(f"   • warning: could not parse {raw_file.name}, skipping")

    if not items:
        # remove stale CSV if exists
        # print(f" → no raw items for {school_dir.name}, skipping without touch")
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
    
    # Build DataFrame and filter
    df = pd.DataFrame(rows)
    df = df[df["relevance_score"] > 0]

    for col in df.select_dtypes(include="object"):
        df[col] = (df[col]
            .fillna("")
            .map(lambda s: re.sub(r'\s{2,}', ' ', re.sub(r'[\n\r\t]{1,}', ' ', s)))
        )

    out_csv = out_dir / "processed.csv"
    if df.empty:
        print(f" → filtered out everything for {school_dir.name} (no relevant rows), keeping old {out_csv.name} if any")
    else:
        df.to_csv(out_csv, index=False)
        print(f" → Wrote {len(df)} relevant records to {out_csv}")

def main():
    print("Processing raw data into processed_data/processed.csv")
    for category in ("priority", "non_priority"):
        base = PROJECT_ROOT / "schools" / category
        if not base.exists(): 
            continue
        for school in sorted(base.iterdir()):
            if not school.is_dir():
                continue
            # print(f"Processing {category}/{school.name} …")
            process_school(school)

if __name__ == "__main__":
    main()
