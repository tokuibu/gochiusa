import requests
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

WEBHOOK_URL = "https://discord.com/api/webhooks/1505806483198050324/7caQ_Y_5pA-s81DF0NFGnSanoEIeQxkAIigAQctPpgTax2-OG9MAFcaUD1ikkfeJsEDZ"

MERCARI_URL = "https://jp.mercari.com/search?keyword=%E3%81%94%E3%81%A1%E3%81%86%E3%81%95%20ONKYO"

SURUGAYA_URL = "https://www.suruga-ya.jp/search?search_word=%E3%81%94%E3%81%A1%E3%81%86%E3%81%95+ONKYO"

LAST_MERCARI = "last_mercari.txt"
LAST_SURUGAYA = "last_surugaya.txt"

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
# 駿河屋監視
# -----------------

requests.post(
    WEBHOOK_URL,
    json={"content": "駿河屋監視開始"}
)

driver2 = webdriver.Chrome(options=options)

try:

    driver2.get("https://www.suruga-ya.jp")

    time.sleep(5)

    driver2.get(SURUGAYA_URL)

    time.sleep(15)

    requests.post(
        WEBHOOK_URL,
        json={"content": "駿河屋検索ページアクセス成功"}
    )

    links = driver2.find_elements(By.TAG_NAME, "a")

    requests.post(
        WEBHOOK_URL,
        json={"content": f"リンク数: {len(links)}"}
    )

    for link in links:

        href = link.get_attribute("href")

        if href:

            requests.post(
                WEBHOOK_URL,
                json={
                    "content": f"取得リンク:\n{href}"
                }
            )

finally:

    driver2.quit()
