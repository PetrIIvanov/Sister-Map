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