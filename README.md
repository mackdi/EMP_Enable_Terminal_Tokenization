🧠 Terminal Tokenization Automation
Overview

This Python automation script uses Playwright to automatically visit multiple terminal edit URLs, enable the
“Supports Tokenization” checkbox (if not already enabled), and click the “Save Terminal” button.

It was designed to handle unreliable admin portals — it automatically retries when encountering 502 or 504
gateway errors and skips saving if the checkbox is already enabled.

🚀 Features

Reads all terminal edit URLs from a urls.txt file

Uses Microsoft Edge (via Playwright’s Chromium channel)

Lets you log in manually once before automation starts

Detects and retries pages that return 502/504 errors

Enables the Supports Tokenization checkbox automatically

Clicks Save Terminal only when needed

Skips saving if checkbox already checked

Logs all results to automation_log.txt

Gracefully continues even if some URLs fail

🧩 Requirements

Python 3.8+

Playwright (with browsers installed)

Install the dependencies:

pip install playwright
playwright install

📂 Files
File	Description
enable_tokenization.py	Main automation script
urls.txt	List of terminal edit URLs (one per line)
automation_log.txt	Generated automatically during execution

Example urls.txt:

https://example.com/terminals/123/edit
https://example.com/terminals/456/edit
https://example.com/terminals/789/edit

⚙️ How It Works

Launches Microsoft Edge using Playwright

Opens the first URL and pauses for manual login

After login, it goes through every URL in urls.txt

For each URL:

Loads the page and waits until it’s stable

If a 502/504 page is detected → retries up to 5 times

Finds the checkbox with id:

<input type="checkbox" id="feature_supports_tokenization">


If unchecked, checks it and clicks:

<input type="submit" name="commit" value="Save Terminal">


If already checked, skips saving and goes to the next URL

Logs every action and retry attempt

🖥️ Running the Script

Place enable_tokenization.py and urls.txt in the same folder.

Run:

python enable_tokenization.py


When Microsoft Edge opens:

Log in manually

Return to the console and press Enter

The script will process all URLs automatically.

Review the output in automation_log.txt.

🔁 Error Handling & Retries

Retries each URL up to 5 times if it encounters:

Page load errors

502 / 504 Gateway issues

Missing checkbox or button

Waits 3 seconds between retries (configurable in the script).

🧾 Example Log Output
[10:42:11] Loaded 12 URLs.
[10:42:14] Opening first URL for login...
[10:43:05] ===== (1/12) Processing: https://example.com/terminals/123/edit =====
[10:43:08] ✓ Enabled 'Supports Tokenization'
[10:43:09] 💾 Clicked 'Save Terminal'
[10:43:12] ✅ Saved successfully.
[10:43:15] ===== (2/12) Processing: https://example.com/terminals/456/edit =====
[10:43:18] → Checkbox already enabled. Skipping save and moving to next URL.

🧱 Configuration

You can adjust behavior inside the script:

Variable	Purpose	Default
MAX_RETRIES	Number of retries per URL	5
RETRY_DELAY	Delay (in seconds) between retries	3
headless=False	Run visible browser (change to True for headless mode)	False
