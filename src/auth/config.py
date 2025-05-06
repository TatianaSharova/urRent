from pathlib import Path
from pydantic import BaseModel


BASE_DIR = Path(__file__).parent


class JWTAuth(BaseModel):
    '''Класс настроек JWT-аунтефикации.'''
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_min: int = 15
    refresh_token_expire_days: int = 30


auth_settings = JWTAuth()
