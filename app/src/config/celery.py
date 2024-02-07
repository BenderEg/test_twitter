from celery import Celery
from celery.schedules import crontab
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.config import settings

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file='./config/celery_config',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    broker_transport_options: dict
    accept_content: list
    task_serializer: str
    imports: list

celery_settings = Settings()

app = Celery("twitter")
app.config_from_object(celery_settings)
app.conf.broker_url = f"redis://{settings.redis.host}:{settings.redis.port}/{settings.redis.db}"
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "test_task": {"task": "background.tasks.test_task", "schedule": crontab()},
}
