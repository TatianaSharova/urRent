from datetime import timedelta

from auth import utils as auth_utils


from auth.config import auth_settings
from auth.schemas import UserAuth


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = auth_settings.access_token_expire_min,
    expire_timedelta: timedelta | None = None,
) -> str:
    """
    Создание jwt-токена,
    в зависимости от token_type - access или refresh.
    """
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_min=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserAuth) -> str:
    """Создание access-токена."""
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=auth_settings.access_token_expire_min,
    )


def create_refresh_token(user: UserAuth) -> str:
    """Создание refresh-токена."""
    jwt_payload = {"sub": user.username}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=auth_settings.refresh_token_expire_days),
    )
