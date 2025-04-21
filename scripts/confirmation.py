# scripts/confirmation.py

import sys
from pathlib import Path

# add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# TODO: ZACH

# Should accept --school (and --mode all) so the Makefile can pass it through