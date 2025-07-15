import json
import requests
from bs4 import BeautifulSoup

# 🔒 Configura tu bot de Telegram
##LOLO
TELEGRAM_TOKEN = "8174192090:AAEqGlNr2MVAIih0kvFYu43eK7PHeONyF5o"
CHAT_ID = "7811372848"

def load_games(filename="games.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def get_prices_from_xbox_deals(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "es-CO,es;q=0.9,en;q=0.8"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Precio actual
    meta_price = soup.find("meta", itemprop="price")
    if not meta_price:
        print("❌ No se encontró el precio actual.")
        return None, None, None
    try:
        current_price = int(meta_price.get("content").strip())
    except:
        current_price = None

    # Precio mínimo (verde)
    min_price_tag = soup.select_one("span.game-stats-col-number-big.game-stats-col-number-green")
    try:
        min_price = int(min_price_tag.text.replace("$", "").replace(",", "").strip())
    except:
        min_price = None

    # Precio máximo (rojo)
    max_price_tag = soup.select_one("span.game-stats-col-number-big.game-stats-col-number-red")
    try:
        max_price = int(max_price_tag.text.replace("$", "").replace(",", "").strip())
    except:
        max_price = None

    return current_price, min_price, max_price

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def main():
    juegos = load_games()

    for juego in juegos:
        print(f"🔍 Revisando {juego['name']}...")
        current, minimo, maximo = get_prices_from_xbox_deals(juego["url"])

        if current is None:
            print("❌ No se pudo obtener el precio actual.\n")
            continue

        print(f"💰 Precio actual: {current} COP")
        print(f"📉 Precio mínimo histórico: {minimo} COP")
        print(f"📈 Precio máximo histórico: {maximo} COP")

        alertas = []

        if minimo and current <= minimo:
            alertas.append("🟢 ¡Precio actual igual o menor al mínimo histórico!")

        if current <= juego["max_price"]:
            alertas.append("🎯 ¡Precio actual igual o menor al precio objetivo!")

        if alertas:
            msg = (
                f"<b>{juego['name']}</b>\n"
                f"💰 <b>Actual:</b> ${current:,} COP\n"
                f"📉 <b>Mínimo histórico:</b> ${minimo:,} COP\n"
                f"📈 <b>Máximo histórico:</b> ${maximo:,} COP\n"
                alertas_texto = "\n".join(alertas)
                ...
                f"{alertas_texto}\n"
                f"🔗 <a href=\"{juego['url']}\">Ver en Xbox Deals</a>"
            )
            send_telegram_message(msg)
            print("📨 ¡Alerta enviada por Telegram!\n")
        else:
            print("⏳ Sin alertas para este juego.\n")

if __name__ == "__main__":
    main()
