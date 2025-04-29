import re
import json
import sys
from pdfminer.high_level import extract_text

def extract_courses_from_pdf(pdf_path):
    text = extract_text(pdf_path)

    # Match "__ENG 2120" or "___BIO 1103" formats
    course_pattern = re.compile(r"(?:_{2,3})\s*([A-Z&/]{2,5})\s*(\d{4})")

    lines = text.splitlines()
    courses = []

    for i, line in enumerate(lines):
        matches = course_pattern.findall(line)
        if matches:
            for match in matches:
                prefix, number = match
                course_id = f"{prefix} {number}"
                title = ""

                # Look ahead 1–2 lines for potential title if they are short and don’t contain another course
                next_lines = ' '.join(lines[i+1:i+3]).strip()
                if next_lines and not course_pattern.search(next_lines) and len(next_lines) < 120:
                    title = next_lines

                courses.append({
                    "Course ID": course_id,
                    "Title": title,
                    "Description": ""
                })

    return courses

def save_courses_to_json(courses, json_path):
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(courses, json_file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python appst.py <input.pdf> <output.json>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_json = sys.argv[2]

    try:
        courses = extract_courses_from_pdf(input_pdf)
        save_courses_to_json(courses, output_json)
        print(f"✅ Extracted {len(courses)} courses to {output_json}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)
