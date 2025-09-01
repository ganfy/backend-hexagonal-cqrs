from fastapi import APIRouter, Depends

from src.contexts.auth.application.login_use_case import LoginUseCase
from src.contexts.auth.domain.auth_token import AuthToken
from src.contexts.auth.domain.login import Login
from src.contexts.auth.infrastructure.auth_dependencies import get_login_use_case

router = APIRouter()


@router.post("/login", response_model=AuthToken)
async def login(
    command: Login,
    use_case: LoginUseCase = Depends(get_login_use_case),
):
    return await use_case.execute(command)
