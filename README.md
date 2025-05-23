# Hydrogen Workforce Scraper

This project is a modular, scalable scraping pipeline for identifying hydrogen-related university courses across U.S. academic institutions. Built by a University of Delaware senior design team in collaboration with EPRI, the tool extracts and organizes course catalog data to inform future hydrogen workforce development initiatives.

---

## 🚀 Project Goal

**Mission:** Provide accurate, scalable tracking of university course offerings that relate to hydrogen skills and knowledge.

The system scrapes academic course catalogs (both websites and PDFs), filters for hydrogen-relevant content using a keyword taxonomy, and organizes results into structured datasets. These datasets will feed into EPRI’s interactive tools to help:

- Prospective students find training programs
- Employers locate skill-relevant curricula
- Regional planners identify gaps in workforce preparation

---

## 📊 Project Highlights

- ✅ Scraped over **50 universities**, including **92%** of priority targets with HTML-based catalogs
- 🔁 Config-driven scraping system, re-usable across similar university sites
- 🖱 Supports **JavaScript-heavy sites** (e.g., Modern Campus) using automated button clicking
- 📄 Developed early-stage PDF parsing for non-web catalogs
- ⚙️ Built a full pipeline: scrape → score → confirm → visualize
- 📁 Output includes cleaned CSVs, keyword frequency maps, and per-school metrics

---

## 🗂️ Repository Structure

```graphql
final_results/
├── scraper_module/         # Core scraper framework (Scrapy + Playwright)
├── scripts/                # Utilities for scraping, processing, and cleaning
├── report_tools/           # Keyword matching, scoring, and data tables
├── schools/                # Data per school, organized by priority
├── data/                   # Keyword taxonomies and word group mappings
├── reports/                # Generated outputs (markdown, figures)
├── metrics.csv             # Summary of scrape/confirm status by school
├── Makefile                # One-click commands for full pipeline
```

---

## 🔧 How It Works

1. **Set up the environment**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the scraper**
   - For schools missing processed data:
     ```bash
     make web-scrape
     ```
   - For all schools (force rerun):
     ```bash
     make web-scrape-all
     ```

3. **Process the scraped data**
   ```bash
   make process-data
   ```

4. **Generate relational tables**
   ```bash
   make relational
   ```

5. **View status overview**
   ```bash
   cat metrics.csv
   ```

---

## 📘 Keyword Scoring System

- Uses a structured spreadsheet (`phrases_spreadsheet.xlsx`) to define keyword groups
- Scores courses based on matches to hydrogen-related concepts
- Supports weighting by group importance and keyword frequency
- Generates enriched metadata: matched phrases, relevance scores, frequencies

---

## 🧪 Confirmation Pipeline

To ensure accuracy, courses can be verified via:
- Independent scraper (e.g., simpler HTML scraper)
- PDF data extraction
- Manual spot checks
- Discrepancy tracking logic (in development)

---

## 🧰 Requirements

- Python 3.10+
- Scrapy, Playwright, pandas, matplotlib
- `make` (for command-line automation)

To enable scraping of JavaScript content, Playwright must be installed with Chromium:
```bash
playwright install
```

---

## 🔍 Known Issues

- Some PDF catalogs are inconsistently formatted — confirmation logic is evolving
- GUI for user-facing operation is a planned stretch goal
- ML text classification and job posting scraping are future phases

---

## 📦 Example Output

- `processed.csv` files per school: scored and cleaned course data
- `metrics.csv`: global overview of scraping/completion progress
- (Planned) Cluster visualizations for keyword similarity
- (Planned) GUI for progress tracking and scraper control

---

## 📈 Metrics Snapshot (Sprint 4)

- **92%** of HTML-based priority schools scraped
- **>30** total schools scraped
- Full multi-school scraping pipeline executable in a single command
- PDF confirmation logic in testing

---

## 🙋 Who Is This For?

- **Researchers** building tools for hydrogen workforce development
- **Policy stakeholders** identifying training gaps
- **Students and educators** exploring course offerings in energy-related fields

---

## 📄 License

MIT License — see `LICENSE` file for details.

---

## ✍️ Authors

University of Delaware Senior Design Team — Fall 2024  
Client Partner: EPRI  
Supervisors: Ashley Roberts, Jeremy Keffer  
Team Lead: Isaac Weber  
Team Members: Alexander Peluso, James Lloyd, Kerry Ferguson, Logan Levine, Thomas Pelosi, Zachary Pruett
