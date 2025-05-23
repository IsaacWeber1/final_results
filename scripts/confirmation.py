# scripts/confirmation.py

import argparse
import csv
import sys
from pathlib import Path

"""
This function is intended to compare the processed CSV files from the WEB and PDF scrapers to ensure a majority of classes were not missed.
To do this we focused on two main factors: the total number of courses found with desired keywords, and the average keyword value of the document
"""


# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

def compare_courses(PDF_path: Path, WEB_path: Path):
    def process_csv(file_path):
        # try:
            with open(file_path, 'r', encoding='utf-8') as f:
                """
                setting values for scoring
                total_score keeps track of the "relevance_score" from the CSV file where it will be divided by the length of the document to get the average
                count will keep track of how long the document is
                seen_titles will keep a list of the course titles. This lets us see if there are duplicate titles and report them.
                seen_description will keep a list of the course descriptions. This lets us see if there are duplicate titles and report them.
                duplicates is a list of the duplicates, title or description that is sent in the report.
                """
                reader = csv.DictReader(f)
                total_score = 0.0
                count = 0
                seen_titles = set()
                seen_descriptions = set()
                duplicates = []
                for row in reader:
                    # try:
                        # Extract and clean the title (handle the list format)
                        title_str = row['title'].strip("[]").replace("'", "")
                        titles_list = [t.strip() for t in title_str.split(',')]
                        primary_title = titles_list[0] if titles_list else ""
                        
                        # Clean the description
                        description = row['description'].strip() if 'description' in row else ""
                        
                        # variable to handle if the course is a duplicate
                        is_duplicate = False
                        #list of explanations for which kind of duplication occured
                        duplicate_reason = []
                        
                        if primary_title in seen_titles:
                            is_duplicate = True
                            duplicate_reason.append("duplicate title")
                        if description in seen_descriptions:
                            is_duplicate = True
                            duplicate_reason.append("duplicate description")
                        
                        if is_duplicate:
                            duplicates.append({
                                'title': primary_title,
                                'description': description,
                                'source': row.get('source', ''),
                                'reason': " or ".join(duplicate_reason)
                            })
                        
                        # Add to seen sets even if it's a duplicate
                        seen_titles.add(primary_title)
                        seen_descriptions.add(description)
                        
                        relevance = float(row['relevance_score'])
                        total_score += relevance
                        count += 1
                    # except (ValueError, KeyError) as e:
                    #     continue
                
                avg_score = total_score / count if count > 0 else 0.0
                return count, avg_score, duplicates
                
        # except FileNotFoundError:
        #     print(f"Error: File not found at {file_path}")
        #     return 0, 0.0, {}
        # except Exception as e:
        #     print(f"Error processing {file_path}: {e}")
        #     return 0, 0.0, {}
    
    pdf_count, pdf_avg, pdf_duplicates = (0, 0.0, {})
    web_count, web_avg, web_duplicates = (0, 0.0, {})

    # Process both files
    if (PDF_path.exists() or ()):
        pdf_count, pdf_avg, pdf_duplicates = process_csv(PDF_path)
    else:
        print("PDF processed data not found")
    if (WEB_path.exists()):
        web_count, web_avg, web_duplicates = process_csv(WEB_path)
    else:
        print("Web processed data not found")
    
    # Calculate comparison metrics
    count_diff = web_count - pdf_count
    score_diff = web_avg - pdf_avg

    return {
    'pdf_stats': {
        'file_path': str(PDF_path),
        'course_count': pdf_count,
        'avg_relevance': pdf_avg,
        'duplicate_count': len(pdf_duplicates)
    },
    'web_stats': {
        'file_path': str(WEB_path),
        'course_count': web_count,
        'avg_relevance': web_avg,
        'duplicate_count': len(web_duplicates)
    },
    'comparison': {
        'count_difference': count_diff,
        'score_difference': score_diff
    },
    'duplicates': {
        'pdf_duplicates': pdf_duplicates,
        'web_duplicates': web_duplicates
    }
}

