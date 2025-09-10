# """
# NDTV News Article Scraper using Selenium
# ---------------------------------------
# Launches Chrome, goes to NDTV, clicks "Latest", opens the first article,
# extracts headline & first paragraph, saves to articles.txt, and prints it.
# """

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# driver = webdriver.Chrome()

# try:
#     driver.get("https://www.ndtv.com")
#     time.sleep(2)

#     driver.find_element(By.CSS_SELECTOR, "a[href*='latest']").click()
#     time.sleep(2)

#     driver.find_elements(By.CSS_SELECTOR, "h2 a")[0].click()
#     time.sleep(2)

#     headline = driver.find_element(By.TAG_NAME, "h1").text
#     paragraph = driver.find_elements(By.TAG_NAME, "p")[0].text

#     result = f" Trending News:\n{headline}\n{paragraph}\n"

#     with open("articles.txt", "w", encoding="utf-8") as f:
#         f.write(result)

#     print("\n Article saved to 'articles.txt'\n")
#     print(result)

# finally:
#     driver.quit()

"""
NDTV News Article Scraper using Selenium
---------------------------------------
Launches Chrome, goes to NDTV, clicks "Latest", opens the first 3 articles,
extracts headline & first 1–2 paragraphs, saves them to articles.txt,
and prints them in the console.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.ndtv.com")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='latest']"))).click()

    results = []
    for i in range(3):
        articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2 a")))[:3]
        articles[i].click()

        headline = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text

        paragraphs = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "p")))
        first_two = " ".join(p.text for p in paragraphs[:2])

        results.append(f"📰 Article {i+1}:\n{headline}\n{first_two}\n")
        driver.back()

    with open("articles.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print("\n✅ 3 Articles saved to 'articles.txt'\n")
    for r in results:
        print(r)

finally:
    driver.quit()
