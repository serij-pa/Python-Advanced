import asyncio
from models import Recipes, Ingredients, IngredientsInRecipe, Base
from database import engine, add_new_data
several_recipes = [

    Recipes(
        name_dish="Блины молочные",
        cooking_time=30,
        text_description="""
        Тесто лучше и быстрее размешается, если все продукты будут комнатной 
        температуры, поэтому выньте яйца и молоко из холодильника заранее. 
        Если вы не успели этого сделать, то молоко подогрейте в микроволновке, 
        а яйца опустите в теплую воду.

        Хорошо помытые и обсушенные яйца вбейте в глубокую миску. Обязательно 
        мойте яйца перед использованием, так как даже на кажущейся чистой 
        скорлупе могут находиться вредные бактерии. Лучше всего использовать 
        моющие средства для пищевых продуктов и щетку. Добавьте к яйцам сахар 
        и соль. Их количество регулируйте по своему вкусу, сахар, как по мне, 
        можно уменьшить.

        Перемешайте тесто. С небольшим количеством молока оно получится очень 
        густым, так и надо — тесто такой консистенции легче размешать до 
        однородности. Именно за счет этого в нем не будет комочков.
    """,
    ),
    Recipes(
        name_dish="Блины овсяные",
        cooking_time=25,
        text_description="any description",
    ),
    Recipes(name_dish="Блины постные", cooking_time=20),
]

several_ingredients = [
    Ingredients(ingredient_name="Мука пшеничная", ingredient_description="высший сорт"),
    Ingredients(ingredient_name="Мука овсяная"),
    Ingredients(ingredient_name="Мука ржаная", ingredient_description="любая"),
    Ingredients(ingredient_name="Соль"),
    Ingredients(ingredient_name="Сахар"),
    Ingredients(ingredient_name="Яйцо куриное", ingredient_description="0 категории"),
    Ingredients(ingredient_name="Яйцо перепелиное"),
    Ingredients(ingredient_name="Масло подсолнечное"),
    Ingredients(ingredient_name="Масло сливочное"),
    Ingredients(ingredient_name="Молоко"),
    Ingredients(ingredient_name="Вода"),
]

relationship_ingredients_to_recipes = [
    IngredientsInRecipe(recipes_id=1, ingredients_id=1, quantity="3 стакана"),
    IngredientsInRecipe(recipes_id=1, ingredients_id=10, quantity="500 миллилитров"),
    IngredientsInRecipe(recipes_id=1, ingredients_id=4, quantity="1/2 чайных ложки"),
    IngredientsInRecipe(recipes_id=1, ingredients_id=5, quantity="2 чайных ложки"),
    IngredientsInRecipe(recipes_id=1, ingredients_id=8, quantity="50 миллилитров"),
    IngredientsInRecipe(recipes_id=1, ingredients_id=7, quantity="2 штуки"),
    IngredientsInRecipe(recipes_id=2, ingredients_id=2, quantity="4 стакана"),
    IngredientsInRecipe(recipes_id=2, ingredients_id=10, quantity="1 литр"),
    IngredientsInRecipe(recipes_id=2, ingredients_id=4, quantity="1/2 чайной ложки"),
    IngredientsInRecipe(recipes_id=2, ingredients_id=5, quantity="2 чайных ложки"),
    IngredientsInRecipe(recipes_id=2, ingredients_id=9, quantity="100 грамм"),
    IngredientsInRecipe(recipes_id=3, ingredients_id=3, quantity="5 стаканов"),
    IngredientsInRecipe(recipes_id=3, ingredients_id=11, quantity="700 миллилитров"),
    IngredientsInRecipe(recipes_id=3, ingredients_id=4, quantity="1/2 чайной ложки"),
    IngredientsInRecipe(recipes_id=3, ingredients_id=5, quantity="1 чайная ложка"),
    IngredientsInRecipe(recipes_id=3, ingredients_id=8, quantity="3 столовых ложки"),
]


async def async_main():
    async with engine.begin() as conn:
        # предварительно очищаем все таблицы
        await conn.run_sync(Base.metadata.drop_all)
        # создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)
    # Вставка рецептов
    await add_new_data(several_recipes)
    # Вставка ингредиентов
    await add_new_data(several_ingredients)
    # Связь рецептов с ингредиентами
    await add_new_data(relationship_ingredients_to_recipes)
    await engine.dispose()

asyncio.run(async_main())