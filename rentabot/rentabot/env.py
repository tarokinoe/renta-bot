import os

from pydantic import BaseSettings


class EnvSettings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    SITE_BASE_URL: str
    START_PAGE: str
    PARSING_PERIOD_S: int
    PARSED_APPARTMENTS_FILE: str

    class Config:
        env_prefix = 'RENTABOT_'
        env_file_encoding = 'utf-8'
        env_file = os.getenv('ENV_PATH', 'conf/.env')
