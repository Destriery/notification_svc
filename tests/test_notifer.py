import uuid

from app import Notifer
from app.schema import NotificationSсhemeIn
from app.models import Target, SenderType, ServiceResponse, ResponseType


class TestNotifer:
    notification_data = {
        'message': 'Test Notifer',
        'targets': {'file': 'test_notifer.txt'}
    }
    response_from_send_service = 'Response'

    def _create_notification(self) -> uuid.uuid4().hex:
        """Создается Notification"""
        notification_in = NotificationSсhemeIn(**self.notification_data)

        return self.notifer.create_notification(notification_in)

    def setup_class(self):
        self.message = self.notification_data.get('message')

        targets = self.notification_data.get('targets')
        targets_keys = tuple(targets.keys())
        targets_values = tuple(targets.values())

        self.TARGET_INDEX = 0
        self.sender_type = SenderType[targets_keys[self.TARGET_INDEX]]
        self.send_strategy = SenderType[targets_keys[self.TARGET_INDEX]].value
        self.recipient = targets_values[self.TARGET_INDEX]

    def setup(self):
        self.notifer = Notifer()

    def teardown(self):
        self.notifer = None

    def test_targets(self):
        """Тестируем задание целей"""
        self.notifer.targets = self.notification_data.get('targets')

        assert len(self.notifer.targets) == 1
        assert self.notifer.targets[self.TARGET_INDEX] == Target(
                                                        sender_type=self.sender_type,
                                                        recipient=self.recipient
                                                    )

    def test_save_response_from_send_service(self):
        """Тестируем задание ответов от сервера"""
        self._create_notification()

        self.notifer.save_response_from_send_service(
            self.notifer.targets[self.TARGET_INDEX],
            self.response_from_send_service
        )

        assert len(self.notifer.notification.responses) == 1

        assert self.notifer.notification.responses[0].dict(exclude={'datetime_create'}) == \
            ServiceResponse(
                type=ResponseType.send,
                target=Target(
                        sender_type=self.sender_type,
                        recipient=self.recipient
                    ),
                message=self.response_from_send_service).dict(exclude={'datetime_create'})

    def test_create_notification(self):
        """Тестируем создание Notification"""
        _id = self._create_notification()

        UUID4_LEN = 32
        assert len(_id) == UUID4_LEN

    def test_send_notification(self):
        """Тестируем отправку уведомления"""
        self._create_notification()

        self.notifer.send_notification()

        assert self.sender_type.name == 'file'
        with open(self.send_strategy(self.recipient).file_path, 'r') as file:
            assert file.read() == self.message
