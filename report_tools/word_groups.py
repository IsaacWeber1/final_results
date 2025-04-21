# report_tools/word_groups.py
import json
import re
from collections import Counter
from pathlib import Path
import pandas as pd

KEYWORD_FILE = Path(__file__).parent.parent / "data" / "word_groups" / "current_keyword_groups.json"

def compile_equivalencies(xlsx_path: Path, out_json: Path):
    df = pd.read_excel(xlsx_path, sheet_name=0)
    unique_words = {}
    for col in df.columns:
        for cell in df[col].dropna():
            words = [w.strip() for w in str(cell).split(",") if w.strip()]
            if len(words) > 1:
                unique_words[words[0]] = words
    out_json.write_text(json.dumps(unique_words, indent=4))
    print(f"Wrote equivalencies → {out_json}")

def compile_keywords(xlsx_path: Path, out_json: Path):
    df = pd.read_excel(xlsx_path, sheet_name=0)
    keyword_groups = {}
    for col in df.columns:
        key = col.strip().lower().replace(" ", "_").replace("&", "and")
        items = []
        for cell in df[col].dropna():
            items += [i.strip() for i in str(cell).split(",") if i.strip()]
        keyword_groups[key] = items
    out_json.write_text(json.dumps(keyword_groups, indent=4))
    print(f"Wrote keywords → {out_json}")

def load_keyword_groups():
    with open(KEYWORD_FILE, "r", encoding="utf8") as f:
        return json.load(f)

def extract_group_weight(group_name: str) -> int:
    m = re.search(r"-([0-9]+)$", group_name)
    return int(m.group(1)) if m else 1

def calculate_score_and_matches(title: str, description: str):
    keyword_groups = load_keyword_groups()
    text = f"{title} {description}".lower()
    score = 0.0
    matched = []
    groups = []
    freqs = Counter()

    for group_name, keywords in keyword_groups.items():
        weight = extract_group_weight(group_name)
        hit = False
        for kw in keywords:
            parts = [p.strip().lower() for p in kw.split(",")]
            if any(p in text for p in parts):
                hit = True
                matched.append(kw)
                for p in parts:
                    cnt = text.count(p)
                    if cnt:
                        freqs[p] += cnt
        if hit:
            score += weight
            groups.append(group_name)

    # add 0.5 per occurrence
    for _, cnt in freqs.items():
        score += cnt * 0.5

    return score, list(set(matched)), list(set(groups)), dict(freqs)
