import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from models import Recipes, Ingredients, IngredientsInRecipe

engine = create_async_engine("sqlite+aiosqlite:///./app.db")
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def select_all_recipes():
    """получения всех рецептов
        сортировка по просмотрам или времени готовки
        - Название рецепта.
        - Время приготовления.
        - Количество просмотров.
        :return: Список рецептов
    """
    async with async_session() as session:
        res = select(Recipes).order_by(-Recipes.number_views, Recipes.cooking_time)
        result = await session.execute(res)
        return result


async def get_detail_recipes(id_recipes: int):
    """получениу инф о рецепте:
        - id
        - Название рецепта.
        - Время приготовления.
        - Список ингредиентов.
        - Текстовое описание.
        :param id_recipes: Id рецепта, который хотим посмотреть.
        :return:
    """
    async with async_session() as session:
        result_1 = await session.execute(select(Recipes).filter(Recipes.id == id_recipes))
        result_2 = await session.execute(select(
            IngredientsInRecipe.quantity,
            Ingredients.ingredient_name,
            Ingredients.ingredient_description,)
            .join(Ingredients, Ingredients.id == IngredientsInRecipe.ingredients_id)
            .where(IngredientsInRecipe.recipes_id == id_recipes))

        recipe = result_1.scalars().one()
        ingredient = result_2.fetchall()

        recipe.number_views += 1
        await session.commit()

        dish_with_ingredients = [
            {"id": recipe.id,
             "name_dish": recipe.name_dish,
             "cooking_time": recipe.cooking_time,
             "description": recipe.text_description,
             "ingredients": [
                 {"name": i_ing.ingredient_name,
                  "description": i_ing.ingredient_description,
                  "quantity": i_ing.quantity,} for i_ing in ingredient
             ],
             },
        ]
        return dish_with_ingredients


async def add_new_data(*objs):
    """Добавляем новый рецепт с ингредиентами
    или связей рецептов с ингредиентами.
    :param objs: Список объектов (Recipe, Ingredients или IngredientsInRecipe)
    :return: None
    """
    async with async_session() as session:
        async with session.begin():
            session.add_all(*objs)



async def add_new_recipe(new_recipes):
    """Cоздаем новый рецепт. Принимает объект
    и возвращает id рецепта
    :param new_recipes:
    :return: recipe_id
    """
    async with async_session() as session:
        async with session.begin():
            session.add(new_recipes)
            await session.commit()
            return new_recipes.id