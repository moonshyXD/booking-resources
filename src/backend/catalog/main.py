from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from catalog.adapters.rest import resources
from catalog.adapters.config.settings import Config
from shared.infrastructure.postgresql_session import PostgresDependency

config = Config.load()

db_url = (
    f"postgresql+asyncpg://"
    f"{config.db.user.get_secret_value()}:"
    f"{config.db.password.get_secret_value()}@"
    f"{config.db.host}/"
    f"{config.db.database}"
)

db_dependency = PostgresDependency(db_url=db_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://127.0.0.1:8001",
    "https://127.0.0.1:8001",
    "http://localhost:8001",
    "https://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Set-Cookie", "Authorization", "Access-Control-Allow-Origin"],
)

app.include_router(resources.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8013, reload=True)
