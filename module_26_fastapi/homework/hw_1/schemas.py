from pydantic import BaseModel
from typing import List


class RecipesOut(BaseModel):
    id: int | None
    name_dish: str
    cooking_time: int
    number_views: int | None

    class Config:
        from_attributes = True


class IngredientsInR(BaseModel):
    ingredients_id: int
    quantity: str


class RecipesIn(BaseModel):
    name_dish: str
    cooking_time: int
    text_description: str
    ingredients: List[IngredientsInR]


class Ingredients(BaseModel):
    name: str
    description: str | None
    quantity: str | None


class RecipesWithIngredients(BaseModel):
    id: int
    name_dish: str
    cooking_time: int
    description: str
    ingredients: List[IngredientsInR]
