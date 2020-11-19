from pydantic import BaseSettings


# Babel
DEFAULT_LOCALE = 'en'
LOCALEDIR = 'locales'
LOCALEDOMAIN = 'messages'

LOCALE = 'en'


class DefaultSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
