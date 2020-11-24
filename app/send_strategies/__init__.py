import json
from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any, List, Optional, Union

from string import Template

from config.locale import _
from config.settings import DefaultSettings


class Response:
    """Ответ сервиса от SendStrategy"""
    original_response: Any = None

    def __init__(self, original_response) -> None:
        self.original_response = original_response

    def __str__(self):
        """Преобразуем ответ в строку в формате JSON"""
        return json.dumps(self.original_response)


class SendStrategy(ABC):
    """Абстрактный класс для стратегий отправки уведомлений \n
        to: str - кому отправлять \n
        message: str - сообщение"""
    template = '${message}'

    class Settings(DefaultSettings):
        TO: Optional[str] = None

    def __init__(self, to: Union[str, List[str], None] = None, message: str = '') -> None:
        """Инициализируются настройки, определяется получатель и формируется сообщение"""
        self.stg = self.Settings()

        self.to = to or self.stg.TO
        self.message = message

    @property
    def to(self) -> str:
        """Кому отправляем"""
        return self._to

    @to.setter
    def to(self, to: Union[str, List[str], None]) -> None:
        """Задается получатель, либо при его отсутствии возвращается ошибка"""
        try:
            self._to = to
        except ValueError:
            # TODO определять название функциии исходя из реального названия
            raise ValueError(
                _('"{}" was not specified').format('to')
            )

    @cached_property
    def html(self) -> str:
        """Формируется итоговый html на основе шаблона и входящего сообщения"""
        return Template(self.template).substitute(message=self.message)

    @abstractmethod
    def send(self) -> Response:
        """Отправка сообщения, возвращаем response"""
        pass
