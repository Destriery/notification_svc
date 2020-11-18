from functools import cached_property
from typing import Optional, Any, Dict, List, Union
from enum import Enum
from datetime import datetime

import emails
from emails.backend.response import SMTPResponse
from string import Template

from fastapi import FastAPI
from pydantic import BaseModel, BaseSettings, Field

from config.locale import _

app = FastAPI()


@app.get('/')
async def root():
    return {'message': _('Hello! {t}').format(t=12), 'add': _('Add')}


@app.get('/en')
async def en():
    return {'message': _('Hello!')}


# models


class SendStrategy:
    """Абстрактный класс для стратегий отправки уведомлений"""
    pass


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


class DefaultSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class EmailSendStrategy(SendStrategy):
    """Стратегия отправки писем через smtp-сервер
        при помощи библиотеки python-emails (`pip install emails`)"""

    subject = _('Message from Notification Service')
    template = '<html><body>${message}</body></html>'

    class Settings(DefaultSettings):
        """Берутся настройки из файла .env с префиксом EMAIL_"""
        # TODO Возможно стоит сделать USER и PASSWORD не обязательными
        SSL: str = True
        PORT: int = 465
        HOST: str
        USER: Optional[str] = None
        PASSWORD: Optional[str] = None

        FROM: str

        class Config:
            env_prefix = 'EMAIL_'

    def __init__(self, to: Union[str, List[str]], message: str = '') -> None:
        """Задаются почта получателя и формируется сообщение по шаблону
            также инициализируются настройки"""
        self.email_to = to
        self.html = message

        self.stg = self.Settings()

    @cached_property
    def connection_params(self) -> dict:
        """Задаются параметры соединения"""
        return dict(
            host=self.stg.HOST,
            port=self.stg.PORT,
            ssl=self.stg.SSL,
            user=self.stg.USER,
            password=self.stg.PASSWORD
        )

    @property
    def html(self) -> str:
        """Итоговый html для отправки"""
        return self._html

    @html.setter
    def html(self, message: str = '') -> None:
        """Формируется итоговый html на основе шаблона и входящего сообщения"""
        self._html = Template(self.template).substitute(message=message)

    @property
    def message(self) -> emails.Message:
        """Объект сообщения для отправки"""
        return emails.Message(
            subject=self.subject,
            html=self.html,
            mail_from=('NotificationService', self.stg.FROM)
        )

    def send(self) -> SMTPResponse:
        """Отправка сообщения"""
        response = self.message.send(
            to=self.email_to,
            smtp=self.connection_params
        )

        return response


# endpoints


@app.post('/notify')
@app.post('/notifications')
async def set_notification(notification: NotificationIn):
    """Получает запрос на отправку уведомления со стороннего сервиса"""
    r = EmailSendStrategy('izzon@yandex.ru', 'Test')
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
