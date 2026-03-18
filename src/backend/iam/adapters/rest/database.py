from adapters.config.settings import Config
from adapters.infrastructure.postgresql_session import PostgresDependency


config = Config.load()
db_url = f"postgresql+asyncpg://{config.db.user.get_secret_value()}:{config.db.password.get_secret_value()}@{config.db.host}/{config.db.database}"
db_dependency = PostgresDependency(db_url)

async def get_db_session():
    async with db_dependency.get_session() as session:
        yield session