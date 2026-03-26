import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from notifications.adapters.rest.smtp import router as smtp_router
from notifications.adapters.worker.runner import start_redis_worker

background_tasks = set()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(start_redis_worker())

    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan, root_path="/notifications")

app.include_router(smtp_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)