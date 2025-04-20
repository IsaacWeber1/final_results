# scripts/populate_folders.py
import os
from pathlib import Path

def populate_school_folder(school_root: Path):
    """
    Given the path to a school directory, create standard subdirectories and files:
      - scraping_configs/
      - raw_data/
      - processed_data/
      - pdfs/
      - screenshots/
      - notes.txt (empty file)
    """
    # Define subdirectories to create
    subdirs = [
        'scraping_configs',
        'raw_data',
        'processed_data',
        'pdfs',
        'screenshots'
    ]
    
    for sub in subdirs:
        dir_path = school_root / sub
        dir_path.mkdir(parents=True, exist_ok=False)
        print(f"Created directory: {dir_path}")

    
    # Create an empty notes.txt, config file in the school root
    notes_file = school_root / 'notes.txt'
    notes_file.touch(exist_ok=False)
    print(f"Created file: {notes_file}")

    config_dir = school_root / 'scraping_configs'
    config_file = config_dir / f"{school_root.name}_config.py"
    if not config_file.exists():
        config_file.touch()
        print(f"Created config file: {config_file}")
    else:
        print(f"Config file already exists: {config_file}")

if __name__ == '__main__':
    base = Path(__file__).resolve().parent.parent / 'schools'
    # Iterate over both priority and non_priority
    for category in ['priority', 'non_priority']:
        category_dir = base / category
        if not category_dir.exists():
            raise FileNotFoundError(f"Directory {category_dir} does not exist.")
        for school_dir in category_dir.iterdir():
            if school_dir.is_dir():
                populate_school_folder(school_dir)