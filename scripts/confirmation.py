# scripts/confirmation.py

import sys
from pathlib import Path
import json
import re
from collections import Counter


# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# TODO: ZACH

# Should accept --school (and --mode all) so the Makefile can pass it through
def load_json_courses(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    seen_descriptions = set()
    titles = set()
    codes = set()
    duplicates = []

    for entry in json_data:
        title_field = entry.get('title')
        description = entry.get('description', '').strip()

        if description.upper() != "N/A" and description:
            if description in seen_descriptions:
                duplicates.append(description)
            else:
                seen_descriptions.add(description)

        if isinstance(title_field, list):
            for t in title_field:
                clean_title = t.strip()
                if ':' in clean_title:
                    code_part, actual_title = map(str.strip, clean_title.split(':', 1))
                    titles.add(actual_title)
                    codes.add(code_part)
                else:
                    titles.add(clean_title)
        elif isinstance(title_field, str):
            clean_title = title_field.strip()
            if ':' in clean_title:
                code_part, actual_title = map(str.strip, clean_title.split(':', 1))
                titles.add(actual_title)
                codes.add(code_part)
            else:
                titles.add(clean_title)

    return titles, codes, duplicates

def load_txt_courses(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = re.split(r'-{10,}', content)

    seen_descriptions = set()
    titles = set()
    codes = set()
    duplicates = []

    for entry in entries:
        code_match = re.search(r'Code:\s*(.*)', entry)
        title_match = re.search(r'Title:\s*(.*)', entry)
        description_match = re.search(r'Description:\s*(.*)', entry, re.DOTALL)

        description = ""
        if description_match:
            description = description_match.group(1).strip()

        if description.upper() != "N/A" and description:
            if description in seen_descriptions:
                duplicates.append(description)
            else:
                seen_descriptions.add(description)

        if code_match:
            codes.add(code_match.group(1).strip())
        if title_match:
            titles.add(title_match.group(1).strip())

    return titles, codes, duplicates

def find_duplicates(descriptions):
    counter = Counter(descriptions)
    return [desc for desc, count in counter.items() if count > 1]

def compare_courses(json_path, txt_path):
    json_titles, json_codes, json_dupes = load_json_courses(json_path)
    txt_titles, txt_codes, txt_dupes = load_txt_courses(txt_path)

    matched_titles = json_titles.intersection(txt_titles)
    matched_codes = json_codes.intersection(txt_codes)

    total_json_courses = len(json_titles.union(json_codes))
    matched_total = len(matched_titles.union(matched_codes))
    match_percentage = (matched_total / total_json_courses) * 100 if total_json_courses else 0

    missing = sorted((json_titles | json_codes) - (txt_titles | txt_codes))
    extra = sorted((txt_titles | txt_codes) - (json_titles | json_codes))

    return {
        'total_json_courses': total_json_courses,
        'matched_courses': matched_total,
        'match_percentage': match_percentage,
        'missing_from_txt': missing,
        'extra_in_txt': extra,
        'json_duplicates': json_dupes,
        'txt_duplicates': txt_dupes,
    }

def save_report(report, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Match Percentage: {report['match_percentage']:.2f}%\n")
        f.write(f"Matched Courses: {report['matched_courses']} / {report['total_json_courses']}\n\n")

        f.write("Missing from TXT file:\n")
        for item in report['missing_from_txt']:
            f.write(f" - {item}\n")

        f.write("\nExtra in TXT file:\n")
        for item in report['extra_in_txt']:
            f.write(f" - {item}\n")

        f.write("\nDuplicate Descriptions in JSON:\n")
        for dup in report['json_duplicates']:
            f.write(f" - {dup}\n")  # Print a shortened version

        f.write("\nDuplicate Descriptions in TXT:\n")
        for dup in report['txt_duplicates']:
            f.write(f" - {dup}\n")

if __name__ == "__main__":
    json_file = 'courses.json'  # path to JSON file
    txt_file = 'courses.txt'    # path to TXT file
    output_file = 'comparison_report.txt'

    report = compare_courses(json_file, txt_file)
    save_report(report, output_file)

    print(f"Comparison report with duplicate detection saved to: {output_file}")