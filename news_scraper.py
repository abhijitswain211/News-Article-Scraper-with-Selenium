"""
News Article Scraper using Selenium (BBC Version)
-------------------------------------------------
This script:
1. Launches Chrome
2. Opens BBC News homepage
3. Opens 3 articles one by one
4. Extracts headline + first 1–2 paragraphs
5. Saves everything in articles.txt (overwrite on each run)
6. Prints the same content in the console for instant viewing

Author: Abhijit Swain
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_articles():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")

    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    try:
        driver.get("https://www.bbc.com/news")

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.gs-c-promo-heading"))
        )

        articles = driver.find_elements(By.CSS_SELECTOR, "a.gs-c-promo-heading")[:3]
        results = []

        for i in range(len(articles)):
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(articles[i])
                ).click()

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                )

                headline = driver.find_element(By.TAG_NAME, "h1").text
                paragraphs = driver.find_elements(By.TAG_NAME, "p")[:2]
                content = "\n".join([p.text for p in paragraphs if p.text.strip()])

                results.append(f"Article {i+1}:\n{headline}\n{content}\n")

            except Exception as e:
                print(f"⚠️ Skipping article {i+1} due to error: {e}")

            driver.back()

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.gs-c-promo-heading"))
            )
            articles = driver.find_elements(By.CSS_SELECTOR, "a.gs-c-promo-heading")[:3]

        with open("articles.txt", "w", encoding="utf-8") as f:
            f.write("\n---\n".join(results))

        print("\n Done! Articles saved to 'articles.txt'\n")
        print(" Scraped Articles:\n")
        print("\n---\n".join(results))  

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_articles()
