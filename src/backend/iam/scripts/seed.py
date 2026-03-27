import asyncio
import os
import uuid

from faker import Faker
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from iam.adapters.auth.hasher import PasswordHasher
from iam.adapters.config.settings import Config
from iam.adapters.notifications.gateway import NotificationRedisGateway
from iam.domain.models.user_role import UserRole
from iam.domain.models.user import User
from iam.repository.models.company import CompanyDB
from iam.repository.models.user import UserDB
from iam.repository.orm.user import UserRepositoryPostgres
from iam.usecases.user import UserService

faker = Faker("ru_RU")
DATABASE_URL = os.getenv("DATABASE_URL")
MOCK_EMAILS = [
    "iiskondra11@yandex.ru",
    "eshekere5252@gmail.com",
    "clavander07@gmail.com",
]


def build_company() -> CompanyDB:
    slug_base = faker.unique.slug()
    slug = f"{slug_base[:50]}-{uuid.uuid4().hex[:8]}"
    return CompanyDB(
        name=faker.unique.company(),
        slug=slug[:64],
        is_active=True,
    )


def build_user(
    *,
    company_id: uuid.UUID,
    role: UserRole,
    email: str | None = None,
) -> User:
    return User(
        company_id=company_id,
        email=email or faker.unique.email(),
        password_hash="",
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        avatar_url=faker.image_url(),
        role=role.value,
        is_active=True,
    )


async def seed_data(companies_count: int = 5, users_per_company: int = 8) -> None:
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is required for seed script")

    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        async with session.begin():
            companies_count_query = await session.execute(
                select(func.count()).select_from(CompanyDB)
            )
            users_count_query = await session.execute(
                select(func.count()).select_from(UserDB)
            )
            if (
                companies_count_query.scalar_one() > 0
                or users_count_query.scalar_one() > 0
            ):
                return

            config = Config.load()
            service = UserService(
                repository=UserRepositoryPostgres(session),
                hasher=PasswordHasher(),
                notifications=NotificationRedisGateway(config.redis.url),
            )

            companies: list[CompanyDB] = [build_company() for _ in range(companies_count)]
            session.add_all(companies)
            await session.flush()

            users: list[User] = []
            mock_email_index = 0
            for idx, company in enumerate(companies):
                admin_email = None
                if mock_email_index < len(MOCK_EMAILS):
                    admin_email = MOCK_EMAILS[mock_email_index]
                    mock_email_index += 1

                users.append(
                    build_user(
                        company_id=company.id,
                        role=UserRole.ADMIN if idx == 0 else UserRole.COMPANY_ADMIN,
                        email=admin_email,
                    )
                )
                for _ in range(users_per_company - 1):
                    user_email = None
                    if mock_email_index < len(MOCK_EMAILS):
                        user_email = MOCK_EMAILS[mock_email_index]
                        mock_email_index += 1

                    users.append(
                        build_user(
                            company_id=company.id,
                            role=UserRole.USER,
                            email=user_email,
                        )
                    )

            # Create users via usecase (it generates password + sends notification)
            for user in users:
                await service.add_user(user)

    await engine.dispose()


async def main() -> None:
    await seed_data()


if __name__ == "__main__":
    asyncio.run(main())
