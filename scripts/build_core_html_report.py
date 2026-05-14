from __future__ import annotations

import argparse
import csv
import html
from collections import Counter, defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


TEXT_REPLACEMENTS = {
    "Quality Report": "Отчёт качества",
    "Coverage Summary": "Покрытие данных",
    "Data Limitations": "Ограничения данных",
    "Quality Checklist": "Чек-лист качества",
    "Main Risks": "Главные риски",
    "Completeness Assessment": "Оценка полноты",
    "Implementation Roadmap": "План внедрения",
    "DEVICE_ALL": "все устройства",
    "include": "включить",
    "exclude": "исключить",
    "hold": "отложить",
    "create": "создать",
    "refresh": "обновить",
    "ok": "готово",
    "not_checked": "не проверено",
    "medium": "средняя",
    "low": "низкая",
    "high": "высокая",
    "SERP not checked live; intent assigned manually": "SERP не проверялся live; интент назначен вручную",
    "off-topic or non-lead intent": "не по теме или не ведёт к заявке",
    "visible response row; long MCP output can be truncated": "строка из видимого ответа; длинный MCP-ответ может быть обрезан",
}


def ru_text(value: object) -> str:
    text = "" if value is None else str(value)
    for source, target in TEXT_REPLACEMENTS.items():
        text = text.replace(source, target)
    return text


def esc(value: object) -> str:
    return html.escape(ru_text(value))


def as_int(value: str) -> int:
    try:
        return int(float(value or "0"))
    except ValueError:
        return 0


