import os
from pydantic import BaseSettings

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Babel
DEFAULT_LOCALE = 'en'
LOCALEDIR = 'locales'
LOCALEDOMAIN = 'messages'

LOCALE = 'en'


class DefaultSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
