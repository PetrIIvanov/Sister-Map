# === БЛОК 1: Импорты ===
import os
import json
import logging

import folium


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
MAP_CENTER = [54, 15]
MAP_ZOOM = 4


# === БЛОК 3: Координаты стран ===
COUNTRY_COORDS = {
    "RU": [61, 40],
    "UA": [49, 31],
    "BY": [53.5, 28],
    "PL": [52, 20],
    "CZ": [49.5, 15.5],
    "SK": [48.7, 19.5],
    "BG": [42.7, 25.5],
    "RS": [44, 21],
    "HR": [45.1, 15.5],
    "SI": [46, 15],
    "GB": [55, -3],
    "DE": [51, 10],
    "AT": [47.5, 14.5],
    "NL": [52, 5],
    "SE": [62, 15],
    "NO": [62, 10],
    "DK": [56, 10],
    "IS": [65, -19],
    "FR": [46.5, 2.5],
    "IT": [42, 12],
    "ES": [40, -3.5],
    "PT": [39.5, -8],
    "RO": [46, 25],
    "MD": [47, 28.5],
    "FI": [64, 26],
    "EE": [59, 26],
    "HU": [47, 19.5],
    "LV": [57, 25],
    "LT": [55, 24],
    "GR": [39, 22],
    "AL": [41, 20],
    "IE": [53, -8],
    "TR": [39, 35],
}


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
    m = folium.Map(location=MAP_CENTER, zoom_start=MAP_ZOOM)

    for entry in data:
        code = entry["code"]
        coords = COUNTRY_COORDS.get(code)
        if coords is None:
            logging.warning("Координаты не найдены для %s (%s)", code, entry["country_name"])
            continue

        group = entry.get("group", "other")
        color = COLOR_MAP.get(group, "gray")

        popup_text = (
            f"<b>{entry['country_name']}</b><br>"
            f"<i>{entry['word']}</i><br>"
            f"{entry['transcription']}<br>"
            f"группа: {group}<br>"
            f"{entry['info']}"
        )

        folium.CircleMarker(
            location=coords,
            radius=12,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=300),
        ).add_to(m)

    m.save(OUTPUT_PATH)
    logging.info("Карта сохранена: %s", OUTPUT_PATH)


# === БЛОК 7: Точка входа ===
def main():
    setup_logging()
    logging.info("Запуск SisterMap")
    data = load_data(DATA_PATH)
    create_map(data)


if __name__ == "__main__":
    main()