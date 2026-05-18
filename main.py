import requests
from bs4 import BeautifulSoup

WEBHOOK_URL = "https://discord.com/api/webhooks/1505806483198050324/7caQ_Y_5pA-s81DF0NFGnSanoEIeQxkAIigAQctPpgTax2-OG9MAFcaUD1ikkfeJsEDZ"

SEARCH_URL = "https://jp.mercari.com/search?keyword=%E3%81%94%E3%81%A1%E3%81%86%E3%81%95%20ONKYO"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(SEARCH_URL, headers=headers)

if response.status_code == 200:

    message = {
        "content": f"ごちうさONKYO検索\n{SEARCH_URL}"
    }

    requests.post(WEBHOOK_URL, json=message)

else:

    requests.post(
        WEBHOOK_URL,
        json={"content": "メルカリ取得失敗"}
    )
