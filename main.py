import requests
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

WEBHOOK_URL = "https://discord.com/api/webhooks/1505806483198050324/7caQ_Y_5pA-s81DF0NFGnSanoEIeQxkAIigAQctPpgTax2-OG9MAFcaUD1ikkfeJsEDZ"

SEARCH_URL = "https://jp.mercari.com/search?keyword=%E3%81%94%E3%81%A1%E3%81%86%E3%81%95%20ONKYO"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:

    driver.get(SEARCH_URL)

    time.sleep(5)

    links = driver.find_elements(By.TAG_NAME, "a")

    found = False

    for link in links:

        href = link.get_attribute("href")

        if href and "/item/" in href:

            requests.post(
                WEBHOOK_URL,
                json={
                    "content": f"【商品検出】\n{href}"
                }
            )

            found = True
            break

    if not found:

        requests.post(
            WEBHOOK_URL,
            json={
                "content": "商品リンク検出失敗"
            }
        )

finally:

    driver.quit()
