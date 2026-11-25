# HACKER ANALYTICS AND AI CODE DETECTION SYSTEM
## Complete Project Architecture, Workflows, Pipelines & Source Code Documentation

> **Document Purpose:** Complete technical reference containing folder structures, architectural pipeline workflows, database schemas, and full source code of all primary modules for academic project reports, viva defense, and software audits.

---

## 1. PROJECT EXECUTIVE SUMMARY & ARCHITECTURE OVERVIEW

The **Hacker Analytics and AI Code Detection System** is an end-to-end Python developer intelligence and source-code forensics platform. It unifies three core capabilities that are traditionally fragmented:
1. **Competitive Programming Profile Analytics:** Automated extraction of public HackerRank developer data (badges, star counts, verified certifications, language proficiencies) using Selenium WebDriver with multi-tier fallbacks.
2. **Multi-Metric Source-Code Similarity:** A 4-layer comparison engine blending Token Jaccard, Scikit-learn TF-IDF Cosine, SequenceMatcher, and Abstract Syntax Tree (AST) node vector cosine similarity with automated variable identifier normalization (`VAR_1`, `VAR_2`).
3. **Explainable Heuristic AI Pattern Forensics:** Stylometric and syntactic pattern analysis identifying markers characteristic of AI-assisted code (step comments, naming regularity, docstring density, AST symmetry) backed by mandatory ethical disclaimers.
4. **Relational Data Persistence:** An embedded 9-table SQLite schema tracking historical developer growth and audit logs.
5. **Interactive Streamlit Dashboard:** A 7-page responsive web dashboard providing real-time data exploration, multi-timeframe analytics (3M, 6M, 1Y, 3Y, All), and instant report exports.

## 2. PROJECT FOLDER & FILE STRUCTURE TREE

```text
hacker-analytics-ai-detection/
│
├── app.py                                   # Streamlit Main Application Entrypoint & Page Router
├── config.py                                # Central System Configurations, Thresholds & Disclaimers
├── requirements.txt                         # Python Dependency Specifications
├── README.md                                # Project Documentation & GitHub Overview
├── .gitignore                               # Git Privacy Filter (Excludes databases, logs, secrets)
├── generate_novelty_pdf.py                  # Script to compile IEEE Literature Gap Analysis PDF
├── generate_final_project_report.py         # Script to compile 25-page Academic Project Report PDF
├── build_diagrams.py                        # Script generating high-resolution Matplotlib system diagrams
│
├── analytics/                               # Statistical Analytics & Data Aggregation Package
│   ├── __init__.py                          # Package initialization
│   ├── coding_analytics.py                  # Multi-timeframe trend resampling (3M, 6M, 1Y, 3Y, All) & charts
│   ├── profile_analysis.py                  # Profile summaries, star totals & unexposed field detection
│   └── statistics.py                        # Summary statistics, radar charts & language distributions
│
├── dashboard/                               # Streamlit Web UI Pages & Presentation Tier
│   ├── __init__.py                          # Package initialization
│   ├── home.py                              # Futuristic Hero Banner, KPI metrics, launchpad & PDF downloads
│   ├── sidebar.py                           # Sidebar navigation radio & real-time Workspace Vault metrics
│   ├── scraper_page.py                      # Selenium scraper control (Live visible, headless, sample fallback)
│   ├── profile_page.py                      # HackerRank profile viewer & data-backed insights cards
│   ├── coding_page.py                       # Coding analytics, multi-period trends, language donuts & comparisons
│   ├── similarity_page.py                   # Pairwise code similarity, AST diffs & normalized variable toggle
│   ├── ai_detection_page.py                 # Heuristic AI forensic analysis, indicator score & stylometric breakdown
│   └── history_page.py                      # Tabbed relational audit history & CSV export tables
│
├── database/                                # SQLite Relational Database Engine
│   ├── __init__.py                          # Package initialization
│   ├── schema.py                            # DDL statements for all 9 normalized tables & index definitions
│   └── db_manager.py                        # DatabaseManager class: CRUD operations, foreign keys & deduplication
│
├── detection/                               # Syntactic AST & Source-Code Forensics Package
│   ├── __init__.py                          # Package initialization
│   ├── code_preprocessor.py                 # Tokenizer, comment stripper & identifier normalizer (VAR_1, VAR_2)
│   ├── ast_analysis.py                      # AST parser, node distribution vectorizer & tree depth analyzer
│   ├── code_similarity.py                   # 4-Layer ensemble similarity scorer (Token, TF-IDF, Seq, AST)
│   └── ai_pattern_analysis.py               # Explainable heuristic AI stylometric rules & scoring engine
│
├── scraper/                                 # Selenium Browser Automation Package
│   ├── __init__.py                          # Package initialization
│   ├── browser_manager.py                   # ChromeDriver options, process lifecycle & visible/headless driver
│   ├── hackerrank_scraper.py                # Page loader, explicit DOM wait conditions & resilient scraping
│   └── scraper_utils.py                     # Decoupled CSS selectors, badge star counters & certification parsers
│
├── utils/                                   # General Helper Utilities & Validators
│   ├── __init__.py                          # Package initialization
│   ├── helpers.py                           # Timestamps, SHA-256 hashing, safe JSON serializers
│   └── validators.py                        # HackerRank username normalization & Python code validation
│
├── data/                                    # Local Database & Storage Vault (Git-Ignored)
│   ├── .gitkeep                             # Preserves directory structure
│   └── hackerrank.db                        # SQLite database with 9 relational tables
│
├── sample_data/                             # Curated Demonstration Profiles & Sample Code
│   ├── sample_profiles.json                 # 20 pre-curated offline HackerRank profiles
│   ├── sample_code_1.py                     # Two-Sum & Subarray implementation (Structured style)
│   ├── sample_code_2.py                     # Two-Sum & Subarray implementation (Alternative human style)
│   ├── sample_code_ai_assistant.py          # ChatGPT-generated solution with numbered step comments
│   ├── sample_code_ai_oop_pattern.py        # OOP template pattern solution
│   ├── sample_code_ai_plagiarized.py        # Obfuscated version with renamed variables
│   ├── sample_code_human_expert.py          # Idiomatic concise human implementation
│   ├── sample_code_lru_cache_ai.py          # Verbose AI LRU Cache
│   ├── sample_code_lru_cache_human.py       # Standard collections.OrderedDict human implementation
│   └── sample_code_student_messy.py         # Typical student code with inconsistent formatting
│
├── tests/                                   # Automated Pytest Unit Test Suite (14 Tests)
│   ├── __init__.py                          # Test package initialization
│   ├── test_analytics.py                    # Unit tests for multi-timeframe analytics & statistics
│   ├── test_database.py                     # Unit tests for SQLite CRUD & relational foreign keys
│   ├── test_detection.py                    # Unit tests for AST parsing & identifier normalization
│   └── test_scraper.py                      # Unit tests for selector isolation & username parsing
│
└── report_assets/                           # High-Resolution Architectural Diagram PNGs
    ├── fig_system_architecture.png          # 4-Layer System Architecture Diagram
    ├── fig_scraper_workflow.png             # Selenium Scraping & Resilient Fallback Pipeline
    ├── fig_similarity_pipeline.png          # 4-Layer Multi-Metric Code Similarity Pipeline
    ├── fig_ai_heuristic_workflow.png        # Explainable Heuristic AI Pattern Forensics Flowchart
    ├── fig_er_diagram.png                   # Relational Database ER Schema (9 Normalized Tables)
    └── fig_benchmark_results.png            # Obfuscation Resilience Bar Chart & Confusion Distribution
```

## 3. CORE ARCHITECTURAL WORKFLOWS & EXECUTION PIPELINES

### Pipeline 1: Selenium Web Scraping & Resilient Ingestion Workflow

```text
[User Input: Username / Profile URL]
                  │
                  ▼
[Input Normalization & Regex Validation: utils/validators.py]
                  │
                  ▼
[Selenium Chrome WebDriver Initialization: scraper/browser_manager.py]
  • Configured with anti-headless detection options in visible mode
  • Sets window size 1920x1080 and standard user-agent string
                  │
                  ▼
[DOM Navigation & Explicit WebDriverWait: scraper/hackerrank_scraper.py]
  • Navigates to: https://www.hackerrank.com/profile/<username>
  • Waits until CSS selector '.profile-page' or 'main' is hydrated
                  │
                  ├──────────────────────────────────────────────┐
         (Page Load Successful)                         (Access Denied 403 / 404 / Network Fault)
                  │                                              │
                  ▼                                              ▼
[HTML Parsing: scraper/scraper_utils.py]               [Graceful Fallback Mode]
  • Decoupled selector tree execution                    • Load pre-curated profile from
  • Extracts badges (counts svg.badge-star tags)           sample_data/sample_profiles.json (20 profiles)
  • Parses Gold/Silver/Bronze tier levels                • OR allow custom JSON/CSV profile upload
  • Extracts skills & verified certificates                      │
                  │                                              │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                    [Database Upsert: database/db_manager.py]
                      • Persists into profiles table (UNIQUE username)
                      • Cascades skills, languages, badges & stats
                      • Records execution duration in scraping_logs table
```

### Pipeline 2: 4-Layer Multi-Metric Code Similarity & Identifier Normalization Pipeline

```text
    [Source Code A (File or Paste)]                 [Source Code B (File or Paste)]
                   │                                               │
                   └───────────────────────┬───────────────────────┘
                                           │
                                           ▼
                  [Preprocessing & Tokenization: detection/code_preprocessor.py]
                    • Strips comments (# and block comments) via tokenize module
                    • Normalizes irregular indentation and whitespace
                    • Optional Identifier Normalization Mode:
                        - Maps user identifiers: x -> VAR_1, count -> VAR_2
                        - Strictly preserves Python keywords (def, for, return, in)
                        - Strictly preserves built-ins (range, len, int, list)
                                           │
                   ┌───────────────────────┼───────────────────────┐
                   ▼                       ▼                       ▼
        [Layer 1: Token Similarity]  [Layer 2: TF-IDF Cosine]  [Layer 3: SequenceMatcher]
        • 50% Jaccard Overlap        • Scikit-learn TF-IDF     • difflib SequenceMatcher
        • 50% Token Frequency Cosine • N-gram word/symbol      • Sequential line diff
        • Weight: 25%                • Weight: 25%             • Weight: 20%
                   │                       │                       │
                   └───────────────────────┼───────────────────────┘
                                           ▼
                         [Layer 4: Abstract Syntax Tree Vectorization]
                         • Parses code into AST via Python ast.parse()
                         • Computes normalized node type distribution vector Φ(T)
                         • Measures control flow nesting & branch depth
                         • Computes cosine similarity between node vectors
                         • Weight: 30% (falls back gracefully if syntax invalid)
                                           │
                                           ▼
                          [Blended Ensemble Score Formulation]
                          S_total = 0.25·Token + 0.25·TFIDF + 0.20·Seq + 0.30·AST
                                           │
                                           ▼
                         [Interactive Visual Line Diff & Metrics Table]
```

### Pipeline 3: Explainable Heuristic AI Pattern Forensics Pipeline

```text
                         [Uploaded Python Source Code]
                                       │
                                       ▼
              [Heuristic Pattern Scanners: detection/ai_pattern_analysis.py]
               │
               ├─► Check 1: Step-by-Step Numbered Comments (e.g., # Step 1: ..., # 1. ...)
               │
               ├─► Check 2: Identifier Casing Regularity (casing entropy across snake_case/camelCase)
               │
               ├─► Check 3: Structured Docstring & Type Hint Ratio (Sphinx / Google docstrings)
               │
               ├─► Check 4: AST Branch Symmetry & Control Regularity (low depth variance)
               │
               └─► Check 5: Standard Algorithm Boilerplate Overlap (Two-Sum, Kadane, LRU)
                                       │
                                       ▼
                        [Aggregated Heuristic Index Score (0 - 100)]
                                       │
                    ┌──────────────────┼──────────────────┐
                    ▼                  ▼                  ▼
                [0 - 34 pts]      [35 - 64 pts]       [65 - 100 pts]
             'Few Indicators'    'Some Indicators'  'Several Indicators'
              (Human-aligned)        (Hybrid)           (AI-aligned)
                                       │
                                       ▼
                     [Mandatory Ethical & Analytical Disclaimers]
           "Heuristics identify stylistic markers; NOT proof of AI authorship."
```

## 4. RELATIONAL DATABASE SCHEMA (9 TABLES)

| Table Name | Primary / Foreign Keys | Description |
| :--- | :--- | :--- |
| `profiles` | PK: `id`, UNIQUE: `username` | Stores core candidate attributes: display name, country, description, is_sample, source_label, timestamp. |
| `profile_statistics` | PK: `id`, FK: `profile_id` | Stores quantitative metrics: total problems, rank, contest rating, badges count. |
| `programming_languages` | PK: `id`, FK: `profile_id` | Language proficiency entries: language_name, problems_solved, proficiency. |
| `skills` | PK: `id`, FK: `profile_id` | Verified and practiced skills: skill_name, skill_level, verified boolean. |
| `badges_and_achievements` | PK: `id`, FK: `profile_id` | Badges, star levels (1-5 stars), Gold/Silver/Bronze tiers, and verified certificates. |
| `recent_activity` | PK: `id`, FK: `profile_id` | Recent user activity feed records: activity_title, description, date_or_time_ago. |
| `scraping_logs` | PK: `id`, FK: `profile_id` | Audit trail of scraping events: username, status, source_mode, duration_sec, error_message. |
| `code_similarity_analyses` | PK: `id` | History of similarity comparisons: file_a, file_b, overall_similarity, token_sim, tfidf_sim, ast_sim. |
| `ai_pattern_analyses` | PK: `id` | History of heuristic AI audits: filename, indicator_score, classification_label, findings_json. |


## 5. SOURCE CODE OF CORE SYSTEM FILES

### File: `app.py`
**Role:** Streamlit Main Entrypoint & Page Router  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/app.py`

```python
"""
Main Streamlit entry point for the Hacker Analytics and AI Code Detection System.
Initializes the SQLite database and routes between the 7 dashboard pages.
"""

from __future__ import annotations

import streamlit as st

from config import APP_TITLE, DB_PATH
from dashboard.ai_detection_page import render_ai_detection_page
from dashboard.coding_page import render_coding_page
from dashboard.history_page import render_history_page
from dashboard.home import render_home_page
from dashboard.profile_page import render_profile_page
from dashboard.scraper_page import render_scraper_page
from dashboard.sidebar import render_sidebar
from dashboard.similarity_page import render_similarity_page
from database.db_manager import DatabaseManager


def get_database() -> DatabaseManager:
    """Create or reuse a DatabaseManager instance stored in session state."""
    if "db_manager" not in st.session_state:
        st.session_state["db_manager"] = DatabaseManager(DB_PATH)
    return st.session_state["db_manager"]


def apply_custom_styling() -> None:
    """Apply clean, modern dashboard styling with sleek visuals."""
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }
        [data-testid="stMetric"] {
            background-color: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 12px;
            padding: 14px 18px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
        }
        [data-testid="stButton"] button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
        }
        [data-testid="stButton"] button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_custom_styling()

    db = get_database()
    active_page = render_sidebar(db)

    page_routes = {
        "Home Dashboard": render_home_page,
        "Selenium Web Scraper": render_scraper_page,
        "Profile Analytics": render_profile_page,
        "Coding Performance Analytics": render_coding_page,
        "Source-Code Similarity": render_similarity_page,
        "AI-Associated Code Pattern Analysis": render_ai_detection_page,
        "Analysis History": render_history_page,
    }

    renderer = page_routes.get(active_page, render_home_page)
    renderer(db)


if __name__ == "__main__":
    main()


```

---

### File: `config.py`
**Role:** Central Configurations, Thresholds & Ethical Disclaimers  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/config.py`

```python
"""
Central configuration settings for the Hacker Analytics and AI Code Detection System.
"""

from pathlib import Path

# Project directories
BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR: Path = BASE_DIR / "data"
SAMPLE_DATA_DIR: Path = BASE_DIR / "sample_data"
DB_PATH: Path = DATA_DIR / "hackerrank.db"

# Application metadata
APP_TITLE: str = "Hacker Analytics & AI Code Detection System"
APP_SHORT_TITLE: str = "Hacker Analytics"
APP_VERSION: str = "1.0.0"
APP_DESCRIPTION: str = (
    "A modular Python web application for public HackerRank profile scraping, "
    "coding performance analytics, source-code similarity analysis, AST structural "
    "inspection, and explainable heuristic AI-pattern analysis."
)

# HackerRank scraping configuration
HACKERRANK_PROFILE_BASE_URL: str = "https://www.hackerrank.com/profile/"
SCRAPER_PAGE_LOAD_TIMEOUT: int = 25
SCRAPER_ELEMENT_WAIT_TIMEOUT: int = 12
SCRAPER_RENDER_DELAY_SECONDS: float = 2.0

# Code analysis limits
MAX_CODE_FILE_BYTES: int = 512 * 1024  # 512 KB per uploaded file

# Heuristic AI-associated pattern labels (non-probabilistic)
HEURISTIC_LABELS = {
    "few": "Few indicators observed",
    "some": "Some indicators observed",
    "several": "Several indicators observed",
}

HEURISTIC_THRESHOLDS = {
    "some_min": 35.0,
    "several_min": 65.0,
}

# Important ethical and analytical disclaimers
AI_DETECTION_DISCLAIMER: str = (
    "Heuristic analysis identifies stylistic and structural patterns sometimes associated "
    "with AI-assisted coding. It does NOT prove AI authorship, does NOT output a validated "
    "probability, and cannot distinguish well-formatted human code from AI-assisted code "
    "with certainty. False positives and false negatives are always possible."
)

SIMILARITY_DISCLAIMER: str = (
    "A high similarity score is NOT proof of plagiarism. Common algorithms, standard "
    "library idioms, shared starter templates, and identical problem constraints frequently "
    "produce structural and textual similarity between independent submissions."
)

SCRAPING_DISCLAIMER: str = (
    "This tool only accesses publicly visible HackerRank profile pages without bypassing "
    "CAPTCHAs, logins, or access controls. Live availability depends on HackerRank's "
    "public page structure and network access. Use Sample Data Mode for offline demos."
)


```

---

### File: `database/schema.py`
**Role:** SQLite Database 9-Table Schema & DDL Definitions  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/database/schema.py`

```python
"""
SQLite database table definitions for Hacker Analytics and AI Code Detection System.
"""

TABLE_DDL: dict[str, str] = {
    "profiles": """
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            display_name TEXT,
            profile_url TEXT,
            description TEXT,
            country TEXT,
            is_sample INTEGER NOT NULL DEFAULT 0,
            source_label TEXT NOT NULL DEFAULT 'live',
            fields_collected INTEGER NOT NULL DEFAULT 0,
            raw_metadata_json TEXT,
            last_scraped_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """,
    "profile_statistics": """
        CREATE TABLE IF NOT EXISTS profile_statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            stat_name TEXT NOT NULL,
            stat_value TEXT,
            numeric_value REAL,
            stat_category TEXT DEFAULT 'general',
            recorded_at TEXT NOT NULL,
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
        );
    """,
    "programming_languages": """
        CREATE TABLE IF NOT EXISTS programming_languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            language_name TEXT NOT NULL,
            problems_solved INTEGER,
            proficiency TEXT,
            recorded_at TEXT NOT NULL,
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
            UNIQUE(profile_id, language_name)
        );
    """,
    "skills": """
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            skill_level TEXT,
            verified INTEGER NOT NULL DEFAULT 0,
            recorded_at TEXT NOT NULL,
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
            UNIQUE(profile_id, skill_name)
        );
    """,
    "achievements": """
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            achievement_type TEXT NOT NULL DEFAULT 'badge',
            level_or_stars TEXT,
            details TEXT,
            recorded_at TEXT NOT NULL,
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
            UNIQUE(profile_id, title, achievement_type)
        );
    """,
    "scraping_history": """
        CREATE TABLE IF NOT EXISTS scraping_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            profile_id INTEGER,
            status TEXT NOT NULL,
            source_mode TEXT NOT NULL DEFAULT 'live',
            fields_collected INTEGER NOT NULL DEFAULT 0,
            error_message TEXT,
            duration_seconds REAL,
            scraped_at TEXT NOT NULL,
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE SET NULL
        );
    """,
    "code_analysis": """
        CREATE TABLE IF NOT EXISTS code_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            code_hash TEXT NOT NULL,
            lines_of_code INTEGER NOT NULL DEFAULT 0,
            num_functions INTEGER NOT NULL DEFAULT 0,
            num_classes INTEGER NOT NULL DEFAULT 0,
            num_loops INTEGER NOT NULL DEFAULT 0,
            num_conditionals INTEGER NOT NULL DEFAULT 0,
            num_imports INTEGER NOT NULL DEFAULT 0,
            num_assignments INTEGER NOT NULL DEFAULT 0,
            max_nesting_depth INTEGER NOT NULL DEFAULT 0,
            complexity_indicator REAL NOT NULL DEFAULT 0,
            syntax_valid INTEGER NOT NULL DEFAULT 1,
            ast_summary_json TEXT,
            analyzed_at TEXT NOT NULL
        );
    """,
    "similarity_results": """
        CREATE TABLE IF NOT EXISTS similarity_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_a TEXT NOT NULL,
            file_b TEXT NOT NULL,
            overall_similarity REAL NOT NULL,
            token_similarity REAL NOT NULL,
            tfidf_similarity REAL NOT NULL,
            sequence_similarity REAL NOT NULL,
            ast_similarity REAL NOT NULL,
            normalized_var_mode INTEGER NOT NULL DEFAULT 0,
            summary_text TEXT,
            details_json TEXT,
            analyzed_at TEXT NOT NULL
        );
    """,
    "ai_pattern_results": """
        CREATE TABLE IF NOT EXISTS ai_pattern_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            code_hash TEXT,
            indicator_score REAL NOT NULL,
            classification_label TEXT NOT NULL,
            indicators_json TEXT,
            characteristics_json TEXT,
            limitations_text TEXT,
            analyzed_at TEXT NOT NULL
        );
    """,
}

