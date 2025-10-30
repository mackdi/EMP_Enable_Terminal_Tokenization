# 🧠 Terminal Tokenization Automation

## Overview
This Python automation script uses **Playwright** to automatically visit multiple terminal edit URLs, enable the  
**“Supports Tokenization”** checkbox (if not already enabled), and click the **“Save Terminal”** button.

It was designed to handle unreliable admin portals — it automatically retries when encountering `502` or `504`  
gateway errors and skips saving if the checkbox is already enabled.

---

## 🚀 Features
- Reads all terminal edit URLs from a `urls.txt` file  
- Uses Microsoft Edge (via Playwright’s Chromium channel)  
- Lets you **log in manually once** before automation starts  
- Detects and **retries pages that return 502/504 errors**  
- Enables the **Supports Tokenization** checkbox automatically  
- Clicks **Save Terminal** only when needed  
- Skips saving if checkbox already checked  
- Logs all results to `automation_log.txt`  
- Gracefully continues even if some URLs fail  

---

## 🧩 Requirements

- **Python 3.8+**
- **Playwright** (with browsers installed)

Install the dependencies:

```bash
pip install playwright
playwright install
