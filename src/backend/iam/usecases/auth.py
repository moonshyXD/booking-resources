from iam.domain.auth.hasher import PasswordHasherI
from iam.domain.auth.token import TokenProviderI
from iam.domain.models.user import UserRepositoryI
from iam.domain.models.company import CompanyRepositoryI
from shared.auth.blacklist import TokenBlacklistAdapter


class AuthService:
    def __init__(
            self,
            hasher: PasswordHasherI,
            token_provider: TokenProviderI,
            repository: UserRepositoryI,
            company_repository: CompanyRepositoryI = None,
            blacklist: TokenBlacklistAdapter = None
    ):
        self.hasher = hasher
        self.token_provider = token_provider
        self.repository = repository
        self.company_repository = company_repository
        self.blacklist = blacklist

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
            "id": str(user.id),
            "company_id": str(user.company_id),
            "role": user.role
        }

        access_token = self.token_provider.create_access_token(token_payload)

        refresh_token = self.token_provider.create_refresh_token({
            "sub": user.email,
            "id": str(user.id)
        })

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": user.role,
            "token_type": "bearer"
        }