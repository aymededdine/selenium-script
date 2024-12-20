from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import random
import string
import time

print("[INFO] Starting the Selenium script.")

try:
    # Start the session
    print("[INFO] Launching the Chrome browser.")
    driver = webdriver.Chrome()
    print("[INFO] Browser launched successfully.")

    # Navigate to Google
    url = "http://www.google.com/?hl=en"
    print(f"[INFO] Navigating to URL: {url}")
    driver.get(url)
    print("[INFO] Page loaded successfully.")

    # Perform the search
    print("[INFO] Getting the page search input.")
    search = driver.find_element(By.NAME, "q")

    print("[INFO] Performing the search.")
    search.send_keys("hello world")
    search.send_keys(Keys.RETURN)

    # Wait for search results to load and add a small delay
    print("[INFO] Waiting for search results to load.")
    time.sleep(2)  # Add a small delay to ensure page loads completely
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    print("[INFO] Search results are displayed.")

    # Try multiple possible selectors for search results
    selectors = [
        "//div[@class='g' and not(ancestor::div[contains(@class, 'related-question-pair')])]",
        "//div[contains(@class, 'g') and not(ancestor::div[contains(@class, 'related-question-pair')])]",
        "//div[@jscontroller and contains(@class, 'g')]",
        "//div[@data-hveid and contains(@class, 'g')]"
    ]

    search_results = []
    for selector in selectors:
        search_results = driver.find_elements(By.XPATH, selector)
        print(f"[INFO] Found {len(search_results)} results with selector: {selector}")
        if len(search_results) > 0:
            break

    # Prepare the data for saving
    results_data = []

    if len(search_results) == 0:
        print("[INFO] No search results found.")
        results_data.append({"Title": "No search results found.", "Description": "", "URL": ""})
    else:
        result_count = 0
        for result in search_results:
            try:
                # Try multiple selectors for title and description
                title = None
                description = None
                url = None

                # Try different title selectors
                title_selectors = ["h3", "h3.LC20lb", ".LC20lb"]
                for selector in title_selectors:
                    try:
                        title_element = result.find_element(By.CSS_SELECTOR, selector)
                        title = title_element.text
                        if title:
                            break
                    except:
                        continue

                # Try different description selectors
                desc_selectors = ["div.VwiC3b", ".VwiC3b", "div.lEBKkf", ".lEBKkf"]
                for selector in desc_selectors:
                    try:
                        desc_element = result.find_element(By.CSS_SELECTOR, selector)
                        description = desc_element.text
                        if description:
                            break
                    except:
                        continue

                # Try to get URL
                try:
                    url_element = result.find_element(By.CSS_SELECTOR, "a")
                    url = url_element.get_attribute("href")
                except:
                    print("[INFO] No URL found for this result.")
                    url = "No URL available"

                # Skip if we couldn't find either title or description
                if not title or not description:
                    continue

                # Add to results data
                results_data.append({"Title": title, "Description": description, "URL": url})
                result_count += 1

                print(f"Result {result_count}:")
                print(f"  Title: {title}")
                print(f"  Description: {description}")
                print(f"  URL: {url}")
                print()

                # Break if we've found 10 valid results
                if result_count >= 10:
                    break

            except Exception as e:
                print(f"[INFO] Couldn't process result: {e}")
                continue

    # Save the results to an Excel file
    random_key = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    output_filename = f'hello-world-{random_key}.xlsx'
    results_df = pd.DataFrame(results_data)
    results_df.to_excel(output_filename, index=False, engine='openpyxl')
    print(f"[INFO] Excel file saved successfully as {output_filename}.")

except Exception as e:
    print(f"[ERROR] An error occurred: {e}")

finally:
    # Close the browser session
    print("[INFO] Closing the browser and ending the session.")
    driver.quit()
    print("[INFO] Script execution completed.")
