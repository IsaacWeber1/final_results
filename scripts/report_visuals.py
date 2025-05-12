# scripts/report_visuals.py

import json
from pathlib import Path

import pandas as pd

# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

from report_tools.viz import heatmap_keyword_frequencies, heatmap_group_matches

# e.g.:
heatmap_keyword_frequencies(
    relations_dir=Path("data/relational_output"),
    out_html=Path("reports/keyword_heatmap.png")
)

heatmap_group_matches(
    relations_dir=Path("data/relational_output"),
    out_html=Path("reports/group_heatmap.png")
)
