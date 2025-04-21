# scripts/directory_initialization/add_gitignores.py

import sys
from pathlib import Path

def add_gitignores(schools_root: Path):
    """
    For each school under priority/ and non_priority/, create an empty
    .gitignore file in every subdirectory (so Git will track the folder).
    """
    for category in ("priority", "non_priority"):
        cat_dir = schools_root / category
        if not cat_dir.is_dir():
            continue
        for school_dir in cat_dir.iterdir():
            if not school_dir.is_dir():
                continue
            # create .gitignore in each immediate subfolder
            for sub in school_dir.iterdir():
                if sub.is_dir():
                    gi = sub / ".gitignore"
                    if not gi.exists():
                        gi.touch()
                        print(f"Created {gi}")
                    else:
                        print(f"Already exists: {gi}")

def main():
    # assume this script lives in PROJECT_ROOT/scripts/
    project_root = Path(__file__).resolve().parent.parent.parent
    schools_dir = project_root / "schools"
    if not schools_dir.exists():
        print(f"Error: could not find schools/ at {schools_dir}", file=sys.stderr)
        sys.exit(1)
    add_gitignores(schools_dir)
    print("Done.")

if __name__ == "__main__":
    main()
