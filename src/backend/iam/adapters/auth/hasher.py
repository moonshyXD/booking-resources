from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from random import choice
from string import ascii_letters, digits

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
        return self.password_hash.verify(plain_password, hashed_password)

    def get_password(self) -> str:
        password = ""
        for i in range(64):
            password += choice(ascii_letters + digits)

        return password

