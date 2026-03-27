from shared.auth.dependencies import setup_auth_dependencies
from shared.auth.role import RoleChecker
from catalog.domain.models.user_role import UserRole
from catalog.adapters.config.settings import Config
from catalog.adapters.dependencies.general import redis_dep

config = Config.load()

get_current_user_payload, get_blacklist_adapter = setup_auth_dependencies(
    secret_key=config.jwt.secret_key.get_secret_value(),
    algorithm=config.jwt.algorithm.get_secret_value(),
    get_redis_session_func=redis_dep.get_redis_session
)

require_admin = RoleChecker(
    [UserRole.ADMIN],
    user_getter=get_current_user_payload
)

require_company_admin = RoleChecker(
    [UserRole.COMPANY_ADMIN],
    user_getter=get_current_user_payload
)
