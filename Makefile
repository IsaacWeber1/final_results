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
.PHONY: help install populate-folders scrape-web scrape-web-all

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
	@echo "  scrape-web         Run web scrapers for schools missing processed_data"
	@echo "  scrape-web-all     Run web scrapers for ALL schools"
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
scrape-web:
	@echo "Running web scraper for schools missing processed_data..."
	@$(PYTHON) scripts/scraping/run_web_scrape.py --mode missing

# -----------------------------------------------------------------------------
# SCRAPE-WEB-ALL
# -----------------------------------------------------------------------------
scrape-web-all:
	@echo "Running web scraper for ALL schools..."
	@$(PYTHON) scripts/scraping/run_web_scrape.py --mode all