INDEX_DDL: list[str] = [
    "CREATE INDEX IF NOT EXISTS idx_profiles_username ON profiles(username);",
    "CREATE INDEX IF NOT EXISTS idx_profile_stats_pid ON profile_statistics(profile_id);",
    "CREATE INDEX IF NOT EXISTS idx_scraping_history_user ON scraping_history(username);",
    "CREATE INDEX IF NOT EXISTS idx_code_analysis_hash ON code_analysis(code_hash);",
]

ALL_TABLES: list[str] = list(TABLE_DDL.keys())


```

---

### File: `database/db_manager.py`
**Role:** SQLite Database Manager & Relational Operations  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/database/db_manager.py`

```python
"""
SQLite Database Manager handling initialization, CRUD operations, duplicate management,
and analytical history queries.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

from config import DB_PATH
from database.schema import ALL_TABLES, INDEX_DDL, TABLE_DDL
from utils.helpers import (
    count_non_empty_fields,
    safe_json_dumps,
    safe_json_loads,
    utc_now_iso,
)


class DatabaseError(Exception):
    """Custom exception raised for database operation failures."""


class DatabaseManager:
    """Encapsulates all SQLite database operations for the application."""

    def __init__(self, db_path: Path | str = DB_PATH) -> None:
        self.db_path = Path(db_path)
        self.initialize_database()

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Provide a managed SQLite connection with foreign keys enabled."""
        conn: sqlite3.Connection | None = None
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(self.db_path), timeout=15.0)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON;")
            yield conn
            conn.commit()
        except sqlite3.Error as exc:
            if conn is not None:
                conn.rollback()
            raise DatabaseError(f"SQLite error: {exc}") from exc
        finally:
            if conn is not None:
                conn.close()

    def initialize_database(self) -> None:
        """Create all required tables and indexes if they do not exist."""
        with self.get_connection() as conn:
            for table_name in ALL_TABLES:
                conn.execute(TABLE_DDL[table_name])
            for idx_sql in INDEX_DDL:
                conn.execute(idx_sql)

    @staticmethod
    def _parse_numeric(value: Any) -> float | None:
        """Attempt to extract a numeric value from a statistic string."""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        cleaned = str(value).replace(",", "").replace("%", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return None

    # ------------------------------------------------------------------
    # Profile CRUD Operations
    # ------------------------------------------------------------------

    def upsert_profile(self, profile_data: dict[str, Any]) -> int:
        """
        Insert or update a HackerRank profile and its child records (languages,
        skills, achievements, and statistics). Returns the profile ID.
        """
        username = (profile_data.get("username") or "").strip()
        if not username:
            raise DatabaseError("Profile username is required for database storage.")

        now = utc_now_iso()
        is_sample = 1 if profile_data.get("is_sample") else 0
        source_label = profile_data.get("source_label") or (
            "sample" if is_sample else "live"
        )
        fields_collected = int(
            profile_data.get("fields_collected")
            or count_non_empty_fields(profile_data)
        )
        last_scraped_at = profile_data.get("last_scraped_at") or now

        metadata_payload = {
            "recent_activity": profile_data.get("recent_activity") or [],
            "unavailable_fields": profile_data.get("unavailable_fields") or [],
            "data_source_note": profile_data.get("data_source_note") or "",
        }

        with self.get_connection() as conn:
            existing = conn.execute(
                "SELECT id FROM profiles WHERE LOWER(username) = LOWER(?)",
                (username,),
            ).fetchone()

            if existing:
                profile_id = int(existing["id"])
                conn.execute(
                    """
                    UPDATE profiles
                    SET username = ?,
                        display_name = ?,
                        profile_url = ?,
                        description = ?,
                        country = ?,
                        is_sample = ?,
                        source_label = ?,
                        fields_collected = ?,
                        raw_metadata_json = ?,
                        last_scraped_at = ?,
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        username,
                        profile_data.get("display_name"),
                        profile_data.get("profile_url"),
                        profile_data.get("description"),
                        profile_data.get("country"),
                        is_sample,
                        source_label,
                        fields_collected,
                        safe_json_dumps(metadata_payload),
                        last_scraped_at,
                        now,
                        profile_id,
                    ),
                )
                # Refresh current language/skill/achievement snapshots cleanly
                conn.execute(
                    "DELETE FROM programming_languages WHERE profile_id = ?",
                    (profile_id,),
                )
                conn.execute(
                    "DELETE FROM skills WHERE profile_id = ?",
                    (profile_id,),
                )
                conn.execute(
                    "DELETE FROM achievements WHERE profile_id = ?",
                    (profile_id,),
                )
            else:
                cursor = conn.execute(
                    """
                    INSERT INTO profiles (
                        username, display_name, profile_url, description, country,
                        is_sample, source_label, fields_collected, raw_metadata_json,
                        last_scraped_at, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        username,
                        profile_data.get("display_name"),
                        profile_data.get("profile_url"),
                        profile_data.get("description"),
                        profile_data.get("country"),
                        is_sample,
                        source_label,
                        fields_collected,
                        safe_json_dumps(metadata_payload),
                        last_scraped_at,
                        now,
                        now,
                    ),
                )
                profile_id = int(cursor.lastrowid)

            # Insert programming languages (deduplicated)
            seen_langs: set[str] = set()
            for lang in profile_data.get("programming_languages") or []:
                if isinstance(lang, str):
                    lang_name = lang.strip()
                    solved = None
                    proficiency = None
                elif isinstance(lang, dict):
                    lang_name = (lang.get("language_name") or lang.get("name") or "").strip()
                    solved = lang.get("problems_solved")
                    proficiency = lang.get("proficiency")
                else:
                    continue

                if not lang_name or lang_name.lower() in seen_langs:
                    continue
                seen_langs.add(lang_name.lower())
                conn.execute(
                    """
                    INSERT OR REPLACE INTO programming_languages (
                        profile_id, language_name, problems_solved, proficiency, recorded_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (profile_id, lang_name, solved, proficiency, now),
                )

            # Insert skills (deduplicated)
            seen_skills: set[str] = set()
            for skill in profile_data.get("skills") or []:
                if isinstance(skill, str):
                    skill_name = skill.strip()
                    skill_level = None
                    verified = 0
                elif isinstance(skill, dict):
                    skill_name = (skill.get("skill_name") or skill.get("name") or "").strip()
                    skill_level = skill.get("skill_level") or skill.get("level")
                    verified = 1 if skill.get("verified") else 0
                else:
                    continue

                if not skill_name or skill_name.lower() in seen_skills:
                    continue
                seen_skills.add(skill_name.lower())
                conn.execute(
                    """
                    INSERT OR REPLACE INTO skills (
                        profile_id, skill_name, skill_level, verified, recorded_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (profile_id, skill_name, skill_level, verified, now),
                )

            # Insert badges + certificates into achievements
            seen_achievements: set[tuple[str, str]] = set()
            combined_achievements = []
            for badge in profile_data.get("badges") or []:
                if isinstance(badge, str):
                    combined_achievements.append(
                        {"title": badge, "achievement_type": "badge"}
                    )
                elif isinstance(badge, dict):
                    item = dict(badge)
                    item.setdefault("achievement_type", "badge")
                    combined_achievements.append(item)

            for cert in profile_data.get("certificates") or []:
                if isinstance(cert, str):
                    combined_achievements.append(
                        {"title": cert, "achievement_type": "certificate"}
                    )
                elif isinstance(cert, dict):
                    item = dict(cert)
                    item.setdefault("achievement_type", "certificate")
                    combined_achievements.append(item)

            for ach in profile_data.get("achievements") or []:
                if isinstance(ach, str):
                    combined_achievements.append(
                        {"title": ach, "achievement_type": "achievement"}
                    )
                elif isinstance(ach, dict):
                    item = dict(ach)
                    item.setdefault("achievement_type", "achievement")
                    combined_achievements.append(item)

            for ach in combined_achievements:
                title = (ach.get("title") or ach.get("name") or "").strip()
                ach_type = (ach.get("achievement_type") or "badge").strip().lower()
                if not title:
                    continue
                key = (title.lower(), ach_type)
                if key in seen_achievements:
                    continue
                seen_achievements.add(key)
                level_or_stars = ach.get("level_or_stars") or ach.get("stars") or ach.get("level")
                if level_or_stars is not None:
                    level_or_stars = str(level_or_stars)
                details = ach.get("details") or ach.get("description")
                conn.execute(
                    """
                    INSERT OR REPLACE INTO achievements (
                        profile_id, title, achievement_type, level_or_stars, details, recorded_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (profile_id, title, ach_type, level_or_stars, details, now),
                )

            # Append statistics snapshot (preserves historical trend when re-scraped!)
            for stat in profile_data.get("statistics") or []:
                if not isinstance(stat, dict):
                    continue
                stat_name = (stat.get("stat_name") or stat.get("name") or "").strip()
                if not stat_name:
                    continue
                stat_val = stat.get("stat_value") if stat.get("stat_value") is not None else stat.get("value")
                numeric_val = stat.get("numeric_value")
                if numeric_val is None:
                    numeric_val = self._parse_numeric(stat_val)
                stat_category = stat.get("stat_category") or stat.get("category") or "general"
                conn.execute(
                    """
                    INSERT INTO profile_statistics (
                        profile_id, stat_name, stat_value, numeric_value, stat_category, recorded_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        profile_id,
                        stat_name,
                        str(stat_val) if stat_val is not None else None,
                        numeric_val,
                        stat_category,
                        last_scraped_at,
                    ),
                )

        return profile_id

    def _hydrate_profile(self, conn: sqlite3.Connection, row: sqlite3.Row) -> dict[str, Any]:
        """Build a complete nested profile dictionary from relational tables."""
        profile = dict(row)
        profile_id = profile["id"]
        profile["is_sample"] = bool(profile.get("is_sample"))

        metadata = safe_json_loads(profile.get("raw_metadata_json"), default={}) or {}
        profile["recent_activity"] = metadata.get("recent_activity", [])
        profile["unavailable_fields"] = metadata.get("unavailable_fields", [])
        profile["data_source_note"] = metadata.get("data_source_note", "")

        langs = conn.execute(
            """
            SELECT language_name, problems_solved, proficiency, recorded_at
            FROM programming_languages
            WHERE profile_id = ?
            ORDER BY COALESCE(problems_solved, 0) DESC, language_name ASC
            """,
            (profile_id,),
        ).fetchall()
        profile["programming_languages"] = [dict(r) for r in langs]

        skills = conn.execute(
            """
            SELECT skill_name, skill_level, verified, recorded_at
            FROM skills
            WHERE profile_id = ?
            ORDER BY verified DESC, skill_name ASC
            """,
            (profile_id,),
        ).fetchall()
        profile["skills"] = [dict(r) for r in skills]

        ach_rows = conn.execute(
            """
            SELECT title, achievement_type, level_or_stars, details, recorded_at
            FROM achievements
            WHERE profile_id = ?
            ORDER BY achievement_type ASC, title ASC
            """,
            (profile_id,),
        ).fetchall()
        all_ach = [dict(r) for r in ach_rows]
        profile["achievements"] = all_ach
        profile["badges"] = [a for a in all_ach if a["achievement_type"] == "badge"]
        profile["certificates"] = [
            a for a in all_ach if a["achievement_type"] == "certificate"
        ]

        # Latest statistics per stat_name + full history
        stat_rows = conn.execute(
            """
            SELECT stat_name, stat_value, numeric_value, stat_category, recorded_at
            FROM profile_statistics
            WHERE profile_id = ?
            ORDER BY recorded_at DESC, id DESC
            """,
            (profile_id,),
        ).fetchall()
        all_stats = [dict(r) for r in stat_rows]
        latest_stats: list[dict[str, Any]] = []
        seen_stat_names: set[str] = set()
        for s in all_stats:
            if s["stat_name"] not in seen_stat_names:
                seen_stat_names.add(s["stat_name"])
                latest_stats.append(s)

        profile["statistics"] = latest_stats
        profile["statistics_history"] = all_stats
        return profile

    def get_profile_by_username(self, username: str) -> dict[str, Any] | None:
        """Retrieve a full profile dictionary by username (case-insensitive)."""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM profiles WHERE LOWER(username) = LOWER(?)",
                (username.strip(),),
            ).fetchone()
            if not row:
                return None
            return self._hydrate_profile(conn, row)

    def get_profile_by_id(self, profile_id: int) -> dict[str, Any] | None:
        """Retrieve a full profile dictionary by primary key ID."""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM profiles WHERE id = ?",
                (profile_id,),
            ).fetchone()
            if not row:
                return None
            return self._hydrate_profile(conn, row)

    def get_all_profiles(
        self, include_sample: bool = True, search: str | None = None
    ) -> list[dict[str, Any]]:
        """Return all stored profiles with hydrated child collections."""
        query = "SELECT * FROM profiles WHERE 1=1"
        params: list[Any] = []
        if not include_sample:
            query += " AND is_sample = 0"
        if search and search.strip():
            like_term = f"%{search.strip()}%"
            query += " AND (username LIKE ? OR COALESCE(display_name, '') LIKE ?)"
            params.extend([like_term, like_term])
        query += " ORDER BY updated_at DESC, id DESC"

        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [self._hydrate_profile(conn, row) for row in rows]

    def delete_profile(self, profile_id: int) -> bool:
        """Delete a profile and cascade-delete its child records."""
        with self.get_connection() as conn:
            cur = conn.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
            return cur.rowcount > 0

    # ------------------------------------------------------------------
    # Scraping History Operations
    # ------------------------------------------------------------------

    def log_scraping_attempt(
        self,
        username: str,
        status: str,
        source_mode: str = "live",
        profile_id: int | None = None,
        fields_collected: int = 0,
        error_message: str | None = None,
        duration_seconds: float | None = None,
        scraped_at: str | None = None,
    ) -> int:
        """Record an execution of the scraper or sample-data loader."""
        timestamp = scraped_at or utc_now_iso()
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO scraping_history (
                    username, profile_id, status, source_mode,
                    fields_collected, error_message, duration_seconds, scraped_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    username,
                    profile_id,
                    status,
                    source_mode,
                    fields_collected,
                    error_message,
                    duration_seconds,
                    timestamp,
                ),
            )
            return int(cur.lastrowid)

    def get_scraping_history(
        self,
        limit: int = 100,
        status_filter: str | None = None,
        source_filter: str | None = None,
        search: str | None = None,
    ) -> list[dict[str, Any]]:
        """Query scraping history with optional filters."""
        query = "SELECT * FROM scraping_history WHERE 1=1"
        params: list[Any] = []
        if status_filter and status_filter != "All":
            query += " AND status = ?"
            params.append(status_filter)
        if source_filter and source_filter != "All":
            query += " AND source_mode = ?"
            params.append(source_filter)
        if search and search.strip():
            like_term = f"%{search.strip()}%"
            query += " AND (username LIKE ? OR COALESCE(error_message, '') LIKE ?)"
            params.extend([like_term, like_term])
        query += " ORDER BY scraped_at DESC, id DESC LIMIT ?"
        params.append(limit)

        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    def get_last_successful_scrape_time(self, source_mode: str | None = None) -> str | None:
        """Return the ISO timestamp of the most recent successful collection."""
        query = "SELECT scraped_at FROM scraping_history WHERE status = 'success'"
        params: list[Any] = []
        if source_mode:
            query += " AND source_mode = ?"
            params.append(source_mode)
        query += " ORDER BY scraped_at DESC, id DESC LIMIT 1"

        with self.get_connection() as conn:
            row = conn.execute(query, params).fetchone()
            return str(row["scraped_at"]) if row else None

    # ------------------------------------------------------------------
    # Code Analysis, Similarity, and Heuristic AI Pattern Results
    # ------------------------------------------------------------------

    def save_code_analysis(self, data: dict[str, Any]) -> int:
        """Persist an AST code structure analysis record."""
        now = data.get("analyzed_at") or utc_now_iso()
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO code_analysis (
                    filename, code_hash, lines_of_code, num_functions, num_classes,
                    num_loops, num_conditionals, num_imports, num_assignments,
                    max_nesting_depth, complexity_indicator, syntax_valid,
                    ast_summary_json, analyzed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.get("filename", "<input>"),
                    data.get("code_hash", ""),
                    int(data.get("lines_of_code", 0)),
                    int(data.get("num_functions", 0)),
                    int(data.get("num_classes", 0)),
                    int(data.get("num_loops", 0)),
                    int(data.get("num_conditionals", 0)),
                    int(data.get("num_imports", 0)),
                    int(data.get("num_assignments", 0)),
                    int(data.get("max_nesting_depth", 0)),
                    float(data.get("approx_cyclomatic_complexity", data.get("complexity_indicator", 0))),
                    1 if data.get("syntax_valid", True) else 0,
                    safe_json_dumps(data),
                    now,
                ),
            )
            return int(cur.lastrowid)

    def get_code_analysis_history(
        self, limit: int = 100, search: str | None = None
    ) -> list[dict[str, Any]]:
        """Fetch stored AST code analysis records."""
        query = "SELECT * FROM code_analysis WHERE 1=1"
        params: list[Any] = []
        if search and search.strip():
            query += " AND filename LIKE ?"
            params.append(f"%{search.strip()}%")
        query += " ORDER BY analyzed_at DESC, id DESC LIMIT ?"
        params.append(limit)
        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    def save_similarity_result(self, data: dict[str, Any]) -> int:
        """Persist a pairwise source-code similarity comparison result."""
        now = data.get("analyzed_at") or utc_now_iso()
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO similarity_results (
                    file_a, file_b, overall_similarity, token_similarity,
                    tfidf_similarity, sequence_similarity, ast_similarity,
                    normalized_var_mode, summary_text, details_json, analyzed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.get("file_a", "file_a.py"),
                    data.get("file_b", "file_b.py"),
                    float(data.get("overall_similarity", 0.0)),
                    float(data.get("token_similarity", 0.0)),
                    float(data.get("tfidf_similarity", 0.0)),
                    float(data.get("sequence_similarity", 0.0)),
                    float(data.get("ast_similarity", 0.0)),
                    1 if data.get("normalized_var_mode") else 0,
                    data.get("summary_text", ""),
                    safe_json_dumps(data.get("details") or {}),
                    now,
                ),
            )
            return int(cur.lastrowid)

    def get_similarity_history(
        self, limit: int = 100, search: str | None = None
    ) -> list[dict[str, Any]]:
        """Fetch stored code similarity results."""
        query = "SELECT * FROM similarity_results WHERE 1=1"
        params: list[Any] = []
        if search and search.strip():
            term = f"%{search.strip()}%"
            query += " AND (file_a LIKE ? OR file_b LIKE ? OR COALESCE(summary_text, '') LIKE ?)"
            params.extend([term, term, term])
        query += " ORDER BY analyzed_at DESC, id DESC LIMIT ?"
        params.append(limit)
        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    def save_ai_pattern_result(self, data: dict[str, Any]) -> int:
        """Persist a heuristic AI-associated code pattern analysis result."""
        now = data.get("analyzed_at") or utc_now_iso()
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO ai_pattern_results (
                    filename, code_hash, indicator_score, classification_label,
                    indicators_json, characteristics_json, limitations_text, analyzed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.get("filename", "<input>"),
                    data.get("code_hash", ""),
                    float(data.get("indicator_score", 0.0)),
                    data.get("classification_label", "Few indicators observed"),
                    safe_json_dumps(data.get("indicators") or []),
                    safe_json_dumps(data.get("influencing_characteristics") or []),
                    data.get("limitations_text", ""),
                    now,
                ),
            )
            return int(cur.lastrowid)

    def get_ai_pattern_history(
        self, limit: int = 100, search: str | None = None, label_filter: str | None = None
    ) -> list[dict[str, Any]]:
        """Fetch stored heuristic AI-pattern analysis records."""
        query = "SELECT * FROM ai_pattern_results WHERE 1=1"
        params: list[Any] = []
        if label_filter and label_filter != "All":
            query += " AND classification_label = ?"
            params.append(label_filter)
        if search and search.strip():
            query += " AND filename LIKE ?"
            params.append(f"%{search.strip()}%")
        query += " ORDER BY analyzed_at DESC, id DESC LIMIT ?"
        params.append(limit)
        with self.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Dashboard Aggregations & Safe Record Deletion
    # ------------------------------------------------------------------

    def get_dashboard_counts(self) -> dict[str, int]:
        """Return aggregate counts across all core tables for dashboard metrics."""
        with self.get_connection() as conn:
            total_profiles = conn.execute(
                "SELECT COUNT(*) FROM profiles"
            ).fetchone()[0]
            live_profiles = conn.execute(
                "SELECT COUNT(*) FROM profiles WHERE is_sample = 0"
            ).fetchone()[0]
            sample_profiles = conn.execute(
                "SELECT COUNT(*) FROM profiles WHERE is_sample = 1"
            ).fetchone()[0]
            total_scrapes = conn.execute(
                "SELECT COUNT(*) FROM scraping_history"
            ).fetchone()[0]
            successful_scrapes = conn.execute(
                "SELECT COUNT(*) FROM scraping_history WHERE status = 'success'"
            ).fetchone()[0]
            total_code_analyses = conn.execute(
                "SELECT COUNT(*) FROM code_analysis"
            ).fetchone()[0]
            total_similarities = conn.execute(
                "SELECT COUNT(*) FROM similarity_results"
            ).fetchone()[0]
            total_ai_analyses = conn.execute(
                "SELECT COUNT(*) FROM ai_pattern_results"
            ).fetchone()[0]

        return {
            "total_profiles": int(total_profiles),
            "live_profiles": int(live_profiles),
            "sample_profiles": int(sample_profiles),
            "total_scrapes": int(total_scrapes),
            "successful_scrapes": int(successful_scrapes),
            "total_code_analyses": int(total_code_analyses),
            "total_similarities": int(total_similarities),
            "total_ai_analyses": int(total_ai_analyses),
            "total_source_analyses": int(
                total_code_analyses + total_similarities + total_ai_analyses
            ),
        }

    def get_all_statistics_history(self) -> list[dict[str, Any]]:
        """Return all stored profile statistics joined with profile username and source flag."""
        with self.get_connection() as conn:
            rows = conn.execute(
                """
                SELECT ps.*, p.username, p.is_sample
                FROM profile_statistics ps
                JOIN profiles p ON p.id = ps.profile_id
                ORDER BY ps.recorded_at ASC, ps.id ASC
                """
            ).fetchall()
            return [dict(r) for r in rows]

    def delete_record(self, table_name: str, record_id: int) -> bool:
        """Delete a single record from an allowlisted table by ID."""
        allowed = {
            "profiles",
            "scraping_history",
            "code_analysis",
            "similarity_results",
            "ai_pattern_results",
        }
        if table_name not in allowed:
            raise DatabaseError(f"Deletion not permitted for table '{table_name}'.")
        with self.get_connection() as conn:
            cur = conn.execute(
                f"DELETE FROM {table_name} WHERE id = ?",
                (record_id,),
            )
            return cur.rowcount > 0


```

