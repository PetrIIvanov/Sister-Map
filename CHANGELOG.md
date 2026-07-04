# Changelog

## [0.1.0] - 2026-07-04
### Added
- AGENTS.md — контекст проекта для opencode
- README.md — описание проекта для людей
- requirements.txt — зависимости (folium)
- .gitignore — Python + IDE + OS
- docs/data-format.md — описание полей JSON
- docs/architecture.md — архитектура решения
- docs/color-scheme.md — цветовая схема языковых групп
- CHANGELOG.md — этот файл
- Инициализация git-репозитория, первый коммит и push на GitHub

## [0.2.0] - 2026-07-04
### Added
- logs/ — папка для файлов логов
- map.py — скелет скрипта (блоки-комментарии, main-заглушка)
- Раздел «Логгирование» в README.md
- Описание функций map.py и logs/ в docs/architecture.md
### Changed
- logs/ добавлена в .gitignore, .gitkeep удалён (папка создаётся скриптом runtime при отсутствии)

## [1.0.0] - 2026-07-04
### Added
- Реализованы все блоки map.py: константы, координаты 33 стран, load_data, create_map
- Сгенерирована sister_map.html (Folium, CircleMarker, popup)
- setup_logging: stdout + FileHandler, уровень INFO, папка logs/ создаётся автоматически

## [1.1.0] - 2026-07-04
### Added
- GeoJson-полигоны стран вместо CircleMarker (Natural Earth 110m)
- download_geojson() — скачивание geojson при отсутствии
- Обогащение GeoJSON свойствами из data.json
- GeoJsonTooltip при наведении (страна → слово)
- GeoJsonPopup по клику (полная информация)
### Changed
- docs/architecture.md: описание GeoJson-логики
- docs/color-scheme.md: уточнение про полигоны
### Removed
- COUNTRY_COORDS — больше не нужны (координаты в GeoJSON)
- CircleMarker — заменён на GeoJson

## [1.2.0] - 2026-07-04
### Changed
- Natural Earth 110m → 50m (все 33 страны теперь обогащаются)
- Матчинг стран: fallback на ADM0_A3, если ISO_A3 = "-99"
- sister_map.html ~3.5 MB (50m геометрия)

## [1.3.0] - 2026-07-04
### Changed
- `style_function` переписана inline (без внешних ссылок) — работает корректно в JS
- other → жёлтый, пусто/нет данных → серый
- Возвращён COUNTRY_COORDS для DivIcon-надписей
### Added
- DivIcon-надписи: слово отображается прямо на карте в центре каждой страны
- docs/color-scheme.md: обновлена таблица (other → жёлтый, fallback → серый)