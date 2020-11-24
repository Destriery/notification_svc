from functools import cached_property

from config.settings import BASE_PATH

from app.send_strategies import SendStrategy, Response


class FileSendStrategy(SendStrategy):
    """Стратегия записи сообщений в файл
        Тестовая стратегия"""

    class Settings(SendStrategy.Settings):
        PATH: str = f'{BASE_PATH}/.temp'
        # TO: Optional[str] = None  # from SendStrategy

        class Config:
            env_prefix = 'FILE_'

    @cached_property
    def file_path(self):
        return f'{self.stg.PATH}/{self.to}'

    @cached_property
    def file(self):
        return open(self.file_path, 'w')

    def send(self) -> Response:
        try:
            self.file.write(self.message)
        finally:
            self.file.close()

        return Response({'status': 'writed'})
