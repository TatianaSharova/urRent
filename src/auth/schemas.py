from pydantic import BaseModel, ConfigDict, EmailStr, ConfigDict


class UserAuth(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
