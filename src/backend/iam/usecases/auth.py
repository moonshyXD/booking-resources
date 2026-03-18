from domain.auth.hasher import PasswordHasherI
from domain.auth.token import TokenProviderI
from domain.models.user import UserRepositoryI


class AuthService:
    def __init__(
        self, hasher: PasswordHasherI, token_provider: TokenProviderI, repository: UserRepositoryI
    ):
        self.hasher = hasher
        self.token_provider = token_provider
        self.repository = repository

    async def authenticate(self, email: str, password: str) -> dict | None:
        user_id = await self.repository.get_id_by_email(email)
        if user_id is None:
            return None

        hashed_password = await self.repository.get_password_by_id(user_id)
        if not hashed_password or not self.hasher.verify_password(
            password, hashed_password
        ):
            return None

        access_token = self.token_provider.create_access_token({"sub": email})
        refresh_token = self.token_provider.create_refresh_token({"sub": email})
        role = await self.repository.get_role_by_id(user_id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": role,
            "token_type": "bearer"
        }
