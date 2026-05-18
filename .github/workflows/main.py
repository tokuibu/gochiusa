import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1505806483198050324/7caQ_Y_5pA-s81DF0NFGnSanoEIeQxkAIigAQctPpgTax2-OG9MAFcaUD1ikkfeJsEDZ"

message = {
    "content": "GitHub Actionsから通知テスト成功！"
}

requests.post(WEBHOOK_URL, json=message)
