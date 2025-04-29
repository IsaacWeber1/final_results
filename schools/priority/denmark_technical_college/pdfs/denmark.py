import re
import json
import sys
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer

def extract_text_from_pages(pdf_path, start_page, end_page):
    """Extract text from a specific page range of a PDF."""
    text = ""
    for i, page_layout in enumerate(extract_pages(pdf_path, laparams=LAParams())):
        if start_page <= i + 1 <= end_page:
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    text += element.get_text()
    return text

def extract_courses_from_text(text):
    """Extract structured course entries from raw text."""
    course_pattern = re.compile(r"\b([A-Z]{3,4}\s\d{3})\s+([A-Za-z0-9 &/,\-:]+)")
    lines = text.splitlines()
    courses = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        match = course_pattern.match(line)
        if match:
            course_id = match.group(1).strip()
            title = match.group(2).strip()
            description_lines = []
            i += 1
            while i < len(lines) and not course_pattern.match(lines[i]):
                desc_line = lines[i].strip()
                if desc_line and not re.match(r"\d+\s*CR", desc_line):  # Skip credit-hour lines like "3 CR"
                    description_lines.append(desc_line)
                i += 1
            description = " ".join(description_lines).strip()
            courses.append({
                "Course ID": course_id,
                "Title": title,
                "Description": description
            })
        else:
            i += 1

    return courses

def save_courses_to_json(courses, json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python denmark_extract_courses.py <input.pdf> <output.json>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_json = sys.argv[2]

    try:
        raw_text = extract_text_from_pages(input_pdf, 183, 202)
        courses = extract_courses_from_text(raw_text)
        save_courses_to_json(courses, output_json)
        print(f"✅ Extracted {len(courses)} courses to {output_json}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
