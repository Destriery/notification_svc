import threading
import asyncore

from main import EmailSendStrategy

from tests.fakesmtp import FakeSMTPServer


class TEmailSendStrategy(EmailSendStrategy):
    class Settings(EmailSendStrategy.Settings):
        SSL: str = False
        PORT: int = 8025
        HOST: str = 'localhost'
        FROM: str = 'fdaew@tesfdsaty.ty'

        class Config:
            env_prefix = 'TEST_EMAIL_'


class TestEmailSendStrategy:
    email_to = 'fdaew@tesfdsaty.ty'
    message = 'Test'

    def setup_class(self):
        self.strategy = TEmailSendStrategy(self.email_to, self.message)
        self.connection_params = {'host': self.strategy.stg.HOST, 'port': self.strategy.stg.PORT}
        self.strategy.connection_params = self.connection_params

        self.smtp_server = FakeSMTPServer(tuple([*self.connection_params.values()]), None)
        # запуск демона для прослушивания smtp порта
        self.smtp_loop = threading.Thread(target=asyncore.loop, daemon=True)
        self.smtp_loop.start()

    def teardown_class(self):
        self.smtp_server.close()

    def test_init_object(self):
        assert isinstance(self.strategy, EmailSendStrategy)

    def test_html(self):
        assert self.strategy.html == \
                self.strategy.template.replace('${message}', self.message)

    def test_send(self):
        response = self.strategy.send()

        assert response.status_code == 250
