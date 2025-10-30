import sys
import time
import importlib.util
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

# ---------- PATHS ----------
if getattr(sys, "frozen", False):
    WORK_DIR = Path(sys.executable).parent
else:
    WORK_DIR = Path(__file__).resolve().parent

URLS_FILE = WORK_DIR / "urls.txt"
LOG_FILE = WORK_DIR / "automation_log.txt"

MAX_RETRIES = 5
RETRY_DELAY = 3  # seconds


# ---------- UTILS ----------
def ensure_playwright_package():
    if importlib.util.find_spec("playwright") is None:
        print("⚠️ Playwright not found. Install it first:\n   pip install playwright")
        sys.exit(1)

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def load_urls():
    if not URLS_FILE.exists():
        print(f"Missing file: {URLS_FILE}")
        sys.exit(0)
    lines = [ln.strip() for ln in URLS_FILE.read_text(encoding="utf-8").splitlines()]
    urls = [u for u in lines if u and not u.startswith("#")]
    log(f"Loaded {len(urls)} URLs.")
    return urls

def is_gateway_error(page):
    """Detects 502/504 or similar error content."""
    try:
        title = page.title()
        html = page.content()
        if "502" in title or "504" in title:
            return True
        if "502 Bad Gateway" in html or "504 Gateway Timeout" in html:
            return True
        return False
    except Exception:
        return True


# ---------- MAIN ----------
def main():
    ensure_playwright_package()
    try:
        LOG_FILE.unlink()
    except FileNotFoundError:
        pass

    urls = load_urls()

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=False, slow_mo=100)
        context = browser.new_context()
        page = context.new_page()

        log("Opening first URL for login...")
        page.goto(urls[0])
        input("\nPlease log in manually in Edge, then press [Enter] to continue... ")

        for i, url in enumerate(urls, 1):
            log(f"\n===== ({i}/{len(urls)}) Processing: {url} =====")
            success = False

            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    log(f"Attempt {attempt}...")
                    page.goto(url, timeout=60000)
                    page.wait_for_load_state("networkidle")

                    if is_gateway_error(page):
                        log(f"⚠️ Detected 502/504 gateway error, retrying in {RETRY_DELAY}s...")
                        time.sleep(RETRY_DELAY)
                        continue

                    checkbox = page.query_selector("#feature_supports_tokenization")
                    if not checkbox:
                        log("⚠️ Checkbox not found on page.")
                        raise Exception("Checkbox not found")

                    if checkbox.is_checked():
                        log("→ Checkbox already enabled. Skipping save and moving to next URL.")
                        success = True
                        break  # move to next URL

                    # Otherwise, enable it and save
                    checkbox.check()
                    log("✓ Enabled 'Supports Tokenization'")

                    save_button = page.query_selector("input[name='commit'][value='Save Terminal']")
                    if not save_button:
                        log("⚠️ Save button not found.")
                        raise Exception("Save button not found")

                    save_button.click()
                    log("💾 Clicked 'Save Terminal'")
                    time.sleep(3)

                    if is_gateway_error(page):
                        log("⚠️ Page returned 502/504 after saving, retrying...")
                        continue

                    success = True
                    log("✅ Saved successfully.")
                    break

                except Exception as e:
                    log(f"❌ Error on attempt {attempt}: {e}")
                    time.sleep(RETRY_DELAY)

            if not success:
                log(f"❌ Skipping {url} after {MAX_RETRIES} failed attempts.")

        log("\n✅ All URLs processed.")
        input("\nPress [Enter] to exit... ")
        browser.close()


if __name__ == "__main__":
    main()
