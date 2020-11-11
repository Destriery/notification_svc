import sys
import os

from babel.messages.frontend import main as babel_script

from config.settings import LOCALEDIR, LOCALEDOMAIN, DEFAULT_LOCALE

class Babel:
    methods_with_required_locale = ('init', 'update', 'compile', 'reload')

    def __init__(self, argv: list) -> None:
        self._get_method(argv)

        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Определяем значения некоторых свойств, связанных с локалью по-умолчанию
        self.default_locale_path = f'{LOCALEDIR}/{DEFAULT_LOCALE}/LC_MESSAGES'
        self.default_locale_file = f'{self.default_locale_path}/{LOCALEDOMAIN}.po'

        # Определяем значения некоторых свойств, связанных с переданной локалью
        self._get_locale(argv)
        self.locale_path = f'{LOCALEDIR}/{self.locale}/LC_MESSAGES'
        self.locale_file = f'{self.locale_path}/{LOCALEDOMAIN}.po'

        # Вызываем требуемый метод
        getattr(self, self.method)()

    def _get_method(self, argv: list) -> None:
        """Определяем вызываемый метод, 
            либо возвращаем ошибку"""
        self.method = argv[0].replace('babel_', '')

        if not hasattr(self, self.method):
            print(f'error: method "{argv[0]}" does not exist')
            sys.exit()

    def _get_locale(self, argv: list) -> None:
        """Определяем переданную локаль, 
            либо возвращаем ошибку, 
            либо выбираем локаль по умолчанию, если аргумент не обязателен для метода"""
        try:
            self.locale = argv[1]
        except IndexError:
            if not self.method in self.methods_with_required_locale:
                self.locale = DEFAULT_LOCALE
            else:
                message = 'Usage: babel_[method] [locale_name]\n\nerror: locale_name is empty'

                print(message)
                sys.exit()

    def _mkdir_for_locale(self) -> None:
        """Создаем директорию под файлы локализации"""
        try:
            os.makedirs(self.locale_path)
        except FileExistsError:
            pass

    @staticmethod
    def _run_babel_script(is_exit: bool = True) -> None:
        """Запускаем скрипты babel, как утилита pybabel"""
        if is_exit:
            sys.exit(babel_script())
        else:
            babel_script()


    def _extract(self, is_exit: bool = True) -> None:
        """(непосредственная реализация) Генерация .po файла для выбранной локали на основе строк в коде приложения
            Console: `pybabel extract -o locales/ru/LC_MESSAGES/messages.po ./`

            Выделена в отдельный метод, чтобы упростить вызов другими методами класса
        """  

        self._mkdir_for_locale()

        sys.argv = ['', 'extract', f'--output={self.locale_file}', self.project_dir]

        self._run_babel_script(is_exit)


    def extract(self) -> None:
        """Генерация .po файла для выбранной локали на основе строк в коде приложения
            `python manage.py babel_extract ru`
            Console: `pybabel extract -o locales/ru/LC_MESSAGES/messages.po ./`
        """   
        
        self._extract()

    def init(self) -> None:
        """Генерация .po файла на основе локали по-умолчанию
            `python manage.py babel_init ru`
            Console: `pybabel init -d locales -l en -i locales/ru/LC_MESSAGES/messages.po`
        """

        sys.argv = ['', 'init', f'--domain={LOCALEDOMAIN}', f'--output-dir={LOCALEDIR}', f'--input-file={self.default_locale_file}', f'--locale={self.locale}']

        self._run_babel_script()

    def update(self) -> None:
        """Обновление .po файла на основе локали по-умолчанию
            `python manage.py babel_update ru`
            Console: `pybabel init -d locales -l en -i locales/ru/LC_MESSAGES/messages.po`
        """

        sys.argv = ['', 'update', f'--domain={LOCALEDOMAIN}', f'--output-dir={LOCALEDIR}', f'--input-file={self.default_locale_file}', f'--locale={self.locale}']

        self._run_babel_script()


    def reload(self) -> None:
        """Извлечение .po файл для локали по-умолчанию изменений в коде и обновление .po файла выбранной локали
            `python manage.py babel_reload ru`
        """
        # Останавливаем выполнение, если выбранная локаль является локалью по умолчанию 
        if self.locale == DEFAULT_LOCALE:
            print(f'error: locale "{self.locale}" is default locale')
            sys.exit()

        self._extract(is_exit=False)

        self.update()

    def compile(self) -> None:
        """Генерация .mo файла для выбранной локали
            `python manage.py babel_compile ru`
            Console: `pybabel compile -d locales -l en`
        """

        sys.argv = ['', 'compile', f'--domain={LOCALEDOMAIN}', f'--directory={LOCALEDIR}', f'--locale={self.locale}']

        self._run_babel_script()