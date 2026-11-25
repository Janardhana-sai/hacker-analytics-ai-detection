"""
Script to capture high-resolution clarity screenshots of all 7 Streamlit dashboard pages.
Saves images to screenshots/ and copies them to the artifact directory.
"""

import os
import time
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path(r"C:\Users\janar\.gemini\antigravity\brain\6472cebe-68df-4ce8-9373-28e544f413c5")

PAGES = [
    ("01_home_dashboard.png", "Home Dashboard"),
    ("02_selenium_web_scraper.png", "Selenium Web Scraper"),
    ("03_profile_analytics.png", "Profile Analytics"),
    ("04_coding_analytics.png", "Coding Analytics"),
    ("05_code_similarity.png", "Code Similarity"),
    ("06_ai_pattern_check.png", "AI Pattern Check"),
    ("07_code_quality_audit.png", "Code Quality"),
    ("08_analysis_history.png", "Analysis History"),
]

def capture_all_pages():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1200")
    chrome_options.add_argument("--force-device-scale-factor=1.25")  # High DPI clarity

    print("Launching headless Chrome for screenshot capture...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1200)

    try:
        url = "http://localhost:8501"
        print(f"Navigating to {url}...")
        driver.get(url)

        # Wait for Streamlit to hydrate
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='stAppViewContainer']"))
        )
        time.sleep(3)  # Allow charts to render

        for filename, page_keyword in PAGES:
            print(f"\nNavigating to: {page_keyword}...")

            # Locate radio button in sidebar
            # Streamlit radio buttons are inside [data-testid="stRadio"]
            radio_labels = driver.find_elements(By.CSS_SELECTOR, "[data-testid='stRadio'] label")
            target_label = None
            for lbl in radio_labels:
                if page_keyword.lower() in lbl.text.lower():
                    target_label = lbl
                    break

            if target_label:
                # Scroll into view and click
                driver.execute_script("arguments[0].scrollIntoView(true);", target_label)
                time.sleep(0.5)
                target_label.click()
                print(f"Clicked radio option: {target_label.text}")
            else:
                print(f"Warning: Could not find label matching '{page_keyword}', searching buttons...")
                # Fallback: check sidebar buttons or text
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    if page_keyword.lower() in btn.text.lower():
                        btn.click()
                        break

            # Wait for content update and charts
            time.sleep(3)

            # Adjust window height to capture full content or generous viewport
            save_path = SCREENSHOT_DIR / filename
            driver.save_screenshot(str(save_path))
            print(f"Saved: {save_path} ({os.path.getsize(save_path)} bytes)")

            # Also copy to artifact directory for easy embedding
            try:
                artifact_copy = ARTIFACT_DIR / filename
                shutil.copy2(save_path, artifact_copy)
                print(f"Copied to artifact dir: {artifact_copy}")
            except Exception as e:
                print(f"Notice: Artifact copy error: {e}")

    finally:
        driver.quit()
        print("\nAll page screenshots captured successfully!")

if __name__ == "__main__":
    capture_all_pages()