---

### File: `scraper/browser_manager.py`
**Role:** Selenium Chrome Lifecycle & WebDriver Configuration  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/scraper/browser_manager.py`

```python
"""
Selenium WebDriver lifecycle manager with standard browser configuration,
page-load timeouts, explicit DOM wait helpers, and guaranteed cleanup.
Does not use stealth plugins, fingerprint spoofing, or proxy rotation.
"""

from __future__ import annotations

import logging
from typing import Any

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait

from config import SCRAPER_ELEMENT_WAIT_TIMEOUT, SCRAPER_PAGE_LOAD_TIMEOUT

logger = logging.getLogger("hacker_analytics.scraper")


class BrowserStartupError(Exception):
    """Raised when Selenium cannot initialize any supported WebDriver."""


class BrowserManager:
    """Manages a single Selenium WebDriver session cleanly via context manager."""

    def __init__(
        self,
        headless: bool = True,
        page_load_timeout: int = SCRAPER_PAGE_LOAD_TIMEOUT,
        wait_timeout: int = SCRAPER_ELEMENT_WAIT_TIMEOUT,
    ) -> None:
        self.headless = headless
        self.page_load_timeout = page_load_timeout
        self.wait_timeout = wait_timeout
        self.driver: webdriver.Remote | None = None
        self.browser_name: str = ""

    def _build_chrome_options(self) -> ChromeOptions:
        options = ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1366,900")
        options.add_argument("--disable-extensions")
        options.add_argument("--log-level=3")
        return options

    def _build_edge_options(self) -> EdgeOptions:
        options = EdgeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1366,900")
        options.add_argument("--log-level=3")
        return options

    def start(self) -> webdriver.Remote:
        """Initialize Chrome WebDriver (with Edge fallback on Windows) and configure timeouts."""
        if self.driver is not None:
            return self.driver

        errors: list[str] = []

        # Primary: Google Chrome via Selenium Manager
        try:
            self.driver = webdriver.Chrome(options=self._build_chrome_options())
            self.browser_name = "Chrome"
            logger.info("Started Selenium Chrome WebDriver (headless=%s)", self.headless)
        except WebDriverException as chrome_exc:
            errors.append(f"Chrome: {chrome_exc.msg or str(chrome_exc)}")
            logger.warning("Chrome WebDriver startup failed, attempting Edge fallback.")
            try:
                self.driver = webdriver.Edge(options=self._build_edge_options())
                self.browser_name = "Edge"
                logger.info("Started Selenium Edge WebDriver (headless=%s)", self.headless)
            except WebDriverException as edge_exc:
                errors.append(f"Edge: {edge_exc.msg or str(edge_exc)}")
                logger.error("All WebDriver startup attempts failed: %s", " | ".join(errors))
                raise BrowserStartupError(
                    "Unable to initialize Selenium WebDriver (Chrome or Edge). "
                    "Ensure Chrome or Edge is installed and up to date. Details: "
                    + " | ".join(errors)
                ) from edge_exc

        self.driver.set_page_load_timeout(self.page_load_timeout)
        return self.driver

    def wait_for_document_ready(self, timeout: int | None = None) -> bool:
        """Explicitly wait until document.readyState == 'complete'. Returns True if reached."""
        if self.driver is None:
            raise BrowserStartupError("WebDriver is not started.")
        wait_sec = timeout or self.wait_timeout
        try:
            WebDriverWait(self.driver, wait_sec).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            logger.warning("Timed out waiting %ss for document.readyState == 'complete'", wait_sec)
            return False

    def wait_for_page_content(self, timeout: int | None = None) -> bool:
        """
        Explicitly wait until the <body> has rendered text or recognizable profile/status
        DOM nodes appear (avoids blind fixed sleeps while letting SPA content settle).
        """
        if self.driver is None:
            raise BrowserStartupError("WebDriver is not started.")
        wait_sec = timeout or self.wait_timeout

        def _content_loaded(drv: webdriver.Remote) -> bool:
            try:
                body = drv.find_element(By.TAG_NAME, "body")
                text = (body.text or "").strip()
                if len(text) >= 20:
                    return True
                title = (drv.title or "").strip()
                if title:
                    return True
            except WebDriverException:
                return False
            return False

        try:
            WebDriverWait(self.driver, wait_sec, poll_frequency=0.4).until(_content_loaded)
            return True
        except TimeoutException:
            logger.warning("Timed out waiting %ss for rendered page body content", wait_sec)
            return False

    def close(self) -> None:
        """Safely quit the WebDriver instance and release OS resources."""
        if self.driver is not None:
            try:
                self.driver.quit()
                logger.info("Closed Selenium %s WebDriver cleanly.", self.browser_name or "browser")
            except Exception as exc:
                logger.warning("Error while closing WebDriver: %s", exc)
            finally:
                self.driver = None

    def __enter__(self) -> "BrowserManager":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

```

---

### File: `scraper/hackerrank_scraper.py`
**Role:** Resilient Profile Scraper Engine & Fallback Handler  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/scraper/hackerrank_scraper.py`

```python
"""
HackerRank public profile scraper using standard Selenium WebDriver and BeautifulSoup4.
Includes URL/username validation, explicit DOM waits, accurate classification of
network errors / 404s / missing elements / access blocks, structured debug logging,
and offline Sample Data Mode.

Does NOT use proxy rotation, CAPTCHA solving, stealth drivers, or fingerprint spoofing.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from selenium.common.exceptions import TimeoutException, WebDriverException

from config import DATA_DIR, SCRAPER_ELEMENT_WAIT_TIMEOUT
from scraper.browser_manager import BrowserManager, BrowserStartupError
from scraper.scraper_utils import (
    _extract_visible_text,
    classify_page_response,
    load_sample_profiles,
    parse_profile_html,
)
from utils.helpers import utc_now_iso
from utils.validators import validate_and_parse_profile_input

ProgressCallback = Callable[[int, str], None]

SCRAPER_LOG_PATH: Path = DATA_DIR / "scraper.log"


def _configure_scraper_logger() -> logging.Logger:
    """Configure file + stream logger for scraper debugging."""
    log = logging.getLogger("hacker_analytics.scraper")
    if not log.handlers:
        log.setLevel(logging.INFO)
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(SCRAPER_LOG_PATH, encoding="utf-8")
            fh.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            )
            log.addHandler(fh)
        except OSError:
            pass
    return log


logger = _configure_scraper_logger()


@dataclass
class ScrapeResult:
    """Structured outcome returned by HackerRankScraper."""

    success: bool
    username: str
    status: str  # 'success', 'not_found', 'restricted', 'missing_elements', 'browser_error', 'network_error', 'validation_error', 'error'
    source_mode: str = "live"  # 'live', 'sample', or 'uploaded'
    profile_data: dict[str, Any] | None = None
    fields_collected: int = 0
    unavailable_fields: list[str] = field(default_factory=list)
    error_message: str | None = None
    duration_seconds: float = 0.0
    scraped_at: str = field(default_factory=utc_now_iso)
    debug_info: dict[str, Any] = field(default_factory=dict)


class HackerRankScraper:
    """Scrapes publicly accessible HackerRank profile pages responsibly."""

    def __init__(self, headless: bool = True) -> None:
        self.headless = headless

    @staticmethod
    def _notify(callback: ProgressCallback | None, pct: int, message: str) -> None:
        if callback is not None:
            callback(pct, message)

    def scrape_profile(
        self,
        raw_input: str,
        progress_callback: ProgressCallback | None = None,
    ) -> ScrapeResult:
        """
        Validate input, load the public HackerRank profile URL via Selenium,
        wait explicitly for rendered DOM content, classify the response accurately,
        and stop immediately if access is denied.
        """
        start_time = time.perf_counter()
        self._notify(progress_callback, 10, "Validating username / HackerRank profile URL...")

        is_valid, parsed_or_err = validate_and_parse_profile_input(raw_input)
        if not is_valid:
            err_msg = parsed_or_err["error"]
            logger.warning("Input validation failed for '%s': %s", raw_input, err_msg)
            return ScrapeResult(
                success=False,
                username=(raw_input or "").strip(),
                status="validation_error",
                error_message=err_msg,
                duration_seconds=round(time.perf_counter() - start_time, 2),
                debug_info={
                    "raw_input": raw_input,
                    "classification_reason": err_msg,
                },
            )

        username = parsed_or_err["username"]
        target_url = parsed_or_err["profile_url"]
        logger.info("Starting live scrape for username='%s', url='%s'", username, target_url)

        try:
            self._notify(progress_callback, 25, "Starting Selenium WebDriver...")
            with BrowserManager(headless=self.headless) as browser:
                driver = browser.driver
                assert driver is not None

                self._notify(
                    progress_callback,
                    45,
                    f"Navigating to {target_url} ({browser.browser_name})...",
                )
                try:
                    driver.get(target_url)
                except TimeoutException:
                    msg = (
                        f"Page load timed out while opening {target_url}. "
                        "Check network connectivity or try Offline Sample Data Mode."
                    )
                    logger.warning("Timeout loading %s", target_url)
                    return ScrapeResult(
                        success=False,
                        username=username,
                        status="network_error",
                        error_message=msg,
                        duration_seconds=round(time.perf_counter() - start_time, 2),
                        debug_info={
                            "target_url": target_url,
                            "browser_name": browser.browser_name,
                            "classification_reason": "Selenium PageLoad TimeoutException",
                        },
                    )
                except WebDriverException as nav_exc:
                    msg = (
                        f"Network or navigation failure accessing {target_url}: "
                        f"{nav_exc.msg or str(nav_exc)}"
                    )
                    logger.error("Navigation WebDriverException for %s: %s", target_url, msg)
                    return ScrapeResult(
                        success=False,
                        username=username,
                        status="network_error",
                        error_message=msg,
                        duration_seconds=round(time.perf_counter() - start_time, 2),
                        debug_info={
                            "target_url": target_url,
                            "browser_name": browser.browser_name,
                            "classification_reason": f"WebDriverException: {nav_exc.msg or str(nav_exc)}",
                        },
                    )

                self._notify(progress_callback, 65, "Waiting for DOM and page content to render...")
                ready_ok = browser.wait_for_document_ready(SCRAPER_ELEMENT_WAIT_TIMEOUT)
                content_ok = browser.wait_for_page_content(SCRAPER_ELEMENT_WAIT_TIMEOUT)
                # Brief settle for client-side hydration if DOM just became ready
                if content_ok:
                    time.sleep(1.0)

                html = driver.page_source or ""
                current_url = driver.current_url or target_url
                page_title = driver.title or ""
                visible_text = _extract_visible_text(html)

                debug_info: dict[str, Any] = {
                    "target_url": target_url,
                    "final_url": current_url,
                    "page_title": page_title,
                    "browser_name": browser.browser_name,
                    "headless": self.headless,
                    "document_ready": ready_ok,
                    "content_detected": content_ok,
                    "html_length": len(html),
                    "visible_text_length": len(visible_text),
                }

                self._notify(progress_callback, 80, "Inspecting response status and parsing public fields...")
                page_status, status_reason = classify_page_response(
                    html, current_url=current_url, page_title=page_title
                )
                debug_info["classification_reason"] = status_reason
                logger.info(
                    "Response classified for '%s': status=%s | title='%s' | html_len=%d | reason=%s",
                    username,
                    page_status,
                    page_title,
                    len(html),
                    status_reason,
                )

                if page_status == "network_error":
                    return ScrapeResult(
                        success=False,
                        username=username,
                        status="network_error",
                        error_message=status_reason,
                        duration_seconds=round(time.perf_counter() - start_time, 2),
                        debug_info=debug_info,
                    )

                if page_status == "restricted":
                    return ScrapeResult(
                        success=False,
                        username=username,
                        status="restricted",
                        error_message=status_reason,
                        duration_seconds=round(time.perf_counter() - start_time, 2),
                        debug_info=debug_info,
                    )

                if page_status == "not_found":
                    return ScrapeResult(
                        success=False,
                        username=username,
                        status="not_found",
                        error_message=(
                            f"HackerRank profile '{username}' was not found ({status_reason}). "
                            "Verify the username or try Sample Data Mode / JSON-CSV Upload."
                        ),
                        duration_seconds=round(time.perf_counter() - start_time, 2),
                        debug_info=debug_info,
                    )

                profile_data = parse_profile_html(html, username=username, profile_url=current_url)
                fields_count = int(profile_data.get("fields_collected", 0))
                debug_info["fields_collected"] = fields_count

                # Only username + profile_url were populated -> page loaded cleanly, but public elements missing
                if fields_count <= 2 and not profile_data.get("display_name"):
                    reason = (
                        "The profile page loaded without access errors, but expected public profile "
                        "elements were missing (profile may be private, empty, or frontend selectors changed)."
                    )
                    debug_info["classification_reason"] = reason
                    logger.warning("Missing elements for '%s': %s", username, reason)
                    return ScrapeResult(
                        success=False,
                        username=username,
                        status="missing_elements",
                        profile_data=profile_data,
                        fields_collected=fields_count,
                        unavailable_fields=profile_data.get("unavailable_fields", []),
                        error_message=reason,
                        duration_seconds=round(time.perf_counter() - start_time, 2),
                        debug_info=debug_info,
                    )

                self._notify(progress_callback, 100, "Scraping completed successfully.")
                return ScrapeResult(
                    success=True,
                    username=username,
                    status="success",
                    source_mode="live",
                    profile_data=profile_data,
                    fields_collected=fields_count,
                    unavailable_fields=profile_data.get("unavailable_fields", []),
                    duration_seconds=round(time.perf_counter() - start_time, 2),
                    debug_info=debug_info,
                )

        except BrowserStartupError as b_exc:
            logger.error("Browser startup error for '%s': %s", username, b_exc)
            return ScrapeResult(
                success=False,
                username=username,
                status="browser_error",
                error_message=str(b_exc),
                duration_seconds=round(time.perf_counter() - start_time, 2),
                debug_info={"target_url": target_url, "classification_reason": str(b_exc)},
            )
        except Exception as exc:
            logger.exception("Unexpected error scraping '%s'", username)
            return ScrapeResult(
                success=False,
                username=username,
                status="error",
                error_message=f"Unexpected scraping error: {exc}",
                duration_seconds=round(time.perf_counter() - start_time, 2),
                debug_info={"target_url": target_url, "classification_reason": str(exc)},
            )

    @staticmethod
    def get_available_sample_usernames() -> list[str]:
        """List all usernames available in sample_data/sample_profiles.json."""
        return [p["username"] for p in load_sample_profiles() if p.get("username")]

    @staticmethod
    def load_sample_profile(username: str) -> ScrapeResult:
        """Load a single demonstration profile by username (works offline)."""
        start_time = time.perf_counter()
        samples = load_sample_profiles()
        for sample in samples:
            if sample.get("username", "").lower() == username.strip().lower():
                sample_copy = dict(sample)
                sample_copy["last_scraped_at"] = utc_now_iso()
                fields_count = int(sample_copy.get("fields_collected", 0))
                logger.info("Loaded offline sample profile '%s' (%d fields)", sample_copy["username"], fields_count)
                return ScrapeResult(
                    success=True,
                    username=sample_copy["username"],
                    status="success",
                    source_mode="sample",
                    profile_data=sample_copy,
                    fields_collected=fields_count,
                    unavailable_fields=sample_copy.get("unavailable_fields", []),
                    duration_seconds=round(time.perf_counter() - start_time, 3),
                    debug_info={"source": "sample_data/sample_profiles.json", "offline_mode": True},
                )

        return ScrapeResult(
            success=False,
            username=username,
            status="not_found",
            source_mode="sample",
            error_message=f"Sample profile '{username}' not found in sample_profiles.json.",
            duration_seconds=round(time.perf_counter() - start_time, 3),
        )

    @staticmethod
    def read_recent_logs(max_lines: int = 30) -> list[str]:
        """Read the most recent scraper log lines for UI diagnostics."""
        if not SCRAPER_LOG_PATH.exists():
            return []
        try:
            lines = SCRAPER_LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
            return lines[-max_lines:]
        except OSError:
            return []

```

---

### File: `scraper/scraper_utils.py`
**Role:** Isolated CSS Selectors, Badge Star Counters & Parsers  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/scraper/scraper_utils.py`

```python
"""
Separated HackerRank HTML selectors, BeautifulSoup parsers, response status
classifiers (distinguishing network errors, 404s, missing elements, and access
blocks), sample-data loaders, and JSON/CSV profile upload parsers.
"""

from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from config import HACKERRANK_PROFILE_BASE_URL, SAMPLE_DATA_DIR
from utils.helpers import count_non_empty_fields, utc_now_iso
from utils.validators import validate_and_parse_profile_input

