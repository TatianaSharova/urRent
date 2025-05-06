from fastapi import (
    APIRouter,
    Depends
)
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from auth.schemas import UserAuth, TokenInfo
from auth.helpers import create_access_token, create_refresh_token
from auth.validation import (get_current_auth_user_for_refresh,
                             validate_auth_user,
                             get_current_active_auth_user,
                             get_current_token_payload)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/jwt/login/",
)

http_bearer = HTTPBearer(auto_error=False)


auth_jwt_router = APIRouter(prefix="/jwt", tags=["JWT"],
                            dependencies=[Depends(http_bearer)])


@auth_jwt_router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserAuth = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@auth_jwt_router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def auth_refresh_jwt(
    user: UserAuth = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


@auth_jwt_router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserAuth = Depends(get_current_active_auth_user),
):
    '''Получение информации о текущем юзере.'''
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
