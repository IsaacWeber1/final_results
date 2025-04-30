# scripts/run_pdf_scrape.py

"""
Script to run per-school PDF scrapers as defined in each school's `pdfs/` folder.
Assumptions:
  - If no .py files found in pdfs/, skip.
  - If exactly one .py file, run it from inside the pdfs/ directory.
  - If more than one .py file, report an error and skip.
  - After running, check for creation of any .json files as proof of success.
  - Finally, move those .json files into pdfs/raw_data/.
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
    Returns True if scraper ran and emitted at least one .json, else False.
    """
    py_files = list(pdf_dir.glob("*.py"))
    if not py_files:
        print(f"  • No PDF scraper found in {pdf_dir}, skipping.")
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

    # check for JSON outputs only
    json_outputs = list(pdf_dir.glob("*.json"))
    if not json_outputs:
        print(f"  ! No .json output found in {pdf_dir} after running scraper")
        return False

    # create /pdfs/raw_data and move JSONs there
    raw_data_dir = pdf_dir / "raw_data"
    raw_data_dir.mkdir(exist_ok=True)
    for js in json_outputs:
        dest = raw_data_dir / js.name
        js.rename(dest)
    print(f"  ✓ Moved JSON outputs to {raw_data_dir}: {[p.name for p in raw_data_dir.glob('*.json')]}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Run school PDF scrapers.")
    parser.add_argument('--mode', choices=['missing','all'], required=True,
                        help="'missing': only schools without JSON in pdfs/raw_data; 'all': every school")
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
            has_processed = pdf_dir.is_dir() and any(pdf_dir.glob("processed.csv"))

            # skip if already done
            if args.mode == 'missing' and has_processed:
                print(f"Skipping {category}/{school.name} (already has PDF JSONs).")
                continue

            if not pdf_dir.is_dir():
                print(f"  • No pdfs/ folder for {school.name}, skipping.")
                continue

            # print(f"Processing {category}/{school.name} …")
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
