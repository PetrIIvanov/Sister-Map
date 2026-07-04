# План: убрать чёрную рамку DivIcon при клике

## Проблема
При клике на страну появлялся чёрный прямоугольник (сам DivIcon), затем поверх — popup.

## Изменения

### 1. map.py
- Убрать `className` из `folium.DivIcon()` — будет использоваться стандартный `leaflet-div-icon`
- В inline-стиль `<div>` добавить `background:transparent;border:none` — отменить фон/рамку по умолчанию

### 2. CHANGELOG.md
- Добавить запись `[1.3.2]`

### 3. AGENTS.md
- Дописать changelog

## Шаги
1. map.py — правка DivIcon
2. CHANGELOG.md — запись
3. AGENTS.md — запись
4. python map.py
5. git add → commit → push