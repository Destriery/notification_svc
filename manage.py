import sys
import re
import os

from babel.messages.frontend import main as babel_script

from config.settings import LOCALEDIR, LOCALEDOMAIN, DEFAULT_LOCALE

class Babel:

    def __init__(self, argv) -> None:
        self.get_method(argv)
        self.get_locale(argv)

        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.default_locale_path = f'{LOCALEDIR}/{DEFAULT_LOCALE}/LC_MESSAGES'
        self.default_locale_file = f'{self.default_locale_path}/{LOCALEDOMAIN}.po'

        self.locale_path = f'{LOCALEDIR}/{self.locale}/LC_MESSAGES'
        self.locale_file = f'{self.locale_path}/{LOCALEDOMAIN}.po'

        getattr(self, self.method)()

    def get_method(self, argv: list) -> None:
        """Определяем вызываемый метод, либо возвращаем ошибку"""
        self.method = argv[0].replace('babel_', '')

        if not hasattr(self, self.method):
            print(f'error: method "{argv[0]}" does not exist')
            sys.exit()

    def get_locale(self, argv: list) -> None:
        """Определяем переданную локаль, либо возвращаем ошибку"""
        try:
            self.locale = argv[1]
        except IndexError:
            message = """Usage: babel_[method] [locale_name]\n\nerror: locale_name is empty"""

            print(message)
            sys.exit()

    def mkdir_for_locale(self) -> None:
        """Создаем директорию под файлы локализации"""
        try:
            os.makedirs(self.locale_path)
        except FileExistsError:
            pass

    @staticmethod
    def run_babel_script(is_exit: bool=True) -> None:
        """Запускаем скрипты babel, как утилита pybabel"""
        if is_exit:
            sys.exit(babel_script())
        else:
            babel_script()


    def extract(self, is_default_locale: bool=False) -> None:
        """Генерация .po файла для выбранной локали на основе строк в коде приложения
            `python manage.py babel_extract ru`
            Console: `pybabel extract -o locales/ru/LC_MESSAGES/messages.po ./`
        """
        is_exit = not is_default_locale
        file = self.default_locale_file if is_default_locale else self.locale_file       

        self.mkdir_for_locale()

        sys.argv = ['', 'extract', f'--output={file}', self.project_dir]

        self.run_babel_script(is_exit)

    def init(self) -> None:
        """Генерация .po файла на основе локали по-умолчанию
            `python manage.py babel_init ru`
            Console: `pybabel init -d locales -l en -i locales/ru/LC_MESSAGES/messages.po`
        """

        sys.argv = ['', 'init', f'--domain={LOCALEDOMAIN}', f'--output-dir={LOCALEDIR}', f'--input-file={self.default_locale_file}', f'--locale={self.locale}']

        self.run_babel_script()

    def update(self) -> None:
        """Обновление .po файла на основе локали по-умолчанию
            `python manage.py babel_update ru`
            Console: `pybabel init -d locales -l en -i locales/ru/LC_MESSAGES/messages.po`
        """

        # self.mkdir_for_locale()

        sys.argv = ['', 'update', f'--domain={LOCALEDOMAIN}', f'--output-dir={LOCALEDIR}', f'--input-file={self.default_locale_file}', f'--locale={self.locale}']

        self.run_babel_script()


    def reload(self) -> None:
        """Извлекаем в .po файл локали по умолчанию изменения в коде и обновлем .po файл выбранной локали
            `python manage.py babel_reload ru`
        """
        # Останавливаем выполнение, если выбранная локаль является локалью по умолчанию 
        if self.locale == DEFAULT_LOCALE:
            print(f'error: locale "{self.locale}" is default locale')
            sys.exit()

        self.extract(is_default_locale=True)

        self.update()

    def compile(self) -> None:
        """Генерация .mo файла для локали
            `python manage.py babel_compile ru`
            Console: `pybabel compile -d locales -l en`
        """

        sys.argv = ['', 'compile', f'--domain={LOCALEDOMAIN}', f'--directory={LOCALEDIR}', f'--locale={self.locale}']

        self.run_babel_script()
        

def main():
    argv = sys.argv

    if 'babel_' in argv[1]:
        Babel(argv[1:])

if __name__ == '__main__':
    main()