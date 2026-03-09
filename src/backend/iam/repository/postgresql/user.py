from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.user import User
from repository.models.user import UserDB


class UserRepositoryPostgres:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        user_db = await self.session.get(UserDB, user_id)

        if user_db is None:
            return None

        return self._to_entity(user_db)

    async def add_user(self, user: User) -> User:
        user_data = self._validate_user_data(user)

        new_user_db = UserDB(**user_data)

        self.session.add(new_user_db)
        await self.session.flush()

        return self._to_entity(new_user_db)

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

        return self._to_entity(user_db)

    async def delete_user_by_id(self, user_id: int) -> User | None:
        user_db = await self.session.get(UserDB, user_id)

        if user_db is None:
            return None

        self.session.delete(user_db)
        await self.session.flush()

        return self._to_entity(user_db)

    @staticmethod
    def _validate_user_data(user: User) -> dict:
        new_user_data = asdict(user)
        new_user_data.pop("id", None)
        new_user_data.pop("created_at", None)

        return new_user_data

    @staticmethod
    def _to_entity(user_db_instance: UserDB) -> User:
        return User(
            id=user_db_instance.id,
            company_id=user_db_instance.company_id,
            email=user_db_instance.email,
            password_hash=user_db_instance.password_hash,
            first_name=user_db_instance.first_name,
            last_name=user_db_instance.last_name,
            telegram_username=user_db_instance.telegram_username,
            avatar_url=user_db_instance.avatar_url,
            role=user_db_instance.role,
            is_active=user_db_instance.is_active,
            created_at=user_db_instance.created_at,
        )
