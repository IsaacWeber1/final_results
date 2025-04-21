# final_results/Makefile

# -----------------------------------------------------------------------------
# VARIABLES
# -----------------------------------------------------------------------------
PYTHON := python3
PIP     := pip install
REQ     := requirements.txt
SCHOOLS := schools
# -----------------------------------------------------------------------------
# PHONY TARGETS
# -----------------------------------------------------------------------------
.PHONY: help install populate-folders web-scrape web-scrape-all

# -----------------------------------------------------------------------------
# DEFAULT
# -----------------------------------------------------------------------------
help:
	@echo ""
	@echo "Usage: make <target> [mode=<missing|all>]"
	@echo ""
	@echo "Available targets:"
	@echo "  install            Install Python dependencies"
	@echo "  populate-folders   Create subfolders & .gitignore for each school"
	@echo "  web-scrape         Run web scrapers for schools missing processed_data"
	@echo "  web-scrape-all     Run web scrapers for ALL schools"
	@echo ""

# -----------------------------------------------------------------------------
# INSTALL
# -----------------------------------------------------------------------------
install:
	@echo "Installing Python dependencies..."
	$(PIP) -r $(REQ)

# -----------------------------------------------------------------------------
# POPULATE FOLDERS
# -----------------------------------------------------------------------------
populate-folders:
	@echo "Populating school directories with standard subfolders & .gitignore..."
	@$(PYTHON) scripts/directory_initialization/create_folders.py
	@$(PYTHON) scripts/directory_initialization/populate_folders.py
	@$(PYTHON) scripts/directory_initialization/add_gitignores.py

# -----------------------------------------------------------------------------
# SCRAPE-WEB (missing only)
# -----------------------------------------------------------------------------
web-scrape:
	@echo "Running web scraper for schools missing processed_data..."
	@$(PYTHON) scripts/run_web_scrape.py --mode missing

# -----------------------------------------------------------------------------
# SCRAPE-WEB-ALL
# -----------------------------------------------------------------------------
web-scrape-all:
	@echo "Running web scraper for ALL schools..."
	@$(PYTHON) scripts/run_web_scrape.py --mode all

# -----------------------------------------------------------------------------
# METRICS
# -----------------------------------------------------------------------------
metrics:
	@echo "Running metrics script..."
	@$(PYTHON) scripts/metrics.py

# -----------------------------------------------------------------------------
# PROCESS-DATA
# -----------------------------------------------------------------------------
process-data:
	@echo "Running process data script..."
	@$(PYTHON) scripts/process_data.py

# -----------------------------------------------------------------------------
# RELATIONAL
# -----------------------------------------------------------------------------
relational:
	@echo "Running relational script..."
	@$(PYTHON) scripts/process_data.py --mode relational

# -----------------------------------------------------------------------------
# CREATE-VISUALS
# -----------------------------------------------------------------------------
create-visuals:
	@echo "Running create visuals script..."
	@$(PYTHON) scripts/create_visuals.py

# -----------------------------------------------------------------------------
# COMPILE
# -----------------------------------------------------------------------------
compile:
	@echo "Compiling all current processed data..."
# TO CHAT: ADD SCRIPT(S) FOR COMPILING KEYWORDS
	@$(PYTHON) 