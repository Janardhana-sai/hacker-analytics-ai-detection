"""
Input validation helpers for HackerRank usernames, profile URLs, and uploaded source code.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from config import HACKERRANK_PROFILE_BASE_URL, MAX_CODE_FILE_BYTES

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,50}$")
ALLOWED_HACKERRANK_HOSTS = {"hackerrank.com", "www.hackerrank.com"}
RESERVED_HACKERRANK_PATHS = {
    "auth",
    "login",
    "signup",
    "dashboard",
    "domains",
    "contests",
    "challenges",
    "skills-verification",
    "certificates",
    "apply",
    "about-us",
    "products",
    "pricing",
    "support",
    "404",
}


def validate_and_parse_profile_input(raw_input: str) -> tuple[bool, dict[str, str]]:
    """
    Validate a HackerRank username or profile URL and return canonical values.

    Returns:
        (True, {"username": ..., "profile_url": ...}) on success
        (False, {"error": ...}) on validation failure
    """
    if not raw_input or not isinstance(raw_input, str):
        return False, {"error": "Please enter a HackerRank username or profile URL."}

    cleaned = raw_input.strip()
    if not cleaned:
        return False, {"error": "Username or profile URL cannot be empty."}

    lowered = cleaned.lower()
    looks_like_url = (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or "hackerrank.com" in lowered
        or "/" in cleaned
    )

    username = ""
    if looks_like_url:
        candidate_url = cleaned if "://" in cleaned else f"https://{cleaned}"
        parsed = urlparse(candidate_url)

        if parsed.scheme not in {"http", "https"}:
            return False, {"error": "Invalid URL scheme. Only http/https HackerRank URLs are supported."}

        host = (parsed.netloc or "").lower().split(":")[0]
        if host not in ALLOWED_HACKERRANK_HOSTS:
            return False, {
                "error": (
                    f"Invalid profile URL host '{host or 'unknown'}'. "
                    "Please enter a valid hackerrank.com/profile/<username> URL or a plain username."
                )
            }

        parts = [p for p in parsed.path.split("/") if p]
        if not parts:
            return False, {"error": "HackerRank URL does not contain a username."}

        if parts[0].lower() == "profile":
            if len(parts) < 2:
                return False, {"error": "Profile URL is missing the username after '/profile/'."}
            username = parts[1]
        elif len(parts) == 1 and parts[0].lower() not in RESERVED_HACKERRANK_PATHS:
            username = parts[0]
        else:
            return False, {
                "error": (
                    "URL does not point to a valid HackerRank user profile. "
                    "Expected format: https://www.hackerrank.com/profile/<username>"
                )
            }
    else:
        username = cleaned.lstrip("@").strip()

    if not username:
        return False, {"error": "Username cannot be empty."}

    if len(username) > 50:
        return False, {"error": "Username must be 50 characters or fewer."}

    if username.lower() in RESERVED_HACKERRANK_PATHS:
        return False, {"error": f"'{username}' is a reserved HackerRank path, not a user profile."}

    if not USERNAME_PATTERN.match(username):
        return False, {
            "error": (
                "Invalid username format. Only letters, numbers, underscores (_), "
                "hyphens (-), and dots (.) are allowed."
            )
        }

    canonical_url = f"{HACKERRANK_PROFILE_BASE_URL}{username}"
    parsed_canonical = urlparse(canonical_url)
    if parsed_canonical.scheme != "https" or parsed_canonical.netloc != "www.hackerrank.com":
        return False, {"error": "Constructed profile URL failed canonical validation."}

    return True, {"username": username, "profile_url": canonical_url}


def normalize_hackerrank_username(raw_input: str) -> str:
    """
    Extract a normalized HackerRank username when valid, or return best-effort stripped text.
    """
    ok, info = validate_and_parse_profile_input(raw_input)
    if ok:
        return info["username"]
    return (raw_input or "").strip().lstrip("@")


def validate_hackerrank_username(raw_input: str) -> tuple[bool, str]:
    """
    Backward-compatible wrapper returning (is_valid, username_or_error_message).
    """
    ok, info = validate_and_parse_profile_input(raw_input)
    if ok:
        return True, info["username"]
    return False, info["error"]


def validate_python_code(code: str, filename: str = "") -> tuple[bool, str]:
    """
    Validate uploaded or pasted Python source code for size and non-emptiness.
    """
    if not isinstance(code, str) or not code.strip():
        return False, "Source code cannot be empty."

    byte_size = len(code.encode("utf-8", errors="replace"))
    if byte_size > MAX_CODE_FILE_BYTES:
        return (
            False,
            f"File '{filename or 'input'}' exceeds the maximum size limit of {MAX_CODE_FILE_BYTES // 1024} KB.",
        )

    if filename and not filename.lower().endswith(".py"):
        return False, f"File '{filename}' is not a Python (.py) file."

    return True, "Valid Python source input."
