# scripts/relational.py

import sys
from pathlib import Path

# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from report_tools.tables import create_relational_tables

def process_school_relations(school_dir: Path):
    proc_csv = school_dir / "processed_data" / "processed.csv"
    if not proc_csv.exists():
        print(f"  – skipping {school_dir.name}: no processed.csv")
        return

    # make sure the output directory exists
    rel_dir = school_dir / "processed_data" / "relations"
    rel_dir.mkdir(parents=True, exist_ok=True)

    # create all the tables in relations/
    create_relational_tables(proc_csv, rel_dir)
    print(f"  ✔ relational tables for {school_dir.name} in {rel_dir}")

def main():
    root = PROJECT_ROOT / "schools"
    for category in ("priority", "non_priority"):
        cat_dir = root / category
        if not cat_dir.exists():
            continue

        print(f"\n== {category.upper()} ==")
        for school in sorted(cat_dir.iterdir()):
            if not school.is_dir():
                continue
            print(f"Processing {school.name}…")
            process_school_relations(school)

if __name__ == "__main__":
    main()
