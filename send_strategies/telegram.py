from abc import abstractproperty

import telebot

from send_strategies import SendStrategy


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


class TGSendStrategyByTelebot(TGSendStrategy):
    """Стратегия отправки писем через телеграм-бота
        с помощью telebot (`pip install pyTelegramBotAPI`)"""

    def bot(self) -> telebot.TeleBot:
        """Объект телеграм-бота"""
        return telebot.TeleBot(self.stg.API_TOKEN)

    def send(self) -> telebot.types.Message:
        return self.bot.send_message(self.stg.TO, self.html)
