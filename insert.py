from flask import Flask, request, jsonify, render_template, session, redirect, sessions, url_for
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from models import *  # import your SQLAlchemy 2.0 models
from config import Config



app = Flask(__name__)
app.config.from_object(Config)


engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=False, future=True)
Base.metadata.create_all(engine)



session = Session(engine)

# delete_stmt = delete(Customer)
session.query(PizzaIngredient).delete()
session.query(Ingredient).delete()
session.query(OrderedPizza).delete()
session.query(OrderedDessert).delete()
session.query(OrderedDrink).delete()
session.query(Drink).delete()
session.query(Dessert).delete()
session.query(Pizza).delete()
session.query(Order).delete()
session.query(DeliveryPerson).delete()
session.query(DiscountCode).delete()
session.query(Customer).delete()
session.commit()

# Customers
customers = [
    Customer(id=1, name="Alice Johnson", birthday=datetime(1990, 5, 14), address="123 Elm Street", postcode=1001),
    Customer(id=2, name="Bob Smith", birthday=datetime(1985, 8, 23), address="45 Oak Avenue", postcode=1002),
    Customer(id=3, name="Charlie Lee", birthday=datetime(2000, 11, 9), address="78 Maple Road", postcode=1003),
]

# Ingredientsinsert
ingredients = [
    Ingredient(id=1, name="Tomato Sauce", price=1, vegan=True, vegetarian=True),
    Ingredient(id=2, name="Mozzarella", price=2, vegan=False, vegetarian=True),
    Ingredient(id=3, name="Pepperoni", price=3, vegan=False, vegetarian=False),
    Ingredient(id=4, name="Bell Peppers", price=1, vegan=True, vegetarian=True),
    Ingredient(id=5, name="Onions", price=1, vegan=True, vegetarian=True),
    Ingredient(id=6, name="BBQ Sauce", price=1, vegan=True, vegetarian=True),
    Ingredient(id=7, name="Chicken", price=3, vegan=False, vegetarian=False),
    Ingredient(id=8, name="Vegan Cheese", price=2, vegan=True, vegetarian=True),
    Ingredient(id=9, name="Olives", price=1, vegan=True, vegetarian=True),
]

# Pizzas
pizzas = [
    Pizza(id=1, name="Margherita"),
    Pizza(id=2, name="Pepperoni"),
    Pizza(id=3, name="Vegetarian Delight"),
    Pizza(id=4, name="BBQ Chicken"),
]

# Attach ingredients
pizzas[0].ingredients = [ingredients[0], ingredients[1]]
pizzas[1].ingredients = [ingredients[0], ingredients[1], ingredients[2]]
pizzas[2].ingredients = [ingredients[0], ingredients[1], ingredients[3], ingredients[4], ingredients[8]]
pizzas[3].ingredients = [ingredients[5], ingredients[6], ingredients[1]]

# Dr_inks
drinks = [
    Drink(id=1, name="Coca-Cola", price=2, vegan=True, vegetarian=True),
    Drink(id=2, name="Water", price=1, vegan=True, vegetarian=True),
]

# Desserts
desserts = [
    Dessert(id=1, name="Chocolate Cake", price=5, vegan=False, vegetarian=True),
    Dessert(id=2, name="Vegan Brownie", price=4, vegan=True, vegetarian=True),
]

# Discounts
discounts = [
    DiscountCode(id=1, code="WELCOME10", type="percentage", amount=10),
    DiscountCode(id=2, code="PIZZA20", type="percentage", amount=20),
]

# Delivery Personnel
delivery = [
    DeliveryPerson(id=1, postcode_start=1000, postcode_end=1002, status="available"),
    DeliveryPerson(id=2, postcode_start=1003, postcode_end=1005, status="available"),
]

# Orders
orders = [
    Order(id=1, customer_id=1, delivery_person_id=1, status="delivered", discount_id=1, timestamp=datetime(2025, 10, 18, 18, 45)),
    Order(id=2, customer_id=2, delivery_person_id=1, status="prepar_ing", discount_id=None, timestamp=datetime(2025, 10, 19, 19, 10)),
]

# Attach items to orders
orders[0].pizzas = [pizzas[1], pizzas[0]]
orders[0].drinks = [drinks[0]]
orders[0].desserts = [desserts[0]]

orders[1].pizzas = [pizzas[2]]
orders[1].drinks = [drinks[1]]
orders[1].desserts = [desserts[1]]

ordered_pizza = [
    OrderedPizza(order_id=1, pizza_id=2),
    OrderedPizza(order_id=1, pizza_id=1),
]

ordered_drink = [
    OrderedDrink(order_id=1, drink_id=1),
    OrderedDrink(order_id=2, drink_id=2),
]

ordered_dessert = [
    OrderedDessert(order_id=1, dessert_id=1),
]

# Add everything
session.add_all(customers + ingredients + pizzas + drinks + desserts + discounts + delivery + orders)
session.commit()

session.add_all(ordered_pizza + ordered_drink + ordered_dessert)
session.commit()
