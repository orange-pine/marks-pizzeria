from cmath import pi
from sqlalchemy import select
from config import Config
import app
from models import Pizza

def get_pizzas():
    pizza_dicts = []
    with app.db_session() as session:
        for pizza in session.scalars(select(Pizza)):
            pizza_dicts.append({
                "id": pizza.id,
                "name": pizza.name,
                # "description": get_description(0, pizza.id),
                "ingredients" : pizza.ingredients,
                "price": calculate_pizza_price(pizza.price),
                "vegetarian" : pizza.vegetarian,
                "vegan" : pizza.vegan
                # "image": get_image(0, pizza.id) or "/static/images/default-pizza.jpg",
            })

    return pizza_dicts


def calculate_pizza_price(price) -> float:
     return round((Config.PIZZA_BASE_PRICE + price) * Config.MARGIN * Config.VAT, 2)
