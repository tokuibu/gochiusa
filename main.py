import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1505806483198050324/7caQ_Y_5pA-s81DF0NFGnSanoEIeQxkAIigAQctPpgTax2-OG9MAFcaUD1ikkfeJsEDZ"

SEARCH_URL = "https://jp.mercari.com/search?keyword=%E3%81%94%E3%81%A1%E3%81%86%E3%81%95%20ONKYO"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(SEARCH_URL, headers=headers)

if response.status_code != 200:
    requests.post(
        WEBHOOK_URL,
        json={"content": "メルカリ取得失敗"}
    )
    exit()

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

sent = False

for link in links:

    href = link.get("href")

    if href and "/item/" in href:

        item_url = "https://jp.mercari.com" + href

        message = {
            "content": f"【新着候補】\n{item_url}"
        }

        requests.post(WEBHOOK_URL, json=message)

        sent = True
        break

if not sent:
    requests.post(
        WEBHOOK_URL,
        json={"content": "商品が見つかりませんでした"}
    )
