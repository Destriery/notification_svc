from typing import Optional, TypeVar
from functools import cached_property
from abc import abstractproperty

import emails
from emails.backend.response import SMTPResponse

from app.send_strategies import SendStrategy, Response

from config.locale import _


Message = TypeVar('Message')


class EmailSendStrategy(SendStrategy):
    """Стратегия отправки писем через smtp-сервер"""

    subject = _('Message from Notification Service')
    template = '<html><body>${message}</body></html>'

    class Settings(SendStrategy.Settings):
        """Берутся настройки из файла .env с префиксом EMAIL_"""
        SSL: bool = True
        PORT: int = 465
        HOST: str
        USER: Optional[str] = None
        PASSWORD: Optional[str] = None

        FROM: str
        # TO: Optional[str] = None  # from SendStrategy

        class Config:
            env_prefix = 'EMAIL_'

    @abstractproperty
    def connection_params(self) -> dict:
        """Задаются параметры соединения"""
        pass

    @abstractproperty
    def email_message(self) -> Message:
        """Объект сообщения для отправки"""
        pass


class EmailResponseByPythonEmails(Response):
    @cached_property
    def status_code(self):
        return self.original_response.status_code


class EmailSendStrategyByPythonEmails(EmailSendStrategy):
    """Стратегия отправки писем через smtp-сервер
        при помощи библиотеки python-emails (`pip install emails`)"""

    @cached_property
    def connection_params(self) -> dict:
        """Задаются параметры соединения"""
        params = dict(
            host=self.stg.HOST,
            port=self.stg.PORT,
            ssl=self.stg.SSL,
            user=self.stg.USER,
            password=self.stg.PASSWORD
        )

        return {key: value for key, value in params.items() if params[key]}

    @property
    def email_message(self) -> emails.Message:
        """Объект сообщения для отправки"""
        return emails.Message(
            subject=self.subject,
            html=self.html,
            mail_from=('NotificationService', self.stg.FROM)
        )

    def send(self) -> SMTPResponse:
        """Отправка сообщения"""
        response = self.email_message.send(
            to=self.to,
            smtp=self.connection_params
        )

        return EmailResponseByPythonEmails(response)
