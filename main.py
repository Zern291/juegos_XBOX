import json
import os
import requests
from bs4 import BeautifulSoup

# 🔐 Cargar token y chat desde variables de entorno (GitHub Secrets)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    print("❌ TELEGRAM_TOKEN o CHAT_ID no definidos en secrets.")
    exit(1)

def load_games(filename="games.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def get_prices_from_xbox_deals(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"⚠️ Error HTTP {response.status_code} al acceder a: {url}")
        return None, None, None

    soup = BeautifulSoup(response.text, "html.parser")

    # Precio actual
    meta_price = soup.find("meta", itemprop="price")
    try:
        current_price = int(meta_price.get("content").strip()) if meta_price else None
    except:
        current_price = None

    # Precio mínimo
    min_price_tag = soup.select_one("span.game-stats-col-number-big.game-stats-col-number-green")
    try:
        min_price = int(min_price_tag.text.replace("$", "").replace(",", "").strip()) if min_price_tag else None
    except:
        min_price = None

    # Precio máximo
    max_price_tag = soup.select_one("span.game-stats-col-number-big.game-stats-col-number-red")
    try:
        max_price = int(max_price_tag.text.replace("$", "").replace(",", "").strip()) if max_price_tag else None
    except:
        max_price =_
