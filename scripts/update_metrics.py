# scripts/update_metrics.py
import csv
from pathlib import Path
from datetime import datetime, timezone
import argparse

def view_metrics(file_path: Path):
    if not file_path.exists():
        print(f"No metrics file at {file_path}")
        return
    with file_path.open(newline="", encoding="utf8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        print("Metrics file is empty")
        return
    # compute column widths
    widths = [max(len(cell) for cell in col) for col in zip(*rows)]
    # print header + separator
    header = rows[0]
    line = "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(header))
    print(line)
    print("-" * len(line))
    # print data
    for row in rows[1:]:
        print("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)))
    
    # --- summary ---
    total = len(rows) - 1
    idx = {col: rows[0].index(col) for col in rows[0]}
    web_count = sum(1 for r in rows[1:] if r[idx["web_scraped"]] == "True")
    pdf_count = sum(1 for r in rows[1:] if r[idx["pdf_scraped"]] == "True")
    conf_count = sum(1 for r in rows[1:] if r[idx["confirmed"]] == "True")

    def pct(n, denom=total):
        return f"{n}/{total} ({n*100/total:.0f}%)"

    print("\n\nOverall Summary:")
    print(f"\t\tTotal schools:      {total}")
    print(f"\t\tWeb scraped:        {pct(web_count)}")
    print(f"\t\tPDF scraped:        {pct(pdf_count)}")
    print(f"\t\tConfirmed:          {pct(conf_count)}")

    # --- priority schools summary ---
    pr_rows = [r for r in rows[1:] if r[idx["category"]] == "priority"]
    pr_total = len(pr_rows)
    if pr_total:
        pr_web = sum(1 for r in pr_rows if r[idx["web_scraped"]] == "True")
        pr_pdf = sum(1 for r in pr_rows if r[idx["pdf_scraped"]] == "True")
        pr_conf = sum(1 for r in pr_rows if r[idx["confirmed"]] == "True")

        print("\n\nPriority Summary:")
        print(f"\t\tTotal priority:     {pr_total}")
        print(f"\t\tWeb scraped:        {pct(pr_web, pr_total)}")
        print(f"\t\tPDF scraped:        {pct(pr_pdf, pr_total)}")
        print(f"\t\tConfirmed:          {pct(pr_conf, pr_total)}")
    else:
        print("\n\nPriority Schools Summary:  none found")


def update_metrics():
    ROOT        = Path(__file__).resolve().parent.parent
    SCHOOLS_DIR = ROOT / "schools"
    OUT_FILE    = ROOT / "metrics.csv"
    now_iso     = datetime.now(timezone.utc).isoformat()

    # gather current state
    new_rows = []
    for category in ("priority", "non_priority"):
        cat_dir = SCHOOLS_DIR / category
        if not cat_dir.exists():
            continue
        for school_dir in sorted(cat_dir.iterdir()):
            if not school_dir.is_dir():
                continue

            web_ok = (school_dir / "processed_data" / "processed.csv").exists()

            pdf_ok = False
            pdf_dir = school_dir / "pdfs"
            if pdf_dir.exists():
                for p in pdf_dir.iterdir():
                    if p.name != ".gitignore":
                        pdf_ok = True
                        break

            conf_ok = (school_dir / "confirmed.txt").exists()

            new_rows.append({
                "school":       school_dir.name,
                "category":     category,
                "web_scraped":  str(web_ok),
                "pdf_scraped":  str(pdf_ok),
                "confirmed":    str(conf_ok),
            })

    # read existing metrics
    existing = {}
    if OUT_FILE.exists():
        with OUT_FILE.open(newline="", encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row["category"], row["school"])
                existing[key] = row

    # merge & decide which timestamps to bump
    final_rows = []
    for row in new_rows:
        key = (row["category"], row["school"])
        if key in existing:
            old = existing[key]
            if (old["web_scraped"]  != row["web_scraped"] or
                old["pdf_scraped"]  != row["pdf_scraped"] or
                old["confirmed"]    != row["confirmed"]):
                # something changed → bump timestamp
                row["last_updated"] = now_iso
            else:
                # no change → preserve
                row["last_updated"] = old.get("last_updated", now_iso)
        else:
            # brand‑new school → set now
            row["last_updated"] = now_iso

        final_rows.append(row)

    # write back
    if final_rows:
        with OUT_FILE.open("w", newline="", encoding="utf8") as f:
            fieldnames = ["school","category","web_scraped","pdf_scraped","confirmed","last_updated"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in final_rows:
                writer.writerow(r)
        print(f"Updated metrics for {len(final_rows)} schools → {OUT_FILE}")
    else:
        print("No schools found!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--view", action="store_true",
        help="Just display metrics.csv in a table and exit"
    )
    args = parser.parse_args()

    ROOT     = Path(__file__).resolve().parent.parent
    METRICS  = ROOT / "metrics.csv"

    if args.view:
        view_metrics(METRICS)
    else:
        update_metrics()
