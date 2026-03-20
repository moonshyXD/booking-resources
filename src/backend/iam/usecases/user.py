from domain.models.user import UserRepositoryI, User


class UserService:
    def __init__(self, repository: UserRepositoryI):
        self.repository = repository

    def create_domain_user(self, user_data: dict, password: str, password_hash: str, role: str) -> User:
        return User(
            company_id=user_data.get("company_id"),
            email=user_data.get("email"),
            password_hash=password_hash,
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            telegram_username=user_data.get("telegram_username"),
            avatar_url=user_data.get("avatar_url"),
            role=role,
            is_active=True
        )

    async def add_user(self, user: User):
        request = await self.repository.add_user(user)
        if request is None:
            return None

        return request

    async def delete_user(self, user_id: int):
        request = await self.repository.delete_user_by_id(user_id)
        if request is None:
            return None

        return request

    async def update_user(self, user_id: int, new_user: User):
        request = await self.repository.update_user_by_id(user_id, new_user)
        if request is None:
            return None

        return request

    async def update_password(self, user_id: int, password_hash: str):
        request = await self.repository.update_password(user_id, password_hash)
        if request is None:
            return None

        return request

    async def get_users(self, offset: int = 0, limit: int = 20):
        return await self.repository.get_users(offset=offset, limit=limit)