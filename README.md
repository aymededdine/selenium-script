# Selenium Google Search Script

This guide provides instructions for installing dependencies and running the Selenium script to perform a Google search and save results to an Excel file.

---

## Prerequisites

1. **Python** (3.6+).
2. **Google Chrome**
3. **PIP** for Python package installation.

---

## Installation

1. **Install Dependencies:**

   ```bash
   pip install selenium pandas openpyxl
   ```

---

## Usage

1. **Run the Script:**

   ```bash
   python3 python-developer-interview-task.py
   ```

2. **Output:**
   - Google search for "hello world."
   - Extracts up to 10 results.
   - Saves results to an Excel file named `hello-world-<random_key>.xlsx`.

---

## Notes

- Update selectors in the script if Google’s structure changes and to handle the People also ask Section PAA.
