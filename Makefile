# final_results/Makefile

# -----------------------------------------------------------------------------
# VARIABLES
# -----------------------------------------------------------------------------
PYTHON   := python3
PIP      := pip install
REQ      := requirements.txt
SCHOOLS  := schools

# -----------------------------------------------------------------------------
# PHONY TARGETS
# -----------------------------------------------------------------------------
.PHONY: help install populate-folders \
        web-scrape web-scrape-all \
        metrics process-data relational create-visuals compile-all \
        compile-keywords confirm-schools confirm-all

# -----------------------------------------------------------------------------
# DEFAULT
# -----------------------------------------------------------------------------
help:
	@echo ""
	@echo "Usage: make <target> [mode=<missing|all>] [SCHOOL=<category/school_name>]"
	@echo ""
	@echo "Available targets:"
	@echo "  install            	Install Python dependencies"
	@echo "  populate-folders   	Create subfolders & .gitignore for each school"
	@echo "  web-scrape         	Run web scrapers for schools missing processed_data"
	@echo "  web-scrape-all     	Run web scrapers for ALL schools"
	@echo "  metrics           		Generate metrics.csv overview"
	@echo "  view-metrics       	View current metrics"
	@echo "  process-data       	Process raw JSON into scored processed_data"
	@echo "  relational         	Build relational tables from processed_data"
	@echo "  create-visuals     	Generate per‑school bar charts & figures"
	@echo "  compile-all        	Compile keyword groups & build relational"
	@echo "  confirm-schools    	Confirm data for a specific school (use SCHOOL=…)"
	@echo "  confirm-all        	Confirm data for ALL schools"
	@echo ""

# -----------------------------------------------------------------------------
# INSTALL
# -----------------------------------------------------------------------------
install:
	@echo "Installing Python dependencies…"
	$(PIP) -r $(REQ)

# -----------------------------------------------------------------------------
# POPULATE FOLDERS
# -----------------------------------------------------------------------------
populate-folders:
	@echo "Populating school directories (create folders & .gitignore)…"
	@$(PYTHON) scripts/directory_initialization/create_folders.py
	@$(PYTHON) scripts/directory_initialization/populate_folders.py
	@$(PYTHON) scripts/directory_initialization/add_gitignores.py

# -----------------------------------------------------------------------------
# WEB-SCRAPE (missing only)
# -----------------------------------------------------------------------------
web-scrape:
	@echo "Running web scraper for schools missing processed_data…"
	@$(PYTHON) scripts/run_web_scrape.py --mode missing
	@$(MAKE) metrics

# -----------------------------------------------------------------------------
# WEB-SCRAPE-ALL
# -----------------------------------------------------------------------------
web-scrape-all:
	@echo "Running web scraper for ALL schools…"
	@$(PYTHON) scripts/run_web_scrape.py --mode all
	@$(MAKE) metrics

# -----------------------------------------------------------------------------
# METRICS
# -----------------------------------------------------------------------------
metrics:
	@echo "Generating metrics.csv…"
	@$(PYTHON) scripts/update_metrics.py

# -----------------------------------------------------------------------------
# VIEW-METRICS
# -----------------------------------------------------------------------------
view-metrics:
	@echo "Current metrics:"
	@$(PYTHON) scripts/update_metrics.py --view

# -----------------------------------------------------------------------------
# PROCESS-DATA
# -----------------------------------------------------------------------------
process-data:
	@echo "Processing raw JSON → processed_data…"
	@$(MAKE) compile-keywords
	@$(PYTHON) scripts/process_data.py
	@$(MAKE) clean-raw
	@$(MAKE) metrics

# -----------------------------------------------------------------------------
# CREATE-VISUALS
# -----------------------------------------------------------------------------
create-visuals:
	@echo "Creating per‑school visualizations…"
	@$(PYTHON) scripts/create_visuals.py

# -----------------------------------------------------------------------------
# COMPILE-ALL
# -----------------------------------------------------------------------------
compile-all:
	@echo "Compiling keyword groups & building relational tables…"
	@$(MAKE) compile-keywords
	@$(MAKE) relational

# -----------------------------------------------------------------------------
# COMPILE-KEYWORDS
# -----------------------------------------------------------------------------
compile-keywords:
	@echo "Compiling keyword groups JSON…"
	@$(PYTHON) scripts/compile_keywords.py

# -----------------------------------------------------------------------------
# RELATIONAL
# -----------------------------------------------------------------------------
relational:
	@echo "Building relational tables from processed_data…"
	@$(PYTHON) scripts/relational.py

# -----------------------------------------------------------------------------
# CLEAN-RAW
# -----------------------------------------------------------------------------
clean-raw:
	@echo "Cleaning raw raw JSON files…"
	@$(PYTHON) scripts/clean_raw.py

# -----------------------------------------------------------------------------
# CONFIRM-SCHOOLS
# -----------------------------------------------------------------------------
confirm-schools:
	@if [ -z "$(SCHOOL)" ]; then \
		echo "Error: please pass SCHOOL=<category/school_name>"; \
		exit 1; \
	fi
	@echo "Confirming data for $(SCHOOL)…"
	@$(PYTHON) scripts/confirmation.py --school "$(SCHOOL)"

# -----------------------------------------------------------------------------
# CONFIRM-ALL
# -----------------------------------------------------------------------------
confirm-all:
	@echo "Confirming data for ALL schools…"
	@$(PYTHON) scripts/confirmation.py --mode all
