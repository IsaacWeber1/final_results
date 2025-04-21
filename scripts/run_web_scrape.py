# scripts/scraping/run_web_scrape.py

import sys
import os
from pathlib import Path

# add project root (two levels up from this file) to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import argparse
import importlib.util
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper_module.scraper_lib.scraper_engine import ScraperEngine

def discover_config_files(schools_root: Path):
    """
    Find all configs in:
        schools/<priority|non_priority>/<school>/scraping_configs/*.py
    """
    configs = []
    for cfg in schools_root.glob('*/*/scraping_configs/*_config.py'):
        if os.path.getsize(cfg) != 0:
            school_dir = cfg.parent.parent
            configs.append((school_dir, cfg))

    return configs

def needs_run(school_dir: Path) -> bool:
    """Return True if processed_data is empty or missing."""
    pd = school_dir / 'processed_data'
    if not pd.exists():
        return True
    # consider "processed" if there's any file in processed_data
    files = [f for f in pd.iterdir() if (f.is_file() and f.name != '.gitignore')]
    return len(files) == 0

def load_config_module(path: Path):
    """Dynamically load a .py file and return its module."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    parser = argparse.ArgumentParser(
        description="Run all school scrapers (mode=missing or all)"
    )
    parser.add_argument(
        '--mode', choices=('missing', 'all'), default='missing',
        help="Run only schools with no processed_data (missing), or run all."
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    schools_root = project_root / 'schools'

    # discover all configs
    configs = discover_config_files(schools_root)
    if not configs:
        print("No scraper configs found under schools/*/scraping_configs/")
        return

    # prepare Scrapy process
    process = CrawlerProcess(get_project_settings())

    for school_dir, cfg_path in configs:
        if args.mode == 'missing' and not needs_run(school_dir):
            print(f"Skipping {school_dir.name} (already has processed data)")
            continue

        # load each config module (expects it to define `config = SpiderConfig(...)`)
        module = load_config_module(cfg_path)
        engine = ScraperEngine(module.config)
        raw_data_dir = school_dir / "raw_data"
        print(f"Scheduling scraper for: {school_dir.name}")
        engine.schedule(process, output_dir=str(raw_data_dir))

    print("Starting crawl process...")
    process.start()
    print("All scrapers finished.")

if __name__ == '__main__':
    main()
