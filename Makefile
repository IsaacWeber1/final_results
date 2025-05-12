# Makefile

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
.PHONY: help install \
        web-scrape web-scrape-all \
		pdf-scrape pdf-scrape-all \
		metrics view-metrics \
        process-data relational clear-raw \
		add-visuals replace-visuals clear-visuals \
        compile-all compile-keywords confirm-schools confirm-all \
		report-images

# -----------------------------------------------------------------------------
# DEFAULT
# -----------------------------------------------------------------------------
help:
	@echo ""
	@echo "Usage: make <target> [mode=<missing|all>] [SCHOOL=<category/school_name>]"
	@echo ""
	@echo "Available targets:"
	@echo ""
	@echo "	install                         Install Python dependencies"
	@echo "	web-scrape                      Run web scrapers for schools missing processed_data"
	@echo "	web-scrape-all                  Run web scrapers for ALL schools"
	@echo "	metrics                         Generate metrics.csv overview"
	@echo "	view-metrics                    View current metrics"
	@echo "	process-data                    Process raw JSON into scored processed_data"
	@echo "	relational                      Build relational tables from processed_data"
	@echo "	add-visuals                     Generate missing visuals (skip existing)"
	@echo "	replace-visuals                 Regenerate all visuals (overwrite existing)"
	@echo "	compile-all                     Compile keyword groups & build relational"
	@echo "	confirm-schools                 Confirm data for a specific school (use SCHOOL=…)"
	@echo "	confirm-all                     Confirm data for ALL schools"
	@echo ""

# -----------------------------------------------------------------------------
# INSTALL
# -----------------------------------------------------------------------------
install:
	@echo "Installing Python dependencies…"
	$(PIP) -r $(REQ)

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
# PDF-SCRAPE (missing only)
# -----------------------------------------------------------------------------
pdf-scrape:
	@echo "Running PDF scraper for schools missing processed_data…"
	@$(PYTHON) scripts/run_pdf_scrape.py --mode missing
	@$(MAKE) metrics

# -----------------------------------------------------------------------------
# PDF-SCRAPE-ALL
# -----------------------------------------------------------------------------
pdf-scrape-all:
	@echo "Running PDF scraper for ALL schools…"
	@$(PYTHON) scripts/run_pdf_scrape.py --mode all
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
	@$(MAKE) clear-raw
	@$(MAKE) metrics

# -----------------------------------------------------------------------------
# ADD-VISUALS
# -----------------------------------------------------------------------------
add-visuals:
	@echo "Adding any missing visuals (skip existing)…"
	@$(PYTHON) scripts/create_visuals.py --mode add

# -----------------------------------------------------------------------------
# REPLACE-VISUALS
# -----------------------------------------------------------------------------
replace-visuals:
	@echo "Regenerating all visuals (overwrite existing)…"
	@$(PYTHON) scripts/create_visuals.py --mode replace

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
# CLEAR-RAW
# -----------------------------------------------------------------------------
clear-raw:
	@echo "Cleaning raw raw JSON files…"
	@$(PYTHON) scripts/clear.py --mode raw

# -----------------------------------------------------------------------------
# CLEAR-VISUALS
# -----------------------------------------------------------------------------
make clear-visuals:
	@echo "Clearing all school figure directories…"
	python scripts/clear.py --mode visuals

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

# -----------------------------------------------------------------------------
# REPORT-IMAGES
# -----------------------------------------------------------------------------
report-images:
	@echo "Creating report images markdown…"
	@$(PYTHON) scripts/compile_md_images.py