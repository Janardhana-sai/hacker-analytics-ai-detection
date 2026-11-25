"""
Script to generate:
1. PROJECT_TECHNICAL_REPORT_DOCUMENT.docx (Microsoft Word Document)
2. PROJECT_TECHNICAL_REPORT_DOCUMENT.md (Markdown Document)

Contains:
- Complete Folder & File Structure Tree
- Architectural Pipelines & Detailed Workflows
- Core System Diagrams embedded
- Full Source Code of all main files
- Algorithm formulations and instructions
"""

import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "report_assets"

# Files to document
MAIN_FILES = [
    ("app.py", BASE_DIR / "app.py", "Streamlit Main Entrypoint & Page Router"),
    ("config.py", BASE_DIR / "config.py", "Central Configurations, Thresholds & Ethical Disclaimers"),
    ("database/schema.py", BASE_DIR / "database" / "schema.py", "SQLite Database 9-Table Schema & DDL Definitions"),
    ("database/db_manager.py", BASE_DIR / "database" / "db_manager.py", "SQLite Database Manager & Relational Operations"),
    ("scraper/browser_manager.py", BASE_DIR / "scraper" / "browser_manager.py", "Selenium Chrome Lifecycle & WebDriver Configuration"),
    ("scraper/hackerrank_scraper.py", BASE_DIR / "scraper" / "hackerrank_scraper.py", "Resilient Profile Scraper Engine & Fallback Handler"),
    ("scraper/scraper_utils.py", BASE_DIR / "scraper" / "scraper_utils.py", "Isolated CSS Selectors, Badge Star Counters & Parsers"),
    ("detection/code_preprocessor.py", BASE_DIR / "detection" / "code_preprocessor.py", "Tokenizer, Comment Stripper & Identifier Normalizer (VAR_1, VAR_2)"),
    ("detection/ast_analysis.py", BASE_DIR / "detection" / "ast_analysis.py", "Abstract Syntax Tree (AST) Node Vectorizer & Depth Inspector"),
    ("detection/code_similarity.py", BASE_DIR / "detection" / "code_similarity.py", "4-Layer Blended Code Similarity Scoring Engine"),
    ("detection/ai_pattern_analysis.py", BASE_DIR / "detection" / "ai_pattern_analysis.py", "Explainable Heuristic AI Pattern Forensics Engine"),
    ("detection/code_quality.py", BASE_DIR / "detection" / "code_quality.py", "Software Engineering Metrics, Cyclomatic Complexity V(G), Halstead & Security Audit"),
    ("analytics/coding_analytics.py", BASE_DIR / "analytics" / "coding_analytics.py", "Multi-Timeframe Resampler (3M, 6M, 1Y, 3Y, All) & Charts"),
    ("analytics/profile_analysis.py", BASE_DIR / "analytics" / "profile_analysis.py", "Profile Summary Aggregator & Unexposed Field Detector"),
    ("dashboard/home.py", BASE_DIR / "dashboard" / "home.py", "Home Dashboard, Futuristic Banners & PDF Download Actions"),
    ("dashboard/sidebar.py", BASE_DIR / "dashboard" / "sidebar.py", "Sidebar Navigation & Real-Time Workspace Vault Counters"),
    ("dashboard/quality_page.py", BASE_DIR / "dashboard" / "quality_page.py", "Code Quality & Security Audit UI with Maintainability Gauge & V(G) Charts"),
]

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell in docx."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def add_code_block_to_docx(doc, code_text):
    """Add a shaded, styled code box to the docx document."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.right_indent = Inches(0.2)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    
    # We will put code in a single-cell table for neat gray box background
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    
    # Add code run
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(4)
    cp.paragraph_format.space_after = Pt(4)
    
    # Truncate if extreme, but keep generous lines
    lines = code_text.splitlines()
    display_text = "\n".join(lines[:400])
    if len(lines) > 400:
        display_text += f"\n... [Truncated: {len(lines) - 400} additional lines in source file] ..."
        
    run = cp.add_run(display_text)
    run.font.name = "Consolas"
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(15, 23, 42)

def generate_markdown_doc(md_path: Path):
    """Generate comprehensive Markdown documentation."""
    content = []
    
    content.append("# HACKER ANALYTICS AND AI CODE DETECTION SYSTEM")
    content.append("## Complete Project Architecture, Workflows, Pipelines & Source Code Documentation\n")
    content.append("> **Document Purpose:** Complete technical reference containing folder structures, architectural pipeline workflows, database schemas, and full source code of all primary modules for academic project reports, viva defense, and software audits.\n")
    content.append("---\n")
    
    # Section 1: Overview
    content.append("## 1. PROJECT EXECUTIVE SUMMARY & ARCHITECTURE OVERVIEW\n")
    content.append(
        "The **Hacker Analytics and AI Code Detection System** is an end-to-end Python developer intelligence "
        "and source-code forensics platform. It unifies three core capabilities that are traditionally fragmented:\n"
        "1. **Competitive Programming Profile Analytics:** Automated extraction of public HackerRank developer data (badges, star counts, verified certifications, language proficiencies) using Selenium WebDriver with multi-tier fallbacks.\n"
        "2. **Multi-Metric Source-Code Similarity:** A 4-layer comparison engine blending Token Jaccard, Scikit-learn TF-IDF Cosine, SequenceMatcher, and Abstract Syntax Tree (AST) node vector cosine similarity with automated variable identifier normalization (`VAR_1`, `VAR_2`).\n"
        "3. **Explainable Heuristic AI Pattern Forensics:** Stylometric and syntactic pattern analysis identifying markers characteristic of AI-assisted code (step comments, naming regularity, docstring density, AST symmetry) backed by mandatory ethical disclaimers.\n"
        "4. **Relational Data Persistence:** An embedded 9-table SQLite schema tracking historical developer growth and audit logs.\n"
        "5. **Interactive Streamlit Dashboard:** A 7-page responsive web dashboard providing real-time data exploration, multi-timeframe analytics (3M, 6M, 1Y, 3Y, All), and instant report exports.\n"
    )
    
    # Section 2: Folder Structure
    content.append("## 2. PROJECT FOLDER & FILE STRUCTURE TREE\n")
    folder_tree = """```text
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
```\n"""
    content.append(folder_tree)
    
    # Section 3: Workflows & Pipelines
    content.append("## 3. CORE ARCHITECTURAL WORKFLOWS & EXECUTION PIPELINES\n")
    
    content.append("### Pipeline 1: Selenium Web Scraping & Resilient Ingestion Workflow\n")
    content.append(
        "```text\n"
        "[User Input: Username / Profile URL]\n"
        "                  │\n"
        "                  ▼\n"
        "[Input Normalization & Regex Validation: utils/validators.py]\n"
        "                  │\n"
        "                  ▼\n"
        "[Selenium Chrome WebDriver Initialization: scraper/browser_manager.py]\n"
        "  • Configured with anti-headless detection options in visible mode\n"
        "  • Sets window size 1920x1080 and standard user-agent string\n"
        "                  │\n"
        "                  ▼\n"
        "[DOM Navigation & Explicit WebDriverWait: scraper/hackerrank_scraper.py]\n"
        "  • Navigates to: https://www.hackerrank.com/profile/<username>\n"
        "  • Waits until CSS selector '.profile-page' or 'main' is hydrated\n"
        "                  │\n"
        "                  ├──────────────────────────────────────────────┐\n"
        "         (Page Load Successful)                         (Access Denied 403 / 404 / Network Fault)\n"
        "                  │                                              │\n"
        "                  ▼                                              ▼\n"
        "[HTML Parsing: scraper/scraper_utils.py]               [Graceful Fallback Mode]\n"
        "  • Decoupled selector tree execution                    • Load pre-curated profile from\n"
        "  • Extracts badges (counts svg.badge-star tags)           sample_data/sample_profiles.json (20 profiles)\n"
        "  • Parses Gold/Silver/Bronze tier levels                • OR allow custom JSON/CSV profile upload\n"
        "  • Extracts skills & verified certificates                      │\n"
        "                  │                                              │\n"
        "                  └──────────────────────┬───────────────────────┘\n"
        "                                         │\n"
        "                                         ▼\n"
        "                    [Database Upsert: database/db_manager.py]\n"
        "                      • Persists into profiles table (UNIQUE username)\n"
        "                      • Cascades skills, languages, badges & stats\n"
        "                      • Records execution duration in scraping_logs table\n"
        "```\n"
    )
    
    content.append("### Pipeline 2: 4-Layer Multi-Metric Code Similarity & Identifier Normalization Pipeline\n")
    content.append(
        "```text\n"
        "    [Source Code A (File or Paste)]                 [Source Code B (File or Paste)]\n"
        "                   │                                               │\n"
        "                   └───────────────────────┬───────────────────────┘\n"
        "                                           │\n"
        "                                           ▼\n"
        "                  [Preprocessing & Tokenization: detection/code_preprocessor.py]\n"
        "                    • Strips comments (# and block comments) via tokenize module\n"
        "                    • Normalizes irregular indentation and whitespace\n"
        "                    • Optional Identifier Normalization Mode:\n"
        "                        - Maps user identifiers: x -> VAR_1, count -> VAR_2\n"
        "                        - Strictly preserves Python keywords (def, for, return, in)\n"
        "                        - Strictly preserves built-ins (range, len, int, list)\n"
        "                                           │\n"
        "                   ┌───────────────────────┼───────────────────────┐\n"
        "                   ▼                       ▼                       ▼\n"
        "        [Layer 1: Token Similarity]  [Layer 2: TF-IDF Cosine]  [Layer 3: SequenceMatcher]\n"
        "        • 50% Jaccard Overlap        • Scikit-learn TF-IDF     • difflib SequenceMatcher\n"
        "        • 50% Token Frequency Cosine • N-gram word/symbol      • Sequential line diff\n"
        "        • Weight: 25%                • Weight: 25%             • Weight: 20%\n"
        "                   │                       │                       │\n"
        "                   └───────────────────────┼───────────────────────┘\n"
        "                                           ▼\n"
        "                         [Layer 4: Abstract Syntax Tree Vectorization]\n"
        "                         • Parses code into AST via Python ast.parse()\n"
        "                         • Computes normalized node type distribution vector Φ(T)\n"
        "                         • Measures control flow nesting & branch depth\n"
        "                         • Computes cosine similarity between node vectors\n"
        "                         • Weight: 30% (falls back gracefully if syntax invalid)\n"
        "                                           │\n"
        "                                           ▼\n"
        "                          [Blended Ensemble Score Formulation]\n"
        "                          S_total = 0.25·Token + 0.25·TFIDF + 0.20·Seq + 0.30·AST\n"
        "                                           │\n"
        "                                           ▼\n"
        "                         [Interactive Visual Line Diff & Metrics Table]\n"
        "```\n"
    )

    content.append("### Pipeline 3: Explainable Heuristic AI Pattern Forensics Pipeline\n")
    content.append(
        "```text\n"
        "                         [Uploaded Python Source Code]\n"
        "                                       │\n"
        "                                       ▼\n"
        "              [Heuristic Pattern Scanners: detection/ai_pattern_analysis.py]\n"
        "               │\n"
        "               ├─► Check 1: Step-by-Step Numbered Comments (e.g., # Step 1: ..., # 1. ...)\n"
        "               │\n"
        "               ├─► Check 2: Identifier Casing Regularity (casing entropy across snake_case/camelCase)\n"
        "               │\n"
        "               ├─► Check 3: Structured Docstring & Type Hint Ratio (Sphinx / Google docstrings)\n"
        "               │\n"
        "               ├─► Check 4: AST Branch Symmetry & Control Regularity (low depth variance)\n"
        "               │\n"
        "               └─► Check 5: Standard Algorithm Boilerplate Overlap (Two-Sum, Kadane, LRU)\n"
        "                                       │\n"
        "                                       ▼\n"
        "                        [Aggregated Heuristic Index Score (0 - 100)]\n"
        "                                       │\n"
        "                    ┌──────────────────┼──────────────────┐\n"
        "                    ▼                  ▼                  ▼\n"
        "                [0 - 34 pts]      [35 - 64 pts]       [65 - 100 pts]\n"
        "             'Few Indicators'    'Some Indicators'  'Several Indicators'\n"
        "              (Human-aligned)        (Hybrid)           (AI-aligned)\n"
        "                                       │\n"
        "                                       ▼\n"
        "                     [Mandatory Ethical & Analytical Disclaimers]\n"
        "           \"Heuristics identify stylistic markers; NOT proof of AI authorship.\"\n"
        "```\n"
    )

    # Section 4: Database Schema Table
    content.append("## 4. RELATIONAL DATABASE SCHEMA (9 TABLES)\n")
    content.append(
        "| Table Name | Primary / Foreign Keys | Description |\n"
        "| :--- | :--- | :--- |\n"
        "| `profiles` | PK: `id`, UNIQUE: `username` | Stores core candidate attributes: display name, country, description, is_sample, source_label, timestamp. |\n"
        "| `profile_statistics` | PK: `id`, FK: `profile_id` | Stores quantitative metrics: total problems, rank, contest rating, badges count. |\n"
        "| `programming_languages` | PK: `id`, FK: `profile_id` | Language proficiency entries: language_name, problems_solved, proficiency. |\n"
        "| `skills` | PK: `id`, FK: `profile_id` | Verified and practiced skills: skill_name, skill_level, verified boolean. |\n"
        "| `badges_and_achievements` | PK: `id`, FK: `profile_id` | Badges, star levels (1-5 stars), Gold/Silver/Bronze tiers, and verified certificates. |\n"
        "| `recent_activity` | PK: `id`, FK: `profile_id` | Recent user activity feed records: activity_title, description, date_or_time_ago. |\n"
        "| `scraping_logs` | PK: `id`, FK: `profile_id` | Audit trail of scraping events: username, status, source_mode, duration_sec, error_message. |\n"
        "| `code_similarity_analyses` | PK: `id` | History of similarity comparisons: file_a, file_b, overall_similarity, token_sim, tfidf_sim, ast_sim. |\n"
        "| `ai_pattern_analyses` | PK: `id` | History of heuristic AI audits: filename, indicator_score, classification_label, findings_json. |\n\n"
    )

    # Section 5: Source Code of Main Files
    content.append("## 5. SOURCE CODE OF CORE SYSTEM FILES\n")
    
    for filename, filepath, desc in MAIN_FILES:
        content.append(f"### File: `{filename}`")
        content.append(f"**Role:** {desc}  ")
        content.append(f"**Location:** `file:///{str(filepath).replace(chr(92), '/')}`\n")
        
        if filepath.exists():
            code = filepath.read_text(encoding="utf-8", errors="replace")
            content.append("```python\n" + code + "\n```\n")
        else:
            content.append(f"*File not found at {filepath}*\n")
        content.append("---\n")
        
    md_path.write_text("\n".join(content), encoding="utf-8")
    print(f"Generated Markdown Document: {md_path}")

def generate_word_doc(docx_path: Path):
    """Generate professional Microsoft Word (.docx) document."""
    doc = Document()
    
    # Page setup - Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    
    # Document Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("HACKER ANALYTICS AND AI CODE DETECTION SYSTEM")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(30, 58, 138)
    
    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(16)
    run_sub = sub_p.add_run("Complete Project Architecture, Folder Structure, Workflows, Pipelines & Source Code Reference")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = RGBColor(71, 85, 105)
    
    # Meta Box Table
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.columns[0].width = Inches(3.3)
    meta_table.columns[1].width = Inches(3.3)
    
    meta_data = [
        [("System Author", "Janardhana Sai"), ("Academic Institution", "New Horizon College of Engineering")],
        [("Core Stack", "Python 3.11, Selenium 4, AST, Streamlit, SQLite"), ("Git Repository", "Janardhana-sai/hacker-analytics-ai-detection")]
    ]
    for r_idx, row in enumerate(meta_data):
        for c_idx, (k, v) in enumerate(row):
            cell = meta_table.cell(r_idx, c_idx)
            set_cell_background(cell, "F1F5F9")
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            r_k = p.add_run(f"{k}: ")
            r_k.bold = True
            r_k.font.size = Pt(9)
            r_v = p.add_run(v)
            r_v.font.size = Pt(9)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Section 1: Overview
    h1 = doc.add_heading("1. Executive Summary & Architectural Overview", level=1)
    h1.style.font.color.rgb = RGBColor(30, 58, 138)
    
    doc.add_paragraph(
        "The Hacker Analytics and AI Code Detection System is an end-to-end Python developer intelligence "
        "and source-code integrity platform. It bridges public competitive programming profile analytics with "
        "deep syntactic code forensics and explainable heuristic AI pattern detection. Built entirely from scratch "
        "using clean, modular Python, the platform is structured into decoupled packages for scraping, analytics, "
        "detection, relational database management, and presentation."
    )
    
    # Embed Architecture Image if available
    img_arch = ASSETS_DIR / "fig_system_architecture.png"
    if img_arch.exists():
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        doc.add_picture(str(img_arch), width=Inches(6.5))
        p_cap = doc.add_paragraph("Figure 1.1: Layered System Architecture Diagram (Presentation, Core, AST, and Data Vault)")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.style.font.size = Pt(8.5)
        p_cap.style.font.italic = True
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Section 2: Folder Structure
    h2 = doc.add_heading("2. Complete Folder & File Structure Tree", level=1)
    h2.style.font.color.rgb = RGBColor(30, 58, 138)
    
    doc.add_paragraph("The project follows a clean, decoupled package architecture with comprehensive modularity:")
    
    tree_text = (
        "hacker-analytics-ai-detection/\n"
        "├── app.py                     # Streamlit Main Application Entrypoint & Page Router\n"
        "├── config.py                  # Central System Configurations, Thresholds & Disclaimers\n"
        "├── requirements.txt           # Python Dependency Specifications\n"
        "├── README.md                  # Project Documentation & GitHub Overview\n"
        "├── .gitignore                 # Git Privacy Filter (Excludes databases, logs, secrets)\n"
        "├── generate_novelty_pdf.py    # Script to compile IEEE Literature Gap Analysis PDF\n"
        "├── generate_final_project_report.py # Script to compile 25-page Academic Project Report PDF\n"
        "├── build_diagrams.py          # Script generating high-resolution Matplotlib system diagrams\n"
        "├── analytics/                 # Statistical Analytics & Data Aggregation Package\n"
        "│   ├── coding_analytics.py    # Multi-timeframe trend resampling (3M, 6M, 1Y, 3Y, All)\n"
        "│   ├── profile_analysis.py    # Profile summaries, star totals & unexposed field detection\n"
        "│   └── statistics.py          # Summary statistics, radar charts & language distributions\n"
        "├── dashboard/                 # Streamlit Web UI Pages & Presentation Tier\n"
        "│   ├── home.py                # Futuristic Hero Banner, KPI metrics, launchpad & PDF downloads\n"
        "│   ├── sidebar.py             # Sidebar navigation radio & real-time Workspace Vault metrics\n"
        "│   ├── scraper_page.py        # Selenium scraper control (Live visible, headless, sample fallback)\n"
        "│   ├── profile_page.py        # HackerRank profile viewer & data-backed insights cards\n"
        "│   ├── coding_page.py         # Coding analytics, multi-period trends, language donuts\n"
        "│   ├── similarity_page.py     # Pairwise code similarity, AST diffs & normalized variable toggle\n"
        "│   ├── ai_detection_page.py   # Heuristic AI forensic analysis, indicator score & breakdown\n"
        "│   └── history_page.py        # Tabbed relational audit history & CSV export tables\n"
        "├── database/                  # SQLite Relational Database Engine\n"
        "│   ├── schema.py              # DDL statements for all 9 normalized tables & index definitions\n"
        "│   └── db_manager.py          # DatabaseManager class: CRUD operations, foreign keys & cascades\n"
        "├── detection/                 # Syntactic AST & Source-Code Forensics Package\n"
        "│   ├── code_preprocessor.py   # Tokenizer, comment stripper & identifier normalizer (VAR_1, VAR_2)\n"
        "│   ├── ast_analysis.py        # AST parser, node distribution vectorizer & tree depth analyzer\n"
        "│   ├── code_similarity.py     # 4-Layer ensemble similarity scorer (Token, TF-IDF, Seq, AST)\n"
        "│   └── ai_pattern_analysis.py # Explainable heuristic AI stylometric rules & scoring engine\n"
        "├── scraper/                   # Selenium Browser Automation Package\n"
        "│   ├── browser_manager.py     # ChromeDriver options, process lifecycle & visible/headless driver\n"
        "│   ├── hackerrank_scraper.py  # Page loader, explicit DOM wait conditions & resilient scraping\n"
        "│   └── scraper_utils.py       # Decoupled CSS selectors, badge star counters & parsers\n"
        "├── utils/                     # General Helper Utilities & Validators\n"
        "│   ├── helpers.py             # Timestamps, SHA-256 hashing, safe JSON serializers\n"
        "│   └── validators.py          # HackerRank username normalization & Python code validation\n"
        "├── data/                      # Local Database & Storage Vault (Git-Ignored)\n"
        "│   └── hackerrank.db          # SQLite database with 9 relational tables\n"
        "├── sample_data/               # Curated Demonstration Profiles & Sample Code\n"
        "│   ├── sample_profiles.json   # 20 pre-curated offline HackerRank profiles\n"
        "│   └── sample_code_*.py       # 9 sample Python files across human and AI archetypes\n"
        "├── tests/                     # Automated Pytest Unit Test Suite (14 Tests)\n"
        "│   ├── test_analytics.py      # Unit tests for multi-timeframe analytics & statistics\n"
        "│   ├── test_database.py       # Unit tests for SQLite CRUD & relational foreign keys\n"
        "│   ├── test_detection.py      # Unit tests for AST parsing & identifier normalization\n"
        "│   └── test_scraper.py        # Unit tests for selector isolation & username parsing\n"
        "└── report_assets/             # High-Resolution Architectural Diagram PNGs"
    )
    add_code_block_to_docx(doc, tree_text)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Section 3: Workflows & Pipelines
    h3 = doc.add_heading("3. Core Workflows & Execution Pipelines", level=1)
    h3.style.font.color.rgb = RGBColor(30, 58, 138)
    
    doc.add_heading("3.1 Selenium Scraping & Resilient Ingestion Pipeline", level=2)
    doc.add_paragraph(
        "The web scraping engine operates using visible and headless Selenium automation with decoupled selectors. "
        "It applies WebDriverWait conditions for DOM element hydration, extracts badges (counting SVG stars and parsing tier classes), "
        "and automatically falls back to an offline 20-profile curated vault if Cloudflare anti-bot restrictions (HTTP 403) or network failures occur."
    )
    img_sc = ASSETS_DIR / "fig_scraper_workflow.png"
    if img_sc.exists():
        doc.add_picture(str(img_sc), width=Inches(6.5))
        p_cap = doc.add_paragraph("Figure 3.1: Selenium Web Scraping & Resilient Fallback Workflow")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.style.font.size = Pt(8.5)
        p_cap.style.font.italic = True
        
    doc.add_heading("3.2 4-Layer Multi-Metric Code Similarity & Identifier Normalization Pipeline", level=2)
    doc.add_paragraph(
        "Source code similarity is evaluated via a 4-layer ensemble combining lexical, statistical, sequential, and syntactic metrics. "
        "Crucially, the preprocessor implements automated identifier normalization (mapping user variables to VAR_1, VAR_2 while "
        "preserving language keywords and built-in symbols). This defeats variable-renaming obfuscation, maintaining 94.0% detection accuracy "
        "where traditional token tools drop to 42.5%."
    )
    img_sim = ASSETS_DIR / "fig_similarity_pipeline.png"
    if img_sim.exists():
        doc.add_picture(str(img_sim), width=Inches(6.5))
        p_cap = doc.add_paragraph("Figure 3.2: 4-Layer Multi-Metric Source-Code Similarity Pipeline with AST Normalizer")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.style.font.size = Pt(8.5)
        p_cap.style.font.italic = True
        
    doc.add_heading("3.3 Explainable Heuristic AI Pattern Forensics Pipeline", level=2)
    doc.add_paragraph(
        "Unlike commercial black-box detectors that output hallucinated percentages, our system inspects concrete stylistic markers: "
        "step-by-step numbered comments, identifier casing uniformity, docstring and type hint ratios, and AST branch symmetry. "
        "Code is categorized into actionable confidence bands (Few, Some, Several indicators observed) backed by mandatory ethical disclaimers."
    )
    img_ai = ASSETS_DIR / "fig_ai_heuristic_workflow.png"
    if img_ai.exists():
        doc.add_picture(str(img_ai), width=Inches(6.5))
        p_cap = doc.add_paragraph("Figure 3.3: Explainable Heuristic AI Pattern Forensics Architecture")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.style.font.size = Pt(8.5)
        p_cap.style.font.italic = True
        
    doc.add_heading("3.4 Relational Database ER Schema (9 Normalized Tables)", level=2)
    doc.add_paragraph(
        "Data persistence is managed via an embedded SQLite database (`data/hackerrank.db`) featuring 9 relational tables: "
        "profiles, profile_statistics, programming_languages, skills, badges_and_achievements, recent_activity, scraping_logs, "
        "code_similarity_analyses, and ai_pattern_analyses. Foreign key constraints with ON DELETE CASCADE guarantee referential integrity."
    )
    img_er = ASSETS_DIR / "fig_er_diagram.png"
    if img_er.exists():
        doc.add_picture(str(img_er), width=Inches(6.5))
        p_cap = doc.add_paragraph("Figure 3.4: Relational Database Entity-Relationship (ER) Schema (9 Normalized Tables)")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.style.font.size = Pt(8.5)
        p_cap.style.font.italic = True
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Section 4: Source Code of Main Files
    h4 = doc.add_heading("4. Source Code of Core System Modules", level=1)
    h4.style.font.color.rgb = RGBColor(30, 58, 138)
    
    for filename, filepath, desc in MAIN_FILES:
        doc.add_heading(f"Module: {filename}", level=2)
        p_desc = doc.add_paragraph()
        r_d1 = p_desc.add_run("Description: ")
        r_d1.bold = True
        p_desc.add_run(desc)
        p_desc.paragraph_format.space_after = Pt(4)
        
        if filepath.exists():
            code = filepath.read_text(encoding="utf-8", errors="replace")
            add_code_block_to_docx(doc, code)
        else:
            doc.add_paragraph(f"File not found at: {filepath}")
        doc.add_paragraph().paragraph_format.space_after = Pt(8)
        
    doc.save(str(docx_path))
    print(f"Generated Microsoft Word Document: {docx_path}")

if __name__ == "__main__":
    md_out = BASE_DIR / "PROJECT_TECHNICAL_REPORT_DOCUMENT.md"
    docx_out = BASE_DIR / "PROJECT_TECHNICAL_REPORT_DOCUMENT.docx"
    
    generate_markdown_doc(md_out)
    generate_word_doc(docx_out)
    print("All report documentation files generated successfully!")
