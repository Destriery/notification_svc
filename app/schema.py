from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from config.locale import _

from app.models import Notification


class ExcludeFieldsModel(BaseModel):
    """Позволяет исключать поля из текущей модели, если у родительской присутствуют лишние

        WARNING: Не документированная в pytdantic функциональность,
            могут быть проблемы при обновлении
    """
    _exclude_fields = []

    def exclude_selected_fields_from_fields(self):
        for field in self._exclude_fields:
            self.__fields__.pop(field, None)

    def __init__(self, **data: Any) -> None:
        self.exclude_selected_fields_from_fields()
        super().__init__(**data)


class NotificationSсhemeOut(Notification):
    pass


class NotificationSсhemeIn(BaseModel):
    # TODO убрать дублирование кода
    message: str = Field(
            title=_('Notification`s message'), max_length=1000, example='Message`s text'
        )
    callback: Optional[str] = Field(
            None, title=_('URL for callback'), max_length=300, example='http://example.com'
        )
    targets: Dict[str, Union[str, List[str]]] = Field(
            title=_('Targets for sending'), example={"email": ["test@test.com"]}
        )
