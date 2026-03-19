from domain.models.user import UserRepositoryI, User


class UserService:
    def __init__(self, repository: UserRepositoryI):
        self.repository = repository

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

    async def get_users(self, offset: int = 0, limit: int = 20):
        return await self.repository.get_users(offset=offset, limit=limit)