from domain.auth.hasher import PasswordHasherI
from domain.auth.token import TokenProviderI

FAKE_DB = {
    "admin": "$2b$12$.xjr2qgyDdy/t7z.ooCHyexXPb6a8bkue3HyzhuqB9r00i3qLD0xG"
}


class AuthService:
    def __init__(
        self, hasher: PasswordHasherI, token_provider: TokenProviderI
    ):
        self.hasher = hasher
        self.token_provider = token_provider

    def authenticate(self, username: str, password: str) -> str | None:
        # user_id = get_id_by_username(username)
        # if user_id is None:
        #   raise NOT_FOUND_USER
        # user = get_user_by_id(user_id)
        # hashed_user_password = get_password_by_id(user_id)
        # hashed_given_password = hash_password(password)
        # if hashed_user_password != hash_given_password:
        #   raise INCORRECT_PASSWORD

        hashed_password = FAKE_DB.get(username)
        print(self.hasher.verify_password(password, hashed_password))
        if not hashed_password or not self.hasher.verify_password(
            password, hashed_password
        ):
            return None

        return self.token_provider.create_access_token({"sub": username})
