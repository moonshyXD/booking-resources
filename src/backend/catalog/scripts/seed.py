import asyncio
import os
import uuid

from faker import Faker
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from catalog.repository.models.resource import ResourceDB
from catalog.repository.models.resource_category import ResourceCategoryDB
from catalog.repository.models.resource_status import ResourceStatus

faker = Faker("ru_RU")
DATABASE_URL = os.getenv("DATABASE_URL")


async def seed_data() -> None:
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is required for seed script")

    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        async with session.begin():
            categories_count_query = await session.execute(
                select(func.count()).select_from(ResourceCategoryDB)
            )
            resources_count_query = await session.execute(
                select(func.count()).select_from(ResourceDB)
            )
            if (
                categories_count_query.scalar_one() > 0
                or resources_count_query.scalar_one() > 0
            ):
                return

            company_id = uuid.uuid4()
            categories = [
                ResourceCategoryDB(name="Meeting room"),
                ResourceCategoryDB(name="Equipment"),
                ResourceCategoryDB(name="Workspace"),
            ]
            session.add_all(categories)
            await session.flush()

            resources: list[ResourceDB] = []
            for category in categories:
                for _ in range(10):
                    resources.append(
                        ResourceDB(
                            company_id=company_id,
                            category_id=category.id,
                            name=f"{category.name} {faker.unique.bothify(text='??-###')}",
                            info=faker.sentence(nb_words=8),
                            photo_url=f"https://picsum.photos/seed/{uuid.uuid4()}/640/480",
                            status=faker.random_element(
                                [
                                    ResourceStatus.FREE,
                                    ResourceStatus.FULL,
                                    ResourceStatus.MAINTENANCE,
                                ]
                            ),
                        )
                    )

            session.add_all(resources)

    await engine.dispose()


async def main() -> None:
    await seed_data()


if __name__ == "__main__":
    asyncio.run(main())
