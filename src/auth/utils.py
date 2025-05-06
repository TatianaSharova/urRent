import uuid
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

from auth.config import auth_settings


def encode_jwt(
       payload: dict,
       private_key: str = auth_settings.private_key_path.read_text(),
       algorithm: str = auth_settings.algorithm,
       expire_min: int = auth_settings.access_token_expire_min,
       expire_timedelta: timedelta | None = None
):
    '''Зашифровывает jwt-токен.'''
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_min)

    to_encode.update(exp=expire, iat=now, jti=str(uuid.uuid4()))

    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm
    )
    return encoded


def decode_jwt(
       token: str | bytes,
       pub_key: str = auth_settings.public_key_path.read_text(),
       algorithm: str = auth_settings.algorithm
):
    '''Расшифровывает jwt-токен.'''
    decoded = jwt.decode(
        token,
        pub_key,
        algorithms=[algorithm]
    )
    return decoded


def hash_password(password: str) -> bytes:
    '''Хеширует пароль.'''
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str,
                      hashed_password: bytes) -> bool:
    '''Проверяет пароль на соответствие.'''
    return bcrypt.checkpw(password.encode(), hashed_password)
