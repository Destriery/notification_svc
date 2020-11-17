import threading
import asyncore

from main import EmailSendStrategy

from tests.fakesmtp import FakeSMTPServer


class TestEmailSendStrategy:
    email_to = 'fdaew@tesfdsaty.ty'
    message = 'Test'
    connection_params = {
        'host': 'localhost',
        'port': 8025
    }

    def setup_class(self):
        self.strategy = EmailSendStrategy(self.email_to, self.message)
        self.strategy.connection_params = self.connection_params

        self.smtp_server = FakeSMTPServer(
            (
                self.connection_params.get('host'),
                self.connection_params.get('port')
            ),
            None
        )
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
