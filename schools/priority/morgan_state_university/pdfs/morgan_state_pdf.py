import pdfplumber
import re
import json

def extract_courses_from_pdf(pdf_path):
    # Regex includes (FALL/SPRING) or similar in the description
    course_pattern = re.compile(
        r"(?P<course_id>[A-Z]{3,4} \d{3}) (?P<title>.+?)—.*?\n(?P<description>.*?\([A-Z/ ]+\))",
        re.DOTALL
    )

    courses = []

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        matches = course_pattern.finditer(full_text)

        for match in matches:
            course_id = match.group("course_id").strip()
            title = match.group("title").strip()
            raw_description = match.group("description").strip()
            description = re.sub(r'\s+', ' ', raw_description)

            courses.append({
                "Course ID": course_id,
                "Title": title,
                "Description": description
            })

    return courses

# Save results
def save_to_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Example usage
pdf_path = "ucat_2016-2018.pdf"
output_path = "morgan_state_out.json"
courses = extract_courses_from_pdf(pdf_path)
save_to_json(courses, output_path)

print(f"Extracted {len(courses)} courses and saved to {output_path}")
