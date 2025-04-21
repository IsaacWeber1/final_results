# scripts/clean_raw.py
"""
Remove all raw JSON files under each school's raw_data/ folder,
and delete the folder if it becomes empty.
"""
from pathlib import Path

def clean_raw_data(schools_root: Path):
    deleted = 0
    for category in ("priority", "non_priority"):
        cat_dir = schools_root / category
        if not cat_dir.is_dir():
            continue
        for school in cat_dir.iterdir():
            raw_dir = school / "raw_data"
            if not raw_dir.is_dir():
                continue

            # delete all .json files in raw_data/
            for jf in raw_dir.glob("*.json"):
                try:
                    jf.unlink()
                    deleted += 1
                except Exception as e:
                    print(f"  ! error deleting {jf}: {e}")

    print(f"✓ Deleted {deleted} raw JSON file(s).")

def main():
    project_root = Path(__file__).resolve().parent.parent
    schools_root = project_root / "schools"
    if not schools_root.exists():
        print(f"Error: cannot find {schools_root}")
        return
    clean_raw_data(schools_root)

if __name__ == "__main__":
    from pathlib import Path
    main()