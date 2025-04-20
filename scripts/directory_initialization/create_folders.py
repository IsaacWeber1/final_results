# scripts/create_folders.py
import os
import csv

def create_dirs_from_csv(csv_path, output_dir):
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:  # skip empty lines
                continue
            school_name = row[0].strip()
            # Create directory path
            school_dir = os.path.join(output_dir, school_name)
            if os.path.exists(school_dir):
                print(f"Directory already exists: {school_dir}")
            else:
                os.makedirs(school_dir, exist_ok=False)
                print(f"Created: {school_dir}")

if __name__ == "__main__":
    base_dir = os.path.join(os.getcwd(), "schools")
    priority_csv = os.path.join(base_dir, "priority_schools.csv")
    non_priority_csv = os.path.join(base_dir, "non_priority_schools.csv")

    create_dirs_from_csv(priority_csv, os.path.join(base_dir, "priority"))
    create_dirs_from_csv(non_priority_csv, os.path.join(base_dir, "non_priority"))
