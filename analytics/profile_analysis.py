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

