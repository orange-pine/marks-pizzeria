from cmath import pi
from datetime import datetime
from sqlalchemy import select
from config import Config
import app
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


def calculate_pizza_price(price) -> float:
     return round((Config.PIZZA_BASE_PRICE + price) * Config.MARGIN * Config.VAT, 2)

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
        if delivery_people.first() == None:
            return None

        # return delivery_people.
        for person in delivery_people:
            if datetime.now() > person.unavailable_before:
                return person.id


