from pathlib import Path
from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent


class JWTAuth(BaseModel):
    '''Класс настроек JWT-аунтефикации.'''
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt_private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt_public.pem'
    algorithm: str = 'RS256'


auth_settings = JWTAuth()
