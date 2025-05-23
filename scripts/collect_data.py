# scripts/collect_data.py

import sys
from pathlib import Path
import pandas as pd

# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    for category in ['priority', 'non_priority']:
        base = PROJECT_ROOT / "schools" / category
        if not base.exists():
            return
        
        all_files = []
        for school in sorted(base.iterdir()):
            path = school / "processed_data" / "processed.csv"
            if path.exists():
                df = pd.read_csv(path)
                all_files.append((school.name, df))


        with pd.ExcelWriter(PROJECT_ROOT / "reports" / f"{category}_combined.xlsx") as writer:
            for name, file in all_files:
                file.to_excel(writer, sheet_name=name[:31], index=False)

if __name__ == "__main__":
    main()