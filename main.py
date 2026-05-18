import requests
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

WEBHOOK_URL = "https://discord.com/api/webhooks/1505806483198050324/7caQ_Y_5pA-s81DF0NFGnSanoEIeQxkAIigAQctPpgTax2-OG9MAFcaUD1ikkfeJsEDZ"

SEARCH_URL = "https://jp.mercari.com/search?keyword=%E3%81%94%E3%81%A1%E3%81%86%E3%81%95%20ONKYO"

LAST_URL_FILE = "last_url.txt"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:

    driver.get(SEARCH_URL)

    time.sleep(5)

    links = driver.find_elements(By.TAG_NAME, "a")

    item_url = None

    for link in links:

        href = link.get_attribute("href")

        if href and "/item/" in href:

            item_url = href
            break

    if not item_url:

        requests.post(
            WEBHOOK_URL,
            json={"content": "商品リンク検出失敗"}
        )

        exit()

    old_url = ""

    if os.path.exists(LAST_URL_FILE):

        with open(LAST_URL_FILE, "r") as f:
            old_url = f.read().strip()

    if item_url != old_url:

        requests.post(
            WEBHOOK_URL,
            json={
                "content": f"【新着商品】\n{item_url}"
            }
        )

        with open(LAST_URL_FILE, "w") as f:
            f.write(item_url)

    else:

        print("同じ商品のため通知なし")

finally:

    driver.quit()
