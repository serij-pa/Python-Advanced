from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, String

class Base(DeclarativeBase):
    pass

class Recipes(Base): # класс рецептов
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_dish: Mapped[str] = mapped_column(String(100))   #название блюда
    cooking_time: Mapped[int] = mapped_column(default=5)  #время приготовления
    number_views: Mapped[int] = mapped_column(default=0)  #количество просмотров
    text_description: Mapped[str] = mapped_column(Text, default="Ведутся технические работы по восстановлению описания блюда.")

    used_ingredients: Mapped[List["Ingredients"]] = relationship(
        back_populates="used_in_recipe",
        secondary="ingredients_in_recipe")

    def __repr__(self):
        return f"Recipe(id={self.id}, name={self.name_dish})"


class Ingredients(Base):  # Класс, описывающий ингредиенты
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_name: Mapped[str] = mapped_column(String(100))
    ingredient_description: Mapped[str | None]

    used_in_recipe: Mapped[List["Recipes"]] = relationship(
        back_populates="used_ingredients",
        secondary="ingredients_in_recipe")

    def __repr__(self):
        return f"Recipe(id={self.id}, name={self.ingredient_name})"


class IngredientsInRecipe(Base):
    __tablename__ = "ingredients_in_recipe"

    recipes_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        primary_key=True)
    ingredients_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        primary_key=True)
    quantity: Mapped[str | None] = mapped_column(String(100))

    def __repr__(self):
        return (f"IngredientsInRecipe(recipes_id={self.recipes_id}, "
                f"ingredients_id={self.ingredients_id}, "
                f"quantity={self.quantity})")