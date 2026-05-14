# Шаблон результата Core

Каждый прогон Core должен создавать папку:

```text
research/semantic-core-runs/<domain-or-topic>-<YYYY-MM-DD>/
```

## Обязательные файлы

```text
index.html
semantic-core.xlsx
README.md
00-brief.md
01-site-inventory.md
02-seed-map.md
03-wordstat-raw.csv
04-keywords-clean.csv
05-clusters.csv
06-url-map.csv
07-content-briefs.md
08-serp-geo-notes.md
09-quality-report.md
10-todo.md
12-implementation-roadmap.md
```

## Главные файлы для человека

1. `index.html` — открыть первым. Здесь всё в одном месте.
2. `semantic-core.xlsx` — таблицы для Excel/Google Sheets.
3. `10-todo.md` — короткий список задач: сделано, проверить, сделать дальше.
4. `12-implementation-roadmap.md` — подробный план внедрения.

## Главные файлы для SEO/редактора

1. `05-clusters.csv`
2. `06-url-map.csv`
3. `07-content-briefs.md`
4. `09-quality-report.md`
5. `10-todo.md`

## Что должно быть в конце HTML

- что уже хорошо;
- что мешает росту;
- что улучшить первым;
- какие страницы создать;
- какие страницы обновить;
- что проверить в SERP;
- что проверить в GSC/Яндекс.Вебмастере;
- план 7/30/90 дней.
