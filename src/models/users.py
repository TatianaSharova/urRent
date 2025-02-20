from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey, String, func

from .base import Base

class User(Base):
    '''Модель для пользователя.'''

    username: Mapped[str] = mapped_column(String(40), unique=True,
                                          nullable=False)
    first_name: Mapped[str] = mapped_column(String(40), nullable=False)
    last_name: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(40), unique=True,
                                       nullable=False)
    date_joined: Mapped[DateTime] = mapped_column(DateTime,
                                                  default=func.now())

    def __repr__(self) -> str:
        return self.username