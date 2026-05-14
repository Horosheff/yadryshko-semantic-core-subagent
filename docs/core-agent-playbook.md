# Core agent playbook

Core — Cursor sub-agent для полного исследования семантического ядра сайта.

Главный результат: не чат-ответ, а папка исследования с HTML, Excel, CSV и Markdown.

## 1. Входной контракт

Минимально:

- сайт, домен, ниша или список услуг.

Желательно:

- регион Wordstat;
- язык;
- цель бизнеса;
- приоритет: Яндекс / Google / оба;
- конкуренты;
- исключения;
- выгрузки GSC/Яндекс.Вебмастера, если есть.

Если чего-то нет, Core фиксирует допущение.

## 2. Папка прогона

```text
research/semantic-core-runs/<domain-or-topic>-<YYYY-MM-DD>/
```

Обязательные файлы:

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
12-implementation-roadmap.md
```

## 3. Wordstat MCP

Core ожидает MCP server `user-mcp-kv` и инструменты:

- `wordstat_get_user_info`
- `wordstat_get_top_requests`

Схема `wordstat_get_top_requests`:

```json
{
  "phrase": "string",
  "numPhrases": 100,
  "regions": ["225"],
  "devices": ["DEVICE_ALL"]
}
```

Правила:

- минимум 10 осмысленных вызовов для нормального проекта;
- регион указывать явно;
- не выдумывать частоты;
- ошибки MCP фиксировать в `09-quality-report.md`;
- сырьё писать в `03-wordstat-raw.csv`.

## 4. CSV-схемы

### `03-wordstat-raw.csv`

```csv
date_collected,seed_phrase,query,raw_frequency,region,device,source,source_call,notes
```

### `04-keywords-clean.csv`

```csv
query,canonical_query,source_sources,frequency_region,frequency_value,intent_initial,intent_confidence,cluster_candidate,include_status,exclude_reason,notes
```

### `05-clusters.csv`

```csv
cluster_id,cluster_name,primary_query,secondary_queries,intent,frequency_total,region_note,page_type,priority,business_value,target_url,url_status,serp_engine,serp_check_status,top_competitors,geo_questions,content_status,last_review,notes
```

### `06-url-map.csv`

```csv
target_url,url_status,page_type,cluster_ids,primary_queries,recommended_h1,title_draft,description_draft,internal_links_from,internal_links_to,implementation_task,owner_hint,notes
```

## 5. HTML-отчёт

`index.html` — главный файл для человека. Он должен быть на русском и включать:

- краткий вывод;
- что уже хорошо;
- что мешает росту;
- методику;
- ограничения;
- покрытие Wordstat;
- полную структуру ядра;
- полные таблицы raw/clean/cluster/url, если размер позволяет;
- контент и GEO/AI-слой;
- риски;
- полный roadmap;
- итоговые рекомендации;
- план 7/30/90 дней.

Генератор:

```text
python scripts/build_core_html_report.py <run-folder>
```

## 6. Excel

`semantic-core.xlsx` нужен для Excel/Google Sheets.

Генератор без внешних зависимостей:

```text
python scripts/build_semantic_core_xlsx.py <run-folder>
```

## 7. Чек-лист перед завершением

- [ ] Бизнес-границы зафиксированы.
- [ ] Регион указан или допущение записано.
- [ ] Wordstat MCP использован или ограничение записано.
- [ ] CSV-файлы существуют.
- [ ] P0/P1 имеют главный запрос.
- [ ] P0/P1 имеют URL-решение.
- [ ] Риски каннибализации указаны.
- [ ] HTML-отчёт большой и на русском.
- [ ] HTML заканчивается рекомендациями.
- [ ] `semantic-core.xlsx` существует.
- [ ] Roadmap существует.

## 8. Запрещено

- выдумывать частотности;
- прятать ошибки MCP;
- называть непроверенную SERP-кластеризацию точной;
- отдавать только CSV;
- заявлять, что файл создан, без проверки на диске.
