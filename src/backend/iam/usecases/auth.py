from domain.auth.hasher import PasswordHasherI
from domain.auth.token import TokenProviderI
from domain.models.user import UserRepositoryI
from domain.models.company import CompanyRepositoryI


class AuthService:
    def __init__(
            self,
            hasher: PasswordHasherI,
            token_provider: TokenProviderI,
            repository: UserRepositoryI,
            company_repository: CompanyRepositoryI = None
    ):
        self.hasher = hasher
        self.token_provider = token_provider
        self.repository = repository
        self.company_repository = company_repository

    async def authenticate(self, email: str, password: str, company_slug: str | None = None) -> dict | None:
        user = await self.repository.get_user_by_email(email)
        if user is None or not self.hasher.verify_password(password, user.password_hash):
            return None

        if user.role != "ADMIN":
            if company_slug is None:
                return None

            if self.company_repository is not None:
                company = await self.company_repository.get_company_by_slug(company_slug)
                if company is None or user.company_id != company.id:
                    return None
        else:
            pass

        token_payload = {
            "sub": user.email,
            "role": user.role,
            "company_id": user.company_id
        }

        access_token = self.token_provider.create_access_token(token_payload)

        refresh_token = self.token_provider.create_refresh_token({"sub": user.email})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": user.role,
            "token_type": "bearer"
        }