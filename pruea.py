from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def obtener_precios_xbox_deals(url):
    # Configuración sin ventana (headless)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)

    time.sleep(3)  # Esperar a que cargue JS

    try:
        # Precio actual
        precio_actual_el = driver.find_element(By.CLASS_NAME, "price")
        precio_actual = precio_actual_el.text.strip()

        # Precio mínimo histórico (dentro de la tabla)
        tabla = driver.find_elements(By.CLASS_NAME, "price-history__lowest")
        precio_minimo = tabla[0].text.strip() if tabla else "No disponible"

        print(f"🔍 Precio actual: {precio_actual}")
        print(f"📉 Precio mínimo histórico: {precio_minimo}")
        return precio_actual, precio_minimo

    except Exception as e:
        print("⚠️ Error al obtener los precios:", e)
        return None, None
    finally:
        driver.quit()

# ▶️ Prueba con este juego (puedes reemplazar)
url = "https://xbdeals.net/co-store/game/887836/elden-ring"
obtener_precios_xbox_deals(url)
