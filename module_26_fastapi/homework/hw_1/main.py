from typing import List
import uvicorn
from fastapi import FastAPI

import models
from schemas import RecipesIn, RecipesOut, RecipesWithIngredients
from database import select_all_recipes, get_detail_recipes, add_new_recipe, add_new_data


app = FastAPI()

@app.get("/recip", response_model=List[RecipesOut])
async def get_all_recipes():
    result = await select_all_recipes()
    return result.scalars().all()


@app.get("/recip/{recipes_id}", response_model=List[RecipesWithIngredients])
async def get_recipe_details(recipes_id):
    dish_with_ingredients = await get_detail_recipes(recipes_id)
    return dish_with_ingredients


@app.post("/recip", response_model=RecipesIn)
async def add_recipe(recipe: RecipesIn):
    new_recip = models.Recipes(
        name_dish=recipe.name_dish,
        cooking_time=recipe.cooking_time,
        text_description=recipe.text_description,
    )
    ingred = recipe.ingredients
    new_rec_id = await add_new_recipe(new_recip)
    ingredients_in_recipe = [
        models.IngredientsInRecipe(
            recipes_id=new_rec_id,
            ingredients_id=i_ing.ingredients_id,
            quantity=i_ing.quantity,
        ) for i_ing in ingred
    ]
    if new_rec_id:
        await add_new_data(ingredients_in_recipe)
        return recipe


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1",
                port=8000,
                reload=True)

