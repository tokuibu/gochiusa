import requests
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

WEBHOOK_URL = "https://discord.com/api/webhooks/1505806483198050324/7caQ_Y_5pA-s81DF0NFGnSanoEIeQxkAIigAQctPpgTax2-OG9MAFcaUD1ikkfeJsEDZ"

MERCARI_URL = "https://jp.mercari.com/search?keyword=%E3%81%94%E3%81%A1%E3%81%86%E3%81%95%20ONKYO"

YAHOO_URL = "https://auctions.yahoo.co.jp/search/search?p=%E3%81%94%E3%81%A1%E3%81%86%E3%81%95+ONKYO"

LAST_MERCARI = "last_mercari.txt"
LAST_YAHOO = "last_yahoo.txt"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# -----------------
# メルカリ監視
# -----------------

driver = webdriver.Chrome(options=options)

try:

    driver.get(MERCARI_URL)

    time.sleep(5)

    links = driver.find_elements(By.TAG_NAME, "a")

    mercari_url = None

    for link in links:

        href = link.get_attribute("href")

        if href and "/item/" in href:

            href = href.split("?")[0]

            mercari_url = href
            break

    if mercari_url:

        old_url = ""

        if os.path.exists(LAST_MERCARI):

            with open(LAST_MERCARI, "r") as f:
                old_url = f.read().strip()

        if mercari_url != old_url:

            requests.post(
                WEBHOOK_URL,
                json={
                    "content": f"【メルカリ新着】\n{mercari_url}"
                }
            )

            with open(LAST_MERCARI, "w") as f:
                f.write(mercari_url)

finally:

    driver.quit()

# -----------------
# ヤフオク監視
# -----------------

driver2 = webdriver.Chrome(options=options)

try:

    driver2.get(YAHOO_URL)

    time.sleep(10)

    links = driver2.find_elements(By.TAG_NAME, "a")

    yahoo_url = None

    for link in links:

        href = link.get_attribute("href")

        if href and "/auction/" in href:

            href = href.split("?")[0]

            yahoo_url = href
            break

    if yahoo_url:

        old_url = ""

        if os.path.exists(LAST_YAHOO):

            with open(LAST_YAHOO, "r") as f:
                old_url = f.read().strip()

        if yahoo_url != old_url:

            requests.post(
                WEBHOOK_URL,
                json={
                    "content": f"【ヤフオク新着】\n{yahoo_url}"
                }
            )

            with open(LAST_YAHOO, "w") as f:
                f.write(yahoo_url)

finally:

    driver2.quit()
