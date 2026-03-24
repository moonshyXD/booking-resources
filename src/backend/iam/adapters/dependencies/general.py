from shared.infrastructure.postgresql_session import PostgresDependency
from shared.infrastructure.redis_session import RedisDependency
from iam.adapters.config.settings import Config

config = Config.load()

db_url = (
    f"postgresql+asyncpg://"
    f"{config.db.user.get_secret_value()}:"
    f"{config.db.password.get_secret_value()}@"
    f"{config.db.host}/"
    f"{config.db.database}"
)
db_obj = PostgresDependency(db_url)
get_db_session = db_obj.get_db_session

redis_dep = RedisDependency(redis_url=config.redis.url)