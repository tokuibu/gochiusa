import requests
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

WEBHOOK_URL = "https://discord.com/api/webhooks/1505806483198050324/7caQ_Y_5pA-s81DF0NFGnSanoEIeQxkAIigAQctPpgTax2-OG9MAFcaUD1ikkfeJsEDZ"

MERCARI_URLS = [
　　"https://jp.mercari.com/search?keyword=%E3%81%94%E3%81%A1%E3%81%86%E3%81%95%20ONKYO&sort=created_time&order=desc",

　　"https://jp.mercari.com/search?keyword=%E3%81%94%E6%B3%A8%E6%96%87%E3%81%AF%E3%81%86%E3%81%95%E3%81%8E%E3%81%A7%E3%81%99%E3%81%8B%20%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&sort=created_time&order=desc"
]

YAHOO_URLS = [
    "https://auctions.yahoo.co.jp/search/search?p=%E3%81%94%E3%81%A1%E3%81%86%E3%81%95+ONKYO&s1=new&o1=d",

    "https://auctions.yahoo.co.jp/search/search?p=%E3%81%94%E6%B3%A8%E6%96%87%E3%81%AF%E3%81%86%E3%81%95%E3%81%8E%E3%81%A7%E3%81%99%E3%81%8B+%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&s1=new&o1=d"
]

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

    for search_url in MERCARI_URLS:

        driver.get(search_url)

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
                        "content":
                        f"【メルカリ新着】\n{mercari_url}"
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

    for search_url in YAHOO_URLS:

        driver2.get(search_url)

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
                        "content":
                        f"【ヤフオク新着】\n{yahoo_url}"
                    }
                )

                with open(LAST_YAHOO, "w") as f:
                    f.write(yahoo_url)

finally:

    driver2.quit()
