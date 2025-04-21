import os
import glob
import pandas as pd

FILES = [
    "*.py",
    "*/*.py",
    "*/*/*.py",
    "*/*/*/*.py",
    "Makefile",
    "*/*/*.xlsx"
]

if __name__ == "__main__":
    if os.path.exists("prompt.txt"):
        os.remove("prompt.txt")
    prompt = ""
    for file in FILES:
        for f in glob.glob(file):
            if f.endswith(".xlsx"):
                prompt += "READING FILE: " + f"{f}" + "\n\n"
                df = pd.read_excel(f, sheet_name=0)
                prompt += df.to_string() + "\n\n"
            else:
                with open(f, "r") as f:
                    prompt += "READING FILE: " + f"{f}" + "\n\n"
                    prompt += f.read() + "\n\n"
    
    with open("prompt.txt", "w") as f:
        f.write(prompt)