def save_report(report, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        if (report['pdf_stats']['course_count'] > 0) and (report['web_stats']['course_count'] > 0):
            # Write header
            f.write("=== COURSE COMPARISON REPORT ===\n\n")
            
            # Write basic file info
            f.write("=== FILE INFORMATION ===\n")
            f.write(f"PDF file: {report['pdf_stats']['file_path']}\n")
            f.write(f"WEB file: {report['web_stats']['file_path']}\n\n")
            
            # Write counts comparison
            f.write("=== COURSE COUNTS ===\n")
            f.write(f"PDF course count: {report['pdf_stats']['course_count']}\n")
            f.write(f"WEB course count: {report['web_stats']['course_count']}\n")
            count_diff = report['comparison']['count_difference']
            if count_diff > 0:
                f.write(f"WEB has {abs(count_diff)} more courses than PDF\n")
            elif count_diff < 0:
                f.write(f"PDF has {abs(count_diff)} more courses than WEB\n")
            else:
                f.write("Both sources have the same number of courses\n")
            f.write("\n")
            
            # Write keyword count comparison
            f.write("=== AVERAGE RELEVANCE SCORES ===\n")
            f.write(f"PDF average keyword count score: {report['pdf_stats']['avg_relevance']:.2f}\n")
            f.write(f"WEB average keyword count score: {report['web_stats']['avg_relevance']:.2f}\n")
            score_diff = report['comparison']['score_difference']
            if score_diff > 0:
                f.write(f"WEB has higher average relevance by {abs(score_diff):.2f}\n")
            elif score_diff < 0:
                f.write(f"PDF has higher average relevance by {abs(score_diff):.2f}\n")
            else:
                f.write("Both sources have the same average relevance\n")
            f.write("\n")
            
            # Write duplicates summary
            f.write("=== DUPLICATES SUMMARY ===\n")
            f.write(f"PDF duplicates found: {report['pdf_stats']['duplicate_count']}\n")
            f.write(f"WEB duplicates found: {report['web_stats']['duplicate_count']}\n\n")

            f.write(f"\n\n\n")
            
            # Write PDF duplicates details
            if report['pdf_stats']['duplicate_count'] > 0:
                f.write("=== PDF DUPLICATES DETAILS ===\n")
                for i, dup in enumerate(report['duplicates']['pdf_duplicates'], 1):
                    f.write(f"Duplicate {i}:\n")
                    f.write(f"Title: {dup['title']}\n")
                    f.write(f"Description: {dup['description'][:100]}...\n")  # First 100 chars
                    f.write(f"Source: {dup['source']}\n")
                    f.write(f"Reason: {dup.get('reason', 'duplicate title or description')}\n\n")
            
            # Write WEB duplicates details
            if report['web_stats']['duplicate_count'] > 0:
                f.write("=== WEB DUPLICATES DETAILS ===\n")
                for i, dup in enumerate(report['duplicates']['web_duplicates'], 1):
                    f.write(f"Duplicate {i}:\n")
                    f.write(f"Title: {dup['title']}\n")
                    f.write(f"Description: {dup['description'][:100]}...\n")  # First 100 chars
                    f.write(f"Source: {dup['source']}\n")
                    f.write(f"Reason: {dup.get('reason', 'duplicate title or description')}\n\n")
            
            # Write overall similarity assessment
            # f.write("=== OVERALL SIMILARITY ASSESSMENT ===\n")
            # count_similarity = 1 - (abs(count_diff) / max(report['pdf_stats']['course_count'], 
            #                                             report['web_stats']['course_count'], 1))
            # score_similarity = 1 - (abs(score_diff) / max(report['pdf_stats']['avg_keyword_count'],
            #                                             report['web_stats']['avg_keyword_count'], 1))
            
            # f.write(f"Course count similarity: {count_similarity*100:.1f}%\n")
            # f.write(f"Average keyword count similarity: {score_similarity*100:.1f}%\n")
            
            # overall_similarity = (count_similarity + score_similarity) / 2
            # f.write(f"\nThe PDF and WEB scraper have: {overall_similarity*100:.1f}% similarity, meaning\n")
            
            # if overall_similarity > 0.8:
            #     f.write("VERY HIGH similarity between sources number of courses and average keyword counts\n")
            # elif overall_similarity > 0.6:
            #     f.write("HIGH similarity between sources number of courses and average keyword counts\n")
            # elif overall_similarity > 0.4:
            #     f.write("MODERATE similarity between sources number of courses and average keyword counts\n")
            # else:
            #     f.write("LOW similarity between sources number of courses and average keyword counts\n")
        else:
            # Write header
            f.write("=== COURSE COMPARISON REPORT ===\n\n")
            
            # Write basic file info
            f.write("=== FILE INFORMATION ===\n")
            f.write(f"PDF file: {report['pdf_stats']['file_path']}\n")
            f.write(f"WEB file: {report['web_stats']['file_path']}\n\n")
            
            # Write counts comparison
            f.write("=== COURSE COUNTS ===\n")
            f.write(f"PDF course count: {report['pdf_stats']['course_count']}\n")
            f.write(f"WEB course count: {report['web_stats']['course_count']}\n")
            count_diff = report['comparison']['count_difference']
            if count_diff > 0:
                f.write(f"WEB has {abs(count_diff)} more courses than PDF\n")
            elif count_diff < 0:
                f.write(f"PDF has {abs(count_diff)} more courses than WEB\n")
            else:
                f.write("Both sources have the same number of courses\n")
            f.write("\n")
            
            # Write keyword count comparison
            f.write("=== AVERAGE RELEVANCE SCORES ===\n")
            f.write(f"PDF average keyword score: {report['pdf_stats']['avg_relevance']:.2f}\n")
            f.write(f"WEB average keyword score: {report['web_stats']['avg_relevance']:.2f}\n")
            score_diff = report['comparison']['score_difference']
            if score_diff > 0:
                f.write(f"WEB has higher average relevance by {abs(score_diff):.2f}\n")
            elif score_diff < 0:
                f.write(f"PDF has higher average relevance by {abs(score_diff):.2f}\n")
            else:
                f.write("Both sources have the same average relevance\n")
            f.write("\n")
            
            # Write duplicates summary
            f.write("=== DUPLICATES SUMMARY ===\n")
            f.write(f"PDF duplicates found: {report['pdf_stats']['duplicate_count']}\n")
            f.write(f"WEB duplicates found: {report['web_stats']['duplicate_count']}\n\n")

            f.write(f"\n\n\n")
            
            # Write PDF duplicates details
            if report['pdf_stats']['duplicate_count'] > 0:
                f.write("=== PDF DUPLICATES DETAILS ===\n")
                for i, dup in enumerate(report['duplicates']['pdf_duplicates'], 1):
                    f.write(f"Duplicate {i}:\n")
                    f.write(f"Title: {dup['title']}\n")
                    f.write(f"Description: {dup['description'][:100]}...\n")  # First 100 chars
                    f.write(f"Source: {dup['source']}\n")
                    f.write(f"Reason: {dup.get('reason', 'duplicate title or description')}\n\n")
            
            # Write WEB duplicates details
            if report['web_stats']['duplicate_count'] > 0:
                f.write("=== WEB DUPLICATES DETAILS ===\n")
                for i, dup in enumerate(report['duplicates']['web_duplicates'], 1):
                    f.write(f"Duplicate {i}:\n")
                    f.write(f"Title: {dup['title']}\n")
                    f.write(f"Description: {dup['description'][:100]}...\n")  # First 100 chars
                    f.write(f"Source: {dup['source']}\n")
                    f.write(f"Reason: {dup.get('reason', 'duplicate title or description')}\n\n")

def process_school(school_dir: Path):
    # accept either "priority/uni_name" or "non_priority/uni_name"
    # school_dir = Path("schools") / school_arg
    PDFCSV_file = school_dir / "pdfs" / "processed.csv"
    WEBCSV_file = school_dir / "processed_data" / "processed.csv"
    report_file= school_dir / "comparison_report.txt"

    report = compare_courses(PDFCSV_file, WEBCSV_file)
    save_report(report, report_file)

def process_all():
    base = Path("schools")
    for category in ("priority", "non_priority"):
        for school in (base / category).iterdir():
            if school.is_dir():
                # school_arg = f"{category}/{school.name}"
                # try:
                    process_school(school)
                # except Exception as e:
                    # print(f"! Error processing {school}: {e}")

# if __name__ == "__main__":
#     json_file = 'courses.json'  # path to JSON file
#     txt_file = 'courses.txt'    # path to TXT file
#     output_file = 'comparison_report.txt'

#     report = compare_courses(json_file, txt_file)
#     save_report(report, output_file)

#     print(f"Comparison report with duplicate detection saved to: {output_file}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Confirm course scraping results")
    p.add_argument("--school", help="category/school_name to process")
    p.add_argument("--mode", choices=["all"], help="process all schools")
    args = p.parse_args()

    if args.mode == "all":
        process_all()
    elif args.school:
        process_school(args.school)
    else:
        p.print_usage()
        sys.exit(1)