from dataclasses import asdict

from domain.models.user import User
from repository.models.user import UserDB
from sqlalchemy.ext.asyncio import AsyncSession
from repository.models.company import CompanyDB
from sqlalchemy import select


class UserRepositoryPostgres:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        user_db = await self.session.get(UserDB, user_id)

        if user_db is None:
            return None

        return self.to_entity(user_db)

    async def add_user(self, user: User) -> User | None:
        if user.company_id is not None:
            company_query = select(CompanyDB).where(CompanyDB.id == user.company_id)
            company_result = await self.session.execute(company_query)
            company_db = company_result.scalar_one_or_none()
            
            if company_db is None:
                return None
            
        user_data = self._validate_user_data(user)

        query = select(UserDB).where(UserDB.email == user.email)
        result = await self.session.execute(query)
        existing_user = result.scalar_one_or_none()
        if existing_user is not None:
            return None

        new_user_db = UserDB(**user_data)

        self.session.add(new_user_db)
        await self.session.flush()

        return self.to_entity(new_user_db)

    async def update_user_by_id(
            self, user_id: int, new_user: User
    ) -> User | None:
        user_db = await self.session.get(UserDB, user_id)
        if user_db is None:
            return None

        new_user_data = self._validate_user_data(new_user)

        for key, value in new_user_data.items():
            setattr(user_db, key, value)

        await self.session.flush()

        return self.to_entity(user_db)

    async def update_password(self, user_id: int, password_hash: str) -> User | None:
        user_db = await self.session.get(UserDB, user_id)
        if user_db is None:
            return None

        user_db.password_hash = password_hash
        await self.session.flush()

        return self.to_entity(user_db)

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(UserDB).where(UserDB.email == email)
        result = await self.session.execute(stmt)
        user_db = result.scalar_one_or_none()

        if user_db is None:
            return None

        return self.to_entity(user_db)

    async def delete_user_by_id(self, user_id: int) -> User | None:
        user_db = await self.session.get(UserDB, user_id)

        if user_db is None:
            return None

        await self.session.delete(user_db)
        await self.session.flush()

        return self.to_entity(user_db)

    async def get_id_by_email(self, email: str) -> int | None:
        stmt = select(UserDB.id).where(UserDB.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_password_by_id(self, user_id: int) -> str | None:
        user_db = await self.session.get(UserDB, user_id)
        if user_db is None:
            return None

        password = user_db.password_hash
        return password

    async def get_users(self, offset: int = 0, limit: int = 20) -> list[User]:
        stmt = select(UserDB).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        users_db = result.scalars().all()
        return [self.to_entity(user) for user in users_db]

    async def get_role_by_id(self, user_id: int) -> str | None:
        user_db = await self.session.get(UserDB, user_id)
        if user_db is None:
            return None

        role = user_db.role
        return role

    @staticmethod
    def _validate_user_data(user: User) -> dict:
        new_user_data = asdict(user)
        new_user_data.pop("id", None)
        new_user_data.pop("created_at", None)
        return {k: v for k, v in new_user_data.items() if v is not None}

    @staticmethod
    def to_entity(user_db_instance: UserDB) -> User:
        return User(
            id=user_db_instance.id,
            company_id=user_db_instance.company_id,
            email=user_db_instance.email,
            password_hash=user_db_instance.password_hash,
            first_name=user_db_instance.first_name,
            last_name=user_db_instance.last_name,
            avatar_url=user_db_instance.avatar_url,
            role=user_db_instance.role,
            is_active=user_db_instance.is_active,
            created_at=user_db_instance.created_at,
        )
