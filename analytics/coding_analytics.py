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

