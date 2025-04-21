#!/usr/bin/env python3
"""
scripts/cleanup_processed_data.py

Walks through each school's processed_data folder and deletes any .json files,
undoing the accidental creation of empty processed outputs.
"""
import sys
from pathlib import Path

def cleanup_processed_data(schools_root: Path):
    """
    Delete all .json files in processed_data directories for each school.
    """
    for category in ("priority", "non_priority"):
        cat_dir = schools_root / category
        if not cat_dir.exists():
            continue
        for school_dir in cat_dir.iterdir():
            if not school_dir.is_dir():
                continue
            proc_dir = school_dir / "processed_data"
            if proc_dir.exists():
                for json_file in proc_dir.glob("*.json"):
                    try:
                        json_file.unlink()
                        print(f"Deleted: {json_file}")
                    except Exception as e:
                        print(f"Failed to delete {json_file}: {e}")

if __name__ == '__main__':
    project_root = Path(__file__).resolve().parent
    schools_dir = project_root / "schools"
    if not schools_dir.exists():
        print(f"Error: could not find schools/ at {schools_dir}", file=sys.stderr)
        sys.exit(1)
    cleanup_processed_data(schools_dir)
    print("Cleanup complete.")
