# Hacker Analytics and AI Code Detection System

## 1. Introduction
The **Hacker Analytics and AI Code Detection System** is a modular Python web application built with **Streamlit**, **Selenium**, **BeautifulSoup4**, **Pandas**, **SQLite**, **Plotly**, **Matplotlib**, **Python AST**, and **Scikit-learn**. It integrates three core capabilities into a single interactive dashboard:

1. **Public HackerRank Profile Web Scraping (Selenium + BeautifulSoup4)**
2. **Coding Profile & Performance Analytics (Pandas + Plotly + Matplotlib)**
3. **Source-Code Similarity, AST Structural Inspection & Explainable Heuristic AI-Pattern Analysis**

---

## 2. Problem Statement
Evaluating coding profiles and student/developer source-code submissions often requires switching between disconnected tools: manual profile checking, spreadsheets for performance charts, and separate scripts for comparing source-code submissions. Additionally, automated AI-detection claims often lack transparency and present probabilistic guesses as proof.

This project addresses these challenges by unifying ethical public profile analytics, multi-metric source-code similarity comparison, AST inspection, and transparent non-probabilistic heuristic code pattern analysis in one reproducible dashboard.

---

## 3. Objectives
- Collect publicly accessible HackerRank profile details responsibly using Selenium WebDriver without bypassing CAPTCHAs, logins, or anti-bot protections.
- Store scraped profiles, statistics, source-code AST reports, similarity comparisons, and heuristic pattern results in a structured SQLite database (`data/hackerrank.db`).
- Generate factual, data-backed coding analytics and interactive visualizations strictly from collected or clearly labeled demonstration data.
- Compare Python source-code files using token, TF-IDF cosine, SequenceMatcher, and AST structural metrics.
- Provide explainable heuristic indicators of AI-associated code traits alongside clear limitations and distinctions from normal programming practices.

---

## 4. Main Features
- **7-Page Streamlit Dashboard**: Home, Selenium Web Scraper, Profile Analytics, Coding Performance Analytics, Source-Code Similarity, AI-Associated Code Pattern Analysis, and Analysis History.
- **Resilient Selenium Scraper**: Configurable Chrome/Edge WebDriver, timeouts, explicit waits, clean shutdown, separated CSS selectors, restriction/404 detection, and an offline **Demonstration Sample Data Mode**.
- **Factual Profile & Coding Analytics**: Language distributions, skill verification breakdowns, badge/certificate summaries, multi-profile comparisons, and historical trend tracking.
- **Multi-Metric Source-Code Similarity**: Token similarity, Scikit-learn TF-IDF cosine similarity, `difflib.SequenceMatcher`, AST structural similarity, optional variable normalization, matching snippet extraction, and unified diffs.
- **AST Structural Analysis**: Extracts functions, classes, loops, conditionals, imports, assignments, nesting depth, and approximate cyclomatic complexity while handling syntax errors gracefully.
- **Explainable Heuristic AI Pattern Analysis**: Evaluates naming uniformity, formatting consistency, comment/docstring patterns, structural regularity, and optional peer overlap using non-probabilistic labels (*Few / Some / Several indicators observed*).

---

## 5. Technology Stack
- **Language**: Python 3.11+
- **Web Dashboard**: Streamlit
- **Browser Automation & HTML Parsing**: Selenium, BeautifulSoup4
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly, Matplotlib
- **Database**: SQLite (`sqlite3`)
- **Code Analysis & ML Similarity**: Python `ast`, `tokenize`, `difflib`, `re`, Scikit-learn (`TfidfVectorizer`, `cosine_similarity`)
- **Testing**: `unittest` / `pytest`

---

## 6. Folder Structure
```text
hacker-analytics-ai-detection/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── scraper/
│   ├── __init__.py
│   ├── browser_manager.py
│   ├── hackerrank_scraper.py
│   └── scraper_utils.py
├── analytics/
│   ├── __init__.py
│   ├── profile_analysis.py
│   ├── coding_analytics.py
│   └── statistics.py
├── detection/
│   ├── __init__.py
│   ├── code_preprocessor.py
│   ├── code_similarity.py
│   ├── ast_analysis.py
│   └── ai_pattern_analysis.py
├── database/
│   ├── __init__.py
│   ├── db_manager.py
│   └── schema.py
├── dashboard/
│   ├── __init__.py
│   ├── sidebar.py
│   ├── home.py
│   ├── scraper_page.py
│   ├── profile_page.py
│   ├── coding_page.py
│   ├── similarity_page.py
│   ├── ai_detection_page.py
│   └── history_page.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── validators.py
├── data/
│   └── .gitkeep
├── sample_data/
│   ├── sample_profiles.json
│   ├── sample_code_1.py
│   └── sample_code_2.py
└── tests/
    ├── __init__.py
    ├── test_database.py
    ├── test_analytics.py
    └── test_detection.py
```

---

## 7. Windows Installation & Execution Instructions

Open **PowerShell** inside the project root (`hacker-analytics-ai-detection`):

1. **Create a virtual environment:**
   ```powershell
   python -m venv venv
   ```
2. **Activate the virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. **Upgrade pip and install dependencies:**
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
4. **Run automated tests (optional verification):**
   ```powershell
   python -m pytest -v
   ```
