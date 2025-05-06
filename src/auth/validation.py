from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from auth.helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from auth import utils as auth_utils
from auth.schemas import UserAuth

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/jwt/login/",
)

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


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    '''
    Проверяем токен пользователя
    и получаем payload из токена.
    .'''
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    '''
    Проверяем тип токена, передаваемый в payload.

    Если тип токена не совпадает с ожидаемым,
    то выбрасываем ошибку.
    '''
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=(f"invalid token type {current_token_type!r} "
                f"expected {token_type!r}"),
    )


def get_user_by_token_sub(payload: dict) -> UserAuth:
    '''
    Получаем аутентифицированного юзера
    по его username (sub) из payload токена.
    '''
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


class UserGetterFromToken:
    '''Класс получения юзера по токену.'''
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
    ):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user(
    user: UserAuth = Depends(get_current_auth_user),
):
    '''Проверка активности юзера.'''
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    '''
    Проверка существования юзера в бд,
    и его вводимых данных(пароля).
    '''
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user
