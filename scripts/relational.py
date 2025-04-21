# scripts/relational.py

import sys
from pathlib import Path

# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import json
import pandas as pd
from pathlib import Path
from report_tools.tables import create_relational_tables

def process_school_relations(school_dir: Path):
    proc_json = school_dir / "processed_data" / "processed.json"
    if not proc_json.exists():
        print(f"  – skipping {school_dir.name}: no processed.json")
        return
    # load JSON into a DataFrame
    df = pd.read_json(proc_json, orient="records")
    # write out a temporary CSV
    csv_path = school_dir / "processed_data" / "processed_temp.csv"
    df.to_csv(csv_path, index=False)
    # create a relations/ subdir
    rel_dir = school_dir / "processed_data" / "relations"
    create_relational_tables(csv_path, rel_dir)
    csv_path.unlink()  # clean up
    print(f"  ✔ relational tables for {school_dir.name} in {rel_dir}")

def main():
    root = Path(__file__).resolve().parent.parent / "schools"
    for category in ("priority","non_priority"):
        cat_dir = root / category
        if not cat_dir.exists(): continue
        print(f"\n== {category.upper()} ==")
        for school in sorted(cat_dir.iterdir()):
            if not school.is_dir(): continue
            print(f"Processing {school.name}…")
            process_school_relations(school)

if __name__ == "__main__":
    main()
