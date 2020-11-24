from app.send_strategies import Response
import uuid
from typing import Optional, List

from app.models import Notification, Target, SenderType, ServiceResponse, ResponseType
from app.schema import NotificationSсhemeIn


class Notifer:
    """Класс, определяющий работу с уведомлениями"""
    notification: Notification

    def __init__(self, notification_id: Optional[int] = None) -> None:
        pass

    @property
    def targets(self) -> List[Target]:
        """Цели для отправки"""
        return self._targets

    @targets.setter
    def targets(self, notification_targets) -> None:
        """Формируются Targets из переданного словаря целей в notification"""
        self._targets = []
        for sender_type, recipient_list in notification_targets.items():
            # если передана строка, а не список, преобразуем в list
            if isinstance(recipient_list, str):
                recipient_list = [recipient_list]

            for recipient in recipient_list:
                self._targets.append(
                    Target(sender_type=SenderType[sender_type], recipient=recipient)
                )

    def save_response_from_send_service(self, target: Target, response: Response) -> None:
        """Сохраняется ответ от сервиса отправки в Notification"""
        response = ServiceResponse(
            type=ResponseType.send,
            target=target,
            message=str(response)
        )

        self.notification.responses.append(response)

    def get_json_of_responses_from_send_service(self) -> dict:
        """Отдает список ответов(responses) в формате dict"""
        responses = []
        for response in self.notification.responses:
            response_dict = response.dict(exclude={'target': {'sender_type'}})
            response_dict.get('target')['sender_type'] = response.target.sender_type.name

            responses.append(response_dict)

        return responses

    def create_notification(self, notification_in: NotificationSсhemeIn) -> uuid.uuid4().hex:
        """Создается Notification на основе переданных данных,
            а также задаются цели для отправки"""
        self.notification = Notification(**notification_in.dict())

        self.targets = self.notification.targets

        return self.notification.id.hex

    def send_notification(self) -> None:
        """Отправляется сообщение указанным целям"""
        for target in self.targets:
            response = target.send(self.notification.message)

            self.save_response_from_send_service(target, response)

        return dict(
            responses=self.get_json_of_responses_from_send_service()
        )

    def send_callback(self) -> None:
        """Отправляется callback, если указан"""
        pass
