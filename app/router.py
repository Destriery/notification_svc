from fastapi import APIRouter

from app import Notifer
from app.schema import NotificationSсhemeIn, NotificationSсhemeOut

router = APIRouter()


@router.post('/notify')
@router.post('/notifications')
async def set_notification(notification: NotificationSсhemeIn):
    """Получает запрос на отправку уведомления со стороннего сервиса"""

    notifer = Notifer()
    notifer.create_notification(notification)

    return notifer.send_notification()


@router.get('/notifications/{id}', response_model=NotificationSсhemeOut)
async def get_notification(id: int):
    """Отдает данные о запрашиваемом по id уведомлении"""
    notifer = Notifer(id)

    return notifer.notification


@router.post('/notifications/{id}/callback')
async def set_notification_callback(id: int):
    """Получает callback со стороннего сервиса и отправляет в приложение,
        из которого пришло уведомление, если есть callback"""
    notifer = Notifer(id)

    notifer.send_callback()

    return {}
