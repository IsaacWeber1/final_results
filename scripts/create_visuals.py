# scripts/create_visuals.py

import sys
from pathlib import Path
# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from report_tools.word_groups import load_keyword_groups

def keyword_histogram(df: pd.DataFrame, out_png: Path):
    """
    Plot a histogram of raw keyword frequencies across all courses.
    """
    # extract frequencies column (JSON string of {keyword: count})
    freqs = df['keyword_frequencies'].dropna().apply(json.loads)
    counter = Counter()
    for d in freqs:
        counter.update(d)
    keywords, counts = zip(*counter.most_common())
    
    plt.figure(figsize=(8, 6))
    plt.bar(keywords, counts)
    plt.xticks(rotation=90)
    plt.title("Keyword Frequency Histogram")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

def group_histogram(df: pd.DataFrame, out_png: Path):
    """
    Plot a histogram of matched keyword group occurrences.
    """
    groups = df['matched_groups'].dropna().str.split(';').explode()
    counts = groups.value_counts()
    
    plt.figure(figsize=(8, 6))
    plt.bar(counts.index, counts.values)
    plt.xticks(rotation=90)
    plt.title("Keyword Group Histogram")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

def collapsed_histogram(df: pd.DataFrame, out_png: Path, equiv_json: Path):
    """
    Collapse synonyms as per unique_word_groups.json and plot histogram.
    """
    mapping = json.loads(equiv_json.read_text(encoding='utf8'))
    freqs = df['keyword_frequencies'].dropna().apply(json.loads)
    counter = Counter()
    for d in freqs:
        for kw, cnt in d.items():
            # find canonical keyword
            canon = next((master for master, group in mapping.items() if kw in group), kw)
            counter[canon] += cnt
    items = counter.most_common()
    keys, vals = zip(*items)
    
    plt.figure(figsize=(8, 6))
    plt.bar(keys, vals)
    plt.xticks(rotation=90)
    plt.title("Collapsed Keyword Histogram")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

def main():
    root = Path(__file__).resolve().parent.parent / "schools"
    equiv_json = Path(__file__).resolve().parent.parent / "data/word_groups/unique_word_groups.json"
    
    for category in ("priority", "non_priority"):
        for school in (root / category).iterdir():
            proc_csv = school / "processed_data" / "processed.csv"
            if not proc_csv.exists():
                continue
            df = pd.read_csv(proc_csv)
            fig_dir = school / "figures"
            fig_dir.mkdir(exist_ok=True)
            
            keyword_histogram(df, fig_dir / "keyword_freq.png")
            group_histogram(df, fig_dir / "group_freq.png")
            collapsed_histogram(df, fig_dir / "collapsed_freq.png")
            print(f"Saved visuals for {school.name} in {fig_dir}")

if __name__ == "__main__":
    main()