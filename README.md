# Notification Service

## Babel

**Текущая локаль**
`config/settings.py`

```python
LOCALE = 'ru'
```

**Настройки для переводов**
`config/locale.py`

По умолчанию:

```python
DEFAULT_LOCALE = 'en'
LOCALEDIR = 'locales'
LOCALEDOMAIN = 'messages'
```

**Создание нового каталога на основе старого**
`pybabel init -d locales -l en -i locales/ru/LC_MESSAGES/messages.po`
locales - директория с файлами
en - новая локаль
locales/ru/LC_MESSAGES/messages.po - путь к существующему файлу

**Генерация .po файла.**
`pybabel extract -o locales/ru/LC_MESSAGES/messages.po ./`
locales/ru/LC_MESSAGES/messages.po - создаваемый файл
./ - директория, откуда генерируем строки

**Генерация .mo файла. для выбранной локали**
`pybabel compile -d locales -l en`
locales - директория с файлами
en - выбранная локаль
