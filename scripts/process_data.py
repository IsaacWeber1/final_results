#!/usr/bin/env python3
import sys
import json
from pathlib import Path

# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from report_tools.word_groups import calculate_score_and_matches


def process_school(school_dir: Path):
    raw_dir = school_dir / "raw_data"
    out_dir = school_dir / "processed_data"

    # make sure output dir exists
    out_dir.mkdir(parents=True, exist_ok=True)

    json_files = list(raw_dir.glob("*.json"))
    if not json_files:
        # print(f" → skipping {school_dir.name}: no JSON in raw_data/")
        return

    all_items = []
    for raw_file in json_files:
        try:
            items = json.loads(raw_file.read_text(encoding="utf8"))
            if isinstance(items, list):
                all_items.extend(items)
            else:
                print(f"   • warning: {raw_file.name} did not contain a list, skipping")
        except json.JSONDecodeError:
            print(f"   • warning: failed to parse {raw_file.name}, skipping")

    if not all_items:
        # if there was a stale processed.json, remove it
        stale = out_dir / "processed.json"
        if stale.exists():
            stale.unlink()
            print(f" → removed stale {stale}")
        print(f" → no items extracted for {school_dir.name}")
        return

    processed = []
    for item in all_items:
        title = item.get("course title") or item.get("title") or ""
        desc  = item.get("course description") or item.get("description") or ""
        score, kws, groups, freqs = calculate_score_and_matches(title, desc)
        item.update({
            "relevance_score":     score,
            "matched_keywords":    kws,
            "matched_groups":      groups,
            "keyword_frequencies": freqs
        })
        processed.append(item)

    out_path = out_dir / "processed.json"
    out_path.write_text(json.dumps(processed, indent=2, ensure_ascii=False), encoding="utf8")
    print(f" → Wrote {len(processed)} records to {out_path}")


def main():
    base = PROJECT_ROOT / "schools"
    for category in ("priority", "non_priority"):
        for school in (base / category).iterdir():
            if not school.is_dir():
                continue
            print(f"Processing {category}/{school.name} …")
            process_school(school)


if __name__ == "__main__":
    main()
