from notifications.domain.builder import AccountEmailBuilderI
from notifications.domain.sender import EmailSenderI


class AccountService:
    def __init__(self, repository: AccountEmailBuilderI, sender: EmailSenderI):
        self.repository = repository
        self.sender = sender

    async def send_created_account(self, email: str, password: str):
        text = self.repository.get_text_created_account(email, password)
        request = await self.sender.send_email(email, text)

        return request

    async def send_updated_password(self, email: str, password: str):
        text = self.repository.get_text_updated_password(email, password)
        request = await self.sender.send_email(email, text)

        return request

    async def send_updated_account_data(self, email: str, password: str):
        text = self.repository.get_text_updated_account_data(email, password)
        request = await self.sender.send_email(email, text)

        return request

    async def send_deleted_account(self, email: str):
        text = self.repository.get_text_deleted_account(email)
        request = await self.sender.send_email(email, text)

        return request
