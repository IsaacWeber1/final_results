import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

def heatmap_keyword_frequencies(relations_dir: Path, out_png: Path):
    """
    Build a school × keyword heatmap of raw counts from
    data/relational_output/keyword_frequencies.csv and save as an interactive HTML.
    """
    freq_csv = relations_dir / "keyword_frequencies.csv"
    if not freq_csv.exists():
        raise FileNotFoundError(f"{freq_csv} not found")

    df = pd.read_csv(freq_csv)
    # pivot into matrix: schools on rows, keywords on columns
    pivot = (
        df
        .pivot_table(index="school", columns="keyword", values="count", aggfunc="sum", fill_value=0)
    )

    fig = px.imshow(
        pivot.values,
        x=pivot.columns,
        y=pivot.index,
        labels={"x": "Keyword", "y": "School", "color": "Count"},
        aspect="auto",
        title="Keyword Frequency Heatmap"
    )
    fig.update_xaxes(side="bottom")
    fig.write_image(file=out_png, format="png", scale=1.0)
    print(f"Saved keyword‐frequency heatmap to {out_png}")


def heatmap_group_matches(relations_dir: Path, out_png: Path):
    """
    Build a school × group heatmap of occurrence counts from
    data/relational_output/group_matches.csv and save as an interactive HTML.
    """
    grp_csv = relations_dir / "group_matches.csv"
    if not grp_csv.exists():
        raise FileNotFoundError(f"{grp_csv} not found")

    df = pd.read_csv(grp_csv)
    # count one row per course × group, so group by school+group
    counts = df.groupby(["school", "group"]).size().reset_index(name="count")
    pivot = counts.pivot(index="school", columns="group", values="count").fillna(0)

    fig = px.imshow(
        pivot.values,
        x=pivot.columns,
        y=pivot.index,
        labels={"x": "Group", "y": "School", "color": "Count"},
        aspect="auto",
        title="Keyword‐Group Occurrence Heatmap"
    )
    fig.update_xaxes(side="bottom")
    fig.write_image(file=out_png, format="png", scale=1.0)
    print(f"Saved group‐match heatmap to {out_png}")
