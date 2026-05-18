import requests
import re
import json

WEBHOOK_URL = "あなたのWebhook URL"

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

html = response.text

matches = re.findall(r'"id":"(m[0-9]+)"', html)

if matches:

    item_id = matches[0]

    item_url = f"https://jp.mercari.com/item/{item_id}"

    requests.post(
        WEBHOOK_URL,
        json={
            "content": f"【商品検出】\n{item_url}"
        }
    )

else:

    requests.post(
        WEBHOOK_URL,
        json={
            "content": "商品ID検出失敗"
        }
    )
