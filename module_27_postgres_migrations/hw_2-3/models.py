from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from typing import Dict, Any

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

class Coffee(Base):
    __tablename__ = 'coffee'

    title: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(200), nullable=True)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    reviews: Mapped[str] = mapped_column(ARRAY(String), nullable=True)
    user: Mapped["User"] = relationship(back_populates="coffee")

    def __repr__(self):
        return (f"Coffee(id={self.id}, title={self.title}, "
                f"category={self.category}, description={self.description}, reviews={self.reviews})")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str | None] = mapped_column(String(100))
    patronymic: Mapped[str | None] = mapped_column(String(100))
    has_sale: Mapped[bool | None]
    address: Mapped[JSON] = mapped_column(JSON)
    coffee_id: Mapped[int] = mapped_column(ForeignKey("coffee.id", ))
    coffee: Mapped["Coffee"] = relationship(back_populates="user", lazy="selectin")

    def __repr__(self):
        return (f"User(id={self.id}, name={self.name}, has_sale={self.has_sale}, address={self.address},"
                f"coffee_id={self.coffee_id})")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
