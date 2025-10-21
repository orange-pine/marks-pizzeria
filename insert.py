from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import *
from config import Config


app = Flask(__name__)
app.config.from_object(Config)


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False, future=True)
Base.metadata.create_all(engine)

session = Session(engine)

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
    Customer(id=4, name="Diana Brooks", birthday=datetime(1995, 3, 3), address="56 Pine Street", postcode=1004),
    Customer(id=5, name="Ethan Clarke", birthday=datetime(1988, 7, 29), address="89 Birch Lane", postcode=1005),
    Customer(id=6, name="Fiona Patel", birthday=datetime(1992, 12, 12), address="21 Cedar Crescent", postcode=1003),
    Customer(id=7, name="George Martinez", birthday=datetime(1979, 9, 2), address="99 Willow Way", postcode=1001),
    Customer(id=8, name="Hannah Wright", birthday=datetime(1998, 6, 25), address="12 Spruce Boulevard", postcode=1006),
    Customer(id=9, name="Ian Thompson", birthday=datetime(1983, 4, 2), address="34 Aspen Avenue", postcode=1007),
    Customer(id=10, name="Julia Kim", birthday=datetime(1997, 10, 1), address="67 Cypress Street", postcode=1008),
    Customer(id=11, name="Kevin Nguyen", birthday=datetime(1991, 11, 19), address="90 Redwood Lane", postcode=1009),
    Customer(id=12, name="Laura Rossi", birthday=datetime(1986, 1, 5), address="22 Alder Road", postcode=1004),
]

# Ingredients
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
    Ingredient(id=10, name="Mushrooms", price=1, vegan=True, vegetarian=True),
    Ingredient(id=11, name="Ham", price=3, vegan=False, vegetarian=False),
    Ingredient(id=12, name="Pineapple", price=1, vegan=True, vegetarian=True),
    Ingredient(id=13, name="Spinach", price=1, vegan=True, vegetarian=True),
    Ingredient(id=14, name="Garlic Sauce", price=1, vegan=True, vegetarian=True),
    Ingredient(id=15, name="Parmesan", price=2, vegan=False, vegetarian=True),
    Ingredient(id=16, name="Basil", price=1, vegan=True, vegetarian=True),
    Ingredient(id=17, name="Prosciutto", price=3, vegan=False, vegetarian=False),
    Ingredient(id=18, name="Truffle Oil", price=2, vegan=True, vegetarian=True),
    Ingredient(id=19, name="Jalapeños", price=1, vegan=True, vegetarian=True),
    Ingredient(id=20, name="Sweetcorn", price=1, vegan=True, vegetarian=True),
]

# Pizzas
pizzas = [
    Pizza(id=1, name="Margherita"),
    Pizza(id=2, name="Pepperoni"),
    Pizza(id=3, name="Vegetarian Delight"),
    Pizza(id=4, name="BBQ Chicken"),
    Pizza(id=5, name="Hawaiian"),
    Pizza(id=6, name="Vegan Paradise"),
    Pizza(id=7, name="Garlic Spinach"),
    Pizza(id=8, name="Truffle Special"),
    Pizza(id=9, name="Hot Jalapeño"),
    Pizza(id=10, name="Sweetcorn Supreme"),
]

# Attach ingredients
pizzas[0].ingredients = [ingredients[0], ingredients[1]]
pizzas[1].ingredients = [ingredients[0], ingredients[1], ingredients[2]]
pizzas[2].ingredients = [ingredients[0], ingredients[1], ingredients[3], ingredients[4], ingredients[8]]
pizzas[3].ingredients = [ingredients[5], ingredients[6], ingredients[1]]
pizzas[4].ingredients = [ingredients[0], ingredients[1], ingredients[11], ingredients[12]]
pizzas[5].ingredients = [ingredients[0], ingredients[7], ingredients[3], ingredients[4], ingredients[8]]
pizzas[6].ingredients = [ingredients[0], ingredients[13], ingredients[14], ingredients[1]]
pizzas[7].ingredients = [ingredients[0], ingredients[1], ingredients[17], ingredients[15]]
pizzas[8].ingredients = [ingredients[0], ingredients[1], ingredients[18], ingredients[2]]
pizzas[9].ingredients = [ingredients[0], ingredients[1], ingredients[19], ingredients[3], ingredients[4]]

# Drinks
drinks = [
    Drink(id=1, name="Coca-Cola", price=2, vegan=True, vegetarian=True),
    Drink(id=2, name="Water", price=1, vegan=True, vegetarian=True),
    Drink(id=3, name="Lemonade", price=2, vegan=True, vegetarian=True),
    Drink(id=4, name="Iced Tea", price=2, vegan=True, vegetarian=True),
]

