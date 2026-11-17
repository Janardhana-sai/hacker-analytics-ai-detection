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
