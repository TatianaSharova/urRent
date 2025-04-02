import jwt

from .config import auth_settings


def encode_jwt(
       payload: dict,
       private_key: str = auth_settings.private_key_path.read_text(),
       algorithm: str = auth_settings.algorithm
):
    '''Зашифровывает jwt-токен.'''
    encoded = jwt.encode(
        payload,
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
        algorithm=[algorithm]
    )
    return decoded
