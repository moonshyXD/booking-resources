from typing import Annotated

from adapters.auth.password import PasswordHasher
from adapters.auth.token import TokenProvider
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from usecases.auth import AuthService

router = APIRouter(prefix="/auth")


def get_auth_service():
    return AuthService(hasher=PasswordHasher(), token_provider=TokenProvider())


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                 auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    token = auth_service.authenticate(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}



