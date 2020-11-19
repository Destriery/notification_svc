from abc import ABC, abstractmethod
from typing import List, Optional, Union

from string import Template

from config.locale import _
from config.settings import DefaultSettings


class SendStrategy(ABC):
    """Абстрактный класс для стратегий отправки уведомлений"""
    template = '${message}'

    class Settings(DefaultSettings):
        TO: Optional[str] = None

    def __init__(self, to: Union[str, List[str], None] = None, message: str = '') -> None:
        """Инициализируются настройки, определяется получатель и формируется сообщение"""
        self.stg = self.Settings()

        self.to = to or self.stg.TO
        self.html = message

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

    @property
    def html(self) -> str:
        """Итоговый html для отправки"""
        return self._html

    @html.setter
    def html(self, message: str = '') -> None:
        """Формируется итоговый html на основе шаблона и входящего сообщения"""
        self._html = Template(self.template).substitute(message=message)

    @abstractmethod
    def send(self) -> object:
        """Отправка сообщения, возвращаем response"""
        pass