# Desserts
desserts = [
    Dessert(id=1, name="Chocolate Cake", price=5, vegan=False, vegetarian=True),
    Dessert(id=2, name="Vegan Brownie", price=4, vegan=True, vegetarian=True),
    Dessert(id=3, name="Tiramisu", price=6, vegan=False, vegetarian=True),
    Dessert(id=4, name="Fruit Salad", price=4, vegan=True, vegetarian=True)
]

# Discounts
discounts = [
    DiscountCode(id=1, code="WELCOME10", type="percentage", amount=10),
    DiscountCode(id=2, code="PIZZA20", type="percentage", amount=20),
    DiscountCode(id=3, code="FREEDRINK", type="fixed", amount=2),
    DiscountCode(id=4, code="WEEKEND15", type="percentage", amount=15),
]

# Delivery Personnel
delivery = [
    DeliveryPerson(id=1, postcode_start=1000, postcode_end=1002, unavailable_before=datetime(2025, 10, 18, 18, 45)),
    DeliveryPerson(id=2, postcode_start=1003, postcode_end=1005, unavailable_before=datetime(2025, 10, 18, 18, 45)),
    DeliveryPerson(id=3, postcode_start=1006, postcode_end=1009, unavailable_before=datetime(2025, 10, 18, 18, 45)),
    DeliveryPerson(id=4, postcode_start=1000, postcode_end=1005, unavailable_before=datetime(2025, 10, 18, 18, 45)),
]

# Orders
orders = [
    Order(id=1, customer_id=1, delivery_person_id=1, status="delivered", discount_id=1, timestamp=datetime(2025, 10, 18, 18, 45)),
    Order(id=2, customer_id=2, delivery_person_id=1, status="preparing", discount_id=None, timestamp=datetime(2025, 10, 19, 19, 10)),
    Order(id=3, customer_id=3, delivery_person_id=2, status="delivered", discount_id=2, timestamp=datetime(2025, 10, 20, 17, 30)),
    Order(id=4, customer_id=4, delivery_person_id=2, status="preparing", discount_id=4, timestamp=datetime(2025, 10, 21, 18, 10)),
    Order(id=5, customer_id=5, delivery_person_id=3, status="delivered", discount_id=None, timestamp=datetime(2025, 10, 19, 20, 45)),
    Order(id=6, customer_id=6, delivery_person_id=1, status="pending", discount_id=3, timestamp=datetime(2025, 10, 21, 19, 5)),
    Order(id=7, customer_id=7, delivery_person_id=1, status="delivered", discount_id=None, timestamp=datetime(2025, 10, 18, 21, 0)),
]

ordered_pizza = [
    OrderedPizza(order_id=1, pizza_id=2),
    OrderedPizza(order_id=1, pizza_id=1),
    OrderedPizza(order_id=2, pizza_id=10),
    OrderedPizza(order_id=3, pizza_id=5),
    OrderedPizza(order_id=3, pizza_id=9),
    OrderedPizza(order_id=4, pizza_id=7),
    OrderedPizza(order_id=4, pizza_id=1),
    OrderedPizza(order_id=5, pizza_id=6),
    OrderedPizza(order_id=6, pizza_id=3),
    OrderedPizza(order_id=6, pizza_id=5),
    OrderedPizza(order_id=7, pizza_id=2),
    OrderedPizza(order_id=7, pizza_id=5),
    OrderedPizza(order_id=4, pizza_id=10),
    OrderedPizza(order_id=1, pizza_id=8),
    OrderedPizza(order_id=3, pizza_id=2),
    OrderedPizza(order_id=1, pizza_id=9),
]

ordered_drink = [
    OrderedDrink(order_id=1, drink_id=1),
    OrderedDrink(order_id=2, drink_id=2),
    OrderedDrink(order_id=3, drink_id=3),
    OrderedDrink(order_id=4, drink_id=4),
    OrderedDrink(order_id=5, drink_id=1),
    OrderedDrink(order_id=5, drink_id=2),
    OrderedDrink(order_id=6, drink_id=4),
    OrderedDrink(order_id=7, drink_id=3),
]

ordered_dessert = [
    OrderedDessert(order_id=1, dessert_id=1),
    OrderedDessert(order_id=3, dessert_id=3),
    OrderedDessert(order_id=4, dessert_id=4),
    OrderedDessert(order_id=5, dessert_id=2),
]

# Add everything
session.add_all(customers + ingredients + pizzas + drinks + desserts + discounts + delivery + orders)
session.commit()

session.add_all(ordered_pizza + ordered_drink + ordered_dessert)
session.commit()
