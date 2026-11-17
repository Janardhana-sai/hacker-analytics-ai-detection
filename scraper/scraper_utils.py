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
