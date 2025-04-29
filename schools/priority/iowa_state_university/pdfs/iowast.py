import re
import json
import sys
from pdfminer.high_level import extract_text

def extract_courses_from_batch(pdf_path, start, end):
    text = extract_text(pdf_path, page_numbers=list(range(start, end)))
    course_pattern = re.compile(r"\b([A-Z]{2,5})\s+(\d{3}[A-Z]?)[:\.]\s+(.+?)\s*(?:\n|$)")
    courses = []
    seen = set()

    for line in text.splitlines():
        match = course_pattern.match(line.strip())
        if match:
            course_id = f"{match.group(1)} {match.group(2)}"
            title = match.group(3).strip()
            if course_id not in seen:
                seen.add(course_id)
                courses.append({
                    "Course ID": course_id,
                    "Title": title,
                    "Description": ""
                })
    return courses

def main():
    if len(sys.argv) != 3:
        print("Usage: python iowast_scraper.py <input.pdf> <output.json>")
        return

    input_pdf = sys.argv[1]
    output_json = sys.argv[2]

    all_courses = []
    # Page numbers: 677–1360 (0-indexed in pdfminer, so 676–1359)
    for start in range(676, 1361, 100):  # Batches of 100 pages
        end = min(start + 100, 1361)
        print(f"Extracting pages {start+1} to {end}")
        batch_courses = extract_courses_from_batch(input_pdf, start, end)
        all_courses.extend(batch_courses)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_courses, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(all_courses)} courses to {output_json}")

if __name__ == "__main__":
    main()
