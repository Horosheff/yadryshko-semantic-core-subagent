# Семантическое ядро субагент (ЯДрышко)

![ЯДрышко — субагент для семантического ядра](assets/yadryshko-cover.png)

[![Установить в Cursor](https://img.shields.io/badge/Установить%20в%20Cursor-ЯДрышко-000000?style=for-the-badge&logo=cursor)](#-установить-в-cursor)
[![MCP--KV Wordstat](https://img.shields.io/badge/MCP--KV-Wordstat-2563eb?style=for-the-badge)](https://mcp-kv.ru/docs/wordstat-mcp-setup)
[![GitHub](https://img.shields.io/badge/GitHub-repository-111111?style=for-the-badge&logo=github)](https://github.com/Horosheff/yadryshko-semantic-core-subagent)

`ЯДрышко` (`Core`) — готовый Cursor sub-agent, который собирает полноценное семантическое ядро сайта: Wordstat, очищенные запросы, кластеры, URL-карту, контент-брифы, GEO/AI-рекомендации, roadmap и большой русский HTML-отчёт.

Главная идея: пользователь даёт сайт, а агент создаёт пакет исследования, который можно отдать SEO-специалисту, редактору, владельцу бизнеса или разработчику.

```text
/core https://example.ru регион Россия, цель: заявки, приоритет Яндекс
```

## 🚀 Установить в Cursor

Откройте терминал **в корне своего проекта** и выполните одну команду.

### Windows / PowerShell

```powershell
irm https://raw.githubusercontent.com/Horosheff/yadryshko-semantic-core-subagent/main/install.ps1 | iex
```

### macOS / Linux / Git Bash

```bash
curl -fsSL https://raw.githubusercontent.com/Horosheff/yadryshko-semantic-core-subagent/main/install.sh | bash
```

После установки перезапустите Cursor или сделайте `Reload Window`, если `/core` не появился сразу.

## Что пользователь получит на выходе

После запуска Core создаёт отдельную папку исследования:

В папке проекта появляется:

```text
research/semantic-core-runs/<site>-<date>/
```

| Файл | Что внутри | Для кого |
|---|---|---|
| `index.html` | Большой русский отчёт “всё в одном”: выводы, таблицы, риски, рекомендации, план 7/30/90 дней | Владелец, SEO, редактор, клиент |
| `semantic-core.xlsx` | Единая Excel-книга со всеми листами исследования | SEO, аналитик, команда |
| `05-clusters.csv` | Кластеры: главный запрос, интент, частотность, URL, приоритет | SEO |
| `06-url-map.csv` | Что создать, что обновить, куда вести внутренние ссылки | SEO + разработчик |
| `07-content-briefs.md` | ТЗ для P0/P1 страниц: H1, title, description, блоки, FAQ/GEO | Редактор |
| `10-todo.md` | Короткий TODO: что сделано, что проверить, что делать дальше | Владелец, SEO, команда |
| `12-implementation-roadmap.md` | Пошаговый план внедрения по спринтам | Владелец проекта |
| `09-quality-report.md` | Ограничения, риски, что нужно проверить вручную | SEO + аналитик |

### Внутри `index.html` человек увидит

- что уже хорошо на сайте;
- что мешает росту;
- какие темы дают спрос;
- какие страницы нужно создать;
- какие страницы нужно обновить;
- где риск каннибализации;
- что проверить в Яндексе, GSC и Яндекс.Вебмастере;
- какие задачи делать в ближайшие 7, 30 и 90 дней.

> Важно: Core не выдумывает частотности. Для реальных Wordstat-данных нужно подключить MCP-KV Wordstat.

## Что внутри репозитория

```text
sub-agent-core/
├─ .cursor/
│  └─ agents/
│     └─ core.md
├─ docs/
│  ├─ core-agent-playbook.md
│  ├─ semantic-core-methodology.md
│  ├─ mcp-kv-wordstat-setup.md
│  └─ repository-map.md
├─ scripts/
│  ├─ build_core_html_report.py
│  ├─ build_semantic_core_xlsx.py
│  ├─ install.ps1
│  └─ install.sh
├─ templates/
│  └─ run-files.md
├─ examples/
│  └─ prompt.md
├─ README.md
├─ LICENSE
└─ .gitignore
```

## Установка в свой проект

### Самый простой вариант: одна команда по ссылке

Откройте терминал **в корне проекта**, куда нужно установить sub-agent, и выполните:

#### Windows / PowerShell

```powershell
irm https://raw.githubusercontent.com/Horosheff/yadryshko-semantic-core-subagent/main/install.ps1 | iex
```

#### macOS / Linux / Git Bash

```bash
curl -fsSL https://raw.githubusercontent.com/Horosheff/yadryshko-semantic-core-subagent/main/install.sh | bash
```

После установки в проекте появятся:

```text
.cursor/agents/core.md
docs/
scripts/
templates/
```

Если `/core` не появился сразу, перезапустите Cursor или выполните reload window.

### Установка по ссылке в конкретную папку

#### Windows / PowerShell

```powershell
$env:YADRYSHKO_TARGET="C:\path\to\your\project"; irm https://raw.githubusercontent.com/Horosheff/yadryshko-semantic-core-subagent/main/install.ps1 | iex
```

#### macOS / Linux / Git Bash

```bash
curl -fsSL https://raw.githubusercontent.com/Horosheff/yadryshko-semantic-core-subagent/main/install.sh | bash -s -- /path/to/your/project
```

### Вариант вручную

Скопируйте в корень своего проекта:

```text
.cursor/agents/core.md
docs/
scripts/
templates/
```

После этого в Cursor можно запускать:

```text
/core https://example.ru регион Россия, цель заявки
```

### Установка из уже скачанного репозитория: PowerShell

Из папки этого репозитория:

```powershell
.\scripts\install.ps1 -Target "C:\path\to\your\project"
```

### Установка из уже скачанного репозитория: Bash/macOS/Linux

```bash
./scripts/install.sh /path/to/your/project
```

## Обязательное условие: MCP-KV и Wordstat

Для настоящих частотностей нужен MCP-KV с подключённым Wordstat.

Полезные ссылки:

- Сервис MCP-KV: https://mcp-kv.ru/
- Инструкция Wordstat MCP: https://mcp-kv.ru/docs/wordstat-mcp-setup

Коротко:

1. Создайте API Key в Yandex AI Studio.
2. Включите биллинг в Yandex Cloud.
3. Скопируйте Folder ID.
4. Выдайте роль `search-api.webSearch.user`.
5. В MCP-KV dashboard откройте “Wordstat API настройки”.
6. Вставьте API Key и Folder ID.
7. Нажмите “Проверить и сохранить”.
8. Подключите MCP-KV к Cursor.

Если Wordstat MCP не подключён, Core всё равно может собрать структуру, но обязан отметить, что частотности не подтверждены.

## Как выглядит хороший запрос

```text
/core https://kv-ai.ru/
Регион: Россия, Wordstat ID 225.
Цель: заявки на обучение и внедрение автоматизации.
Приоритет: Яндекс, Google вторично.
Исключить: вакансии, бесплатные скачивания, нерелевантный make up/made.
```

## Почему это sub-agent, а не skill

`Core` делает длинную многошаговую работу: сайт, Wordstat, кластеризация, CSV, HTML, Excel, roadmap. Для такого процесса нужен отдельный контекст и возможность долго работать автономно. Поэтому формат Cursor sub-agent подходит лучше, чем skill.

## Публикация на GitHub

Локально:

```bash
git init
git add .
git commit -m "Initial Core sub-agent package"
```

Через GitHub CLI:

```bash
gh repo create sub-agent-core --public --source=. --remote=origin --push
```

Если нужен приватный репозиторий:

```bash
gh repo create sub-agent-core --private --source=. --remote=origin --push
```

## Лицензия

MIT. Можно использовать, дорабатывать и встраивать в свои проекты.
