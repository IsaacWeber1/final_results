# scripts/ui.py
import streamlit as st
import subprocess, glob, os, json

st.set_page_config(page_title="H2 Workforce Tools", layout="wide")
st.title("💧 Hydrogen Scraper Toolkit")

# —–––––––––––––––––––––––––
# Part 1: Run any script
# —–––––––––––––––––––––––––
st.subheader("Run a script")
scripts = [os.path.basename(p) for p in glob.glob("scripts/*.py") if p.endswith(".py") and p!='ui.py']
sel = st.selectbox("Select script to run", scripts)
if st.button("▶️ Run"):
    with st.spinner(f"Running {sel}…"):
        proc = subprocess.run(
            ["python3", os.path.join("scripts", sel)],
            capture_output=True, text=True
        )
    st.text_area("Output", proc.stdout + proc.stderr, height=300)

st.markdown("---")

# —–––––––––––––––––––––––––
# Part 2: Inspect raw JSON data
# —–––––––––––––––––––––––––
st.subheader("Browse raw data outputs")
json_paths = sorted(glob.glob("schools/*/*/raw_data/*.json"))
for path in json_paths:
    if st.checkbox(path):
        try:    
            data = json.load(open(path, "r", encoding="utf8"))
            st.json(data)
        except Exception as e:
            st.error(f"Failed to load {path}: {e}")
