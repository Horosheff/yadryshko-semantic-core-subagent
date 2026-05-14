# Карта репозитория

## `.cursor/agents/core.md`

Главный Cursor sub-agent. Его копируют в проект пользователя в:

```text
.cursor/agents/core.md
```

После этого агент доступен как:

```text
/core
```

## `docs/core-agent-playbook.md`

Рабочий регламент агента: вход, выходные файлы, CSV-схемы, HTML, Excel, чек-лист качества.

## `docs/semantic-core-methodology.md`

Короткая SEO/GEO-методология: интенты, кластеры, URL-статусы, приоритеты, что нельзя делать.

## `docs/mcp-kv-wordstat-setup.md`

Инструкция, как подключить MCP-KV и Wordstat.

## `scripts/build_core_html_report.py`

Создаёт главный HTML-отчёт `index.html` из CSV и Markdown файлов прогона.

Запуск:

```text
python scripts/build_core_html_report.py research/semantic-core-runs/<run>
```

## `scripts/build_semantic_core_xlsx.py`

Создаёт `semantic-core.xlsx` без внешних библиотек. Используется как fallback, если `openpyxl` не установлен.

Запуск:

```text
python scripts/build_semantic_core_xlsx.py research/semantic-core-runs/<run>
```

## `scripts/install.ps1`

Установщик для Windows/PowerShell.

## `scripts/install.sh`

Установщик для macOS/Linux/Git Bash.

## `templates/run-files.md`

Памятка по структуре файлов, которые должен создавать Core.

## `examples/prompt.md`

Примеры запросов для запуска Core.
