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

