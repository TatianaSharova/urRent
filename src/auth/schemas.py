from pydantic import BaseModel, ConfigDict, EmailStr


class UserAuth(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
