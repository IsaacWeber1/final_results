# scripts/clear.py

import argparse
from pathlib import Path

def clear_raw(schools_root: Path):
    deleted = 0
    for category in ("priority", "non_priority"):
        cat_dir = schools_root / category
        if not cat_dir.is_dir():
            continue
        for school in cat_dir.iterdir():
            for raw_sub in ("raw_data", "pdfs/raw_data"):
                raw_dir = school / raw_sub
                if not raw_dir.is_dir():
                    continue
                for jf in raw_dir.glob("*.json"):
                    try:
                        jf.unlink()
                        deleted += 1
                    except Exception as e:
                        print(f"  ! error deleting {jf}: {e}")
    print(f"✓ Deleted {deleted} raw JSON file(s).")

def clear_visuals(schools_root: Path):
    deleted = 0
    for category in ("priority", "non_priority"):
        cat_dir = schools_root / category
        if not cat_dir.is_dir():
            continue
        for school in cat_dir.iterdir():
            fig_dir = school / "figures"
            if not fig_dir.is_dir():
                continue
            for f in fig_dir.iterdir():
                if f.is_file():
                    try:
                        f.unlink()
                        deleted += 1
                    except Exception as e:
                        print(f"  ! error deleting {f}: {e}")
    print(f"✓ Deleted {deleted} figure file(s).")

def main():
    parser = argparse.ArgumentParser(
        description="Clear out raw_data or figures for all schools."
    )
    parser.add_argument(
        "--mode",
        choices=("raw", "visuals", "all"),
        default="raw",
        help="What to clear: raw (raw_data), visuals (figures), or all"
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    schools_root = project_root / "schools"
    if not schools_root.exists():
        print(f"Error: cannot find schools/ at {schools_root}")
        return

    if args.mode in ("raw", "all"):
        print("Clearing raw JSON…")
        clear_raw(schools_root)

    if args.mode in ("visuals", "all"):
        print("Clearing figures…")
        clear_visuals(schools_root)

if __name__ == "__main__":
    main()
