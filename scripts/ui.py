# scripts/ui.py
import streamlit as st
import subprocess, glob, os, json

# Page config
st.set_page_config(page_title="H2 Toolkit", layout="wide")
st.title("💧 Hydrogen Scraper Toolkit")

# Sidebar for controls
st.sidebar.header("▶️ Run a Script")
# fetch and filter scripts
all_scripts = sorted(p for p in os.listdir("scripts") if p.endswith(".py") and p != "ui.py")
filter_txt = st.sidebar.text_input("Filter", "")
scripts = [s for s in all_scripts if filter_txt.lower() in s.lower()]
sel = st.sidebar.selectbox("Script", scripts)
args = st.sidebar.text_input("Args (space-separated)")
if st.sidebar.button("Run Script"):
    cmd = ["python3", os.path.join("scripts", sel)] + args.split()
    with st.spinner("Running..."):
        proc = subprocess.run(cmd, capture_output=True, text=True)
    st.subheader(f"Output: {sel}")
    st.code(proc.stdout + proc.stderr)

st.sidebar.markdown("---")
st.sidebar.header("📂 Browse Raw JSON")
json_paths = sorted(glob.glob("schools/*/*/raw_data/*.json"))
jsel = st.sidebar.selectbox("JSON File", [""] + json_paths)
if jsel:
    try:
        data = json.load(open(jsel, "r"))
        st.subheader(os.path.basename(jsel))
        st.json(data)
        st.download_button(
            "Download JSON",
            data=json.dumps(data, indent=2),
            file_name=os.path.basename(jsel),
            mime="application/json"
        )
    except Exception as e:
        st.error(f"Failed to load: {e}")

# Main area tips
st.info("Use the sidebar to run any script or inspect raw JSON outputs.")