5. **Start the Streamlit dashboard:**
   ```powershell
   python -m streamlit run app.py
   ```
   Open the local URL printed in the terminal (typically `http://localhost:8501`).

---

## 8. Troubleshooting (Windows)
- **Python not recognised**: Reinstall Python 3.11+ from python.org or Microsoft Store and check **"Add Python to PATH"**, then reopen PowerShell.
- **Virtual environment activation error (`ExecutionPolicy`)**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell, then rerun `.\venv\Scripts\Activate.ps1`.
- **Missing dependencies / `ModuleNotFoundError`**: Ensure the virtual environment is active (`(venv)` prefix visible) and run `python -m pip install -r requirements.txt`. Always run Streamlit via `python -m streamlit run app.py` from the project root directory.
- **Selenium browser startup problems**: Ensure Google Chrome or Microsoft Edge is installed and updated. Selenium 4's built-in Selenium Manager automatically fetches a matching driver when online. If offline or blocked by a corporate proxy, use **Demonstration Sample Data Mode** in the scraper page.
- **Database errors**: Delete `data/hackerrank.db` (if corrupted during manual edits) and restart the app; `DatabaseManager` recreates the schema automatically on startup.
- **Streamlit blank page**: Clear browser cache, try incognito mode, or specify another port: `python -m streamlit run app.py --server.port 8502`.
- **Incorrect working directory**: Confirm `Get-Location` ends in `hacker-analytics-ai-detection` before running `app.py` or `pytest`.

---

## 9. Module Explanations

### Selenium Web Scraper (`scraper/`)
- `browser_manager.py` configures headless/headed Chrome (with Edge fallback), page load timeouts, explicit DOM waits, and guaranteed `driver.quit()` cleanup.
- `scraper_utils.py` isolates `HACKERRANK_SELECTORS` and BeautifulSoup parsing logic so frontend markup changes can be updated in one place. It explicitly detects CAPTCHAs, Cloudflare challenges, login walls, and 404 pages, stopping immediately without attempting to bypass protections.
- Missing profile fields are recorded as `NULL` / empty values rather than fabricated.

### Analytics Modules (`analytics/`)
- `profile_analysis.py` converts a profile's languages, skills, badges, certificates, and statistics into Pandas DataFrames and generates insights strictly from collected values.
- `coding_analytics.py` aggregates metrics across profiles and builds interactive Plotly bar, pie, horizontal skill, stacked badge, multi-profile comparison, and historical trend line charts (plus a Matplotlib summary figure).

### Code Similarity & AST Analysis (`detection/`)
- `code_preprocessor.py` cleans comments via Python's `tokenize` module, normalizes whitespace, extracts tokens, and optionally normalizes user identifiers (`VAR_1`, `VAR_2`, ...) while preserving keywords and built-ins.
- `ast_analysis.py` inspects the Python AST for functions, classes, loops, conditionals, imports, assignments, nesting depth, and approximate cyclomatic complexity, handling `SyntaxError` cleanly.
- `code_similarity.py` combines token Jaccard/cosine, TF-IDF cosine, `SequenceMatcher`, and AST structural similarity. **Note:** Similarity scores reflect shared structure or vocabulary and are **not** proof of plagiarism.

### Heuristic AI-Associated Code Pattern Analysis (`detection/ai_pattern_analysis.py`)
Evaluates five transparent indicators:
1. Naming Uniformity
2. Formatting Consistency
3. Explanatory Comment & Docstring Patterns
4. Structural & Template Regularity
5. Cross-Submission Similarity (when peer files are supplied)

Results use descriptive, non-probabilistic labels:
- **Few indicators observed** (`0 – 34.9`)
- **Some indicators observed** (`35.0 – 64.9`)
- **Several indicators observed** (`65.0 – 100`)

### SQLite Database (`database/`)
Automatically initializes `data/hackerrank.db` with 9 normalized tables:
`profiles`, `profile_statistics`, `programming_languages`, `skills`, `achievements`, `scraping_history`, `code_analysis`, `similarity_results`, and `ai_pattern_results`.

---

## 10. Sample Data Instructions
1. Launch the dashboard and navigate to **Selenium Web Scraper**.
2. Open the **Demonstration Sample Data Mode** tab.
3. Load one or all profiles from `sample_data/sample_profiles.json`. Sample profiles are tagged `is_sample = 1` (`[SAMPLE DATA]`) so they never mix silently with live scraped records.
4. On **Source-Code Similarity** or **AI-Associated Code Pattern Analysis**, click **Load Sample Python Files** / **Load Sample Python Code** to test `sample_data/sample_code_1.py` and `sample_data/sample_code_2.py`.

---

## 11. Limitations & Future Enhancements
### Limitations
- Live HackerRank scraping depends on public profile visibility, network availability, and anti-bot protections; HackerRank may serve dynamic or gated responses.
- Code similarity and AST analysis currently target Python (`.py`) source code.
- Heuristic AI-pattern indicators cannot prove authorship and may produce false positives on clean, formatter-styled human code or false negatives on edited AI outputs.

### Future Enhancements
- Multi-language AST/tree-sitter support (Java, C++, JavaScript).
- Batch ZIP upload for classroom-scale similarity clustering.
- Scheduled automated profile snapshot refreshes for longitudinal tracking.
- PDF/HTML executive report export for analyzed profiles and code submissions.

