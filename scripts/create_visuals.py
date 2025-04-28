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

def keyword_histogram(df: pd.DataFrame, out_png: Path, name: str, keywords_universe: list[str]) -> int:
    """
    Plot a histogram of raw keyword frequencies using a fixed universe of keywords.
    Returns the max count.
    """
    freqs = df['keyword_frequencies'].dropna().apply(json.loads)
    counter = Counter()
    for d in freqs:
        counter.update(d)
    # build counts in universe order
    counts = [counter.get(kw, 0) for kw in keywords_universe]
    if not any(counts):
        return 0

    n_bars = len(keywords_universe)
    fig_w  = max(8, n_bars * 0.3)
    fig_h = 6
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.bar(keywords_universe, counts)
    ax.set_xticklabels(keywords_universe, rotation=90)
    ax.set_title(f"{name} — Keyword Frequency Histogram")
    plt.tight_layout()
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    return max(counts)


def group_histogram(df: pd.DataFrame, out_png: Path, name: str, groups_universe: list[str]) -> int:
    """
    Plot a histogram of matched keyword group occurrences using fixed universe.
    Returns the max count.
    """
    groups = df['matched_groups'].dropna().str.split(';').explode()
    counts_series = groups.value_counts()
    counter = {g: counts_series.get(g, 0) for g in groups_universe}
    counts = list(counter.values())
    if not any(counts):
        return 0

    n_bars = len(groups_universe)
    fig_w  = max(8, n_bars * 0.3)
    fig_h = 6
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.bar(groups_universe, counts)
    ax.set_xticklabels(groups_universe, rotation=90)
    ax.set_title(f"{name} — Keyword Group Histogram")
    plt.tight_layout()
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    return max(counts)


def collapsed_histogram(df: pd.DataFrame, out_png: Path, equiv_json: Path, name: str, collapsed_universe: list[str]) -> int:
    """
    Collapse synonyms and plot histogram with fixed universe.
    Returns the max count.
    """
    mapping = json.loads(equiv_json.read_text(encoding='utf8'))
    freqs = df['keyword_frequencies'].dropna().apply(json.loads)
    counter = Counter()
    for d in freqs:
        for kw, cnt in d.items():
            canon = next((master for master, group in mapping.items() if kw in group), kw)
            counter[canon] += cnt
    counts = [counter.get(k, 0) for k in collapsed_universe]
    if not any(counts):
        return 0

    n_bars = len(collapsed_universe)
    fig_w  = max(8, n_bars * 0.3)
    fig_h = 6
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.bar(collapsed_universe, counts)
    ax.set_xticklabels(collapsed_universe, rotation=90)
    ax.set_title(f"{name} — Collapsed Keyword Histogram")
    plt.tight_layout()
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    return max(counts)

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

    root = PROJECT_ROOT / "schools"
    equiv_json = PROJECT_ROOT / "data/word_groups/unique_word_groups.json"

    # build global universes
    mapping = json.loads(equiv_json.read_text(encoding='utf8'))
    collapsed_universe = sorted(mapping.keys())

    keywords_universe = set()
    groups_universe = set()
    for category in ("priority", "non_priority"):
        cat_dir = root / category
        if not cat_dir.exists():
            continue
        for school in cat_dir.iterdir():
            csv_path = school / "processed_data" / "processed.csv"
            if not csv_path.exists():
                continue
            df = pd.read_csv(csv_path)
            # raw keywords
            freqs = df['keyword_frequencies'].dropna().apply(json.loads)
            for d in freqs:
                keywords_universe.update(d.keys())
            # groups
            groups = df['matched_groups'].dropna().str.split(';').explode()
            groups_universe.update(groups.tolist())

    keywords_universe = sorted(keywords_universe)
    groups_universe = sorted(groups_universe)

    # track maxima and per-school metrics (optional)
    kw_max_by_school   = {}
    grp_max_by_school  = {}
    coll_max_by_school = {}

    for category in ("priority", "non_priority"):
        cat_dir = root / category
        if not cat_dir.exists():
            continue
        for school in cat_dir.iterdir():
            name = f"{category}/{school.name}"
            csv_path = school / "processed_data" / "processed.csv"
            if not csv_path.exists():
                continue
            df = pd.read_csv(csv_path)

            fig_dir = school / "figures"
            fig_dir.mkdir(exist_ok=True)

            # keyword histogram
            out_kw = fig_dir / "keyword_freq.png"
            if args.mode == 'replace' or not out_kw.exists():
                kw_max = keyword_histogram(df, out_kw, name, keywords_universe)
            else:
                # compute max without plotting
                freqs = df['keyword_frequencies'].dropna().apply(json.loads)
                counter = Counter()
                for d in freqs:
                    counter.update(d)
                kw_max = max(counter.values()) if counter else 0
            kw_max_by_school[name] = kw_max

            # group histogram
            out_grp = fig_dir / "group_freq.png"
            if args.mode == 'replace' or not out_grp.exists():
                grp_max = group_histogram(df, out_grp, name, groups_universe)
            else:
                groups = df['matched_groups'].dropna().str.split(';').explode()
                grp_max = int(groups.value_counts().max()) if not groups.empty else 0
            grp_max_by_school[name] = grp_max

            # collapsed histogram
            out_coll = fig_dir / "collapsed_freq.png"
            if args.mode == 'replace' or not out_coll.exists():
                coll_max = collapsed_histogram(df, out_coll, equiv_json, name, collapsed_universe)
            else:
                freqs = df['keyword_frequencies'].dropna().apply(json.loads)
                counter = Counter()
                for d in freqs:
                    for kw, cnt in d.items():
                        canon = next((m for m, grp in mapping.items() if kw in grp), kw)
                        counter[canon] += cnt
                coll_max = max(counter.values()) if counter else 0
            coll_max_by_school[name] = coll_max

            print(f"Saved visuals for {name} (mode={args.mode})")

    # summary
    def top(d):
        if not d:
            return ("n/a", 0)
        return max(d.items(), key=lambda kv: kv[1])

    kw_school,   kw_val   = top(kw_max_by_school)
    grp_school,  grp_val  = top(grp_max_by_school)
    coll_school, coll_val = top(coll_max_by_school)

    print("\n=== VISUALS SUMMARY ===")
    print(f"Highest raw-keyword count:      {kw_val}  ({kw_school})")
    print(f"Highest group-keyword count:    {grp_val}  ({grp_school})")
    print(f"Highest collapsed-keyword count: {coll_val}  ({coll_school})")

if __name__ == "__main__":
    main()