# report_tools/tables.py
import pandas as pd
from pathlib import Path

def create_relational_tables(raw_csv: Path, out_dir: Path):
    """
    Read raw CSV, split out any list‑oriented columns into
    separate relational tables, then save everything into out_dir.
    """
    df = pd.read_csv(raw_csv)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Example: if a column holds comma‑separated lists
    for col in df.columns:
        if df[col].dtype == object and df[col].str.contains("[,;]").any():
            relations = []
            for idx, cell in df[col].dropna().items():
                for val in map(str.strip, cell.split("[,;]")):
                    relations.append({"id": idx, col: val})
            rel_df = pd.DataFrame(relations)
            rel_df.to_csv(out_dir / f"{col}_relation.csv", index=False)
            print(f"  – relational table: {col}_relation.csv")

    df.to_csv(out_dir / "main_table.csv", index=False)
    print(f"  – main table: main_table.csv")
