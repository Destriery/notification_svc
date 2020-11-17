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

### Пример

1. `python manage.py babel_extract` # экспортируем стороки из файлов приложения
2. `python manage.py babel_update ru` # перезагружаем выбранный перевод, либо `python manage.py babel_init ru` - создаем новый
3. Удаляем метку `#, fuzzy` из файла *messages.py*
4. Переводим необходимые строки
5. `python manage.py babel_compile ru` - компилируем .mo файл
6. Перезагружаем uvicorn

Либо, если требуется перезагрузить уже готовый файл вместо первый двух пунктов делаем `python manage.py babel_reload ru`
