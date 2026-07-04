# === БЛОК 1: Импорты ===
import os
import logging



# === БЛОК 2: Константы ===



# === БЛОК 3: Координаты стран ===



# === БЛОК 4: Настройка логгирования ===
def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/sister_map.log", mode="a", encoding="utf-8")
        ]
    )


# === БЛОК 5: Загрузка данных ===
def load_data(path: str) -> list[dict]:
    pass


# === БЛОК 6: Создание карты ===
def create_map(data: list[dict]):
    pass


# === БЛОК 7: Точка входа ===
def main():
    # 1. Настройка логгирования
    # 2. Загрузка данных из data.json
    # 3. Создание карты Folium
    # 4. Сохранение карты в sister_map.html
    # 5. Лог результата
    pass


if __name__ == "__main__":
    main()