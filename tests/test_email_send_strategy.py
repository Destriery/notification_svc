import threading
import asyncore

from send_strategies.email import EmailSendStrategyByPythonEmails

from tests.fakesmtp import FakeSMTPServer


class Settings(EmailSendStrategyByPythonEmails.Settings):
    SSL: bool = False
    PORT: int = 8025
    HOST: str = 'localhost'
    FROM: str = 'fdaew@tesfdsaty.ty'

    class Config:
        env_prefix = 'TEST_EMAIL_'


EmailSendStrategyByPythonEmails.Settings = Settings


class TestEmailSendStrategyByPythonEmails:
    email_to = 'fdaew@tesfdsaty.ty'
    message = 'Test'

    def setup_class(self):
        self.strategy = EmailSendStrategyByPythonEmails(self.email_to, self.message)

        self.smtp_server = FakeSMTPServer(tuple(self.strategy.connection_params.values()), None)

        # запуск демона для прослушивания smtp порта
        self.smtp_loop = threading.Thread(target=asyncore.loop, daemon=True)
        self.smtp_loop.start()

    def teardown_class(self):
        self.smtp_server.close()

    def test_init_object(self):
        assert isinstance(self.strategy, EmailSendStrategyByPythonEmails)

    def test_html(self):
        assert self.strategy.html == \
                self.strategy.template.replace('${message}', self.message)

    def test_send(self):
        response = self.strategy.send()

        assert response.status_code == 250
