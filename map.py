# === БЛОК 1: Импорты ===
import os
import json
import logging
import urllib.request

import folium
from folium import GeoJsonTooltip, GeoJsonPopup
from branca.element import Element


# === БЛОК 2: Константы ===
DATA_PATH = "data.json"
OUTPUT_PATH = "sister_map.html"
GEOJSON_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson"
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
    "TR": "TUR", "BE": "BEL",
}

COUNTRY_COORDS = {
    "RU": [61, 40], "UA": [49, 31], "BY": [53.5, 28],
    "PL": [52, 20], "CZ": [49.5, 15.5], "SK": [48.7, 19.5],
    "BG": [42.7, 25.5], "RS": [44, 21], "HR": [45.1, 15.5],
    "SI": [46, 15], "GB": [55, -3], "DE": [51, 10],
    "AT": [47.5, 14.5], "NL": [52, 5], "SE": [62, 15],
    "NO": [62, 10], "DK": [56, 10], "IS": [65, -19],
    "FR": [46.5, 2.5], "IT": [42, 12], "ES": [40, -3.5],
    "PT": [39.5, -8], "RO": [46, 25], "MD": [47, 28.5],
    "FI": [64, 26], "EE": [59, 26], "HU": [47, 19.5],
    "LV": [57, 25], "LT": [55, 24], "GR": [39, 22],
    "AL": [41, 20], "IE": [53, -8], "TR": [39, 35],
    "BE": [50.5, 4.5],
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
        props = feature["properties"]
        iso_a3 = props.get("ISO_A3")
        if iso_a3 in (None, "", "-99", "-099"):
            iso_a3 = props.get("ADM0_A3")
        entry = data_by_a3.get(iso_a3)
        if entry:
            props["word"] = entry["word"]
            props["country_name"] = entry["country_name"]
            props["transcription"] = entry["transcription"]
            props["group"] = entry["group"]
            props["info"] = entry["info"]
            enriched += 1
        else:
            props["word"] = ""
            props["country_name"] = ""
            props["transcription"] = ""
            props["group"] = ""
            props["info"] = ""

    logging.info("Обогащено %d стран из GeoJSON", enriched)

    def style_function(feature):
        group = feature["properties"].get("group", "")
        if group == "slavic":
            return {"fillColor": "red", "color": "black", "weight": 0.5, "fillOpacity": 0.6}
        if group == "germanic":
            return {"fillColor": "blue", "color": "black", "weight": 0.5, "fillOpacity": 0.6}
        if group == "romance":
            return {"fillColor": "green", "color": "black", "weight": 0.5, "fillOpacity": 0.6}
        if group == "uralic":
            return {"fillColor": "purple", "color": "black", "weight": 0.5, "fillOpacity": 0.6}
        if group == "baltic":
            return {"fillColor": "orange", "color": "black", "weight": 0.5, "fillOpacity": 0.6}
        if group == "other":
            return {"fillColor": "yellow", "color": "black", "weight": 0.5, "fillOpacity": 0.6}
        return {"fillColor": "gray", "color": "black", "weight": 0.5, "fillOpacity": 0.6}
    
    def highlight_function(feature):
        return {"fillOpacity": 0.8, "color": "transparent", "weight": 0}

    m = folium.Map(location=MAP_CENTER, zoom_start=MAP_ZOOM)
    m.get_root().header.add_child(Element("""
    <style>
        .leaflet-popup-content-wrapper {
            border-radius: 0 !important;
            box-shadow: none !important;
            border: none !important;
        }
        .leaflet-popup-tip {
            display: none !important;
        }
        .leaflet-interactive:focus {
            outline: none !important;
        }
        .leaflet-path {
            outline: none !important;
        }
    </style>
"""))

    folium.GeoJson(
        geojson,
        style_function=style_function,
        highlight_function=style_function,
        tooltip=GeoJsonTooltip(
            fields=["country_name", "word", "transcription", "group", "info"],
            aliases=["Страна", "Слово", "Транскрипция", "Группа", ""],
            localize=True,
        ),
        popup=GeoJsonPopup(
            fields=["country_name", "word", "transcription", "group", "info"],
            aliases=["Страна", "Слово", "Транскрипция", "Группа", ""],
            localize=True,
        ),
    ).add_to(m)

    for entry in data:
        code = entry["code"]
        coords = COUNTRY_COORDS.get(code)
        if coords is None:
            continue
        folium.Marker(
            location=coords,
            icon=folium.DivIcon(
                class_name="",
                html=f"<div style=\"font-size:11px;font-weight:bold;background:rgba(255,255,255,0.7);padding:1px 3px;border-radius:2px;display:inline-block;white-space:nowrap;\">{entry['word']}</div>"
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