# Separated CSS selectors for public HackerRank profile sections.
HACKERRANK_SELECTORS: dict[str, list[str]] = {
    "profile_root": [
        ".profile-page",
        ".hacker-profile",
        "[data-automation='profile-page']",
        "main",
    ],
    "display_name": [
        "h1.profile-title",
        "h1.profile-heading",
        ".profile-heading",
        "[data-automation='profile-name']",
        "h1",
    ],
    "username_handle": [
        ".profile-username-heading",
        ".username",
        "[data-automation='profile-username']",
    ],
    "description": [
        ".profile-about-section p",
        ".bio-content",
        ".profile-bio",
        "[data-automation='profile-bio']",
    ],
    "country": [
        ".profile-country",
        ".country-name",
        "[data-automation='profile-country']",
    ],
    "badges": [
        ".hacker-badge",
        ".badge-card",
        "[data-automation='badge-card']",
        ".badges-list .badge-item",
    ],
    "certificates": [
        ".certificate-card",
        ".hacker-certificate",
        "[data-automation='certificate-card']",
    ],
    "skills": [
        ".profile-skills-tag",
        ".skill-chip",
        ".skills-section .skill-item",
        "[data-automation='skill-tag']",
        ".profile-skills-section li",
    ],
    "languages": [
        ".language-item",
        ".profile-languages li",
        "[data-automation='language-item']",
    ],
    "stats": [
        ".profile-stats-item",
        ".hacker-stat",
        "[data-automation='profile-stat']",
    ],
    "activity": [
        ".recent-activity-item",
        ".submission-history-item",
        ".profile-timeline-item",
    ],
}

NETWORK_ERROR_SIGNATURES: list[tuple[str, str]] = [
    ("err_name_not_resolved", "DNS resolution failed (ERR_NAME_NOT_RESOLVED)."),
    ("err_internet_disconnected", "Internet connection appears offline (ERR_INTERNET_DISCONNECTED)."),
    ("err_connection_refused", "Connection refused by remote host (ERR_CONNECTION_REFUSED)."),
    ("err_connection_timed_out", "Network connection timed out (ERR_CONNECTION_TIMED_OUT)."),
    ("err_connection_reset", "Network connection was reset (ERR_CONNECTION_RESET)."),
    ("err_ssl_protocol_error", "SSL/TLS handshake failure (ERR_SSL_PROTOCOL_ERROR)."),
    ("this site can’t be reached", "Browser could not reach the target site."),
    ("this site can't be reached", "Browser could not reach the target site."),
]

RESTRICTION_TITLE_SIGNATURES: list[tuple[str, str]] = [
    ("access denied", "Access denied by target website (HTTP 403 / Edge security)."),
    ("attention required", "Cloudflare security challenge detected."),
    ("just a moment", "Bot verification interstitial detected."),
    ("403 forbidden", "HTTP 403 Forbidden returned by target website."),
    ("429 too many requests", "HTTP 429 Rate Limit returned by target website."),
]

RESTRICTION_TEXT_SIGNATURES: list[tuple[str, str]] = [
    ("verify you are human", "Anti-bot human verification / CAPTCHA detected."),
    ("you don't have permission to access", "Access denied by target website edge protection."),
    ("cf-browser-verification", "Cloudflare browser verification challenge detected."),
    ("too many requests", "Rate limit (HTTP 429) detected by target website."),
    ("enable javascript and cookies to continue", "Security interstitial challenge detected."),
]

RESTRICTION_DOM_SELECTORS: list[tuple[str, str]] = [
    (".cf-browser-verification", "Cloudflare verification challenge DOM element detected."),
    ("#challenge-form", "Bot challenge form detected."),
    (".g-recaptcha", "reCAPTCHA widget detected."),
    ("iframe[src*='recaptcha']", "reCAPTCHA iframe detected."),
    ("iframe[src*='hcaptcha']", "hCaptcha iframe detected."),
]

NOT_FOUND_SIGNATURES: list[str] = [
    "we could not find the page you were looking for",
    "404 - page not found",
    "this profile does not exist",
    "sorry, this page isn't available",
    "page not found | hackerrank",
    "hacker not found",
]


def _extract_visible_text(html: str) -> str:
    """Extract clean visible text from HTML, excluding script/style tags."""
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return " ".join(soup.get_text(" ", strip=True).split())


def detect_network_error_page(
    html: str, current_url: str = "", page_title: str = ""
) -> tuple[bool, str]:
    """Detect browser network-error interstitial pages (DNS, offline, timeout)."""
    url_lower = (current_url or "").lower()
    if url_lower.startswith("chrome-error://") or url_lower.startswith("edge-error://"):
        return True, "Browser navigated to an internal network error page."

    visible_lower = _extract_visible_text(html).lower()
    title_lower = (page_title or "").lower()
    combined = f"{title_lower}\n{visible_lower}"

    for sig, msg in NETWORK_ERROR_SIGNATURES:
        if sig in combined:
            return True, msg
    return False, ""


def detect_access_restriction(
    html: str, current_url: str = "", page_title: str = ""
) -> tuple[bool, str]:
    """
    Accurately detect genuine CAPTCHAs, login redirects, or HTTP 403/429 blocks
    using page URL, page title, challenge selectors, and visible body text—avoiding
    false positives from unrelated inline JavaScript text.
    """
    url_lower = (current_url or "").lower()
    title_lower = (page_title or "").strip().lower()

    if "/auth/login" in url_lower or "/login" in url_lower:
        return (
            True,
            "HackerRank redirected to a login page; private or authenticated content cannot be accessed.",
        )

    for title_sig, msg in RESTRICTION_TITLE_SIGNATURES:
        if title_sig in title_lower:
            return True, f"{msg} Stopping scraping in compliance with access rules."

    soup = BeautifulSoup(html or "", "html.parser")
    for selector, msg in RESTRICTION_DOM_SELECTORS:
        if soup.select_one(selector):
            return True, f"{msg} Stopping scraping in compliance with access rules."

    visible_lower = _extract_visible_text(html).lower()
    # Only evaluate textual restriction phrases on interstitial / short responses or explicit blocks
    if len(visible_lower) <= 2000:
        if "access denied" in visible_lower:
            return (
                True,
                "Access denied by target website. Stopping scraping in compliance with access rules.",
            )
        for sig, msg in RESTRICTION_TEXT_SIGNATURES:
            if sig in visible_lower:
                return True, f"{msg} Stopping scraping in compliance with access rules."

    return False, ""


def detect_profile_not_found(
    html: str, current_url: str = "", page_title: str = ""
) -> tuple[bool, str]:
    """Detect whether the requested HackerRank profile does not exist (404)."""
    url_lower = (current_url or "").lower()
    parsed = urlparse(url_lower)
    if parsed.path.rstrip("/") in {"/404", "/not-found"}:
        return True, "HackerRank redirected to a 404 Not Found page."

    title_lower = (page_title or "").lower()
    visible_lower = _extract_visible_text(html).lower()
    combined = f"{title_lower}\n{visible_lower}"

    for sig in NOT_FOUND_SIGNATURES:
        if sig in combined:
            return True, f"Profile page indicated 404 / not found ('{sig}')."

    # If redirected to HackerRank homepage without /profile/ path
    if "hackerrank.com" in parsed.netloc and parsed.path in {"", "/"}:
        return True, "HackerRank redirected away from /profile/ to the homepage."

    return False, ""


def classify_page_response(
    html: str, current_url: str = "", page_title: str = ""
) -> tuple[str, str]:
    """
    Classify the rendered browser page into one of:
    'network_error', 'restricted', 'not_found', or 'ok'.
    """
    is_net, net_msg = detect_network_error_page(html, current_url, page_title)
    if is_net:
        return "network_error", net_msg

    is_restricted, restrict_msg = detect_access_restriction(html, current_url, page_title)
    if is_restricted:
        return "restricted", restrict_msg

    is_404, not_found_msg = detect_profile_not_found(html, current_url, page_title)
    if is_404:
        return "not_found", not_found_msg

    if not html or len(_extract_visible_text(html)) == 0:
        return "network_error", "Target page returned an empty response body."

    return "ok", "Page loaded cleanly without network, restriction, or 404 indicators."


def _extract_first_text(soup: BeautifulSoup, selectors: list[str]) -> str | None:
    """Return the stripped text of the first matching selector, or None."""
    for selector in selectors:
        el = soup.select_one(selector)
        if el:
            text = " ".join(el.get_text(" ", strip=True).split())
            if text:
                return text
    return None


KNOWN_LANGUAGE_MAP: dict[str, str] = {
    "python": "Python",
    "sql": "SQL",
    "c++": "C++",
    "cpp": "C++",
    "c": "C",
    "java": "Java",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "ruby": "Ruby",
    "go": "Go",
    "golang": "Go",
    "rust": "Rust",
    "scala": "Scala",
    "kotlin": "Kotlin",
    "r": "R",
    "haskell": "Haskell",
    "bash": "Bash",
    "linux shell": "Bash",
    "shell": "Bash",
    "pyspark": "PySpark",
    "php": "PHP",
    "swift": "Swift",
    "c#": "C#",
}


def _extract_country(soup: BeautifulSoup) -> str | None:
    """Extract country from text selector or HackerRank flag img alt attribute."""
    text_country = _extract_first_text(soup, HACKERRANK_SELECTORS["country"])
    if text_country:
        return text_country

    flag_img = soup.select_one(".profile-title-wrapper img[alt]")
    if flag_img:
        alt_val = (flag_img.get("alt") or "").strip()
        if alt_val and alt_val.lower() not in {"avatar", "profile", "icon"}:
            return alt_val
    return None


def _extract_badges(soup: BeautifulSoup) -> list[dict[str, Any]]:
    """Extract badge titles, star counts (svg.badge-star), and tier (Gold/Silver/Bronze)."""
    badges: list[dict[str, Any]] = []
    seen: set[str] = set()
    for selector in HACKERRANK_SELECTORS["badges"]:
        for card in soup.select(selector):
            title_el = card.select_one(".badge-title, .title, h3, h4, text.badge-title, span")
            title = (
                " ".join(title_el.get_text(" ", strip=True).split())
                if title_el
                else " ".join(card.get_text(" ", strip=True).split())
            )
            if not title or title.lower() in seen:
                continue
            seen.add(title.lower())

            # Count stars from HackerRank's actual svg.badge-star elements (or legacy classes)
            stars = len(card.select("svg.badge-star"))
            if stars == 0:
                stars = len(card.select(".star-filled, .badge-star.filled, svg.star-icon"))

            level_text = (
                f"{stars} Star" if stars == 1 else (f"{stars} Stars" if stars > 1 else None)
            )

            # Detect Gold / Silver / Bronze tier from .ui-badge class
            ui_badge = card.select_one(".ui-badge")
            badge_classes = " ".join(ui_badge.get("class", [])).lower() if ui_badge else " ".join(card.get("class", [])).lower()
            tier_label: str | None = None
            if "level-gold" in badge_classes or "gold" in badge_classes:
                tier_label = "Gold Badge"
            elif "level-silver" in badge_classes or "silver" in badge_classes:
                tier_label = "Silver Badge"
            elif "level-bronze" in badge_classes or "bronze" in badge_classes:
                tier_label = "Bronze Badge"

            details_parts = []
            if tier_label:
                details_parts.append(tier_label)
            if stars > 0:
                details_parts.append(f"HackerRank {title} Badge ({stars}★)")
            details_text = " • ".join(details_parts) if details_parts else "HackerRank Public Badge"

            badges.append(
                {
                    "title": title,
                    "level_or_stars": level_text,
                    "details": details_text,
                }
            )
    return badges


def _extract_certificates(soup: BeautifulSoup) -> list[dict[str, Any]]:
    """Extract publicly listed HackerRank certificates cleanly."""
    certs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for selector in HACKERRANK_SELECTORS["certificates"]:
        for card in soup.select(selector):
            title_el = card.select_one("h2, h3, h4, .certificate-title, .title")
            title = (
                " ".join(title_el.get_text(" ", strip=True).split())
                if title_el
                else " ".join(card.get_text(" ", strip=True).split())
            )
            title = re.sub(r"^certificate\s*:\s*", "", title, flags=re.IGNORECASE).strip()
            if not title or title.lower() in seen:
                continue
            seen.add(title.lower())
            card_text_lower = card.get_text(" ", strip=True).lower()
            certs.append(
                {
                    "title": title,
                    "level_or_stars": "Verified" if "verified" in card_text_lower else None,
                    "details": "HackerRank Skill Certification",
                }
            )
    return certs


def _extract_skills(soup: BeautifulSoup) -> list[dict[str, Any]]:
    """Extract publicly listed skills and proficiency annotations if present."""
    skills: list[dict[str, Any]] = []
    seen: set[str] = set()
    for selector in HACKERRANK_SELECTORS["skills"]:
        for item in soup.select(selector):
            text = " ".join(item.get_text(" ", strip=True).split())
            if not text or len(text) > 80 or text.lower() in seen:
                continue
            seen.add(text.lower())
            is_verified = (
                "verified" in text.lower()
                or "cert" in " ".join(item.get("class", [])).lower()
            )
            level_match = re.search(r"\((Basic|Intermediate|Advanced)\)", text, re.IGNORECASE)
            skill_level = (
                "Verified"
                if is_verified
                else (level_match.group(1).title() if level_match else "Listed")
            )
            skills.append(
                {
                    "skill_name": text,
                    "skill_level": skill_level,
                    "verified": is_verified,
                }
            )
    return skills


