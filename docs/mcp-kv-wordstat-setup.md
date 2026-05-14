# Подключение MCP-KV и Wordstat для Core

Core использует Wordstat через MCP-KV. Без этого агент может собрать структуру и рекомендации, но не должен выдумывать частотности.

Ссылки:

- MCP-KV: https://mcp-kv.ru/
- Гайд Wordstat MCP: https://mcp-kv.ru/docs/wordstat-mcp-setup

## Что нужно

- аккаунт Яндекса;
- активный биллинг Yandex Cloud;
- API Key;
- Folder ID каталога;
- роль `search-api.webSearch.user`;
- подключённый MCP-KV в Cursor.

## Быстрый маршрут

1. Откройте Yandex AI Studio: https://aistudio.yandex.ru/
2. Войдите в аккаунт Яндекса.
3. Привяжите карту в биллинге Yandex Cloud.
4. Создайте API Key.
5. Сохраните ключ сразу: Яндекс показывает его один раз.
6. Откройте Yandex Cloud Console.
7. Скопируйте Folder ID из URL каталога после `/folders/`.
8. В IAM выдайте роль `search-api.webSearch.user`.
9. Откройте MCP-KV dashboard.
10. Перейдите в “Wordstat API настройки”.
11. Вставьте API Key и Folder ID.
12. Нажмите “Проверить и сохранить новое подключение Wordstat”.
13. Подключите MCP-KV к Cursor и убедитесь, что доступны Wordstat tools.

## Какие MCP tools ожидает Core

Минимально:

- `wordstat_get_user_info`
- `wordstat_get_top_requests`

Если в вашем MCP-KV доступны дополнительные инструменты, Core может использовать их при доработке:

- `wordstat_get_dynamics`
- `wordstat_get_regions`

## Частые ошибки

### 401

API Key неполный, скопирован с пробелом или уже удалён. Создайте новый ключ.

### 403

Обычно причина одна из этих:

- не подключён биллинг;
- не привязана карта;
- не выдана роль `search-api.webSearch.user`;
- ключ создан не с той областью доступа.

### Folder ID

Нужен ID каталога, а не ID облака и не ID сервисного аккаунта. Обычно начинается с `b1`.

### 429

Превышены квоты Yandex Search API. Проверьте лимиты в Yandex Cloud.

## Как проверить в Cursor

Запустите Core на маленьком тесте:

```text
/core тест: собрать 3-5 seed по теме "доставка цветов", регион Москва 213, проверить Wordstat.
```

В `09-quality-report.md` должно быть написано, что Wordstat MCP использован успешно. Если там написано, что MCP недоступен, проверьте подключение MCP-KV.
