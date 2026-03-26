from notifications.usecases.account import AccountService


class AccountEventHandlers:
    def __init__(self, account_service: AccountService):
        self.account_service = account_service

    async def on_account_created(self, payload: dict):
        email = payload.get("email")
        password = payload.get("password")
        if not email or not password:
            return None

        return await self.account_service.send_created_account(email, password)

    async def on_password_updated(self, payload: dict):
        email = payload.get("email")
        password = payload.get("password")
        if not email or not password:
            return None

        return await self.account_service.send_updated_password(email, password)

    async def on_account_deleted(self, payload: dict):
        email = payload.get("email")
        if not email:
            return None

        return await self.account_service.send_deleted_account(email)

    async def on_account_data_updated(self, payload: dict):
        email = payload.get("email")
        if not email:
            return None

        return await self.account_service.send_updated_account_data(email)