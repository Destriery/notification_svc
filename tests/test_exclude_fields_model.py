from typing import Any
from pydantic import BaseModel

from app.schema import ExcludeFieldsModel
from config.locale import _


# модели для тестов

class ParentModel(BaseModel):
    first_field: Any
    second_field: Any


class ChildModel(ParentModel, ExcludeFieldsModel):
    _exclude_fields = ('second_field',)


class ChildModelWithOtherField(ParentModel, ExcludeFieldsModel):
    _exclude_fields = ('second_field', 'other_field')

# тесты


def test_exclude_fields_model():
    """Тест на исключение поля у дочерней модели при наследовании от ExcludeFieldsModel
        и указании выбранного поля в _exclude_fields"""
    exclude_fields_model = ChildModel(first_field=True, second_field=True)

    assert exclude_fields_model.dict() == {'first_field': True}


def test_exclude_fields_model_with_other_field():
    """Тест на ошибку исключение поля у дочерней модели при указании не существующего поля"""
    try:
        ChildModelWithOtherField(first_field=True, second_field=True)
    except KeyError as e:
        assert e.args[0] == _(
                            '_exclude_fields in ChildModelWithOtherField has field "other_field" '
                            'which missing in ChildModelWithOtherField`s fields'
                        )
