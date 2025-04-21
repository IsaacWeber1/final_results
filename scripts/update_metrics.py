# scripts/update_metrics.py
import csv
from pathlib import Path
from datetime import datetime, timezone

ROOT        = Path(__file__).resolve().parent.parent
SCHOOLS_DIR = ROOT / "schools"
OUT_FILE    = ROOT / "metrics.csv"

def check_web_scraped(school_dir):
    return any((school_dir / "raw_data").glob("*.json"))

def check_pdf_scraped(school_dir):
    return any((school_dir / "pdfs").iterdir())

def check_confirmed(school_dir):
    # Suppose you touch a file `confirmed.txt` when you confirm manually
    return (school_dir / "confirmed.txt").exists()

def gather():
    rows = []
    for category in ("priority", "non_priority"):
        cat_dir = SCHOOLS_DIR / category
        if not cat_dir.exists(): continue
        for school in sorted(cat_dir.iterdir()):
            if not school.is_dir(): continue
            rows.append({
                "school":        school.name,
                "category":      category,
                "web_scraped":   str(check_web_scraped(school)),
                "pdf_scraped":   str(check_pdf_scraped(school)),
                "confirmed":     str(check_confirmed(school)),
                "last_updated":  datetime.now(timezone.utc)
            })
    return rows

def write_csv(rows):
    with OUT_FILE.open("w", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"Wrote metrics for {len(rows)} schools to {OUT_FILE}")

if __name__ == "__main__":
    data = gather()
    if data:
        write_csv(data)
    else:
        print("No schools found!")
