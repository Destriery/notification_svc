from typing import Optional, Any, Dict, List
from collections import namedtuple
from enum import Enum, auto
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field
from pydantic import fields

from config.locale import _

app = FastAPI()

@app.get('/')
async def root():
    return {'message': _('Hello!'), 'add': _('Add')}

@app.get('/en')
async def en():
    return {'message': _('Hello!')}

# models

class SendStrategy:
    """Абстрактный класс для стратегий отправки уведомлений"""
    pass


class ResponseType(str, Enum):
    """Тип ответа сервиса отправки (либо ответ при инициализации отправки, либо при callback'е сервиса)"""
    send = 'send'
    callback = 'callback'


class SenderType(BaseModel):
    """Способ отправки уведомления с указанием стратегии отправки"""
    name: str = Field(
            title=_('Type`s name'), max_length=8
        )
    strategy: Optional[Any]

class Target(BaseModel):
    """Цель уведомления (кому и куда будет отправлено)"""
    sender_type: SenderType
    recipient: str = Field(
            title=_('Recipient'), max_length=32
        )

class Response(BaseModel):
    """Ответ используемого сервиса отправки"""
    type: ResponseType
    datetime: datetime
    message: str


class Notification(BaseModel):
    """Уведомление"""
    id: int
    message: str = Field(
            title=_('Notification`s message'), max_length=1000, example='Message`s text'
        )
    callback: Optional[str] = Field(
            None, title=_('URL for callback'), max_length=300, example='http://example.com'
        )
    targets: List[Target]
    responses: List[Response]
    datetime_create: datetime
    

class NotificationOut(Notification):
    targets: Dict[str, List[str]] = Field(
            title=_('Targets for sending'), example={"email": ["test@test.com"]}
        )


class NotificationIn(NotificationOut):
    id: Any = Field(default=None, const=None)
    responses: Any = Field(default=None, const=None)
    datetime_create: Any = Field(default=None, const=None)


# endpoints

@app.post('/notify')
@app.post('/notifications')
async def set_notification(notification: NotificationIn):
    """Получает запрос на отправку уведомления со стороннего сервиса"""

    return notification

@app.get('/notifications/{id}')
async def get_notification(id: int):
    """Отдает данные о запрашиваемом по id уведомлении"""
    return {}

@app.post('/notifications/{id}/callback')
async def set_notification_callback(id: int):
    """Получает callback со стороннего сервиса"""
    return {}


# classes


class Notifer:
    
    def __init__(self, id: Optional[int] = None) -> None:
        pass