def rows_to_table(
    rows: list[dict[str, str]],
    columns: list[str | tuple[str, str]],
    limit: int | None = None,
) -> str:
    shown = rows[:limit] if limit else rows
    keys = [col[0] if isinstance(col, tuple) else col for col in columns]
    labels = [col[1] if isinstance(col, tuple) else col for col in columns]
    head = "".join(f"<th>{esc(label)}</th>" for label in labels)
    body = []
    for row in shown:
        body.append("<tr>" + "".join(f"<td>{esc(row.get(key, ''))}</td>" for key in keys) + "</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def md_to_html(text: str) -> str:
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            out.append(f"<h2>{esc(stripped[2:])}</h2>")
        elif stripped.startswith("## "):
            out.append(f"<h3>{esc(stripped[3:])}</h3>")
        elif stripped.startswith("### "):
            out.append(f"<h4>{esc(stripped[4:])}</h4>")
        elif stripped.startswith("- "):
            out.append(f"<li>{esc(stripped[2:])}</li>")
        else:
            out.append(f"<p>{esc(stripped)}</p>")
    return "\n".join(out)


def build(run_dir: Path) -> str:
    raw = read_csv(run_dir / "03-wordstat-raw.csv")
    clean = read_csv(run_dir / "04-keywords-clean.csv")
    clusters = read_csv(run_dir / "05-clusters.csv")
    urls = read_csv(run_dir / "06-url-map.csv")
    quality = read_text(run_dir / "09-quality-report.md")

    included = [row for row in clean if row.get("include_status") == "include"]
    excluded = [row for row in clean if row.get("include_status") == "exclude"]
    p01 = [row for row in clusters if row.get("priority") in {"P0", "P1"}]
    p0 = [row for row in clusters if row.get("priority") == "P0"]

    priorities = Counter(row.get("priority", "") for row in clusters)
    statuses = Counter(row.get("url_status", "") for row in clusters)
    intents = Counter(row.get("intent", "") for row in clusters)

    by_seed: dict[str, int] = defaultdict(int)
    for row in raw:
        by_seed[row.get("seed_phrase", "")] += 1
    seed_rows = [
        {"seed": seed, "raw_rows": str(count)}
        for seed, count in sorted(by_seed.items(), key=lambda item: item[1], reverse=True)
    ]

    sorted_clusters = sorted(clusters, key=lambda row: as_int(row.get("frequency_total", "")), reverse=True)

    files = [
        "semantic-core.xlsx",
        "README.md",
        "00-brief.md",
        "01-site-inventory.md",
        "02-seed-map.md",
        "03-wordstat-raw.csv",
        "04-keywords-clean.csv",
        "05-clusters.csv",
        "06-url-map.csv",
        "07-content-briefs.md",
        "08-serp-geo-notes.md",
        "09-quality-report.md",
        "10-todo.md",
        "12-implementation-roadmap.md",
    ]
    file_links = "".join(
        f'<li><a href="{esc(name)}">{esc(name)}</a></li>'
        for name in files
        if (run_dir / name).exists()
    )

    recommendation_rows = []
    for row in p01:
        status = row.get("url_status")
        recommendation_rows.append(
            {
                "priority": row.get("priority", ""),
                "cluster": row.get("cluster_name", ""),
                "what_to_do": "Создать страницу"
                if status == "create"
                else "Усилить существующую страницу"
                if status == "refresh"
                else "Проверить и развить",
                "url": row.get("target_url", ""),
                "why": row.get("business_value", ""),
                "risk": row.get("notes", ""),
            }
        )

    md_files = [
        ("Бриф", "00-brief.md"),
        ("Инвентаризация сайта", "01-site-inventory.md"),
        ("Карта seed-запросов", "02-seed-map.md"),
        ("Контент-брифы", "07-content-briefs.md"),
        ("SERP / GEO заметки", "08-serp-geo-notes.md"),
        ("Отчёт качества", "09-quality-report.md"),
        ("TODO", "10-todo.md"),
        ("План внедрения", "12-implementation-roadmap.md"),
    ]
    md_sections = []
    for title, filename in md_files:
        text = read_text(run_dir / filename)
        if text.strip():
            md_sections.append(f"<article><h3>{esc(title)}</h3>{md_to_html(text)}</article>")

    priority_pills = " ".join(f'<span class="pill">{esc(k)}: {v}</span>' for k, v in sorted(priorities.items()))
    status_pills = " ".join(f'<span class="pill">{esc(k)}: {v}</span>' for k, v in sorted(statuses.items()))
    intent_pills = " ".join(f'<span class="pill">{esc(k)}: {v}</span>' for k, v in sorted(intents.items()))

    title = run_dir.name.replace("-", " ")

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Полный отчёт Core: {esc(title)}</title>
  <style>
    body {{ margin:0; font-family:Arial, Helvetica, sans-serif; color:#111; background:#fff; line-height:1.5; }}
    header {{ padding:44px 52px 30px; border-bottom:1px solid #ddd; background:linear-gradient(180deg,#fff,#f7f7f7); }}
    main {{ max-width:1180px; margin:0 auto; padding:34px 28px 70px; }}
    h1 {{ font-size:42px; line-height:1.08; margin:0 0 14px; letter-spacing:-.03em; }}
    h2 {{ font-size:28px; margin:42px 0 14px; padding-top:8px; border-top:2px solid #111; }}
    h3 {{ font-size:20px; margin:28px 0 10px; }}
    p {{ margin:0 0 12px; }}
    .lead {{ font-size:18px; max-width:900px; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:12px; margin:22px 0; }}
    .card {{ border:1px solid #ddd; border-radius:14px; padding:16px; background:#fafafa; }}
    .card b {{ display:block; font-size:13px; text-transform:uppercase; letter-spacing:.05em; color:#555; margin-bottom:8px; }}
    .card span {{ font-size:28px; font-weight:700; }}
    .two {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
    table {{ width:100%; border-collapse:collapse; margin:12px 0 24px; font-size:14px; }}
    th,td {{ border:1px solid #ddd; padding:8px 9px; vertical-align:top; text-align:left; }}
    th {{ background:#efefef; position:sticky; top:0; z-index:1; }}
    code {{ background:#f0f0f0; padding:1px 5px; border-radius:4px; }}
    .note {{ border-left:4px solid #111; padding:12px 14px; background:#fafafa; margin:16px 0; }}
    .pill {{ display:inline-block; border:1px solid #111; border-radius:999px; padding:2px 9px; margin:2px; font-size:12px; }}
    li {{ margin:0 0 7px; }}
    footer {{ padding:24px 52px; border-top:1px solid #ddd; color:#555; }}
    @media (max-width:800px) {{ header {{ padding:28px 22px; }} .two {{ grid-template-columns:1fr; }} h1 {{ font-size:32px; }} }}
  </style>
</head>
<body>
<header>
  <p>Semantic Core / SEO + GEO / Wordstat / Cursor sub-agent</p>
  <h1>Полный отчёт по семантическому ядру: {esc(title)}</h1>
  <p class="lead">Это общий файл “всё в одном”: выводы, методика, таблицы, карта страниц, контент-план, риски, ограничения и рекомендации.</p>
</header>
<main>
  <section>
    <h2>1. Краткий вывод</h2>
    <div class="grid">
      <div class="card"><b>Строк Wordstat</b><span>{len(raw)}</span></div>
      <div class="card"><b>Очищенных запросов</b><span>{len(clean)}</span></div>
      <div class="card"><b>Включено</b><span>{len(included)}</span></div>
      <div class="card"><b>Исключено</b><span>{len(excluded)}</span></div>
      <div class="card"><b>Кластеров</b><span>{len(clusters)}</span></div>
      <div class="card"><b>P0/P1</b><span>{len(p01)}</span></div>
    </div>
    <p>Пакет показывает, какие темы уже можно переводить в страницы, какие требуют проверки SERP, где есть риск каннибализации и что делать в ближайшие 7/30/90 дней.</p>
  </section>

  <section>
    <h2>2. Файлы пакета</h2>
    <ul>{file_links}</ul>
  </section>

  <section>
    <h2>3. Что уже хорошо и что мешает росту</h2>
    <div class="two">
      <div class="note">
        <h3>Что уже хорошо</h3>
        <ul>
          <li>Есть карта спроса, кластеры и URL-решения.</li>
          <li>Есть P0/P1 приоритеты для ближайшей работы.</li>
          <li>Есть отдельные брифы и roadmap внедрения.</li>
        </ul>
      </div>
      <div class="note">
        <h3>Что мешает</h3>
        <ul>
          <li>Без live SERP нельзя считать границы кластеров финальными.</li>
          <li>Без GSC/Яндекс.Вебмастера неизвестны фактические URL-показы.</li>
          <li>Шумные seed-направления требуют ручной фильтрации.</li>
        </ul>
      </div>
    </div>
  </section>

  <section>
    <h2>4. Покрытие Wordstat</h2>
    {rows_to_table(seed_rows, [("seed", "Seed-фраза"), ("raw_rows", "Строк Wordstat")])}
  </section>

  <section>
    <h2>5. Структура ядра</h2>
    <p>Приоритеты: {priority_pills}</p>
    <p>URL-статусы: {status_pills}</p>
    <p>Интенты: {intent_pills}</p>
    {rows_to_table(sorted_clusters, [("cluster_id","ID"),("cluster_name","Кластер"),("primary_query","Главный запрос"),("intent","Интент"),("frequency_total","Частотность"),("page_type","Тип страницы"),("priority","Приоритет"),("target_url","Целевой URL"),("url_status","Статус URL"),("notes","Примечания")])}
  </section>

  <section>
    <h2>6. URL roadmap</h2>
    {rows_to_table(urls, [("target_url","Целевой URL"),("url_status","Статус"),("page_type","Тип страницы"),("cluster_ids","Кластеры"),("primary_queries","Главные запросы"),("recommended_h1","Рекомендуемый H1"),("implementation_task","Задача"),("notes","Примечания")])}
  </section>

  <section>
    <h2>7. Очищенные запросы</h2>
    {rows_to_table(clean, [("query","Запрос"),("canonical_query","Каноническая формулировка"),("frequency_value","Частотность"),("intent_initial","Интент"),("intent_confidence","Уверенность"),("cluster_candidate","Кандидат в кластер"),("include_status","Статус"),("exclude_reason","Причина исключения"),("notes","Примечания")])}
  </section>

  <section>
    <h2>8. Wordstat-сырьё</h2>
    {rows_to_table(raw, [("date_collected","Дата"),("seed_phrase","Seed-фраза"),("query","Запрос"),("raw_frequency","Частотность"),("region","Регион"),("device","Устройство"),("source","Источник"),("notes","Примечания")])}
  </section>

  <section>
    <h2>9. Практические рекомендации по страницам</h2>
    {rows_to_table(recommendation_rows, [("priority","Приоритет"),("cluster","Кластер"),("what_to_do","Что сделать"),("url","URL"),("why","Почему важно"),("risk","Риск / примечание")])}
  </section>

  <section>
    <h2>10. Полные текстовые разделы</h2>
    {''.join(md_sections)}
  </section>

  <section>
    <h2>11. Итоговые рекомендации</h2>
    <h3>Что улучшить первым</h3>
    <ol>
      <li>Развести информационные и коммерческие интенты по разным страницам.</li>
      <li>Создать или обновить все P0-страницы.</li>
      <li>Проверить live SERP по P0/P1 запросам.</li>
      <li>Подключить GSC и Яндекс.Вебмастер.</li>
      <li>Добавить кейсы, доверие, FAQ/GEO-блоки и сильные CTA.</li>
    </ol>
    <h3>План 7/30/90 дней</h3>
    <ul>
      <li>7 дней: проверить SERP, конкурентов, URL-структуру и первые ТЗ.</li>
      <li>30 дней: опубликовать P0-страницы, перелинковать, добавить FAQ.</li>
      <li>90 дней: сравнить показы/клики/CTR, обновить title/description, пересобрать ядро по фактическим данным.</li>
    </ul>
  </section>
</main>
<footer>Сгенерировано Core. Частотности не выдумываются; ограничения должны быть явно указаны в отчёте качества.</footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    output = args.run_dir / "index.html"
    output.write_text(build(args.run_dir), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
