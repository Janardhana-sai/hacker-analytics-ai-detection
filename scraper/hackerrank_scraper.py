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
