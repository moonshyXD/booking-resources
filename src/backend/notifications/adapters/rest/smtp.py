from fastapi import APIRouter, Depends
from notifications.usecases.account import AccountService
from typing import Annotated

from notifications.adapters.email.builder import AccountEmailBuilder
from notifications.adapters.email.sender import EmailSender
from notifications.adapters.config.settings import Config

router = APIRouter(prefix="/account", tags=["account"])

config = Config.load()

def get_account_creating_service():
    return AccountService(repository=AccountEmailBuilder(), sender=EmailSender(config.smtp))


@router.post("/v1/send-created-account")
async def send_created_account(service: Annotated[AccountService, Depends(get_account_creating_service)], email: str, password: str):
    request = await service.send_created_account(email, password)

    return {"message": str(request)}


@router.post("/v1/send-updated-password")
async def send_updated_password(service: Annotated[AccountService, Depends(get_account_creating_service)], email: str, password: str):
    request = await service.send_updated_password(email, password)

    return {"message": "Сообщение отправлено"}

@router.post("/v1/send-updated-account")
async def send_updated_account(service: Annotated[AccountService, Depends(get_account_creating_service)], email: str, password: str):
    request = await service.send_updated_account(email, password)

    return {"message": "Сообщение отправлено"}

@router.post("/v1/send-deleted-account")
async def send_deleted_account(service: Annotated[AccountService, Depends(get_account_creating_service)], email: str):
    request = await service.send_deleted_account(email)

    return {"message": "Сообщение отправлено"}

