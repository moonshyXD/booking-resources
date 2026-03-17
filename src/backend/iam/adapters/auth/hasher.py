from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

class PasswordHasher:
    password_hash = PasswordHash(
        hashers=[
            BcryptHasher(),
        ]
    )

    def get_password_hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        print(self.password_hash.hash(plain_password))
        return self.password_hash.verify(plain_password, hashed_password)
