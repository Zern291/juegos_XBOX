import requests
from bs4 import BeautifulSoup

def obtener_precios_xbox_deals(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "es-CO,es;q=0.9,en;q=0.8"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error al acceder a la página: {response.status_code}")
        return None, None, None

    soup = BeautifulSoup(response.text, "html.parser")

    def extraer_precio(selector):
        elemento = soup.select_one(selector)
        if elemento:
            try:
                return int(elemento.text.strip().replace("$", "").replace(",", "").replace(".", ""))
            except:
                return None
        return None

    def extraer_precio_meta():
        meta_tag = soup.find("meta", {"itemprop": "price"})
        if meta_tag and meta_tag.get("content"):
            try:
                return int(meta_tag["content"].strip())
            except:
                return None
        return None

    # ✅ Extraemos los 3 valores
    precio_actual = extraer_precio_meta()
    precio_minimo = extraer_precio("span.game-stats-col-number-big.game-stats-col-number-green")
    precio_maximo = extraer_precio("span.game-stats-col-number-big.game-stats-col-number-red")

    print("🔎 Resultados extraídos:")
    print(f"💰 Precio actual: {precio_actual if precio_actual else 'No encontrado'}")
    print(f"📉 Precio mínimo histórico: {precio_minimo if precio_minimo else 'No encontrado'}")
    print(f"📈 Precio máximo histórico: {precio_maximo if precio_maximo else 'No encontrado'}")

    return precio_actual, precio_minimo, precio_maximo

# 🔍 Prueba con un juego
url = "https://xbdeals.net/co-store/game/717107/red-dead-redemption-2-edici%C3%B3n-definitiva"
obtener_precios_xbox_deals(url)
