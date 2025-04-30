# scripts/compile_md_images.py

import os
import sys
from pathlib import Path

# add project root to sys.path if you ever need imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MD_DIR = PROJECT_ROOT / "reports" / "figures"

def main():
    # ensure output folder exists
    MD_DIR.mkdir(parents=True, exist_ok=True)

    keyword_figures = []
    group_figures   = []
    collapsed_figures = []

    # scan every school
    for category in ("priority", "non_priority"):
        cat_dir = PROJECT_ROOT / "schools" / category
        if not cat_dir.is_dir():
            continue
        for school in sorted(cat_dir.iterdir()):
            if not school.is_dir():
                continue
            fig_dir = school / "figures"
            # define each expected file
            kw = fig_dir / "keyword_freq.png"
            gp = fig_dir / "group_freq.png"
            cl = fig_dir / "collapsed_freq.png"

            if kw.exists():
                keyword_figures.append(os.path.relpath(kw, start=MD_DIR))
            else:
                print(f"⚠️  {school.name} missing {kw.name}")

            if gp.exists():
                group_figures.append(os.path.relpath(gp, start=MD_DIR))
            else:
                print(f"⚠️  {school.name} missing {gp.name}")

            if cl.exists():
                collapsed_figures.append(os.path.relpath(cl, start=MD_DIR))
            else:
                print(f"⚠️  {school.name} missing {cl.name}")

    # helper to write a list of img tags to a markdown file
    def write_md(filename: str, rel_paths: list[str]):
        out = MD_DIR / filename
        with open(out, "w", encoding="utf-8") as f:
            for src in rel_paths:
                f.write(f'<img src="{src}" />\n')
        print(f"✓ Wrote {out.relative_to(PROJECT_ROOT)}")

    # emit three separate markdowns
    write_md("keywords.md", keyword_figures)
    write_md("groups.md",   group_figures)
    write_md("collapsed.md", collapsed_figures)

if __name__ == "__main__":
    main()
