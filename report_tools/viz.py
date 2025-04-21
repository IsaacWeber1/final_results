import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

def heatmap(main_csv: Path, relations_dir: Path, out_html: Path):
    df_main = pd.read_csv(main_csv)
    # load relations if needed…
    fig = px.imshow([[0]], title="(placeholder)")
    # …build real static figures here
    fig.write_html(out_html)
    print(f"Saved heatmap to {out_html}")

def bar_metrics_per_school(processed_csv: Path, out_png: Path, metrics: dict):
    """
    processed_csv:  the school’s processed_data/<somefile>.csv
    out_png:        where to save the bar chart (e.g. schools/<school>/figures/metrics.png)
    metrics:        a dict mapping metric_name -> a function(df) returning a numeric value
    """
    df = pd.read_csv(processed_csv)
    results = {name: func(df) for name, func in metrics.items()}

    names = list(results.keys())
    values = list(results.values())

    plt.figure(figsize=(6, 4))
    plt.bar(names, values)
    plt.ylabel("Count / Value")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Key Metrics for {processed_csv.parent.name}")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()
