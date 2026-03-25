import asyncio
import json
from shared.infrastructure.logger import logging
import redis.asyncio as redis
from notifications.adapters.config.settings import Config
from notifications.adapters.worker.handlers import AccountEventHandlers
from notifications.adapters.email.builder import AccountEmailBuilder
from notifications.adapters.email.sender import EmailSender
from notifications.usecases.account import AccountService
from notifications.adapters.worker.event import EventDispatcher

config = Config.load()


async def setup_worker_dispatcher() -> EventDispatcher:
    sender = EmailSender(smtp_config=config.smtp)
    builder = AccountEmailBuilder()

    account_service = AccountService(repository=builder, sender=sender)

    handlers = AccountEventHandlers(account_service=account_service)

    dispatcher = EventDispatcher()
    dispatcher.register("account_created", handlers.on_account_created)
    dispatcher.register("password_updated", handlers.on_password_updated)
    dispatcher.register("account_deleted", handlers.on_account_deleted)
    dispatcher.register("account_data_updated", handlers.on_account_data_updated)

    return dispatcher

async def start_redis_worker():
    dispatcher = await setup_worker_dispatcher()

    redis_client = redis.from_url(config.redis.url)
    queue = "email_tasks_queue"

    try:
        while True:
            result = await redis_client.brpop(queue, timeout=1)

            if result:
                _, message = result
                task_data = json.loads(message.decode('utf-8'))

                event = task_data.get("event")
                payload = task_data.get("payload", {})

                await dispatcher.handle(event, payload)

    except asyncio.CancelledError:
        logging.info("Сигнал остановки получен. Закрываю воркер...")
    except Exception as e:
        logging.error(f"Критическая ошибка в цикле воркера: {e}")
    finally:
        await redis_client.aclose()
        logging.info("Соединение с Redis закрыто")
