import json
import redis.asyncio as redis
from shared.infrastructure.logger import logging


class NotificationRedisGateway:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.queue_name = "email_tasks_queue"

    async def send_created_account(self, email: str, password: str):
        task = {
            "event": "account_created",
            "payload": {
                "email": email,
                "password": password
            }
        }
        try:
            await self.redis.lpush(self.queue_name, json.dumps(task))
            logging.info(f"Задача 'создание аккаунта' для {email} отправлена в очередь")
        except Exception as e:
            logging.error(f"Redis недоступен, задача для {email} потеряна: {e}")

    async def send_updated_password(self, email: str, password: str):
        task = {
            "event": "password_updated",
            "payload": {
                "email": email, 
                "password": password
            }
        }
        try:
            await self.redis.lpush(self.queue_name, json.dumps(task))
            logging.info(f"Задача 'смена пароля' для {email} отправлена в очередь")
        except Exception as e:
            logging.error(f"Redis недоступен, задача для {email} потеряна: {e}")

    async def send_deleted_account(self, email: str):
        task = {
            "event": "account_deleted",
            "payload": {
                "email": email
            }
        }
        try:
            await self.redis.lpush(self.queue_name, json.dumps(task))
            logging.info(f"Задача 'удаление аккаунта' для {email} отправлена в очередь")
        except Exception as e:
            logging.error(f"Redis недоступен, задача для {email} потеряна: {e}")

    async def send_updated_account_data(self, email: str):
        task = {
            "event": "account_data_updated",
            "payload": {
                "email": email
            }
        }
        try:
            await self.redis.lpush(self.queue_name, json.dumps(task))
            logging.info(f"Задача 'обновление профиля' для {email} отправлена в очередь")
        except Exception as e:
            logging.error(f"Redis недоступен, задача для {email} потеряна: {e}")