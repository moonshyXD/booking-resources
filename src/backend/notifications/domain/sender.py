from typing import Protocol

class EmailSenderI(Protocol):
    async def send_email(self, email: str, message: str): ...
