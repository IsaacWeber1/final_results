# scripts/process_data.py
import json
from pathlib import Path
from report_tools.word_groups import calculate_score_and_matches

def process_school(school_dir: Path):
    raw_dir = school_dir / "raw_data"
    out_dir = school_dir / "processed_data"
    out_dir.mkdir(exist_ok=True, parents=True)

    all_items = []
    # gather every .json under raw_data
    for raw_file in raw_dir.glob("*.json"):
        with raw_file.open("r", encoding="utf8") as f:
            items = json.load(f)
        all_items.extend(items)

    processed = []
    for item in all_items:
        title = item.get("course title") or item.get("title") or ""
        desc  = item.get("course description") or item.get("description") or ""
        score, kws, groups, freqs = calculate_score_and_matches(title, desc)
        item.update({
            "relevance_score":        score,
            "matched_keywords":       kws,
            "matched_groups":         groups,
            "keyword_frequencies":    freqs
        })
        processed.append(item)

    out_path = out_dir / "processed.json"
    with out_path.open("w", encoding="utf8") as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)
    print(f" → Wrote {len(processed)} records to {out_path}")

def main():
    base = Path(__file__).resolve().parent.parent / "schools"
    for category in ("priority", "non_priority"):
        for school in (base / category).iterdir():
            if school.is_dir():
                print(f"Processing {category}/{school.name} …")
                process_school(school)

if __name__ == "__main__":
    main()
