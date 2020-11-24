from enum import Enum
from datetime import datetime
from uuid import uuid4
from typing import Optional, Union, Dict, List

from pydantic import BaseModel, Field

from config.locale import _

from app.send_strategies import Response
from app.send_strategies.email import EmailSendStrategyByPythonEmails
from app.send_strategies.telegram import TGSendStrategyByTelebot
from app.send_strategies.file import FileSendStrategy


class ResponseType(str, Enum):
    """Тип ответа сервиса отправки
        (либо ответ при инициализации отправки, либо при callback'е сервиса)"""
    send = 'send'
    callback = 'callback'


class SenderType(Enum):
    """Способ отправки уведомления с указанием стратегии отправки"""
    email = EmailSendStrategyByPythonEmails
    telegram = TGSendStrategyByTelebot
    file = FileSendStrategy


class Target(BaseModel):
    """Цель уведомления (кому и куда будет отправлено)"""
    sender_type: SenderType
    recipient: str = Field(
            title=_('Recipient'), max_length=32
        )

    def send(self, message) -> Response:
        """Отправка сообщение цели"""
        send_strategy = self.sender_type.value(self.recipient, message)
        return send_strategy.send()


class ServiceResponse(BaseModel):
    """Ответ используемого сервиса отправки"""
    type: ResponseType
    target: Target
    message: str
    datetime_create: datetime = Field(default_factory=datetime.now)


class Notification(BaseModel):
    """Уведомление"""
    id: int = Field(default_factory=uuid4)
    message: str = Field(
            title=_('Notification`s message'), max_length=1000, example='Message`s text'
        )
    callback: Optional[str] = Field(
            None, title=_('URL for callback'), max_length=300, example='http://example.com'
        )
    targets: Dict[str, Union[str, List[str]]] = Field(
            title=_('Targets for sending'), example={"email": ["test@test.com"]}
        )
    responses: List[ServiceResponse] = []
    datetime_create: datetime = Field(default_factory=datetime.now)
