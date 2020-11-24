import json
import threading
import asyncore

from app.send_strategies.file import FileSendStrategy
from app.send_strategies.email import EmailSendStrategyByPythonEmails

from tests.fakesmtp import FakeSMTPServer


class FileSendStrategySettings(FileSendStrategy.Settings):

    class Config:
        env_prefix = 'TEST_FILE_'


class TestFileSendStrategy:
    to = 'test_file_send_strategy.txt'
    message = 'Test'

    def setup_class(self):
        self.strategy = FileSendStrategy(self.to, self.message)

    def test_html(self):
        assert self.strategy.html == \
                self.strategy.template.replace('${message}', self.message)

    def test_send(self):
        response = self.strategy.send()

        assert str(response) == json.dumps({'status': 'writed'})

        with open(self.strategy.file_path, 'r') as file:
            assert file.read() == self.message


class EmailSendStrategyByPythonEmailsSettings(EmailSendStrategyByPythonEmails.Settings):
    SSL: bool = False
    PORT: int = 8025
    HOST: str = 'localhost'
    FROM: str = 'fdaew@tesfdsaty.ty'

    class Config:
        env_prefix = 'TEST_EMAIL_'


EmailSendStrategyByPythonEmails.Settings = EmailSendStrategyByPythonEmailsSettings


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