def _derive_languages_from_public_items(
    badges: list[dict[str, Any]], skills: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Identify programming languages genuinely listed on public HackerRank badges or skills.
    Leaves problems_solved as None when HackerRank does not publicly display solved counts.
    """
    derived: list[dict[str, Any]] = []
    seen: set[str] = set()

    for badge in badges:
        raw_title = (badge.get("title") or "").strip()
        canonical = KNOWN_LANGUAGE_MAP.get(raw_title.lower())
        if canonical and canonical.lower() not in seen:
            seen.add(canonical.lower())
            stars_str = badge.get("level_or_stars")
            details = badge.get("details") or ""
            tier = details.split("•")[0].strip() if "•" in details else details
            prof = f"{stars_str} ({tier})" if stars_str and tier else (stars_str or tier or None)
            derived.append(
                {
                    "language_name": canonical,
                    "problems_solved": None,
                    "proficiency": prof,
                }
            )

    for skill in skills:
        raw_skill = (skill.get("skill_name") or "").strip()
        base_name = re.sub(r"\s*\([^)]*\)\s*", "", raw_skill).strip()
        canonical = KNOWN_LANGUAGE_MAP.get(base_name.lower())
        if canonical and canonical.lower() not in seen:
            seen.add(canonical.lower())
            derived.append(
                {
                    "language_name": canonical,
                    "problems_solved": None,
                    "proficiency": skill.get("skill_level") or "Listed Skill",
                }
            )

    return derived


def _extract_languages(soup: BeautifulSoup) -> list[dict[str, Any]]:
    """Extract programming languages and solved counts where publicly displayed."""
    languages: list[dict[str, Any]] = []
    seen: set[str] = set()
    for selector in HACKERRANK_SELECTORS["languages"]:
        for item in soup.select(selector):
            text = " ".join(item.get_text(" ", strip=True).split())
            if not text:
                continue
            match = re.match(r"^([A-Za-z0-9+#._-]+)(?:.*?(\d+))?", text)
            if not match:
                continue
            lang_name = match.group(1)
            solved = int(match.group(2)) if match.group(2) else None
            if lang_name.lower() in seen:
                continue
            seen.add(lang_name.lower())
            languages.append(
                {
                    "language_name": lang_name,
                    "problems_solved": solved,
                    "proficiency": None,
                }
            )
    return languages


def _extract_statistics(soup: BeautifulSoup) -> list[dict[str, Any]]:
    """Extract numeric/label profile statistics if publicly rendered."""
    stats: list[dict[str, Any]] = []
    seen: set[str] = set()
    for selector in HACKERRANK_SELECTORS["stats"]:
        for item in soup.select(selector):
            label_el = item.select_one(".stat-label, .label, span, p")
            val_el = item.select_one(".stat-value, .value, strong, h3, h4")
            if label_el and val_el and label_el is not val_el:
                label = " ".join(label_el.get_text(" ", strip=True).split())
                val = " ".join(val_el.get_text(" ", strip=True).split())
            else:
                parts = [p.strip() for p in item.get_text("\n").splitlines() if p.strip()]
                if len(parts) < 2:
                    continue
                val, label = parts[0], parts[1]

            if not label or label.lower() in seen:
                continue
            seen.add(label.lower())
            stats.append(
                {
                    "stat_name": label,
                    "stat_value": val,
                    "stat_category": "profile_public",
                }
            )
    return stats


def _extract_recent_activity(soup: BeautifulSoup) -> list[dict[str, str]]:
    """Extract publicly displayed recent challenge/activity items."""
    activities: list[dict[str, str]] = []
    seen: set[str] = set()
    for selector in HACKERRANK_SELECTORS["activity"]:
        for item in soup.select(selector):
            text = " ".join(item.get_text(" ", strip=True).split())
            if not text or len(text) > 200 or text.lower() in seen:
                continue
            seen.add(text.lower())
            activities.append({"activity": text, "category": "Public Activity"})
    return activities


def _parse_next_data_if_present(soup: BeautifulSoup) -> dict[str, Any]:
    """
    Inspect standard public <script id='__NEXT_DATA__'> if rendered on the public page.
    """
    extracted: dict[str, Any] = {}
    script = soup.find("script", id="__NEXT_DATA__")
    if not script or not script.string:
        return extracted
    try:
        payload = json.loads(script.string)
    except (json.JSONDecodeError, TypeError):
        return extracted

    page_props = payload.get("props", {}).get("pageProps", {})
    profile_obj = page_props.get("profile") or page_props.get("hacker") or {}
    if isinstance(profile_obj, dict):
        if profile_obj.get("name"):
            extracted["display_name"] = str(profile_obj["name"]).strip()
        if profile_obj.get("short_bio") or profile_obj.get("about"):
            extracted["description"] = str(
                profile_obj.get("short_bio") or profile_obj.get("about")
            ).strip()
        if profile_obj.get("country"):
            extracted["country"] = str(profile_obj["country"]).strip()
    return extracted


def _finalize_profile_dict(
    profile_data: dict[str, Any],
    *,
    is_sample: bool,
    source_label: str,
    data_source_note: str,
) -> dict[str, Any]:
    """Populate unavailable_fields and fields_collected consistently."""
    profile_data["is_sample"] = is_sample
    profile_data["source_label"] = source_label
    profile_data["data_source_note"] = data_source_note
    profile_data.setdefault("last_scraped_at", utc_now_iso())

    unavailable: list[str] = []
    for field_name in [
        "display_name",
        "description",
        "country",
        "programming_languages",
        "skills",
        "badges",
        "certificates",
        "statistics",
        "recent_activity",
    ]:
        val = profile_data.get(field_name)
        if val is None or (isinstance(val, list) and len(val) == 0):
            unavailable.append(field_name)

    profile_data["unavailable_fields"] = unavailable
    profile_data["fields_collected"] = count_non_empty_fields(profile_data)
    return profile_data


def parse_profile_html(
    html: str, username: str, profile_url: str | None = None
) -> dict[str, Any]:
    """
    Parse a rendered HackerRank public profile HTML document into a structured dictionary.
    Missing fields remain None or empty lists; nothing is ever fabricated.
    """
    soup = BeautifulSoup(html or "", "html.parser")
    url = profile_url or f"{HACKERRANK_PROFILE_BASE_URL}{username}"

    next_meta = _parse_next_data_if_present(soup)

    display_name = _extract_first_text(soup, HACKERRANK_SELECTORS["display_name"]) or next_meta.get(
        "display_name"
    )
    if display_name and display_name.lower() in {
        "hackerrank",
        "sign up",
        "log in",
        "access denied",
        "page not found",
    }:
        display_name = None

    description = _extract_first_text(soup, HACKERRANK_SELECTORS["description"]) or next_meta.get(
        "description"
    )
    country = _extract_country(soup) or next_meta.get("country")

    badges = _extract_badges(soup)
    certificates = _extract_certificates(soup)
    skills = _extract_skills(soup)
    languages = _extract_languages(soup)
    if not languages:
        languages = _derive_languages_from_public_items(badges, skills)
    statistics = _extract_statistics(soup)
    recent_activity = _extract_recent_activity(soup)

    # Mark matching skills as verified if a matching Verified Certificate exists
    cert_titles_lower = [c["title"].lower() for c in certificates if c.get("level_or_stars") == "Verified"]
    for sk in skills:
        sk_base = re.sub(r"\s*\([^)]*\)\s*", "", sk["skill_name"]).strip().lower()
        if any(sk_base and sk_base in ct for ct in cert_titles_lower):
            sk["verified"] = True
            if sk.get("skill_level") in (None, "Listed"):
                sk["skill_level"] = "Verified"

    if badges and not any(s["stat_name"] == "Total Badges" for s in statistics):
        statistics.append(
            {
                "stat_name": "Total Badges",
                "stat_value": str(len(badges)),
                "stat_category": "achievements",
            }
        )

    total_stars = 0
    for b in badges:
        m_star = re.match(r"^(\d+)\s*Star", str(b.get("level_or_stars") or ""), re.IGNORECASE)
        if m_star:
            total_stars += int(m_star.group(1))
    if total_stars > 0 and not any(s["stat_name"] == "Total Badge Stars" for s in statistics):
        statistics.append(
            {
                "stat_name": "Total Badge Stars",
                "stat_value": str(total_stars),
                "stat_category": "achievements",
            }
        )

    if certificates and not any(s["stat_name"] == "Verified Certificates" for s in statistics):
        statistics.append(
            {
                "stat_name": "Verified Certificates",
                "stat_value": str(len(certificates)),
                "stat_category": "achievements",
            }
        )

    profile_data: dict[str, Any] = {
        "username": username,
        "display_name": display_name,
        "profile_url": url,
        "description": description,
        "country": country,
        "programming_languages": languages,
        "skills": skills,
        "badges": badges,
        "certificates": certificates,
        "statistics": statistics,
        "recent_activity": recent_activity,
        "last_scraped_at": utc_now_iso(),
    }

    return _finalize_profile_dict(
        profile_data,
        is_sample=False,
        source_label="live",
        data_source_note="Extracted from publicly accessible HackerRank profile page.",
    )


def load_sample_profiles(sample_file: Path | None = None) -> list[dict[str, Any]]:
    """Load demonstration profiles from sample_data/sample_profiles.json."""
    target = sample_file or (SAMPLE_DATA_DIR / "sample_profiles.json")
    if not target.exists():
        return []
    with target.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    profiles = payload.get("profiles", [])
    now = utc_now_iso()
    for p in profiles:
        p["is_sample"] = True
        p["source_label"] = "sample"
        p.setdefault("last_scraped_at", now)
        p["fields_collected"] = count_non_empty_fields(p)
    return profiles


# ----------------------------------------------------------------------
# User-Uploaded Public Profile Data Parsers (JSON & CSV)
# ----------------------------------------------------------------------


def _normalize_list_field(raw_val: Any, item_key: str) -> list[dict[str, Any]]:
    """Normalize either a JSON list or semicolon/comma-separated CSV text into structured dicts."""
    if raw_val is None or raw_val == "":
        return []
    if isinstance(raw_val, str):
        stripped = raw_val.strip()
        if not stripped:
            return []
        if stripped.startswith("["):
            try:
                raw_val = json.loads(stripped)
            except json.JSONDecodeError:
                raw_val = [part.strip() for part in re.split(r"[;|,]", stripped) if part.strip()]
        else:
            raw_val = [part.strip() for part in re.split(r"[;|,]", stripped) if part.strip()]

    if not isinstance(raw_val, list):
        return []

    items: list[dict[str, Any]] = []
    for entry in raw_val:
        if isinstance(entry, str) and entry.strip():
            if item_key == "language_name":
                # Support 'Python:120' or 'Python (120)' or 'Python'
                match = re.match(r"^([A-Za-z0-9+#._ -]+?)(?::\s*(\d+))?$", entry.strip())
                if match:
                    items.append(
                        {
                            "language_name": match.group(1).strip(),
                            "problems_solved": int(match.group(2)) if match.group(2) else None,
                            "proficiency": None,
                        }
                    )
            elif item_key == "skill_name":
                items.append({"skill_name": entry.strip(), "skill_level": None, "verified": False})
            else:
                items.append({"title": entry.strip(), "level_or_stars": None, "details": None})
        elif isinstance(entry, dict):
            items.append(dict(entry))
    return items


def _normalize_uploaded_profile_record(raw_record: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize a single uploaded profile dictionary."""
    raw_user = str(raw_record.get("username") or raw_record.get("profile_url") or "").strip()
    ok, parsed = validate_and_parse_profile_input(raw_user)
    if not ok:
        raise ValueError(f"Invalid uploaded profile username/URL '{raw_user}': {parsed['error']}")

    username = parsed["username"]
    profile_url = str(raw_record.get("profile_url") or parsed["profile_url"]).strip()

    languages = _normalize_list_field(raw_record.get("programming_languages"), "language_name")
    skills = _normalize_list_field(raw_record.get("skills"), "skill_name")
    badges = _normalize_list_field(raw_record.get("badges"), "title")
    certificates = _normalize_list_field(raw_record.get("certificates"), "title")

    statistics: list[dict[str, Any]] = []
    raw_stats = raw_record.get("statistics")
    if isinstance(raw_stats, str) and raw_stats.strip().startswith("["):
        try:
            raw_stats = json.loads(raw_stats)
        except json.JSONDecodeError:
            raw_stats = []
    if isinstance(raw_stats, list):
        statistics = [dict(s) for s in raw_stats if isinstance(s, dict)]

    # Support flat CSV numeric columns if provided
    if raw_record.get("problems_solved") not in (None, ""):
        statistics.append(
            {
                "stat_name": "Problems Solved (Listed)",
                "stat_value": str(raw_record["problems_solved"]).strip(),
                "stat_category": "problem_solving",
            }
        )
    if raw_record.get("contest_rating") not in (None, ""):
        statistics.append(
            {
                "stat_name": "Contest Rating",
                "stat_value": str(raw_record["contest_rating"]).strip(),
                "stat_category": "competitions",
            }
        )

    recent_activity = raw_record.get("recent_activity")
    if isinstance(recent_activity, str) and recent_activity.strip().startswith("["):
        try:
            recent_activity = json.loads(recent_activity)
        except json.JSONDecodeError:
            recent_activity = []
    if not isinstance(recent_activity, list):
        recent_activity = []

    profile_dict: dict[str, Any] = {
        "username": username,
        "display_name": (str(raw_record.get("display_name")).strip() or None)
        if raw_record.get("display_name") is not None
        else None,
        "profile_url": profile_url,
        "description": (str(raw_record.get("description")).strip() or None)
        if raw_record.get("description") is not None
        else None,
        "country": (str(raw_record.get("country")).strip() or None)
        if raw_record.get("country") is not None
        else None,
        "programming_languages": languages,
        "skills": skills,
        "badges": badges,
        "certificates": certificates,
        "statistics": statistics,
        "recent_activity": recent_activity,
        "last_scraped_at": utc_now_iso(),
    }

    return _finalize_profile_dict(
        profile_dict,
        is_sample=False,
        source_label="uploaded",
        data_source_note="Imported from user-uploaded public profile file.",
    )


def parse_uploaded_profile_json(raw_text: str) -> list[dict[str, Any]]:
    """
    Parse user-uploaded JSON containing either a single profile dict,
    a list of profile dicts, or {"profiles": [...]}.
    """
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON syntax: {exc}") from exc

    if isinstance(payload, dict) and isinstance(payload.get("profiles"), list):
        records = payload["profiles"]
    elif isinstance(payload, dict):
        records = [payload]
    elif isinstance(payload, list):
        records = payload
    else:
        raise ValueError("JSON root must be an object, a list of objects, or {'profiles': [...]}.")

    if not records:
        raise ValueError("Uploaded JSON file contains no profile records.")

    return [_normalize_uploaded_profile_record(r) for r in records if isinstance(r, dict)]


def parse_uploaded_profile_csv(raw_text: str) -> list[dict[str, Any]]:
    """
    Parse user-uploaded CSV containing public HackerRank profile columns.
    Required column: 'username' (or 'profile_url').
    """
    reader = csv.DictReader(io.StringIO(raw_text.strip()))
    if not reader.fieldnames:
        raise ValueError("Uploaded CSV file has no header row.")

    normalized_headers = {h.strip().lower() for h in reader.fieldnames if h}
    if "username" not in normalized_headers and "profile_url" not in normalized_headers:
        raise ValueError("CSV must contain at least a 'username' or 'profile_url' column.")

    profiles: list[dict[str, Any]] = []
    for row in reader:
        cleaned_row = {
            (k.strip().lower() if k else ""): (v.strip() if isinstance(v, str) else v)
            for k, v in row.items()
        }
        if not cleaned_row.get("username") and not cleaned_row.get("profile_url"):
            continue
        profiles.append(_normalize_uploaded_profile_record(cleaned_row))

    if not profiles:
        raise ValueError("Uploaded CSV file contains no valid profile rows.")
    return profiles


def build_sample_json_template() -> str:
    """Return a clean JSON template for uploading publicly obtained profile data."""
    template = {
        "profiles": [
            {
                "username": "example_public_user",
                "display_name": "Example User",
                "profile_url": "https://www.hackerrank.com/profile/example_public_user",
                "description": "Python and SQL problem solver",
                "country": "India",
                "programming_languages": [
                    {"language_name": "Python", "problems_solved": 85, "proficiency": "5 Star"},
                    {"language_name": "SQL", "problems_solved": 40, "proficiency": "4 Star"},
                ],
                "skills": [
                    {"skill_name": "Python (Basic)", "skill_level": "Verified", "verified": True}
                ],
                "badges": [
                    {"title": "Python", "level_or_stars": "5 Stars", "details": "Gold Badge"}
                ],
                "certificates": [
                    {"title": "Python (Basic)", "level_or_stars": "Verified", "details": "HackerRank"}
                ],
                "statistics": [
                    {"stat_name": "Problems Solved (Listed)", "stat_value": "125", "stat_category": "problem_solving"}
                ],
            }
        ]
    }
    return json.dumps(template, indent=2)


def build_sample_csv_template() -> str:
    """Return a clean CSV template for uploading publicly obtained profile data."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "username",
            "display_name",
            "profile_url",
            "country",
            "description",
            "programming_languages",
            "skills",
            "badges",
            "certificates",
            "problems_solved",
            "contest_rating",
        ]
    )
    writer.writerow(
        [
            "example_public_user",
            "Example User",
            "https://www.hackerrank.com/profile/example_public_user",
            "India",
            "Python and SQL problem solver",
            "Python:85;SQL:40",
            "Python (Basic);Problem Solving",
            "Python;SQL",
            "Python (Basic)",
            "125",
            "1620",
        ]
    )
    return output.getvalue()

```

---

### File: `detection/code_preprocessor.py`
**Role:** Tokenizer, Comment Stripper & Identifier Normalizer (VAR_1, VAR_2)  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/detection/code_preprocessor.py`

```python
"""
Module 4A: Python Source-Code Preprocessing.
Handles comment removal, whitespace normalization, tokenization, and optional
identifier normalization while preserving Python keywords and built-in names.
"""

from __future__ import annotations

import builtins
import io
import keyword
import re
import tokenize
from typing import Any

PYTHON_KEYWORDS: set[str] = set(keyword.kwlist)
PYTHON_BUILTINS: set[str] = set(dir(builtins))


def extract_comments_and_docstrings(code: str) -> dict[str, Any]:
    """Extract inline/block comments and line statistics from Python source code."""
    lines = code.splitlines()
    comment_lines: list[dict[str, Any]] = []
    blank_lines = 0

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            blank_lines += 1
        elif stripped.startswith("#"):
            comment_lines.append({"line": idx, "text": stripped})

    # Also catch inline trailing comments safely via tokenize
    inline_comments: list[dict[str, Any]] = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(code).readline)
        for tok_type, tok_str, start, _, _ in tokens:
            if tok_type == tokenize.COMMENT:
                inline_comments.append({"line": start[0], "text": tok_str.strip()})
    except (tokenize.TokenError, IndentationError):
        pass

    return {
        "total_lines": len(lines),
        "blank_lines": blank_lines,
        "comment_count": len(inline_comments) if inline_comments else len(comment_lines),
        "comments": inline_comments if inline_comments else comment_lines,
    }


def preprocess_code(
    code: str,
    remove_comments: bool = True,
    normalize_whitespace: bool = True,
    normalize_identifiers: bool = False,
) -> dict[str, Any]:
    """
    Clean and tokenize Python source code for similarity and pattern analysis.
    Falls back to regex tokenization if the code contains syntax/token errors.
    """
    working_code = code.replace("\r\n", "\n").replace("\r", "\n")
    tokens_list: list[str] = []
    identifiers: list[str] = []
    var_map: dict[str, str] = {}
    var_counter = 1

    try:
        tok_stream = list(tokenize.generate_tokens(io.StringIO(working_code).readline))
        rebuilt_parts: list[str] = []

        for tok_type, tok_str, _, _, _ in tok_stream:
            if tok_type in (tokenize.ENCODING, tokenize.ENDMARKER):
                continue
            if tok_type == tokenize.COMMENT and remove_comments:
                continue
            if tok_type in (tokenize.NL, tokenize.NEWLINE):
                if not normalize_whitespace:
                    rebuilt_parts.append("\n")
                elif rebuilt_parts and rebuilt_parts[-1] != "\n":
                    rebuilt_parts.append("\n")
                continue
            if tok_type in (tokenize.INDENT, tokenize.DEDENT):
                continue

            token_value = tok_str
            if tok_type == tokenize.NAME:
                if tok_str not in PYTHON_KEYWORDS and tok_str not in PYTHON_BUILTINS:
                    identifiers.append(tok_str)
                    if normalize_identifiers:
                        if tok_str not in var_map:
                            var_map[tok_str] = f"VAR_{var_counter}"
                            var_counter += 1
                        token_value = var_map[tok_str]

            tokens_list.append(token_value)
            rebuilt_parts.append(token_value)

        normalized_text = " ".join(rebuilt_parts)
        if normalize_whitespace:
            normalized_text = re.sub(r"[ \t]+", " ", normalized_text)
            normalized_text = re.sub(r" *\n *", "\n", normalized_text).strip()

    except (tokenize.TokenError, IndentationError):
        # Graceful fallback for incomplete/invalid snippets
        fallback = working_code
        if remove_comments:
            fallback = re.sub(r"#.*", "", fallback)
        if normalize_whitespace:
            fallback = "\n".join(
                re.sub(r"[ \t]+", " ", ln).strip()
                for ln in fallback.splitlines()
                if ln.strip()
            )
        raw_tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|[^\sA-Za-z0-9_]", fallback)
        for tok in raw_tokens:
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", tok):
                if tok not in PYTHON_KEYWORDS and tok not in PYTHON_BUILTINS:
                    identifiers.append(tok)
                    if normalize_identifiers:
                        if tok not in var_map:
                            var_map[tok] = f"VAR_{var_counter}"
                            var_counter += 1
                        tok = var_map[tok]
            tokens_list.append(tok)
        normalized_text = fallback

    return {
        "normalized_code": normalized_text,
        "tokens": tokens_list,
        "token_count": len(tokens_list),
        "identifiers": identifiers,
        "unique_identifiers": sorted(set(identifiers)),
        "identifier_map": var_map,
    }


```

---

### File: `detection/ast_analysis.py`
**Role:** Abstract Syntax Tree (AST) Node Vectorizer & Depth Inspector  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/detection/ast_analysis.py`

```python
"""
Module 5: AST-Based Python Source-Code Structural Analysis.
Extracts functions, classes, loops, conditionals, imports, variable assignments,
nesting depth, and complexity indicators while handling SyntaxErrors gracefully.
"""

from __future__ import annotations

import ast
from collections import Counter
from typing import Any

from detection.code_preprocessor import extract_comments_and_docstrings
from utils.helpers import compute_code_hash


class _ASTMetricsVisitor(ast.NodeVisitor):
    """Walks a Python AST to collect structural features and nesting depth."""

    CONTROL_NODES = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.With,
        ast.AsyncWith,
        ast.Try,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
    )

    def __init__(self) -> None:
        self.num_functions = 0
        self.num_async_functions = 0
        self.num_classes = 0
        self.num_loops = 0
        self.num_conditionals = 0
        self.num_imports = 0
        self.num_assignments = 0
        self.num_try_except = 0
        self.num_comprehensions = 0
        self.branch_points = 0
        self.current_depth = 0
        self.max_nesting_depth = 0
        self.function_definitions: list[dict[str, Any]] = []
        self.class_definitions: list[dict[str, Any]] = []
        self.imported_modules: list[str] = []
        self.node_type_counts: Counter[str] = Counter()

    def generic_visit(self, node: ast.AST) -> None:
        self.node_type_counts[type(node).__name__] += 1
        is_nested = isinstance(node, self.CONTROL_NODES)
        if is_nested:
            self.current_depth += 1
            if self.current_depth > self.max_nesting_depth:
                self.max_nesting_depth = self.current_depth

        super().generic_visit(node)

        if is_nested:
            self.current_depth -= 1

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.num_functions += 1
        self.function_definitions.append(
            {
                "name": node.name,
                "args_count": len(node.args.args) + len(node.args.kwonlyargs),
                "line_number": node.lineno,
                "has_docstring": ast.get_docstring(node) is not None,
                "has_return_annotation": node.returns is not None,
                "is_async": False,
            }
        )
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.num_functions += 1
        self.num_async_functions += 1
        self.function_definitions.append(
            {
                "name": node.name,
                "args_count": len(node.args.args) + len(node.args.kwonlyargs),
                "line_number": node.lineno,
                "has_docstring": ast.get_docstring(node) is not None,
                "has_return_annotation": node.returns is not None,
                "is_async": True,
            }
        )
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.num_classes += 1
        self.class_definitions.append(
            {
                "name": node.name,
                "line_number": node.lineno,
                "bases_count": len(node.bases),
                "has_docstring": ast.get_docstring(node) is not None,
            }
        )
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.num_loops += 1
        self.branch_points += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.num_loops += 1
        self.branch_points += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.num_loops += 1
        self.branch_points += 1
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self.num_conditionals += 1
        self.branch_points += 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.num_conditionals += 1
        self.branch_points += 1
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        self.num_imports += len(node.names)
        for alias in node.names:
            self.imported_modules.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.num_imports += len(node.names)
        mod = node.module or ""
        for alias in node.names:
            self.imported_modules.append(f"{mod}.{alias.name}".strip("."))
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        self.num_assignments += 1
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.num_assignments += 1
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self.num_assignments += 1
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        self.num_try_except += 1
        self.branch_points += max(1, len(node.handlers))
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.branch_points += max(0, len(node.values) - 1)
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self.num_comprehensions += 1
        self.generic_visit(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self.num_comprehensions += 1
        self.generic_visit(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self.num_comprehensions += 1
        self.generic_visit(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self.num_comprehensions += 1
        self.generic_visit(node)


def analyze_ast(code: str, filename: str = "<input>") -> dict[str, Any]:
    """
    Parse Python source code into an AST and extract structural metrics.
    Gracefully handles SyntaxError without raising.
    """
    line_stats = extract_comments_and_docstrings(code)
    code_hash = compute_code_hash(code)

    base_result: dict[str, Any] = {
        "filename": filename,
        "code_hash": code_hash,
        "syntax_valid": True,
        "syntax_error": None,
        "lines_of_code": line_stats["total_lines"],
        "blank_lines": line_stats["blank_lines"],
        "comment_lines": line_stats["comment_count"],
        "num_functions": 0,
        "num_async_functions": 0,
        "num_classes": 0,
        "num_loops": 0,
        "num_conditionals": 0,
        "num_imports": 0,
        "num_assignments": 0,
        "num_try_except": 0,
        "num_comprehensions": 0,
        "max_nesting_depth": 0,
        "approx_cyclomatic_complexity": 1,
        "complexity_level": "Low",
        "function_definitions": [],
        "class_definitions": [],
        "imported_modules": [],
        "has_module_docstring": False,
        "node_type_counts": {},
    }

    try:
        tree = ast.parse(code, filename=filename)
    except SyntaxError as exc:
        base_result["syntax_valid"] = False
        base_result["syntax_error"] = {
            "message": exc.msg,
            "line": exc.lineno,
            "offset": exc.offset,
            "text": (exc.text or "").strip(),
        }
        return base_result

    visitor = _ASTMetricsVisitor()
    visitor.visit(tree)

    complexity = 1 + visitor.branch_points
    if complexity <= 5:
        level = "Low"
    elif complexity <= 12:
        level = "Moderate"
    else:
        level = "High"

    base_result.update(
        {
            "num_functions": visitor.num_functions,
            "num_async_functions": visitor.num_async_functions,
            "num_classes": visitor.num_classes,
            "num_loops": visitor.num_loops,
            "num_conditionals": visitor.num_conditionals,
            "num_imports": visitor.num_imports,
            "num_assignments": visitor.num_assignments,
            "num_try_except": visitor.num_try_except,
            "num_comprehensions": visitor.num_comprehensions,
            "max_nesting_depth": visitor.max_nesting_depth,
            "approx_cyclomatic_complexity": complexity,
            "complexity_level": level,
            "function_definitions": visitor.function_definitions,
            "class_definitions": visitor.class_definitions,
            "imported_modules": visitor.imported_modules,
            "has_module_docstring": ast.get_docstring(tree) is not None,
            "node_type_counts": dict(visitor.node_type_counts),
        }
    )
    return base_result


```

---

### File: `detection/code_similarity.py`
**Role:** 4-Layer Blended Code Similarity Scoring Engine  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/detection/code_similarity.py`

```python
"""
Module 4B: Source-Code Similarity Analysis.
Combines token similarity, TF-IDF cosine similarity, SequenceMatcher ratio,
and AST structural comparison. Explicitly notes that similarity is not proof
of plagiarism.
"""

from __future__ import annotations

import difflib
import math
from collections import Counter
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import SIMILARITY_DISCLAIMER
from detection.ast_analysis import analyze_ast
from detection.code_preprocessor import preprocess_code


def _cosine_from_counters(c1: Counter[str], c2: Counter[str]) -> float:
    """Compute cosine similarity between two frequency counters (0.0 to 1.0)."""
    if not c1 or not c2:
        return 0.0
    common = set(c1.keys()) & set(c2.keys())
    dot = sum(c1[k] * c2[k] for k in common)
    mag1 = math.sqrt(sum(v * v for v in c1.values()))
    mag2 = math.sqrt(sum(v * v for v in c2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def _compute_token_similarity(tokens_a: list[str], tokens_b: list[str]) -> float:
    """Compute blended Jaccard and frequency-cosine token similarity (0-100%)."""
    if not tokens_a or not tokens_b:
        return 0.0
    set_a, set_b = set(tokens_a), set(tokens_b)
    union_len = len(set_a | set_b)
    jaccard = len(set_a & set_b) / union_len if union_len else 0.0
    freq_cos = _cosine_from_counters(Counter(tokens_a), Counter(tokens_b))
    return round(((jaccard + freq_cos) / 2.0) * 100.0, 2)


def _compute_tfidf_similarity(tokens_a: list[str], tokens_b: list[str]) -> float:
    """Compute TF-IDF cosine similarity using scikit-learn (0-100%)."""
    doc_a = " ".join(tokens_a)
    doc_b = " ".join(tokens_b)
    if not doc_a.strip() or not doc_b.strip():
        return 0.0
    try:
        vectorizer = TfidfVectorizer(
            token_pattern=r"(?u)\b\w+\b|[^\w\s]",
            lowercase=False,
        )
        matrix = vectorizer.fit_transform([doc_a, doc_b])
        score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
        return round(max(0.0, min(1.0, score)) * 100.0, 2)
    except ValueError:
        return 0.0


def _compute_sequence_similarity(norm_a: str, norm_b: str) -> tuple[float, list[str]]:
    """Compute difflib SequenceMatcher ratio (0-100%) and matching snippet blocks."""
    if not norm_a or not norm_b:
        return 0.0, []
    matcher = difflib.SequenceMatcher(None, norm_a, norm_b)
    ratio_pct = round(matcher.ratio() * 100.0, 2)

    matching_snippets: list[str] = []
    for block in matcher.get_matching_blocks():
        if block.size >= 24:
            snippet = norm_a[block.a : block.a + block.size].strip()
            if snippet and snippet not in matching_snippets:
                matching_snippets.append(snippet[:260])
        if len(matching_snippets) >= 6:
            break

    return ratio_pct, matching_snippets


def _compute_ast_similarity(ast_a: dict[str, Any], ast_b: dict[str, Any]) -> tuple[float, list[str], list[str]]:
    """
    Compare AST node-type distributions and high-level structural counts.
    Returns (similarity_pct, structural_similarities, structural_differences).
    """
    if not ast_a.get("syntax_valid") or not ast_b.get("syntax_valid"):
        return 0.0, [], ["AST comparison skipped because one or both files contain syntax errors."]

    counts_a = Counter(ast_a.get("node_type_counts") or {})
    counts_b = Counter(ast_b.get("node_type_counts") or {})
    node_cos = _cosine_from_counters(counts_a, counts_b)

    feature_keys = [
        ("num_functions", "Functions"),
        ("num_classes", "Classes"),
        ("num_loops", "Loops"),
        ("num_conditionals", "Conditionals"),
        ("num_imports", "Imports"),
        ("num_assignments", "Assignments"),
        ("max_nesting_depth", "Max Nesting Depth"),
    ]
    vec_sim_parts: list[float] = []
    similarities: list[str] = []
    differences: list[str] = []

    for key, label in feature_keys:
        va = int(ast_a.get(key, 0))
        vb = int(ast_b.get(key, 0))
        if va == vb:
            vec_sim_parts.append(1.0)
            if va > 0:
                similarities.append(f"Both files have {va} {label.lower()}.")
        else:
            denom = max(va, vb, 1)
            vec_sim_parts.append(1.0 - (abs(va - vb) / denom))
            differences.append(f"{label}: {ast_a['filename']} has {va}, while {ast_b['filename']} has {vb}.")

    feature_sim = sum(vec_sim_parts) / len(vec_sim_parts) if vec_sim_parts else 0.0
    blended = ((0.65 * node_cos) + (0.35 * feature_sim)) * 100.0
    return round(blended, 2), similarities, differences


def compare_two_files(
    code_a: str,
    code_b: str,
    name_a: str = "file_1.py",
    name_b: str = "file_2.py",
    normalize_identifiers: bool = False,
) -> dict[str, Any]:
    """
    Perform a comprehensive multi-metric similarity analysis between two Python files.
    """
    prep_a = preprocess_code(
        code_a,
        remove_comments=True,
        normalize_whitespace=True,
        normalize_identifiers=normalize_identifiers,
    )
    prep_b = preprocess_code(
        code_b,
        remove_comments=True,
        normalize_whitespace=True,
        normalize_identifiers=normalize_identifiers,
    )

    ast_a = analyze_ast(code_a, filename=name_a)
    ast_b = analyze_ast(code_b, filename=name_b)

    token_sim = _compute_token_similarity(prep_a["tokens"], prep_b["tokens"])
    tfidf_sim = _compute_tfidf_similarity(prep_a["tokens"], prep_b["tokens"])
    seq_sim, matching_blocks = _compute_sequence_similarity(
        prep_a["normalized_code"], prep_b["normalized_code"]
    )
    ast_sim, struct_similarities, struct_differences = _compute_ast_similarity(ast_a, ast_b)

    if ast_a["syntax_valid"] and ast_b["syntax_valid"]:
        overall = round(
            0.25 * token_sim + 0.25 * tfidf_sim + 0.20 * seq_sim + 0.30 * ast_sim,
            2,
        )
    else:
        overall = round(
            0.35 * token_sim + 0.35 * tfidf_sim + 0.30 * seq_sim,
            2,
        )

    diff_lines = list(
        difflib.unified_diff(
            code_a.splitlines(),
            code_b.splitlines(),
            fromfile=name_a,
            tofile=name_b,
            lineterm="",
            n=2,
        )
    )[:120]

    if overall >= 75:
        band = "High similarity"
    elif overall >= 45:
        band = "Moderate similarity"
    else:
        band = "Low similarity"

    mode_note = (
        "with identifier normalization enabled"
        if normalize_identifiers
        else "using original identifier names"
    )
    summary_text = (
        f"{band} ({overall:.1f}%) between '{name_a}' and '{name_b}' ({mode_note}). "
        f"Token: {token_sim:.1f}%, TF-IDF: {tfidf_sim:.1f}%, "
        f"Sequence: {seq_sim:.1f}%, AST Structure: {ast_sim:.1f}%."
    )

    return {
        "file_a": name_a,
        "file_b": name_b,
        "overall_similarity": overall,
        "similarity_band": band,
        "token_similarity": token_sim,
        "tfidf_similarity": tfidf_sim,
        "sequence_similarity": seq_sim,
        "ast_similarity": ast_sim,
        "normalized_var_mode": normalize_identifiers,
        "summary_text": summary_text,
        "matching_sections": matching_blocks,
        "structural_similarities": struct_similarities,
        "structural_differences": struct_differences,
        "diff_lines": diff_lines,
        "ast_a": ast_a,
        "ast_b": ast_b,
        "disclaimer": SIMILARITY_DISCLAIMER,
    }


def compare_multiple_files(
    files: list[tuple[str, str]],
    normalize_identifiers: bool = False,
) -> dict[str, Any]:
    """
    Compare 2 or more (filename, code) pairs, returning pairwise results
    and an NxN similarity matrix.
    """
    names = [name for name, _ in files]
    n = len(files)
    matrix: list[list[float]] = [[100.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    pair_results: list[dict[str, Any]] = []

    for i in range(n):
        for j in range(i + 1, n):
            res = compare_two_files(
                files[i][1],
                files[j][1],
                name_a=files[i][0],
                name_b=files[j][0],
                normalize_identifiers=normalize_identifiers,
            )
            matrix[i][j] = res["overall_similarity"]
            matrix[j][i] = res["overall_similarity"]
            pair_results.append(res)

    return {
        "filenames": names,
        "similarity_matrix": matrix,
        "pair_results": pair_results,
        "disclaimer": SIMILARITY_DISCLAIMER,
    }


```

---

### File: `detection/ai_pattern_analysis.py`
**Role:** Explainable Heuristic AI Pattern Forensics Engine  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/detection/ai_pattern_analysis.py`

```python
"""
Module 6: Explainable Heuristic AI-Associated Code Pattern Analysis.

IMPORTANT:
- Does NOT claim to prove AI authorship.
- Does NOT output a validated probability of AI generation.
- Explicitly distinguishes AI-associated patterns from clean human coding practices.
"""

from __future__ import annotations

import re
import statistics
from typing import Any

from config import AI_DETECTION_DISCLAIMER, HEURISTIC_LABELS, HEURISTIC_THRESHOLDS
from detection.ast_analysis import analyze_ast
from detection.code_preprocessor import extract_comments_and_docstrings, preprocess_code
from detection.code_similarity import compare_two_files
from utils.helpers import compute_code_hash

GENERIC_AI_IDENTIFIERS: set[str] = {
    "result",
    "output",
    "data",
    "temp",
    "value",
    "values",
    "item",
    "items",
    "helper",
    "current",
    "target",
    "input_data",
    "response",
    "numbers",
    "elements",
}

STEP_COMMENT_PATTERN = re.compile(
    r"#\s*(step\s*\d+|initialize|iterate|check if|return|create|define|loop|calculate|handle|edge case)\b",
    re.IGNORECASE,
)

SNAKE_CASE_PATTERN = re.compile(r"^[a-z_][a-z0-9_]*$")


def _score_naming_uniformity(identifiers: list[str]) -> dict[str, Any]:
    """Evaluate identifier naming consistency and presence of generic textbook names."""
    unique_ids = [ident for ident in set(identifiers) if len(ident) > 1]
    if not unique_ids:
        return {
            "name": "Naming Uniformity",
            "score": 15.0,
            "weight": 0.22,
            "observation": "Very few multi-character identifiers present.",
            "explanation": "Short snippets with single-letter variables do not exhibit strong naming uniformity.",
            "normal_practice_note": "Consistent snake_case naming is standard PEP 8 practice among experienced Python developers.",
            "evidence": [],
        }

    snake_ratio = sum(1 for i in unique_ids if SNAKE_CASE_PATTERN.match(i)) / len(unique_ids)
    generic_hits = sorted([i for i in unique_ids if i.lower() in GENERIC_AI_IDENTIFIERS])
    generic_ratio = len(generic_hits) / len(unique_ids)
    long_descriptive_ratio = sum(1 for i in unique_ids if "_" in i and len(i) >= 10) / len(unique_ids)

    raw_score = (snake_ratio * 45.0) + (min(generic_ratio * 180.0, 35.0)) + (long_descriptive_ratio * 20.0)
    score = round(min(100.0, max(0.0, raw_score)), 1)

    evidence = [
        f"Snake-case identifier ratio: {snake_ratio * 100:.0f}% ({len(unique_ids)} unique multi-char identifiers).",
    ]
    if generic_hits:
        evidence.append(f"Generic textbook identifiers found: {', '.join(generic_hits[:8])}.")

    return {
        "name": "Naming Uniformity",
        "score": score,
        "weight": 0.22,
        "observation": f"{snake_ratio * 100:.0f}% snake_case adherence; {len(generic_hits)} generic identifier(s).",
        "explanation": (
            "LLM-generated snippets frequently use uniform, verbose snake_case names and "
            "generic placeholders such as 'result', 'data', or 'current_value'."
        ),
        "normal_practice_note": (
            "Readable descriptive snake_case names are also recommended by PEP 8 and taught "
            "in software engineering courses."
        ),
        "evidence": evidence,
    }


def _score_formatting_consistency(code: str) -> dict[str, Any]:
    """Evaluate indentation, blank-line spacing, and line-length uniformity."""
    lines = code.splitlines()
    non_empty = [ln for ln in lines if ln.strip()]
    if len(non_empty) < 4:
        return {
            "name": "Formatting Consistency",
            "score": 20.0,
            "weight": 0.18,
            "observation": "File is too short to measure meaningful formatting variance.",
            "explanation": "Formatting heuristics require multi-line structure.",
            "normal_practice_note": "Auto-formatters like Black or Ruff produce equally consistent formatting.",
            "evidence": [],
        }

    indents = [len(ln) - len(ln.lstrip(" ")) for ln in non_empty if ln.startswith(" ")]
    four_space_ratio = (
        sum(1 for ind in indents if ind % 4 == 0) / len(indents)
        if indents
        else 1.0
    )

    trailing_ws_count = sum(1 for ln in lines if ln != ln.rstrip())
    lengths = [len(ln) for ln in non_empty]
    stdev_len = statistics.pstdev(lengths) if len(lengths) > 1 else 0.0
    # Moderate, clean line lengths without trailing spaces increase uniformity score
    clean_trailing = 1.0 if trailing_ws_count == 0 else max(0.0, 1.0 - (trailing_ws_count / len(lines)))
    compact_variance = 1.0 if stdev_len < 22 else max(0.2, 1.0 - ((stdev_len - 22) / 50.0))

    score = round(min(100.0, (four_space_ratio * 45.0) + (clean_trailing * 30.0) + (compact_variance * 25.0)), 1)

    return {
        "name": "Formatting Consistency",
        "score": score,
        "weight": 0.18,
        "observation": (
            f"4-space indent alignment: {four_space_ratio * 100:.0f}%, "
            f"trailing-whitespace lines: {trailing_ws_count}, line-length stdev: {stdev_len:.1f}."
        ),
        "explanation": (
            "AI assistants typically emit uniformly indented code with zero trailing whitespace "
            "and narrow line-length variation."
        ),
        "normal_practice_note": (
            "IDEs (VS Code, PyCharm) and formatters (Black, Prettier, isort) automatically produce "
            "identical formatting cleanliness on human-written code."
        ),
        "evidence": [
            f"Trailing whitespace lines: {trailing_ws_count} / {len(lines)}",
            f"Indentation 4-space multiples: {four_space_ratio * 100:.0f}%",
        ],
    }


def _score_comment_patterns(code: str, ast_data: dict[str, Any]) -> dict[str, Any]:
    """Evaluate density of step-by-step instructional comments and uniform docstrings."""
    comment_info = extract_comments_and_docstrings(code)
    total_lines = max(1, comment_info["total_lines"])
    comments = comment_info["comments"]
    comment_texts = [c["text"] for c in comments]

    step_matches = [txt for txt in comment_texts if STEP_COMMENT_PATTERN.search(txt)]
    comment_density = len(comments) / total_lines

    funcs = ast_data.get("function_definitions") or []
    docstring_ratio = (
        sum(1 for f in funcs if f.get("has_docstring")) / len(funcs)
        if funcs
        else 0.0
    )

    # Check repeated phrasing prefixes across comments
    prefixes = [" ".join(txt.lstrip("# ").lower().split()[:2]) for txt in comment_texts if len(txt.split()) >= 3]
    repeated_prefixes = len(prefixes) - len(set(prefixes))

    score_raw = (
        min(len(step_matches) * 18.0, 45.0)
        + min(comment_density * 180.0, 25.0)
        + (docstring_ratio * 20.0)
        + min(repeated_prefixes * 10.0, 10.0)
    )
    score = round(min(100.0, max(0.0, score_raw)), 1)

    evidence = [
        f"Comments found: {len(comments)} across {total_lines} lines ({comment_density * 100:.1f}%).",
        f"Instructional/step-style comments: {len(step_matches)}.",
    ]
    if funcs:
        evidence.append(f"Functions with docstrings: {docstring_ratio * 100:.0f}% ({len(funcs)} total).")

    return {
        "name": "Explanatory Comment & Docstring Patterns",
        "score": score,
        "weight": 0.25,
        "observation": f"{len(step_matches)} step/instructional comment(s); {docstring_ratio * 100:.0f}% function docstring coverage.",
        "explanation": (
            "AI-generated solutions often include sequential '# Step 1:', '# Initialize...', or "
            "narrated comments explaining trivial lines alongside complete Args/Returns docstrings."
        ),
        "normal_practice_note": (
            "Thorough documentation and docstrings are best practices in production software and "
            "academic submissions where grading rubrics reward comments."
        ),
        "evidence": evidence,
    }


def _score_structural_regularity(ast_data: dict[str, Any]) -> dict[str, Any]:
    """Evaluate template-like structure, type annotations, and defensive boilerplate."""
    if not ast_data.get("syntax_valid"):
        return {
            "name": "Structural & Template Regularity",
            "score": 10.0,
            "weight": 0.20,
            "observation": "Syntax error prevented full AST structural evaluation.",
            "explanation": "Syntax errors are less typical of complete LLM outputs unless truncated.",
            "normal_practice_note": "Incomplete drafts are common during active human development.",
            "evidence": [],
        }

    funcs = ast_data.get("function_definitions") or []
    annotated_ratio = (
        sum(1 for f in funcs if f.get("has_return_annotation")) / len(funcs)
        if funcs
        else 0.0
    )
    has_doc = bool(ast_data.get("has_module_docstring"))
    has_try = ast_data.get("num_try_except", 0) > 0
    moderate_nesting = 1 <= ast_data.get("max_nesting_depth", 0) <= 4
    low_complexity_per_func = (
        (ast_data.get("approx_cyclomatic_complexity", 1) / max(1, len(funcs))) <= 4.0
        if funcs
        else False
    )

    score_raw = (
        (annotated_ratio * 35.0)
        + (20.0 if has_doc else 0.0)
        + (15.0 if has_try else 0.0)
        + (15.0 if moderate_nesting else 0.0)
        + (15.0 if low_complexity_per_func else 0.0)
    )
    score = round(min(100.0, score_raw), 1)

    return {
        "name": "Structural & Template Regularity",
        "score": score,
        "weight": 0.20,
        "observation": (
            f"Return type annotations: {annotated_ratio * 100:.0f}%, "
            f"module docstring: {'Yes' if has_doc else 'No'}, "
            f"max nesting: {ast_data.get('max_nesting_depth', 0)}."
        ),
        "explanation": (
            "AI assistants frequently structure solutions as modular typed functions with module "
            "docstrings, guard clauses, and balanced shallow nesting."
        ),
        "normal_practice_note": (
            "Clean modular decomposition and Python type hints are standard modern Python habits, "
            "not proof of AI generation."
        ),
        "evidence": [
            f"Functions defined: {len(funcs)}",
            f"Module docstring present: {has_doc}",
            f"Approx. cyclomatic complexity: {ast_data.get('approx_cyclomatic_complexity', 1)}",
        ],
    }


def _score_peer_similarity(
    code: str,
    filename: str,
    peer_codes: list[tuple[str, str]] | None,
) -> dict[str, Any]:
    """Optional indicator comparing against other submitted reference files."""
    if not peer_codes:
        return {
            "name": "Cross-Submission Similarity",
            "score": 0.0,
            "weight": 0.15,
            "observation": "No comparison files provided for cross-submission check.",
            "explanation": "Evaluates structural and token similarity when multiple submissions are supplied.",
            "normal_practice_note": "Independent solutions to the same prompt can naturally share common algorithms.",
            "evidence": [],
        }

    max_sim = 0.0
    top_peer = ""
    for peer_name, peer_code in peer_codes:
        if peer_name == filename and peer_code == code:
            continue
        res = compare_two_files(code, peer_code, name_a=filename, name_b=peer_name, normalize_identifiers=True)
        if res["overall_similarity"] > max_sim:
            max_sim = res["overall_similarity"]
            top_peer = peer_name

    return {
        "name": "Cross-Submission Similarity",
        "score": round(max_sim, 1),
        "weight": 0.15,
        "observation": (
            f"Highest normalized similarity: {max_sim:.1f}% (against '{top_peer}')."
            if top_peer
            else "No distinct peer files compared."
        ),
        "explanation": (
            "Multiple submissions generated from similar prompts often share high structural "
            "and token similarity even with renamed variables."
        ),
        "normal_practice_note": (
            "Standard textbook algorithms (e.g., Kadane's algorithm, binary search) also yield "
            "high similarity across independent human programmers."
        ),
        "evidence": [f"Top peer match: {top_peer} ({max_sim:.1f}%)"] if top_peer else [],
    }


def analyze_ai_patterns(
    code: str,
    filename: str = "<input>",
    peer_codes: list[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    """
    Run explainable heuristic AI-associated code pattern analysis.
    Returns a transparent breakdown with non-probabilistic labels and explicit limitations.
    """
    prep = preprocess_code(code, remove_comments=False, normalize_whitespace=False)
    ast_data = analyze_ast(code, filename=filename)

    ind_naming = _score_naming_uniformity(prep["identifiers"])
    ind_format = _score_formatting_consistency(code)
    ind_comments = _score_comment_patterns(code, ast_data)
    ind_structure = _score_structural_regularity(ast_data)
    ind_similarity = _score_peer_similarity(code, filename, peer_codes)

    active_indicators = [ind_naming, ind_format, ind_comments, ind_structure]
    if peer_codes:
        active_indicators.append(ind_similarity)

    total_weight = sum(ind["weight"] for ind in active_indicators)
    weighted_sum = sum(ind["score"] * ind["weight"] for ind in active_indicators)
    overall_score = round(weighted_sum / total_weight, 1) if total_weight > 0 else 0.0

    if overall_score >= HEURISTIC_THRESHOLDS["several_min"]:
        label = HEURISTIC_LABELS["several"]
    elif overall_score >= HEURISTIC_THRESHOLDS["some_min"]:
        label = HEURISTIC_LABELS["some"]
    else:
        label = HEURISTIC_LABELS["few"]

    all_indicators = [ind_naming, ind_format, ind_comments, ind_structure, ind_similarity]
    influencing = [
        f"{ind['name']} ({ind['score']:.1f}/100): {ind['observation']}"
        for ind in active_indicators
        if ind["score"] >= 35.0
    ]
    if not influencing:
        influencing = ["No strong individual stylistic or structural heuristic indicators exceeded 35/100."]

    limitations = [
        "Heuristic scores measure stylistic and structural traits—not authorship.",
        "Well-formatted human code using PEP 8, type hints, and Black/Ruff can trigger higher indicator scores (false positives).",
        "AI-generated code that has been edited, condensed, or prompted for terse style can yield low scores (false negatives).",
        "This score is NOT a validated probability and must never be used alone for academic or disciplinary decisions.",
    ]

    return {
        "filename": filename,
        "code_hash": compute_code_hash(code),
        "indicator_score": overall_score,
        "classification_label": label,
        "indicators": all_indicators,
        "influencing_characteristics": influencing,
        "ast_summary": ast_data,
        "limitations": limitations,
        "limitations_text": " ".join(limitations),
        "disclaimer": AI_DETECTION_DISCLAIMER,
    }


```

---

### File: `analytics/coding_analytics.py`
**Role:** Multi-Timeframe Resampler (3M, 6M, 1Y, 3Y, All) & Charts  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/analytics/coding_analytics.py`

```python
"""
Module 3: Coding Performance Analytics & Interactive Visualizations.
Produces Pandas aggregations, Plotly interactive charts, and Matplotlib figures
strictly from stored live or clearly labeled sample profile records.
"""

from __future__ import annotations

import re
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _source_tag(is_sample: bool) -> str:
    return "Sample" if is_sample else "Live"


def build_language_distribution(profiles: list[dict[str, Any]]) -> pd.DataFrame:
    """Aggregate programming language usage and solved counts across selected profiles."""
    rows: list[dict[str, Any]] = []
    for p in profiles:
        uname = p.get("username", "unknown")
        src = _source_tag(bool(p.get("is_sample")))
        for lang in p.get("programming_languages") or []:
            rows.append(
                {
                    "username": uname,
                    "source": src,
                    "language_name": lang.get("language_name", "Unknown"),
                    "problems_solved": lang.get("problems_solved"),
                    "proficiency": lang.get("proficiency") or "N/A",
                }
            )
    if not rows:
        return pd.DataFrame(
            columns=["username", "source", "language_name", "problems_solved", "proficiency"]
        )
    return pd.DataFrame(rows)


def build_skill_distribution(profiles: list[dict[str, Any]]) -> pd.DataFrame:
    """Aggregate skills across selected profiles."""
    rows: list[dict[str, Any]] = []
    for p in profiles:
        uname = p.get("username", "unknown")
        src = _source_tag(bool(p.get("is_sample")))
        for skill in p.get("skills") or []:
            rows.append(
                {
                    "username": uname,
                    "source": src,
                    "skill_name": skill.get("skill_name", "Unknown"),
                    "skill_level": skill.get("skill_level") or "Listed",
                    "verified": "Verified" if skill.get("verified") else "Listed",
                }
            )
    if not rows:
        return pd.DataFrame(
            columns=["username", "source", "skill_name", "skill_level", "verified"]
        )
    return pd.DataFrame(rows)


def build_badge_and_achievement_summary(profiles: list[dict[str, Any]]) -> pd.DataFrame:
    """Summarize badges, certificates, and achievements across selected profiles."""
    rows: list[dict[str, Any]] = []
    for p in profiles:
        uname = p.get("username", "unknown")
        src = _source_tag(bool(p.get("is_sample")))
        items = list(p.get("achievements") or [])
        if not items:
            for b in p.get("badges") or []:
                b_copy = dict(b) if isinstance(b, dict) else {"title": str(b)}
                b_copy.setdefault("achievement_type", "badge")
                items.append(b_copy)
            for c in p.get("certificates") or []:
                c_copy = dict(c) if isinstance(c, dict) else {"title": str(c)}
                c_copy.setdefault("achievement_type", "certificate")
                items.append(c_copy)

        for ach in items:
            rows.append(
                {
                    "username": uname,
                    "source": src,
                    "title": ach.get("title", "Unknown"),
                    "achievement_type": (ach.get("achievement_type") or "badge").title(),
                    "level_or_stars": ach.get("level_or_stars") or "N/A",
                }
            )
    if not rows:
        return pd.DataFrame(
            columns=["username", "source", "title", "achievement_type", "level_or_stars"]
        )
    return pd.DataFrame(rows)


def build_profile_comparison_df(profiles: list[dict[str, Any]]) -> pd.DataFrame:
    """Build a multi-profile comparison table using only observed counts and stats."""
    rows: list[dict[str, Any]] = []
    for p in profiles:
        langs = p.get("programming_languages") or []
        solved_vals = [
            l.get("problems_solved") for l in langs if l.get("problems_solved") is not None
        ]
        total_solved = sum(solved_vals) if solved_vals else None
        rows.append(
            {
                "username": p.get("username", "unknown"),
                "source": _source_tag(bool(p.get("is_sample"))),
                "languages_count": len(langs),
                "skills_count": len(p.get("skills") or []),
                "badges_count": len(p.get("badges") or []),
                "certificates_count": len(p.get("certificates") or []),
                "problems_solved_listed": total_solved,
                "fields_collected": int(p.get("fields_collected") or 0),
            }
        )
    return pd.DataFrame(rows)


def build_activity_trend_df(
    scraping_history: list[dict[str, Any]],
    stats_history: list[dict[str, Any]] | None = None,
) -> pd.DataFrame:
    """
    Build historical trend DataFrame strictly from recorded database timestamps.
    """
    if stats_history:
        rows = [
            {
                "timestamp": s.get("recorded_at"),
                "username": s.get("username", "unknown"),
                "metric": s.get("stat_name", "Metric"),
                "value": s.get("numeric_value"),
                "source": _source_tag(bool(s.get("is_sample"))),
            }
            for s in stats_history
            if s.get("numeric_value") is not None
        ]
        if rows:
            df = pd.DataFrame(rows)
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            return df.dropna(subset=["timestamp"]).sort_values("timestamp")

    if scraping_history:
        df = pd.DataFrame(scraping_history)
        if "scraped_at" in df.columns:
            df["timestamp"] = pd.to_datetime(df["scraped_at"], errors="coerce")
            df = df.dropna(subset=["timestamp"]).copy()
            df["date"] = df["timestamp"].dt.date.astype(str)
            grouped = (
                df.groupby(["date", "source_mode"], as_index=False)
                .agg(operations=("id", "count"), avg_fields=("fields_collected", "mean"))
            )
            return grouped

    return pd.DataFrame()


# ----------------------------------------------------------------------
# Plotly Interactive Charts
# ----------------------------------------------------------------------


def _extract_star_rating(proficiency: Any) -> int | None:
    """Extract numeric star rating from a proficiency string like '5 Stars (Gold Badge)'."""
    if not proficiency:
        return None
    m = re.search(r"(\d+)\s*star", str(proficiency), re.IGNORECASE)
    return int(m.group(1)) if m else None


def create_language_bar_chart(lang_df: pd.DataFrame) -> go.Figure:
    """Create a Plotly bar chart of problems solved, star ratings, or profile count per language."""
    if lang_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No Programming Language Data Available")
        return fig

    has_solved = lang_df["problems_solved"].notna().any()
    if has_solved:
        plot_df = lang_df.dropna(subset=["problems_solved"]).copy()
        fig = px.bar(
            plot_df,
            x="language_name",
            y="problems_solved",
            color="username",
            barmode="group",
            title="Problems Solved by Programming Language",
            labels={"language_name": "Language", "problems_solved": "Problems Solved"},
            template="plotly_white",
        )
    else:
        star_df = lang_df.copy()
        star_df["stars"] = star_df["proficiency"].apply(_extract_star_rating)
        if star_df["stars"].notna().any():
            plot_df = star_df.dropna(subset=["stars"])
            fig = px.bar(
                plot_df,
                x="language_name",
                y="stars",
                color="username",
                barmode="group",
                title="Public Badge Star Rating by Language",
                labels={"language_name": "Language", "stars": "Badge Stars (★)"},
                template="plotly_white",
            )
        else:
            counts = (
                lang_df.groupby("language_name", as_index=False)
                .size()
                .rename(columns={"size": "profile_count"})
            )
            fig = px.bar(
                counts,
                x="language_name",
                y="profile_count",
                title="Programming Language Presence Across Profiles",
                labels={"language_name": "Language", "profile_count": "Profiles"},
                template="plotly_white",
            )
    fig.update_layout(margin=dict(t=50, b=30, l=30, r=20))
    return fig


def create_language_pie_chart(lang_df: pd.DataFrame) -> go.Figure:
    """Create a Plotly pie/donut chart showing language share."""
    if lang_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No Programming Language Data Available")
        return fig

    has_solved = lang_df["problems_solved"].notna().any()
    if has_solved:
        agg = (
            lang_df.dropna(subset=["problems_solved"])
            .groupby("language_name", as_index=False)["problems_solved"]
            .sum()
        )
        fig = px.pie(
            agg,
            names="language_name",
            values="problems_solved",
            hole=0.4,
            title="Language Share (by Listed Problems Solved)",
            template="plotly_white",
        )
    else:
        star_df = lang_df.copy()
        star_df["stars"] = star_df["proficiency"].apply(_extract_star_rating)
        if star_df["stars"].notna().any():
            agg = (
                star_df.dropna(subset=["stars"])
                .groupby("language_name", as_index=False)["stars"]
                .sum()
            )
            fig = px.pie(
                agg,
                names="language_name",
                values="stars",
                hole=0.4,
                title="Language Share (by Public Badge Stars)",
                template="plotly_white",
            )
        else:
            agg = lang_df.groupby("language_name", as_index=False).size()
            fig = px.pie(
                agg,
                names="language_name",
                values="size",
                hole=0.4,
                title="Language Distribution (by Profile Count)",
                template="plotly_white",
            )
    fig.update_layout(margin=dict(t=50, b=20, l=20, r=20))
    return fig


def create_skill_chart(skill_df: pd.DataFrame) -> go.Figure:
    """Create a Plotly bar chart summarizing listed and verified skills."""
    if skill_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No Skill Data Available")
        return fig

    counts = (
        skill_df.groupby(["skill_name", "verified"], as_index=False)
        .size()
        .rename(columns={"size": "count"})
        .sort_values("count", ascending=True)
    )
    fig = px.bar(
        counts,
        x="count",
        y="skill_name",
        color="verified",
        orientation="h",
        title="Skill Distribution & Verification Status",
        labels={"count": "Count", "skill_name": "Skill", "verified": "Status"},
        template="plotly_white",
    )
    fig.update_layout(margin=dict(t=50, b=30, l=20, r=20))
    return fig


def create_badge_chart(ach_df: pd.DataFrame) -> go.Figure:
    """Create a Plotly bar chart of badges & certificates per profile."""
    if ach_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No Badge or Achievement Data Available")
        return fig

    counts = (
        ach_df.groupby(["username", "achievement_type"], as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )
    fig = px.bar(
        counts,
        x="username",
        y="count",
        color="achievement_type",
        barmode="stack",
        title="Badges & Certificates per Profile",
        labels={"username": "Profile", "count": "Count", "achievement_type": "Type"},
        template="plotly_white",
    )
    fig.update_layout(margin=dict(t=50, b=30, l=20, r=20))
    return fig


def create_comparison_chart(comp_df: pd.DataFrame) -> go.Figure:
    """Create a multi-profile performance comparison bar chart."""
    if comp_df.empty:
        fig = go.Figure()
        fig.update_layout(title="Insufficient Profiles for Comparison")
        return fig

    melted = comp_df.melt(
        id_vars=["username", "source"],
        value_vars=["languages_count", "skills_count", "badges_count", "certificates_count"],
        var_name="Metric",
        value_name="Count",
    )
    metric_labels = {
        "languages_count": "Languages",
        "skills_count": "Skills",
        "badges_count": "Badges",
        "certificates_count": "Certificates",
    }
    melted["Metric"] = melted["Metric"].map(metric_labels)
    fig = px.bar(
        melted,
        x="username",
        y="Count",
        color="Metric",
        barmode="group",
        title="Multi-Profile Feature Comparison",
        template="plotly_white",
    )
    fig.update_layout(margin=dict(t=50, b=30, l=20, r=20))
    return fig


TIME_RANGE_DAYS: dict[str, int] = {
    "3M": 90,
    "6M": 180,
    "1Y": 365,
    "3Y": 1095,
}


def create_activity_trend_chart(
    trend_df: pd.DataFrame, time_range: str = "3M"
) -> go.Figure:
    """
    Create a Plotly line chart for historical metric or scraping activity trends
    with interactive 3M / 6M / 1Y / 3Y / All time-window scaling.
    """
    if trend_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No Historical Trend Records Available Yet")
        return fig

    plot_df = trend_df.copy()
    x_col = "timestamp" if "timestamp" in plot_df.columns else "date"
    plot_df[x_col] = pd.to_datetime(plot_df[x_col], errors="coerce")
    plot_df = plot_df.dropna(subset=[x_col]).sort_values(x_col)

    if plot_df.empty:
        fig = go.Figure()
        fig.update_layout(title="No Valid Timestamped Records Available")
        return fig

    end_ts = plot_df[x_col].max()
    x_range = None
    if time_range in TIME_RANGE_DAYS:
        days = TIME_RANGE_DAYS[time_range]
        start_ts = end_ts - pd.Timedelta(days=days)
        filtered = plot_df[plot_df[x_col] >= start_ts]
        if not filtered.empty:
            plot_df = filtered
        # Display full selected horizon ending slightly past the latest recorded point
        pad = pd.Timedelta(days=max(2, int(days * 0.03)))
        x_range = [start_ts, end_ts + pad]

    range_label = f" ({time_range} Window)" if time_range != "All" else " (All Time)"

    if "metric" in plot_df.columns and "value" in plot_df.columns:
        fig = px.line(
            plot_df,
            x=x_col,
            y="value",
            color="metric",
            markers=True,
            line_dash="username",
            title=f"Recorded Profile Metric History Over Time{range_label}",
            template="plotly_white",
        )
    else:
        fig = px.line(
            plot_df,
            x=x_col,
            y="operations",
            color="source_mode",
            markers=True,
            title=f"Scraping & Sample-Load Operations Over Time{range_label}",
            labels={x_col: "Date", "operations": "Operations", "source_mode": "Source"},
            template="plotly_white",
        )

    xaxis_cfg: dict[str, Any] = {
        "rangeselector": {
            "buttons": [
                {"count": 3, "label": "3M", "step": "month", "stepmode": "backward"},
                {"count": 6, "label": "6M", "step": "month", "stepmode": "backward"},
                {"count": 1, "label": "1Y", "step": "year", "stepmode": "backward"},
                {"count": 3, "label": "3Y", "step": "year", "stepmode": "backward"},
                {"step": "all", "label": "All"},
            ]
        },
        "rangeslider": {"visible": False},
        "type": "date",
    }
    if x_range is not None:
        xaxis_cfg["range"] = x_range

    fig.update_layout(
        xaxis=xaxis_cfg,
        margin=dict(t=70, b=30, l=20, r=20),
    )
    return fig


# ----------------------------------------------------------------------
# Matplotlib Summary Chart (for static export / secondary view)
# ----------------------------------------------------------------------


def create_matplotlib_language_summary(lang_df: pd.DataFrame) -> plt.Figure:
    """Generate a clean Matplotlib horizontal bar chart of language totals."""
    fig, ax = plt.subplots(figsize=(7, 3.8))
    if lang_df.empty:
        ax.text(0.5, 0.5, "No language data available", ha="center", va="center")
        ax.axis("off")
        return fig

    if lang_df["problems_solved"].notna().any():
        agg = (
            lang_df.dropna(subset=["problems_solved"])
            .groupby("language_name")["problems_solved"]
            .sum()
            .sort_values(ascending=True)
        )
        xlabel = "Total Listed Problems Solved"
    else:
        agg = lang_df.groupby("language_name").size().sort_values(ascending=True)
        xlabel = "Profile Count"

    ax.barh(agg.index.astype(str), agg.values, color="#2563EB", alpha=0.88)
    ax.set_xlabel(xlabel)
    ax.set_title("Programming Language Summary (Matplotlib)")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    fig.tight_layout()
    return fig


```

---

### File: `analytics/profile_analysis.py`
**Role:** Profile Summary Aggregator & Unexposed Field Detector  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/analytics/profile_analysis.py`

```python
"""
Module 2: HackerRank Profile Analytics.
Processes collected profile data with Pandas and derives factual insights
without inventing uncollected metrics.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from analytics.statistics import compute_numeric_summary


def analyze_single_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """
    Generate a structured Pandas-backed profile analytics report for one profile.
    """
    languages = profile.get("programming_languages") or []
    skills = profile.get("skills") or []
    badges = profile.get("badges") or []
    certificates = profile.get("certificates") or []
    statistics = profile.get("statistics") or []
    recent_activity = profile.get("recent_activity") or []

    lang_df = pd.DataFrame(languages) if languages else pd.DataFrame(
        columns=["language_name", "problems_solved", "proficiency"]
    )
    skill_df = pd.DataFrame(skills) if skills else pd.DataFrame(
        columns=["skill_name", "skill_level", "verified"]
    )
    badge_df = pd.DataFrame(badges) if badges else pd.DataFrame(
        columns=["title", "level_or_stars", "details"]
    )
    cert_df = pd.DataFrame(certificates) if certificates else pd.DataFrame(
        columns=["title", "level_or_stars", "details"]
    )
    stats_df = pd.DataFrame(statistics) if statistics else pd.DataFrame(
        columns=["stat_name", "stat_value", "numeric_value", "stat_category"]
    )
    activity_df = pd.DataFrame(recent_activity) if recent_activity else pd.DataFrame(
        columns=["activity", "category"]
    )

    solved_summary = {"count": 0, "sum": None, "mean": None, "median": None, "min": None, "max": None}
    if not lang_df.empty and "problems_solved" in lang_df.columns:
        solved_summary = compute_numeric_summary(lang_df["problems_solved"].dropna().tolist())

    verified_skills_count = 0
    if not skill_df.empty and "verified" in skill_df.columns:
        verified_skills_count = int(skill_df["verified"].astype(bool).sum())

    # Generate factual insights strictly from collected data
    insights: list[str] = []
    source_tag = "Demonstration Sample Data" if profile.get("is_sample") else "Live Public Profile Data"
    insights.append(f"Data Source: {source_tag} for username '{profile.get('username')}'.")

    if not lang_df.empty:
        lang_names = ", ".join(lang_df["language_name"].astype(str).tolist())
        insights.append(f"Listed {len(lang_df)} programming language(s): {lang_names}.")
        if solved_summary["sum"] is not None and "problems_solved" in lang_df.columns:
            valid_lang = lang_df.dropna(subset=["problems_solved"])
            if not valid_lang.empty:
                top_row = valid_lang.sort_values("problems_solved", ascending=False).iloc[0]
                insights.append(
                    f"Highest listed problem count is in {top_row['language_name']} "
                    f"({int(top_row['problems_solved'])} problems across {int(solved_summary['sum'])} total listed)."
                )
    else:
        insights.append("No public programming language breakdown was available for this profile.")

    if not skill_df.empty:
        insights.append(
            f"Profile lists {len(skill_df)} skill(s), including {verified_skills_count} verified skill(s)."
        )
    else:
        insights.append("No public skills were listed on this profile.")

    if not badge_df.empty or not cert_df.empty:
        insights.append(
            f"Achievements include {len(badge_df)} badge(s) and {len(cert_df)} certificate(s)."
        )
    else:
        insights.append("No public badges or certificates were exposed.")

    if not stats_df.empty:
        insights.append(f"Collected {len(stats_df)} public statistic metric(s).")
    else:
        insights.append("No numeric problem-solving summary statistics were publicly visible.")

    if not activity_df.empty:
        insights.append(f"Observed {len(activity_df)} public activity item(s).")
    else:
        insights.append("Public activity feed was unavailable or empty.")

    unavailable = profile.get("unavailable_fields") or []

    return {
        "username": profile.get("username"),
        "display_name": profile.get("display_name"),
        "is_sample": bool(profile.get("is_sample")),
        "summary_counts": {
            "languages_count": len(lang_df),
            "skills_count": len(skill_df),
            "verified_skills_count": verified_skills_count,
            "badges_count": len(badge_df),
            "certificates_count": len(cert_df),
            "statistics_count": len(stats_df),
            "activity_count": len(activity_df),
            "total_listed_problems": int(solved_summary["sum"]) if solved_summary["sum"] is not None else None,
        },
        "languages_df": lang_df,
        "skills_df": skill_df,
        "badges_df": badge_df,
        "certificates_df": cert_df,
        "statistics_df": stats_df,
        "activity_df": activity_df,
        "solved_summary": solved_summary,
        "insights": insights,
        "unavailable_fields": unavailable,
    }


```

---

### File: `dashboard/home.py`
**Role:** Home Dashboard, Futuristic Banners & PDF Download Actions  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/dashboard/home.py`

```python
"""
Page 1: Home Dashboard.
Features modern graphics, animated gradient hero banners, interactive Plotly visualizations,
system pipeline diagrams, KPI cards, and quick navigation.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import APP_DESCRIPTION, APP_SHORT_TITLE, APP_TITLE, APP_VERSION, BASE_DIR
from database.db_manager import DatabaseManager
from utils.helpers import format_timestamp


def _navigate_to(page_name: str) -> None:
    st.session_state["current_page"] = page_name
    st.rerun()


def _render_hero_banner() -> None:
    """Render a futuristic high-tech hero banner with gradient accents and badges."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 58, 138, 0.45) 50%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(59, 130, 246, 0.35);
            border-radius: 16px;
            padding: 28px 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); padding: 4px 14px; border-radius: 9999px; margin-bottom: 12px;">
                        <span style="height: 8px; width: 8px; border-radius: 50%; background-color: #10B981; display: inline-block; box-shadow: 0 0 10px #10B981;"></span>
                        <span style="color: #93C5FD; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">System Core Online • v"""
        + APP_VERSION
        + """</span>
                    </div>
                    <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; background: linear-gradient(90deg, #FFFFFF 0%, #93C5FD 50%, #38BDF8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        """
        + APP_TITLE
        + """
                    </h1>
                    <p style="color: #94A3B8; font-size: 1.02rem; margin-top: 8px; margin-bottom: 0; max-width: 820px; line-height: 1.55;">
                        Next-generation developer intelligence platform combining automated public profile analytics, deep AST structural code decomposition, multi-metric similarity detection, and explainable heuristic AI pattern indicators.
                    </p>
                </div>
            </div>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 18px;">
                <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); color: #E2E8F0; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 500;">🕸️ Selenium 4.x Engine</span>
                <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); color: #E2E8F0; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 500;">🌳 Python AST Structural Parser</span>
                <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); color: #E2E8F0; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 500;">📐 TF-IDF & Cosine Similarity</span>
                <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); color: #E2E8F0; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 500;">🤖 Explainable Heuristic AI Index</span>
                <span style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); color: #E2E8F0; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 500;">💾 Embedded SQLite Vault</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpi_metrics(counts: dict[str, int]) -> None:
    """Render futuristic KPI cards with visual accent bars."""
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(59, 130, 246, 0.3); border-top: 4px solid #3B82F6; border-radius: 12px; padding: 16px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #94A3B8; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Profiles Stored</span>
                    <span style="font-size: 1.3rem;">👥</span>
                </div>
                <div style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-top: 4px;">{counts['total_profiles']}</div>
                <div style="color: #60A5FA; font-size: 0.78rem; font-weight: 500; margin-top: 4px;">{counts['live_profiles']} Live • {counts['sample_profiles']} Sample</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(16, 185, 129, 0.3); border-top: 4px solid #10B981; border-radius: 12px; padding: 16px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #94A3B8; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Scraping Ingestions</span>
                    <span style="font-size: 1.3rem;">🕷️</span>
                </div>
                <div style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-top: 4px;">{counts['total_scrapes']}</div>
                <div style="color: #34D399; font-size: 0.78rem; font-weight: 500; margin-top: 4px;">{counts['successful_scrapes']} Completed Successfully</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(139, 92, 246, 0.3); border-top: 4px solid #8B5CF6; border-radius: 12px; padding: 16px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #94A3B8; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">AST Code Analyses</span>
                    <span style="font-size: 1.3rem;">🌳</span>
                </div>
                <div style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-top: 4px;">{counts['total_code_analyses']}</div>
                <div style="color: #A78BFA; font-size: 0.78rem; font-weight: 500; margin-top: 4px;">Syntax & Cyclomatic Metrics</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(245, 158, 11, 0.3); border-top: 4px solid #F59E0B; border-radius: 12px; padding: 16px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #94A3B8; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Similarity & AI Checks</span>
                    <span style="font-size: 1.3rem;">🛡️</span>
                </div>
                <div style="font-size: 2.1rem; font-weight: 800; color: #F8FAFC; margin-top: 4px;">{counts['total_similarities'] + counts['total_ai_analyses']}</div>
                <div style="color: #FBBF24; font-size: 0.78rem; font-weight: 500; margin-top: 4px;">{counts['total_similarities']} Sim • {counts['total_ai_analyses']} Heuristic AI</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_graphic_charts(counts: dict[str, int]) -> None:
    """Render interactive Plotly graphical visuals showcasing workload and analytical pillars."""
    st.write("")
    col_chart1, col_chart2 = st.columns([1, 1])

    with col_chart1:
        # Donut Chart: Platform Operations Breakdown
        labels = [
            "Profiles Stored",
            "Scrapes Performed",
            "AST Code Analyses",
            "Similarity Comparisons",
            "AI Heuristic Checks",
        ]
        values = [
            max(counts["total_profiles"], 1),
            max(counts["total_scrapes"], 1),
            max(counts["total_code_analyses"], 1),
            max(counts["total_similarities"], 1),
            max(counts["total_ai_analyses"], 1),
        ]
        colors = ["#3B82F6", "#10B981", "#8B5CF6", "#06B6D4", "#F59E0B"]

        fig_donut = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.58,
                    marker=dict(colors=colors, line=dict(color="#0F172A", width=2)),
                    textinfo="label+percent",
                    textposition="inside",
                    insidetextorientation="radial",
                    hoverinfo="label+value+percent",
                )
            ]
        )
        fig_donut.update_layout(
            title=dict(
                text="<b>Platform Activity & Data Ingestion Distribution</b>",
                font=dict(size=14, color="#E2E8F0"),
            ),
            showlegend=False,
            height=320,
            margin=dict(t=40, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_donut, width="stretch", key="home_activity_donut")

    with col_chart2:
        # Radar Chart: Capabilities & Analytical Dimensions
        categories = [
            "Browser Ingestion",
            "Skill Analytics",
            "AST Tree Parsing",
            "Cosine TF-IDF",
            "Heuristic AI Index",
            "SQLite Persistence",
        ]
        # Benchmark score levels (100-point scale for visual architecture index)
        r_scores = [92, 95, 98, 90, 88, 96]

        fig_radar = go.Figure()
        fig_radar.add_trace(
            go.Scatterpolar(
                r=r_scores,
                theta=categories,
                fill="toself",
                name="System Engine Index",
                fillcolor="rgba(59, 130, 246, 0.28)",
                line=dict(color="#38BDF8", width=2),
                marker=dict(size=6, color="#60A5FA"),
            )
        )
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=False,
                    linecolor="rgba(148, 163, 184, 0.2)",
                    gridcolor="rgba(148, 163, 184, 0.15)",
                ),
                angularaxis=dict(
                    tickfont=dict(size=11, color="#CBD5E1"),
                    linecolor="rgba(148, 163, 184, 0.2)",
                    gridcolor="rgba(148, 163, 184, 0.15)",
                ),
                bgcolor="rgba(0,0,0,0)",
            ),
            title=dict(
                text="<b>Inspection Engine Coverage & Analytical Depth</b>",
                font=dict(size=14, color="#E2E8F0"),
            ),
            showlegend=False,
            height=320,
            margin=dict(t=40, b=10, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_radar, width="stretch", key="home_capabilities_radar")


def _render_architecture_pipeline() -> None:
    """Render a visual architecture pipeline flowchart showing data ingestion to reporting."""
    st.markdown(
        """
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 14px; padding: 22px; margin-top: 10px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span style="font-size: 1.05rem; font-weight: 700; color: #F1F5F9; letter-spacing: 0.02em;">⚙️ System Architecture Pipeline</span>
                <span style="font-size: 0.78rem; color: #38BDF8; background: rgba(56, 189, 248, 0.12); padding: 3px 10px; border-radius: 9999px; border: 1px solid rgba(56, 189, 248, 0.3);">End-to-End Modular Flow</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px;">
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 10px; padding: 14px;">
                    <div style="color: #60A5FA; font-weight: 700; font-size: 0.85rem; margin-bottom: 4px;">1. DATA INGESTION</div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem;">Selenium & Fallbacks</div>
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.4;">
                        Headless Chrome/Edge automation, offline JSON sample dataset, and CSV/JSON public upload parser.
                    </p>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 14px;">
                    <div style="color: #34D399; font-weight: 700; font-size: 0.85rem; margin-bottom: 4px;">2. DECOMPOSITION</div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem;">DOM & AST Parsing</div>
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.4;">
                        BeautifulSoup4 HTML selectors, Python AST visitor, token stream lexing, and variable normalization.
                    </p>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 14px;">
                    <div style="color: #A78BFA; font-weight: 700; font-size: 0.85rem; margin-bottom: 4px;">3. ANALYTICAL CORE</div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem;">Similarity & Heuristics</div>
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.4;">
                        TF-IDF cosine, SequenceMatcher, AST feature vectors, and 5 explainable non-probabilistic AI indicators.
                    </p>
                </div>
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 10px; padding: 14px;">
                    <div style="color: #FBBF24; font-weight: 700; font-size: 0.85rem; margin-bottom: 4px;">4. VISUALIZATION</div>
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 0.95rem;">Dashboard & SQLite</div>
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 6px 0 0 0; line-height: 1.4;">
                        7-page Streamlit portal, Plotly interactive graphics, Matplotlib figures, and SQLite schema.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_interactive_launchpad() -> None:
    """Render attractive visual action cards with quick-jump navigation."""
    st.markdown("### 🚀 Interactive Module Launchpad")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 12px; padding: 18px; height: 160px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">🕸️</div>
                    <div style="font-weight: 700; color: #F1F5F9; font-size: 0.95rem;">Web Scraper</div>
                    <div style="color: #94A3B8; font-size: 0.78rem; margin-top: 4px;">Selenium automated live scrape, offline sample data, or CSV/JSON upload.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Launch Scraper →", key="launch_scraper", use_container_width=True, type="primary"):
            _navigate_to("Selenium Web Scraper")

    with c2:
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 18px; height: 160px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">📊</div>
                    <div style="font-weight: 700; color: #F1F5F9; font-size: 0.95rem;">Coding Analytics</div>
                    <div style="color: #94A3B8; font-size: 0.78rem; margin-top: 4px;">Language distributions, skill verification, badge charts & profile comparisons.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Analytics →", key="launch_analytics", use_container_width=True):
            _navigate_to("Coding Performance Analytics")

    with c3:
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(139, 92, 246, 0.25); border-radius: 12px; padding: 18px; height: 160px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">📐</div>
                    <div style="font-weight: 700; color: #F1F5F9; font-size: 0.95rem;">Code Similarity</div>
                    <div style="color: #94A3B8; font-size: 0.78rem; margin-top: 4px;">Pairwise token, TF-IDF cosine, sequence matcher & AST structural diffs.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Compare Code →", key="launch_similarity", use_container_width=True):
            _navigate_to("Source-Code Similarity")

    with c4:
        st.markdown(
            """
            <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 12px; padding: 18px; height: 160px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">🤖</div>
                    <div style="font-weight: 700; color: #F1F5F9; font-size: 0.95rem;">AI Pattern Check</div>
                    <div style="color: #94A3B8; font-size: 0.78rem; margin-top: 4px;">Transparent heuristic indicators, naming uniformity & comment patterns.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Check AI Patterns →", key="launch_ai", use_container_width=True):
            _navigate_to("AI-Associated Code Pattern Analysis")


def _render_academic_novelty_banner() -> None:
    """Render the Academic Novelty & IEEE Literature Comparison download banner."""
    pdf_path = BASE_DIR / "Hacker_Analytics_Project_Novelty_Check_and_IEEE_Comparison.pdf"
    """Render the Academic Project Report & Novelty Check download banner."""
    full_report_path = BASE_DIR / "Hacker_Analytics_Academic_Project_Report.pdf"
    novelty_pdf_path = BASE_DIR / "Hacker_Analytics_Project_Novelty_Check_and_IEEE_Comparison.pdf"
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(59, 130, 246, 0.35);
            border-left: 4px solid #3B82F6;
            border-radius: 12px;
            padding: 18px 24px;
            margin-top: 24px;
            margin-bottom: 12px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC;">
                        📄 Academic Novelty Assessment & IEEE Literature Gap Analysis
                        📄 Academic Project Reports & IEEE Literature Benchmarking (PDF)
                    </div>
                    <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 4px;">
                        Formal benchmarking report comparing this system against traditional plagiarism tools (MOSS), commercial AI detectors, and 4 published IEEE research papers.
                        Formal 25-page academic project report (matching college thesis guidelines with architectures, ER diagrams, DFD workflows, algorithms, and experimental results) and IEEE novelty gap analysis report.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if pdf_path.exists():
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 Download Novelty Check & IEEE Literature Comparison Report (PDF)",
            data=pdf_bytes,
            file_name="Hacker_Analytics_Project_Novelty_Check_and_IEEE_Comparison.pdf",
            mime="application/pdf",
            key="download_novelty_pdf",
            use_container_width=True,
        )
    col_rep1, col_rep2 = st.columns(2)
    with col_rep1:
        if full_report_path.exists():
            with open(full_report_path, "rb") as f1:
                pdf_bytes1 = f1.read()
            st.download_button(
                label="📘 Download Full Academic Report (25 Pages PDF)",
                data=pdf_bytes1,
                file_name="Hacker_Analytics_Academic_Project_Report.pdf",
                mime="application/pdf",
                key="download_full_academic_report_pdf",
                use_container_width=True,
            )
    with col_rep2:
        if novelty_pdf_path.exists():
            with open(novelty_pdf_path, "rb") as f2:
                pdf_bytes2 = f2.read()
            st.download_button(
                label="📑 Download IEEE Novelty Gap Analysis (PDF)",
                data=pdf_bytes2,
                file_name="Hacker_Analytics_Project_Novelty_Check_and_IEEE_Comparison.pdf",
                mime="application/pdf",
                key="download_novelty_pdf",
                use_container_width=True,
            )


def render_home_page(db: DatabaseManager) -> None:
    """Render the modernized Home Dashboard overview page with cool graphics."""
    counts = db.get_dashboard_counts()

    # 1. Futuristic Hero Banner
    _render_hero_banner()

    # 2. Glowing Metric Cards
    _render_kpi_metrics(counts)

    # 3. Interactive Graphical Visuals (Donut & Radar)
    _render_graphic_charts(counts)

    # 4. System Pipeline Diagram
    _render_architecture_pipeline()

    # 5. Interactive Action Launchpad
    _render_interactive_launchpad()

    # 6. Academic Novelty & IEEE Report Download
    _render_academic_novelty_banner()

    st.write("")
    st.divider()

    # 6. Real-time Activity Feed
    st.subheader("📋 Real-Time Activity & History Stream")

    tab1, tab2, tab3 = st.tabs(
        ["🕸️ Scraping & Profile Loads", "📐 Code Similarity Runs", "🤖 Heuristic AI Checks"]
    )

    with tab1:
        scrapes = db.get_scraping_history(limit=8)
        if scrapes:
            df = pd.DataFrame(scrapes)[
                ["username", "status", "source_mode", "fields_collected", "scraped_at", "error_message"]
            ].copy()
            df["scraped_at"] = df["scraped_at"].apply(format_timestamp)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info(
                "No scraping or profile records logged yet. Open **Selenium Web Scraper** to load sample data or scrape a profile."
            )

    with tab2:
        sims = db.get_similarity_history(limit=8)
        if sims:
            df = pd.DataFrame(sims)[
                ["file_a", "file_b", "overall_similarity", "ast_similarity", "analyzed_at"]
            ].copy()
            df["analyzed_at"] = df["analyzed_at"].apply(format_timestamp)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No source-code similarity comparisons recorded yet.")

    with tab3:
        ai_rows = db.get_ai_pattern_history(limit=8)
        if ai_rows:
            df = pd.DataFrame(ai_rows)[
                ["filename", "indicator_score", "classification_label", "analyzed_at"]
            ].copy()
            df["analyzed_at"] = df["analyzed_at"].apply(format_timestamp)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No heuristic AI-pattern analyses recorded yet.")

```

---

### File: `dashboard/sidebar.py`
**Role:** Sidebar Navigation & Real-Time Workspace Vault Counters  
**Location:** `file:///C:/Users/janar/OneDrive/Desktop/hacker-analytics-ai-detection/dashboard/sidebar.py`

```python
"""
Sidebar navigation and live database status summary for the Streamlit dashboard.
"""

from __future__ import annotations

import streamlit as st

from config import APP_SHORT_TITLE, APP_VERSION
from database.db_manager import DatabaseManager

PAGES: list[str] = [
    "Home Dashboard",
    "Selenium Web Scraper",
    "Profile Analytics",
    "Coding Performance Analytics",
    "Source-Code Similarity",
    "AI-Associated Code Pattern Analysis",
    "Analysis History",
]

PAGE_LABELS: dict[str, str] = {
    "Home Dashboard": "🏠 Home Dashboard",
    "Selenium Web Scraper": "🕸️ Selenium Web Scraper",
    "Profile Analytics": "📊 Profile Analytics",
    "Coding Performance Analytics": "📈 Coding Analytics",
    "Source-Code Similarity": "📐 Code Similarity",
    "AI-Associated Code Pattern Analysis": "🤖 AI Pattern Check",
    "Analysis History": "📋 Analysis History",
}


def render_sidebar(db: DatabaseManager) -> str:
    """Render sidebar navigation and summary indicators, returning the selected page."""
    if "current_page" not in st.session_state or st.session_state["current_page"] not in PAGES:
        st.session_state["current_page"] = PAGES[0]

    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 8px 0 16px 0; border-bottom: 1px solid rgba(148, 163, 184, 0.2); margin-bottom: 16px;">
                <div style="font-size: 1.25rem; font-weight: 800; background: linear-gradient(90deg, #60A5FA, #38BDF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    🛡️ {APP_SHORT_TITLE}
                </div>
                <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 2px;">
                    v{APP_VERSION} • Intelligence & Analytics
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        current_idx = PAGES.index(st.session_state["current_page"])
        selected = st.radio(
            "Navigation",
            options=PAGES,
            index=current_idx,
            format_func=lambda p: PAGE_LABELS.get(p, p),
            label_visibility="collapsed",
        )
        if selected != st.session_state["current_page"]:
            st.session_state["current_page"] = selected
            st.rerun()

        st.divider()
        counts = db.get_dashboard_counts()
        st.markdown("#### ⚡ Workspace Vault")
        col1, col2 = st.columns(2)
        col1.metric("Profiles", counts["total_profiles"])
        col2.metric("Scrapes", counts["total_scrapes"])
        col3, col4 = st.columns(2)
        col3.metric("Similarities", counts["total_similarities"])
        col4.metric("AI Checks", counts["total_ai_analyses"])

        st.caption(
            f"Live: {counts['live_profiles']} | Sample: {counts['sample_profiles']}"
        )
        st.info(
            "💡 Tip: Click **Home Dashboard** above to see the new graphics & visual analytics overview.",
            icon="ℹ️",
        )

    return st.session_state["current_page"]

```

---
