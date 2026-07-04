# SisterMap — контекст проекта

## Описание
Визуализация слова «сестра» в языках Европы на интерактивной карте (Folium).

33 страны, 6 языковых групп: slavic, germanic, romance, uralic, baltic, other.

## Структура
```
SisterMap/
├── AGENTS.md         # этот файл
├── CHANGELOG.md      # лог изменений
├── README.md         # описание для людей
├── requirements.txt  # зависимости
├── .gitignore
├── docs/
│   ├── data-format.md
│   ├── architecture.md
│   └── color-scheme.md
├── data.json         # исходные данные (33 записи)
├── logs/             # файлы логов
├── map.py            # скрипт генерации карты
└── sister_map.html   # результат (генерируется)
```

## Команды
- `pip install -r requirements.txt` — установка зависимостей
- `python map.py` — генерация карты → sister_map.html

## Соглашения
- snake_case для файлов и переменных
- Комментарии в коде не добавлять
- Все тексты на русском (кроме кода)
- Перед коммитом проверять git status

## Changelog
- 2026-07-04 — создана база знаний (AGENTS.md, README.md, docs/*, requirements.txt, .gitignore), инициализирован репозиторий, push на GitHub
- 2026-07-04 — добавлен CHANGELOG.md, обновлены AGENTS.md/README.md/docs/architecture.md, созданы logs/ и скелет map.py
- 2026-07-04 — logs/ добавлена в .gitignore, .gitkeep удалён (папка создаётся скриптом runtime при отсутствии)
- 2026-07-04 — реализован map.py (7 блоков), сгенерирована sister_map.html, push
- 2026-07-04 — CircleMarker заменён на GeoJson-полигоны (Natural Earth), тултип при наведении, поп-ап по клику, скачивание geojson, countries.geojson добавлен в .gitignore
- 2026-07-04 — Natural Earth 110m → 50m, матчинг по ADM0_A3, все 33 страны на карте
- 2026-07-04 — inline style_function (other→жёлтый, пусто→серый), DivIcon-надписи слов на карте
- 2026-07-04 — исправлен фон DivIcon (display:inline-block), обновлён CHANGELOG
- 2026-07-04 — убран className DivIcon (чёрная рамка при клике)
- 2026-07-04 — добавлен highlight_function=style_function (убрана подсветка полигона при клике)
- 2026-07-04 — кастомный CSS: убрано оформление попапа (скругления, тень, рамка)