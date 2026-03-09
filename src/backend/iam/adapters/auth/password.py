from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

password_hash = PasswordHash(
    hashers=[
        BcryptHasher(),
    ]
)


class PasswordHasher:
    def get_password_hash(self, password: str) -> str:
        return password_hash.hash(password)

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        print(password_hash.hash(plain_password))
        return password_hash.verify(plain_password, hashed_password)
