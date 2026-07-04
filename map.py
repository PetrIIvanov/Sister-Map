# === БЛОК 1: Импорты ===
import os
import json
import logging
import urllib.request

import folium
from folium import GeoJsonTooltip, GeoJsonPopup


# === БЛОК 2: Константы ===
COLOR_MAP = {
    "slavic": "red",
    "germanic": "blue",
    "romance": "green",
    "uralic": "purple",
    "baltic": "orange",
    "other": "gray",
}

DATA_PATH = "data.json"
OUTPUT_PATH = "sister_map.html"
GEOJSON_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
GEOJSON_PATH = "countries.geojson"
MAP_CENTER = [54, 15]
MAP_ZOOM = 4

ISO_A2_TO_A3 = {
    "RU": "RUS", "UA": "UKR", "BY": "BLR", "PL": "POL",
    "CZ": "CZE", "SK": "SVK", "BG": "BGR", "RS": "SRB",
    "HR": "HRV", "SI": "SVN", "GB": "GBR", "DE": "DEU",
    "AT": "AUT", "NL": "NLD", "SE": "SWE", "NO": "NOR",
    "DK": "DNK", "IS": "ISL", "FR": "FRA", "IT": "ITA",
    "ES": "ESP", "PT": "PRT", "RO": "ROU", "MD": "MDA",
    "FI": "FIN", "EE": "EST", "HU": "HUN", "LV": "LVA",
    "LT": "LTU", "GR": "GRC", "AL": "ALB", "IE": "IRL",
    "TR": "TUR",
}


# === БЛОК 3: Скачивание GeoJSON ===
def download_geojson():
    if os.path.exists(GEOJSON_PATH):
        logging.info("GeoJSON уже существует: %s", GEOJSON_PATH)
        return
    logging.info("Скачивание %s ...", GEOJSON_URL)
    urllib.request.urlretrieve(GEOJSON_URL, GEOJSON_PATH)
    logging.info("GeoJSON сохранён: %s", GEOJSON_PATH)


# === БЛОК 4: Настройка логгирования ===
def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/sister_map.log", mode="a", encoding="utf-8"),
        ],
    )


# === БЛОК 5: Загрузка данных ===
def load_data(path: str) -> list[dict]:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        logging.info("Загружено %d записей из %s", len(data), path)
        return data
    except FileNotFoundError:
        logging.error("Файл не найден: %s", path)
        raise
    except json.JSONDecodeError as e:
        logging.error("Ошибка парсинга JSON: %s", e)
        raise


# === БЛОК 6: Создание карты ===
def create_map(data: list[dict]):
    with open(GEOJSON_PATH, encoding="utf-8") as f:
        geojson = json.load(f)

    data_by_a3 = {ISO_A2_TO_A3[entry["code"]]: entry for entry in data}

    enriched = 0
    for feature in geojson["features"]:
        iso_a3 = feature["properties"].get("ISO_A3")
        entry = data_by_a3.get(iso_a3)
        if entry:
            feature["properties"]["word"] = entry["word"]
            feature["properties"]["country_name"] = entry["country_name"]
            feature["properties"]["transcription"] = entry["transcription"]
            feature["properties"]["group"] = entry["group"]
            feature["properties"]["info"] = entry["info"]
            enriched += 1
        else:
            feature["properties"]["word"] = ""
            feature["properties"]["country_name"] = ""
            feature["properties"]["transcription"] = ""
            feature["properties"]["group"] = ""
            feature["properties"]["info"] = ""

    logging.info("Обогащено %d стран из GeoJSON", enriched)

    def style_function(feature):
        group = feature["properties"].get("group", "other")
        color = COLOR_MAP.get(group, "gray")
        return {
            "fillColor": color,
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.6,
        }

    m = folium.Map(location=MAP_CENTER, zoom_start=MAP_ZOOM)

    folium.GeoJson(
        geojson,
        style_function=style_function,
        tooltip=GeoJsonTooltip(
            fields=["country_name", "word"],
            aliases=["Страна", "Слово"],
            localize=True,
        ),
        popup=GeoJsonPopup(
            fields=["country_name", "word", "transcription", "group", "info"],
            aliases=["Страна", "Слово", "Транскрипция", "Группа", ""],
            localize=True,
        ),
    ).add_to(m)

    m.save(OUTPUT_PATH)
    logging.info("Карта сохранена: %s", OUTPUT_PATH)


# === БЛОК 7: Точка входа ===
def main():
    setup_logging()
    logging.info("Запуск SisterMap")
    download_geojson()
    data = load_data(DATA_PATH)
    create_map(data)


if __name__ == "__main__":
    main()