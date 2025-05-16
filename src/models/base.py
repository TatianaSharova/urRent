from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from config import settings


class Base(DeclarativeBase):
    """Базовая модель."""

    __abstract__ = True

    metadata = MetaData(
        namiing_convention=settings.db.naming_convention,
    )

    # даём имя таблице на основе названия модели
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
