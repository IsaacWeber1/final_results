# scripts/compile_keywords.py

import sys
from pathlib import Path

# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from pathlib import Path
from report_tools.word_groups import compile_equivalencies, compile_keywords

def main():
    wg_dir = Path(__file__).resolve().parent.parent / "data" / "word_groups"
    xlsx = wg_dir / "phrases_spreadsheet.xlsx"

    equiv_out = wg_dir / "unique_word_groups.json"
    kw_out    = wg_dir / "current_keyword_groups.json"

    print(f"Compiling equivalencies from {xlsx} → {equiv_out}")
    compile_equivalencies(xlsx, equiv_out)

    print(f"Compiling keyword groups from {xlsx} → {kw_out}")
    compile_keywords(xlsx, kw_out)

if __name__ == "__main__":
    main()
