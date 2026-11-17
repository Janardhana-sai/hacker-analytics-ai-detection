"""Analytics and statistical visualization package."""

from analytics.coding_analytics import (
    build_activity_trend_df,
    build_badge_and_achievement_summary,
    build_language_distribution,
    build_profile_comparison_df,
    build_skill_distribution,
    create_activity_trend_chart,
    create_badge_chart,
    create_comparison_chart,
    create_language_bar_chart,
    create_language_pie_chart,
    create_matplotlib_language_summary,
    create_skill_chart,
)
from analytics.profile_analysis import analyze_single_profile
from analytics.statistics import compute_numeric_summary, safe_percentage

__all__ = [
    "compute_numeric_summary",
    "safe_percentage",
    "analyze_single_profile",
    "build_language_distribution",
    "build_skill_distribution",
    "build_badge_and_achievement_summary",
    "build_profile_comparison_df",
    "build_activity_trend_df",
    "create_language_bar_chart",
    "create_language_pie_chart",
    "create_skill_chart",
    "create_badge_chart",
    "create_comparison_chart",
    "create_activity_trend_chart",
    "create_matplotlib_language_summary",
]

