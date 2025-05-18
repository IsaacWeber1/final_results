# scripts/report_visuals.py

import json
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from report_tools.viz import heatmap_keyword_frequencies, heatmap_group_matches

heatmap_keyword_frequencies(
    relations_dir=Path("data/relational_output"),
    out_png=Path("reports/keyword_heatmap.png"),
    y_max=200
)

heatmap_group_matches(
    relations_dir=Path("data/relational_output"),
    out_png=Path("reports/group_heatmap.png"),
    y_max=200
)
