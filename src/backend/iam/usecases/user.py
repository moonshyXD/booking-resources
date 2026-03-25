from iam.domain.models.user import UserRepositoryI, User
from iam.domain.auth.hasher import PasswordHasherI
from iam.domain.notifications.gateway import NotificationGatewayI
import uuid


class UserService:
    def __init__(
            self,
            repository: UserRepositoryI,
            hasher: PasswordHasherI,
            notifications: NotificationGatewayI
    ):
        self.repository = repository
        self.hasher = hasher
        self.notifications = notifications

    def create_domain_user(self, user_data: dict, password_hash: str, role: str) -> User:
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
        password = await self.hasher.get_password()
        user.password_hash = self.hasher.get_password_hash(password)

        request = await self.repository.add_user(user)
        if request is None:
            return None

        await self.notifications.send_created_account(email=user.email, password=password)

        return request

    async def delete_user(self, user_id: uuid.UUID):
        user_email = await self.repository.get_email_by_id(user_id)

        request = await self.repository.delete_user_by_id(user_id)
        if request is None:
            return None

        if user_email:
             await self.notifications.send_deleted_account(email=user_email)

        return request

    async def update_user(self, user_id: uuid.UUID, new_user: User):
        request = await self.repository.update_user_by_id(user_id, new_user)
        if request is None:
            return None

        await self.notifications.send_updated_account_data(email=new_user.email)

        return request

    async def update_password(self, user_id: int, email: str):
        password = await self.hasher.get_password()
        password_hash = self.hasher.get_password_hash(password)

        request = await self.repository.update_password(user_id, password_hash)
        if request is None:
            return None

        await self.notifications.send_updated_password(email=email, password=password)

        return request

    async def get_users(self, offset: int = 0, limit: int = 20):
        return await self.repository.get_users(offset=offset, limit=limit)