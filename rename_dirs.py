#!/usr/bin/env python3
import sys
from pathlib import Path

def rename_screenshots_to_figures(root: Path):
    for screenshots_dir in root.joinpath("schools").rglob("screenshots"):
        if screenshots_dir.is_dir():
            target = screenshots_dir.parent / "figures"
            if target.exists():
                print(f"SKIP: {screenshots_dir} → target already exists")
            else:
                screenshots_dir.rename(target)
                print(f"RENAMED: {screenshots_dir} → {target}")

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    rename_screenshots_to_figures(project_root)
