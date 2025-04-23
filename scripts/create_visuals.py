# scripts/create_visuals.py

import sys
from pathlib import Path
# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import argparse
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from report_tools.word_groups import load_keyword_groups

def keyword_histogram(df: pd.DataFrame, out_png: Path, name: str):
    """
    Plot a histogram of raw keyword frequencies across all courses.
    """
    freqs = df['keyword_frequencies'].dropna().apply(json.loads)
    counter = Counter()
    for d in freqs:
        counter.update(d)
    if not counter:
        return
    keywords, counts = zip(*counter.most_common())
    
    n_bars = len(keywords)
    fig_w  = max(8, n_bars * 0.3)
    fig_h = 6

    plt.figure(figsize=(fig_w, fig_h))
    plt.bar(keywords, counts)
    plt.xticks(rotation=90)
    plt.title(f"{name} — Keyword Frequency Histogram")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
    return max(counts)


def group_histogram(df: pd.DataFrame, out_png: Path, name: str):
    """
    Plot a histogram of matched keyword group occurrences.
    """
    groups = df['matched_groups'].dropna().str.split(';').explode()
    counts = groups.value_counts()
    if counts.empty:
        return

    # n_bars = len(groups)
    # fig_w  = max(8, n_bars * 0.3)
    fig_w  = 8
    fig_h = 6

    plt.figure(figsize=(fig_w, fig_h))
    plt.bar(counts.index, counts.values)
    plt.xticks(rotation=90)
    plt.title(f"{name} — Keyword Group Histogram")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
    return int(counts.max())

def collapsed_histogram(df: pd.DataFrame, out_png: Path, equiv_json: Path, name: str):
    """
    Collapse synonyms as per unique_word_groups.json and plot histogram.
    """
    mapping = json.loads(equiv_json.read_text(encoding='utf8'))
    freqs = df['keyword_frequencies'].dropna().apply(json.loads)
    counter = Counter()
    for d in freqs:
        for kw, cnt in d.items():
            canon = next((master for master, group in mapping.items() if kw in group), kw)
            counter[canon] += cnt
    if not counter:
        return
    items = counter.most_common()
    keys, vals = zip(*items)

    n_bars = len(keys)
    fig_w  = max(8, n_bars * 0.3)
    fig_h = 6

    plt.figure(figsize=(fig_w, fig_h))
    plt.bar(keys, vals)
    plt.xticks(rotation=90)
    plt.title(f"{name} — Collapsed Keyword Histogram")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
    return max(vals)

def compute_global_maxima(schools_root: Path, equiv_json: Path):
    """
    Scan all schools to determine maximum y-axis values for each histogram type.
    """
    max_kw = max_grp = max_coll = 0
    for category in ("priority", "non_priority"):
        base = schools_root / category
        if not base.exists():
            continue
        for school in base.iterdir():
            csv_path = school / "processed_data" / "processed.csv"
            if not csv_path.exists():
                continue
            df = pd.read_csv(csv_path)
            # keyword
            freqs = df['keyword_frequencies'].dropna().apply(json.loads)
            counter = Counter()
            for d in freqs:
                counter.update(d)
            if counter:
                max_kw = max(max_kw, max(counter.values()))
            # group
            groups = df['matched_groups'].dropna().str.split(';').explode()
            counts = groups.value_counts()
            if not counts.empty:
                max_grp = max(max_grp, counts.max())
            # collapsed
            mapping = json.loads(equiv_json.read_text(encoding='utf8'))
            counter2 = Counter()
            for d in freqs:
                for kw, cnt in d.items():
                    canon = next((master for master, group in mapping.items() if kw in group), kw)
                    counter2[canon] += cnt
            if counter2:
                max_coll = max(max_coll, max(counter2.values()))
    return max_kw, max_grp, max_coll

def main():
    parser = argparse.ArgumentParser(description="Generate course keyword visuals.")
    parser.add_argument(
        '--mode', choices=['add', 'replace'], default='add',
        help="'add': skip existing figures; 'replace': regenerate all"
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent / "schools"
    equiv_json = Path(__file__).resolve().parent.parent / "data/word_groups/unique_word_groups.json"

    # track per-school maxima
    kw_max_by_school   = {}
    grp_max_by_school  = {}
    coll_max_by_school = {}

    for category in ("priority", "non_priority"):
        cat_dir = root / category
        if not cat_dir.exists():
            continue
        for school in cat_dir.iterdir():
            skip_flag = False
            # print(f"Processing {school.name}...")
            proc_csv = school / "processed_data" / "processed.csv"
            if not proc_csv.exists():
                # print(f"  ! Missing processed CSV: {proc_csv}")
                skip_flag = True
                continue
            if skip_flag:
                raise Exception("CONTINUE NOT WORKING")
            df = pd.read_csv(proc_csv)

            fig_dir = school / "figures"
            if not fig_dir.exists():
                raise FileNotFoundError(f"Missing figures directory: {fig_dir}")

            # raw keyword histogram
            out_kw = fig_dir / "keyword_freq.png"
            if args.mode=='replace' or not out_kw.exists():
                kw_max = keyword_histogram(df, out_kw, school.name)
            else:
                # if skipping, still compute counts
                freqs = df['keyword_frequencies'].dropna().apply(json.loads)
                counter = Counter(); [counter.update(d) for d in freqs]
                kw_max = max(counter.values()) if counter else 0
            kw_max_by_school[school.name] = kw_max

            # group histogram
            out_grp = fig_dir / "group_freq.png"
            if args.mode=='replace' or not out_grp.exists():
                grp_max = group_histogram(df, out_grp, school.name)
            else:
                groups = df['matched_groups'].dropna().str.split(';').explode()
                counts = groups.value_counts()
                grp_max = int(counts.max()) if not counts.empty else 0
            grp_max_by_school[school.name] = grp_max

            # collapsed histogram
            out_coll = fig_dir / "collapsed_freq.png"
            if args.mode=='replace' or not out_coll.exists():
                coll_max = collapsed_histogram(df, out_coll, equiv_json, school.name)
            else:
                mapping = json.loads(equiv_json.read_text(encoding='utf8'))
                freqs = df['keyword_frequencies'].dropna().apply(json.loads)
                counter = Counter()
                for d in freqs:
                    for kw, cnt in d.items():
                        canon = next((m for m, grp in mapping.items() if kw in grp), kw)
                        counter[canon] += cnt
                coll_max = max(counter.values()) if counter else 0
            coll_max_by_school[school.name] = coll_max

            if args.mode == 'replace':
                print(f"Saved visuals for {school.name} (mode={args.mode})")
            else:
                # check if any of the files exist
                if out_kw.exists() or out_grp.exists() or out_coll.exists():
                    print(f"SKIP: {school.name} (mode={args.mode})")
                    continue
                else:
                    print(f"Saved visuals for {school.name} (mode={args.mode})")
    
    # --- summary ---
    # print("creating summary")
    def top(d):
        if not d: return ("n/a", 0)
        school, val = max(d.items(), key=lambda kv: kv[1])
        return school, val

    # print(f"kwmax_by_school: {kw_max_by_school}")
    kw_school,   kw_val   = top(kw_max_by_school)
    grp_school,  grp_val  = top(grp_max_by_school)
    coll_school, coll_val = top(coll_max_by_school)

    print("\n=== VISUALS SUMMARY ===")
    print(f"Highest raw-keyword count:     {kw_val}  ({kw_school})")
    print(f"Highest group-keyword count:   {grp_val}  ({grp_school})")
    print(f"Highest collapsed-keyword count: {coll_val}  ({coll_school})")

if __name__ == "__main__":
    main()