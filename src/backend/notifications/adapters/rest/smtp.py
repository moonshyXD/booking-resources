from fastapi import APIRouter, Depends, HTTPException
from usecases.account import AccountCreatingService


router = APIRouter()

def get_account_creating_service(service: AccountCreatingService):
    pass


# @router.get("/send-email")
# async def send_email(email: str, password: str, Depends(get_account_creating_service)):
#     pass
