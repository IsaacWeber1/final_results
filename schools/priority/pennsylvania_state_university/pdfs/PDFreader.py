import re
import sys
import json
from PyPDF2 import PdfReader

def extract_courses(pdf_path, output_path, format1_range=(3188, 3275), format2_range=(3300, 4772)):
    """
    Extracts courses in two different formats and outputs in JSON format:
    {
        "title": "CODE: TITLE",
        "description": "DESCRIPTION",
        "source": "PDF"
    }
    """
    # Pattern for format 1: single line courses
    pattern1 = re.compile(r'^([A-Z]{2,}\s\d+[A-Z]?)\s+(.+?)\s+(\d+)$')
    
    # Pattern for format 2: multi-line courses
    pattern2_code_title = re.compile(r'^([A-Z]{2,}\s\d+[A-Z]?):\s+(.+)$')
    pattern2_credits = re.compile(r'^\s*(\d+)\s+Credits?\s*$', re.IGNORECASE)
    
    courses = []
    current_course = None
    collecting_description = False
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf = PdfReader(file)
            total_pages = len(pdf.pages)
            
            # Validate page ranges
            ranges = [format1_range, format2_range]
            for start, end in ranges:
                if start < 0 or end >= total_pages:
                    print(f"Error: PDF only has {total_pages} pages")
                    return
            
            print(f"Processing format 1 (pages {format1_range[0]+1} to {format1_range[1]+1})...")
            for page_num in range(format1_range[0], format1_range[1] + 1):
                sys.stdout.write(f"\rProcessing page {page_num+1}/{format1_range[1]+1}... ")
                sys.stdout.flush()
                
                try:
                    text = pdf.pages[page_num].extract_text()
                    if not text:
                        continue
                        
                    for line in text.split('\n'):
                        line = line.strip()
                        match = pattern1.match(line)
                        if match:
                            code, title, _ = match.groups()  # We ignore credits in this format
                            # Format 1 courses don't have descriptions
                            courses.append({
                                'title': f"{code}: {title}",
                                'description': 'N/A',
                                'source': 'PDF'
                            })
                except Exception as e:
                    print(f"\nError processing page {page_num+1}: {str(e)}")
                    continue
            
            print(f"\nProcessing format 2 (pages {format2_range[0]+1} to {format2_range[1]+1})...")
            for page_num in range(format2_range[0], format2_range[1] + 1):
                sys.stdout.write(f"\rProcessing page {page_num+1}/{format2_range[1]+1}... ")
                sys.stdout.flush()
                
                try:
                    text = pdf.pages[page_num].extract_text()
                    if not text:
                        continue
                        
                    for line in text.split('\n'):
                        line = line.strip()
                        
                        # Check for code and title line
                        code_title_match = pattern2_code_title.match(line)
                        if code_title_match:
                            if current_course:  # Save previous course if exists
                                courses.append({
                                    'title': f"{current_course['code']}: {current_course['title']}",
                                    'description': current_course['description'],
                                    'source': 'PDF'
                                })
                            code, title = code_title_match.groups()
                            current_course = {
                                'code': code,
                                'title': title,
                                'description': 'N/A'  # Default if no description found
                            }
                            collecting_description = False
                            continue
                        
                        # Check for credits line
                        credits_match = pattern2_credits.match(line)
                        if credits_match and current_course:
                            collecting_description = True
                            continue
                        
                        # Collect description lines
                        if collecting_description and current_course:
                            if current_course['description'] == 'N/A':  # First description line
                                current_course['description'] = line
                            else:  # Additional description lines
                                current_course['description'] += " " + line
                except Exception as e:
                    print(f"\nError processing page {page_num+1}: {str(e)}")
                    continue
        
            # Add the last course if exists
            if current_course:
                courses.append({
                    'title': f"{current_course['code']}: {current_course['title']}",
                    'description': current_course['description'],
                    'source': 'PDF'
                })
            
            print(f"\nFound {len(courses)} courses")
            
            # Write in JSON format
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(courses, f, indent=4, ensure_ascii=False)
            print(f"Successfully saved to {output_path} in JSON format")
            
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = "undergraduate.pdf"
    
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        output_path = "PDFCourses.json"
    
    extract_courses(pdf_path, output_path)