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

