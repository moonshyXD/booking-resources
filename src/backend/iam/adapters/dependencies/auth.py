from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from iam.adapters.auth.hasher import PasswordHasher
from iam.adapters.auth.token import TokenProvider
from iam.usecases.auth import AuthService
from iam.repository.orm.user import UserRepositoryPostgres
from iam.repository.orm.company import CompanyRepositoryPostgres

from shared.auth.blacklist import TokenBlacklistAdapter
from shared.auth.dependencies import setup_auth_dependencies
from shared.auth.role import RoleChecker
from iam.domain.models.user_role import UserRole

from iam.adapters.config.settings import Config
from iam.adapters.dependencies.general import redis_dep, get_db_session

config = Config.load()

get_current_user_payload, get_blacklist_adapter = setup_auth_dependencies(
    secret_key=config.jwt.secret_key.get_secret_value(),
    algorithm=config.jwt.algorithm.get_secret_value(),
    get_redis_session_func=redis_dep.get_redis_session
)

def get_auth_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    blacklist: Annotated[TokenBlacklistAdapter, Depends(get_blacklist_adapter)]
) -> AuthService:
    return AuthService(
        hasher=PasswordHasher(),
        token_provider=TokenProvider(
            secret_key=config.jwt.secret_key.get_secret_value(),
            algorithm=config.jwt.algorithm.get_secret_value(),
            expires_in=config.jwt.expires_in
        ),
        repository=UserRepositoryPostgres(session),
        company_repository=CompanyRepositoryPostgres(session),
        blacklist=blacklist
    )

require_admin = RoleChecker(
    [UserRole.ADMIN],
    user_getter=get_current_user_payload
)

require_admin_or_company_admin = RoleChecker(
    [UserRole.ADMIN, UserRole.COMPANY_ADMIN],
    user_getter=get_current_user_payload
)