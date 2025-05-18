# scripts/relational.py

import json
from pathlib import Path

import pandas as pd

# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main():
    project_root   = PROJECT_ROOT
    schools_root   = project_root / "schools"
    out_dir        = project_root / "data" / "relational_output"
    out_dir.mkdir(parents=True, exist_ok=True)

    # collectors
    relevance_rows = []
    keyword_rows   = []
    group_rows     = []
    freq_rows      = []

    for category in ("priority", "non_priority"):
        category_dir = schools_root / category
        if not category_dir.is_dir():
            continue

        for school_dir in sorted(category_dir.iterdir()):
            if not school_dir.is_dir():
                continue

            csv_path = school_dir / "processed_data" / "processed.csv"
            if not csv_path.exists():
                continue

            df = pd.read_csv(csv_path)
            school_name = school_dir.name

            for idx, row in df.iterrows():
                # generate a simple course identifier
                course_id = f"{school_name}__{idx}"

                # relevance_score
                relevance_rows.append({
                    "school": school_name,
                    "course_id": course_id,
                    "relevance_score": row.get("relevance_score", None)
                })

                # matched_keywords → explode on ';'
                kws = str(row.get("matched_keywords", "")).split(";")
                for kw in kws:
                    kw = kw.strip()
                    if kw:
                        keyword_rows.append({
                            "school": school_name,
                            "course_id": course_id,
                            "keyword": kw
                        })

                # matched_groups → explode on ';'
                grps = str(row.get("matched_groups", "")).split(";")
                for grp in grps:
                    grp = grp.strip()
                    if grp:
                        group_rows.append({
                            "school": school_name,
                            "course_id": course_id,
                            "group": grp
                        })

                # keyword_frequencies JSON → flatten
                freqs = {}
                try:
                    freqs = json.loads(row.get("keyword_frequencies", "{}"))
                except Exception:
                    pass

                for kw, cnt in freqs.items():
                    freq_rows.append({
                        "school": school_name,
                        "course_id": course_id,
                        "keyword": kw,
                        "count": cnt
                    })

    # write out
    pd.DataFrame(relevance_rows).to_csv(
        out_dir / "relevance_scores.csv", index=False
    )
    pd.DataFrame(keyword_rows).to_csv(
        out_dir / "keyword_matches.csv", index=False
    )
    pd.DataFrame(group_rows).to_csv(
        out_dir / "group_matches.csv", index=False
    )
    pd.DataFrame(freq_rows).to_csv(
        out_dir / "keyword_frequencies.csv", index=False
    )

    print(f"✓ Wrote relational output to {out_dir}")

if __name__ == "__main__":
    main()
