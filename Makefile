# Makefile

# -----------------------------------------------------------------------------
# VARIABLES
# -----------------------------------------------------------------------------
PYTHON       := python3
PIP          := pip install
REQ          := requirements.txt
SCHOOLS      := schools

# Make “help” the default if no target is given
.DEFAULT_GOAL := help

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
        report-images \
        scripts run-script run-% ui list-json

# auto-detect all scripts
SCRIPTS := $(patsubst scripts/%.py,%, $(wildcard scripts/*.py))

# -----------------------------------------------------------------------------
# USAGE HELP
# -----------------------------------------------------------------------------
help:
	@echo ""
	@echo " Usage: make <target> [OPTIONS]"
	@echo ""
	@echo " Targets:"
	@echo "   install               install Python deps"
	@echo "   web-scrape            scrape missing processed_data"
	@echo "   web-scrape-all        scrape ALL"
	@echo "   pdf-scrape            pdf-scrape missing"
	@echo "   pdf-scrape-all        pdf-scrape ALL"
	@echo "   metrics               generate metrics.csv"
	@echo "   view-metrics          print metrics"
	@echo "   process-data          raw → processed (clears raw afterwards)"
	@echo "   relational            build relational tables"
	@echo "   add-visuals           create missing visuals"
	@echo "   replace-visuals       regenerate all visuals"
	@echo "   clear-visuals         wipe visuals dirs"
	@echo "   compile-all           compile keywords + relational"
	@echo "   confirm-schools       confirm one school (SCHOOL=…)"
	@echo "   confirm-all           confirm all schools"
	@echo "   report-images         build markdown + meta figures"
	@echo "   scripts               list available scripts"
	@echo "   run-script            run a script by name (name=…)"
	@echo "   run-<script>          shorthand to run scripts/<script>.py"
	@echo "   list-json             list raw_data JSON files"
	@echo "   ui                    launch Streamlit UI"
	@echo ""

# -----------------------------------------------------------------------------
# INSTALL
# -----------------------------------------------------------------------------
install:
	@echo "⚙️  Installing dependencies…"
	@$(PIP) -r $(REQ)

# -----------------------------------------------------------------------------
# WEB & PDF SCRAPE
# -----------------------------------------------------------------------------
web-scrape:
	@echo "🌐 scraping missing..."
	@$(PYTHON) scripts/run_web_scrape.py --mode missing
	@$(MAKE) metrics

web-scrape-all:
	@echo "🌐 scraping all..."
	@$(PYTHON) scripts/run_web_scrape.py --mode all
	@$(MAKE) metrics

pdf-scrape:
	@echo "📄 pdf-scraping missing..."
	@$(PYTHON) scripts/run_pdf_scrape.py --mode missing
	@$(MAKE) metrics

pdf-scrape-all:
	@echo "📄 pdf-scraping all..."
	@$(PYTHON) scripts/run_pdf_scrape.py --mode all
	@$(MAKE) metrics

# -----------------------------------------------------------------------------
# METRICS
# -----------------------------------------------------------------------------
metrics:
	@echo "📊 generating metrics.csv"
	@$(PYTHON) scripts/update_metrics.py

view-metrics:
	@echo "📊 current metrics:"
	@$(PYTHON) scripts/update_metrics.py --view

# -----------------------------------------------------------------------------
# DATA PIPELINE
# -----------------------------------------------------------------------------
process-data:
	@echo "🔄 processing data…"
	@$(MAKE) compile-keywords
	@$(PYTHON) scripts/process_data.py
	@$(MAKE) clear-raw
	@$(MAKE) metrics

compile-keywords:
	@echo "🗂️  compiling keyword groups…"
	@$(PYTHON) scripts/compile_keywords.py

relational:
	@echo "🔗 building relational tables…"
	@$(PYTHON) scripts/relational.py

clear-raw:
	@echo "🧹 clearing raw JSON…"
	@$(PYTHON) scripts/clear.py --mode raw

clear-visuals:
	@echo "🧹 clearing visuals…"
	@$(PYTHON) scripts/clear.py --mode visuals

add-visuals:
	@echo "➕ adding missing visuals…"
	@$(PYTHON) scripts/create_visuals.py --mode add

replace-visuals:
	@echo "♻️  regenerating visuals…"
	@$(PYTHON) scripts/create_visuals.py --mode replace

compile-all: compile-keywords relational

confirm-schools:
	@if [ -z "$(SCHOOL)" ]; then \
		echo "❗ specify SCHOOL=<category/school_name>"; exit 1; \
	fi
	@echo "✅ confirming $(SCHOOL)…"
	@$(PYTHON) scripts/confirmation.py --school "$(SCHOOL)"

confirm-all:
	@echo "✅ confirming all schools…"
	@$(PYTHON) scripts/confirmation.py --mode all

report-images:
	@echo "🖼️  building report images…"
	@$(PYTHON) scripts/compile_md_images.py
	@$(PYTHON) scripts/report_visuals.py

# -----------------------------------------------------------------------------
# SCRIPT RUNNERS
# -----------------------------------------------------------------------------
scripts:
	@echo "🛠️  Available scripts:"
	@printf "  %-20s %s\n" $(SCRIPTS) " "

run-script:
	@if [ -z "$(name)" ]; then \
	  echo "❗ Usage: make run-script name=<script>"; exit 1; \
	fi
	@echo "▶️  scripts/$(name).py"
	@$(PYTHON) scripts/$(name).py

# shorthand: make run-foo → scripts/foo.py
run-%:
	@echo "▶️  scripts/$*.py"
	@$(PYTHON) scripts/$*.py

list-json:
	@echo "📂 raw JSON files:"
	@find $(SCHOOLS) -type f -path "*/raw_data/*.json" | sed 's/^/  /'

# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------
ui:
	@echo "🚀 launching UI at http://localhost:8501"
	streamlit run scripts/ui.py
