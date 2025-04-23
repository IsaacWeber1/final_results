# scripts/run_pdf_scrape.py

"""
Script to run per‑school PDF scrapers as defined in each school's `pdf/` folder.
Assumptions:
  - If no .py files found in pdf/, skip.
  - If exactly one .py file, run it from inside the pdf/ directory.
  - If more than one .py file, report an error and skip.
  - After running, check for creation of any .json, .csv, or .txt files as proof of success.
Usage:
  make pdf-scrape
  make pdf-scrape-all

  or

  python scripts/run_pdf_scrape.py --mode <missing|all>
"""

import argparse
import subprocess
import sys
from pathlib import Path

def run_pdf_scraper(pdf_dir: Path) -> bool:
    """
    Locate and run the single PDF scraper in pdf_dir.
    Returns True if scraper ran and emitted at least one output file (.json/.csv/.txt), else False.
    """
    # find python scripts
    py_files = list(pdf_dir.glob("*.py"))
    if not py_files:
        print(f"No PDF scraper found in {pdf_dir}, skipping.")
        return True
    if len(py_files) > 1:
        print(f"  ! Multiple scraper scripts in {pdf_dir}: {[p.name for p in py_files]}")
        return False
    scraper = py_files[0]
    print(f"  → Running PDF scraper: {scraper.name}")
    result = subprocess.run([sys.executable, scraper.name], cwd=str(pdf_dir))
    if result.returncode != 0:
        print(f"  ! Scraper {scraper.name} exited with code {result.returncode}")
        return False
    # check outputs
    outputs = []
    for ext in ("*.json", "*.csv", "*.txt"):
        outputs.extend(pdf_dir.glob(ext))
    if not outputs:
        print(f"  ! No output files (.json/.csv/.txt) in {pdf_dir} after running scraper")
        return False
    print(f"  ✓ Output files: {[p.name for p in outputs]}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Run school PDF scrapers.")
    parser.add_argument('--mode', choices=['missing','all'], required=True,
                        help="'missing': only schools without processed_data; 'all': every school")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    schools_root = project_root / 'schools'

    failures = []
    for category in ('priority', 'non_priority'):
        cat_dir = schools_root / category
        if not cat_dir.is_dir():
            continue
        for school in sorted(cat_dir.iterdir()):
            if not school.is_dir():
                continue

            pdf_dir = school / 'pdfs'

            existing_outputs = []
            for ext in ("*.json", "*.csv", "*.txt"):
                existing_outputs.extend(pdf_dir.glob(ext))

            if args.mode == 'missing' and existing_outputs:
                print(f"Skipping {category}/{school.name} (already has PDF outputs).")
                continue

            if not pdf_dir.is_dir():
                print(f"No pdf/ folder for {school.name}, skipping.")
                continue

            ok = run_pdf_scraper(pdf_dir)
            if not ok:
                failures.append(f"{category}/{school.name}")

    if failures:
        print("\nPDF scraping failed for the following schools:")
        for f in failures:
            print(f" - {f}")
        sys.exit(1)

    print("\nPDF scraping completed successfully.")

if __name__ == '__main__':
    main()
