import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import select, text

from iam.adapters.rest.auth import router as auth_router
from iam.adapters.auth.hasher import PasswordHasher
from shared.infrastructure.postgresql_session import PostgresDependency
from iam.adapters.rest.company import router as company_router
from iam.adapters.rest.user import router as user_router

import uvicorn
from iam.repository.models.user import UserDB

from iam.adapters.config.settings import Config

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
    async with db_dependency.get_session() as session:
        test_email = "admin2@example.com"
        test_password = "admin"

        query = select(UserDB).where(UserDB.email == test_email)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            company_query = await session.execute(
                text("SELECT id FROM companies WHERE name = 'Test Company'")
            )
            company_id = company_query.scalar_one_or_none()

            if not company_id:
                company_id = uuid.uuid4()
                await session.execute(
                    text("""
                        INSERT INTO companies (id, name, slug, is_active)
                        VALUES (:id, 'Test Company', 'test-company', true)
                    """),
                    {"id": company_id}
                )

            hasher = PasswordHasher()
            hashed_password = hasher.get_password_hash(test_password)

            new_user = UserDB(
                company_id=company_id,
                email=test_email,
                password_hash=hashed_password,
                first_name="Admin",
                last_name="Adminov",
                role="ADMIN",
                is_active=True
            )

            session.add(new_user)
            await session.commit()

    yield



app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(company_router)

@app.get("/")
def greet():
    return {"data": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8012, reload=True)