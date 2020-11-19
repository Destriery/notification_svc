from typing import Optional, Any, Dict, List
from enum import Enum
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

from config.locale import _

from send_strategies.email import EmailSendStrategyByPythonEmails

app = FastAPI()


@app.get('/')
async def root():
    return {'message': _('Hello! {t}').format(t=12), 'add': _('Add')}


@app.get('/en')
async def en():
    return {'message': _('Hello!')}


# models

class ResponseType(str, Enum):
    """Тип ответа сервиса отправки
        (либо ответ при инициализации отправки, либо при callback'е сервиса)"""
    send = 'send'
    callback = 'callback'


class ExcludeFieldsModel(BaseModel):
    """Позволяет исключать поля из текущей модели, если у родительской присутствуют лишние

        WARNING: Не документированная в pytdantic функциональность,
            могут быть проблемы при обновлении
    """
    _exclude_fields = []

    def exclude_selected_fields_from_fields(self):
        for field in self._exclude_fields:
            try:
                self.__fields__.pop(field)
            except KeyError:
                raise KeyError(
                    _(
                        '_exclude_fields in {class_name} has field "{field}" '
                        'which missing in {class_name}`s fields'
                    ).format(
                        class_name=self.__class__.__name__,
                        field=field
                    )
                )

    def __init__(self, **data: Any) -> None:
        self.exclude_selected_fields_from_fields()
        super().__init__(**data)


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


class NotificationIn(NotificationOut, ExcludeFieldsModel):
    _exclude_fields = ('id', 'responses', 'datetime_create')


# endpoints


@app.post('/notify')
@app.post('/notifications')
async def set_notification(notification: NotificationIn):
    """Получает запрос на отправку уведомления со стороннего сервиса"""
    r = EmailSendStrategyByPythonEmails('izzon@yandex.ru', 'Test')
    r.send()

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


"""
m = emails.Message(html=T("<html><p>Build passed: {{ project_name }} <img src='cid:icon.png'> ..."),
                   text=T("Build passed: {{ project_name }} ..."),
                   subject=T("Passed: {{ project_name }}#{{ build_id }}"),
                   mail_from=("CI", "ci@mycompany.com"))
m.attach(filename="icon.png", content_disposition="inline", data=open("icon.png", "rb"))
response = m.send(
    render={"project_name": "user/project1", "build_id": 121},
    to='somebody@mycompany.com',
    smtp={"host":"mx.mycompany.com", "port": 25}
)

if response.status_code not in [250, ]:
"""


class Notifer:
    def __init__(self, id: Optional[int] = None) -> None:
        pass
