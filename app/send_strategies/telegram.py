from abc import abstractproperty

import telebot

from app.send_strategies import SendStrategy, Response


class TGSendStrategy(SendStrategy):
    """Стратегия отправки писем через телеграм-бота"""

    class Settings(SendStrategy.Settings):
        API_TOKEN: str
        # TO: Optional[str] = None  # from SendStrategy

        class Config:
            env_prefix = 'TG_'

    @abstractproperty
    def bot(self) -> object:
        """Объект телеграм-бота"""
        pass


class TGResponseByTelebot(Response):
    pass


class TGSendStrategyByTelebot(TGSendStrategy):
    """Стратегия отправки писем через телеграм-бота
        с помощью telebot (`pip install pyTelegramBotAPI`)"""

    def bot(self) -> telebot.TeleBot:
        """Объект телеграм-бота"""
        return telebot.TeleBot(self.stg.API_TOKEN)

    def send(self) -> TGResponseByTelebot:
        return TGResponseByTelebot(self.bot.send_message(self.to, self.html))
