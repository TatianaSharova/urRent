from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer

from auth import utils as auth_utils
from .schemas import UserAuth, TokenInfo

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login/",
)


auth_jwt_router = APIRouter(prefix="/jwt", tags=["JWT"])

john = UserAuth(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)
sam = UserAuth(
    username="sam",
    password=auth_utils.hash_password("secret"),
)

users_db: dict[str, UserAuth] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    '''Проверяем существует ли пользователь и активен ли он.'''
    if not (user := users_db.get(username)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    '''Проверяем токен пользователя.'''
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}"
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserAuth:
    '''Получаем аутентифицированного юзера.'''
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_active_auth_user(
    user: UserAuth = Depends(get_current_auth_user),
):
    '''Получаем аутентифицированного активного юзера.'''
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


@auth_jwt_router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserAuth = Depends(validate_auth_user),
):
    '''Получение токена для юзера.'''
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@auth_jwt_router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserAuth = Depends(get_current_active_auth_user),
):
    '''Получение инфы о юзере.'''
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
