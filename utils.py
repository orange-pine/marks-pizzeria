from cmath import pi
from datetime import datetime
from sqlalchemy import select
from config import Config
import app
from insert import desserts, drinks
from models import DeliveryPerson, Dessert, Drink, OrderedDessert, OrderedDrink, OrderedPizza, Pizza, Customer

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

def get_drinks():
    drinks_dicts = []
    with app.db_session() as session:
        for drink in session.scalars(select(Drink)):
            drinks_dicts.append({
                "id": drink.id,
                "name": drink.name,
                # "description": get_description(0, pizza.id),
                # "ingredients" : pizza.ingredients,
                "price": calculate_other_price(drink.price),
                "vegetarian" : drink.vegetarian,
                "vegan" : drink.vegan
                # "image": get_image(0, pizza.id) or "/static/images/default-pizza.jpg",
            })

    return desserts_dicts

def get_desserts():
    desserts_dicts = []
    with app.db_session() as session:
        for dessert in session.scalars(select(Dessert)):
            desserts_dicts.append({
                "id": dessert.id,
                "name": dessert.name,
                # "description": get_description(0, pizza.id),
                # "ingredients" : pizza.ingredients,
                "price": calculate_other_price(dessert.price),
                "vegetarian" : dessert.vegetarian,
                "vegan" : dessert.vegan
                # "image": get_image(0, pizza.id) or "/static/images/default-pizza.jpg",
            })

    return desserts_dicts



def calculate_pizza_price(price) -> float:
     return round((Config.PIZZA_BASE_PRICE + price) * Config.MARGIN * Config.VAT, 2)

def calculate_other_price(price) -> float:
     return round((price) * Config.MARGIN * Config.VAT, 2)

def get_customer_by_name(name):
    with app.db_session() as session:
        db_customer = session.execute(select(Customer).where(Customer.name == name))
        return db_customer.first()

def cart_to_items(cart, current_order_id):
    pizzas = []
    drinks = []
    desserts = []
    for item in cart:
        if item["type"] == "pizza":
            pizzas.append(OrderedPizza(order_id=current_order_id, pizza_id=item["id"]))
        elif item.type == "drink":
            pizzas.append(OrderedDrink(order_id=current_order_id, name=item["id"]))
        else:
            pizzas.append(OrderedDessert(order_id=current_order_id, name=item["id"]))

    return (pizzas, drinks, desserts)

def get_delivery_person(postcode):
    with app.db_session() as session:
        delivery_people = session.scalars(select(DeliveryPerson)
                                         .where(DeliveryPerson.postcode_start <= postcode)
                                         .where(DeliveryPerson.postcode_end >= postcode))

        for person in delivery_people:
            if datetime.now() > person.unavailable_before:
                return person.id

        return None


