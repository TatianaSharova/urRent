from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column,
                            declared_attr)


class Base(DeclarativeBase):
    '''Базовая модель.'''
    __abstract__ = True

    # даём имя таблице на основе названия модели
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    id: Mapped[int] = mapped_column(primary_key=True)
