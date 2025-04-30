import json
import sys
import re
from pdfminer.high_level import extract_text

def extract_courses_from_text(text):
    # Normalize text
    text = re.sub(r'\s+', ' ', text)
    text += " END 999 EndMarker"

    # Find all course IDs and their positions
    course_matches = list(re.finditer(
        r'([A-Z]{2,4}\s*\d{3}[A-Z]?(?:/\s*[A-Z]{2,4}\s*\d{3}[A-Z]?)?)',
        text
    ))

    courses = []

    for i in range(len(course_matches) - 1):
        current = course_matches[i]
        next_ = course_matches[i + 1]

        course_id = current.group(1).strip()
        start_of_title = current.end()
        end_of_title = next_.start()

        title = text[start_of_title:end_of_title].strip()

        # Avoid false matches like title being another course ID
        if re.match(r'^[A-Z]{2,4}\s*\d{3}[A-Z]?$', title):
            continue

        courses.append({
            "Course ID": course_id,
            "Title": title,
            "Description": ""
        })

    return courses

def pdf_to_json(pdf_path, json_path):
    try:
        text = extract_text(pdf_path)
        extracted_courses = extract_courses_from_text(text)

        data = {
            "matches": extracted_courses
        }

        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        print(f"✅ Extracted {len(extracted_courses)} courses. JSON saved to {json_path}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

def main():
    # if len(sys.argv) != 3:
    #     print("Usage: python script.py <input.pdf> <output.json>")
    #     return

    input_pdf = "bamaAM.pdf"
    output_json = "raw_data/alabama_pdf.json"

    pdf_to_json(input_pdf, output_json)

if __name__ == "__main__":
    main()
