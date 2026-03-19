from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import select, text

from adapters.rest.auth import router as auth_router
from adapters.auth.hasher import PasswordHasher
from adapters.infrastructure.postgresql_session import PostgresDependency
from adapters.rest.company import router as company_router
from adapters.rest.user import router as user_router

from repository.models.user import UserDB

db_dependency = PostgresDependency()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_dependency.get_session() as session:
        test_email = "admin2@example.com"
        test_password = "admin"

        query = select(UserDB).where(UserDB.email == test_email)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            await session.execute(text("""
                                       INSERT INTO companies (id, name, slug, is_active)
                                       VALUES (1, 'Test Company', 'test-company', true) ON CONFLICT (id) DO NOTHING;
                                       """))

            hasher = PasswordHasher()
            hashed_password = hasher.get_password_hash(test_password)

            new_user = UserDB(
                company_id=1,
                email=test_email,
                password_hash=hashed_password,
                first_name="Admin",
                last_name="Adminov",
                role="ADMIN",
                is_active=True
            )

            session.add(new_user)
            await session.commit()
        else:
            print(f"⚡ Юзер {test_email} уже существует, создание пропускаем.")

    yield



app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(company_router)

@app.get("/")
def greet():
    return {"data": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8012, reload=True)