# Notification Service

## Babel

### Настройки переводов

`config/settings.py`

```python
DEFAULT_LOCALE = 'en'
LOCALEDIR = 'locales'
LOCALEDOMAIN = 'messages'

LOCALE = 'ru'
```

### Генерация .po файла для выбранной локали на основе строк в коде приложения

`python manage.py babel_extract [en]`

Без аргумента: локаль по-умолчанию

### Генерация .po файла на основе локали по-умолчанию

`python manage.py babel_init ru`

### Обновление .po файла на основе локали по-умолчанию

`python manage.py babel_update ru`

### Извлечение изменений в коде в .po файл для локали по-умолчанию и обновление .po файла выбранной локали

`python manage.py babel_reload ru`

### Генерация .mo файла для выбранной локали

`python manage.py babel_compile ru`
