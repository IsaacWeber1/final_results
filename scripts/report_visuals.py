# scripts/report_visuals.py

import json
from pathlib import Path
import sys

import pandas as pd

# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from report_tools.viz import heatmap_keyword_frequencies, heatmap_group_matches

# e.g.:
heatmap_keyword_frequencies(
    relations_dir=Path("data/relational_output"),
    out_png=Path("reports/keyword_heatmap.png")
)

heatmap_group_matches(
    relations_dir=Path("data/relational_output"),
    out_png=Path("reports/group_heatmap.png")
)
