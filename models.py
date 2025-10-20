
from ast import In
from datetime import date, datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    Table
)
from sqlalchemy.orm import relationship, declarative_base, Mapped

Base = declarative_base()

PizzaIngredient = Table(
    'PizzaIngredient',
    Base.metadata,
    Column('pizza_id', Integer, ForeignKey('Pizza.id')),
    Column('ingredient_id', Integer, ForeignKey('Ingredient.id'))
    )

class Ingredient(Base):
    __tablename__ = "Ingredient"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(Integer)
    vegan = Column(Boolean)
    vegetarian = Column(Boolean)


class Pizza(Base):
    __tablename__ = "Pizza"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    ingredients: Mapped[list[Ingredient]] = relationship(
        secondary=PizzaIngredient    )
    # ordered_pizzas = relationship("OrderedPizza", back_populates="pizza")

    # Calculate price dynamically from ingredient prices
    @property
    def price(self):
        """Compute total price based on the sum of ingredient prices."""
        if not self.ingredients:
            return 0
        return sum(ingredient.price for ingredient in self.ingredients)



class Drink(Base):
    __tablename__ = "Drink"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(Integer)
    vegan = Column(Boolean)
    vegetarian = Column(Boolean)

    # ordered_drinks = relationship("OrderedDrink", back_populates="drink")


class Dessert(Base):
    __tablename__ = "Dessert"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(Integer)
    vegan = Column(Boolean)
    vegetarian = Column(Boolean)

    # ordered_desserts = relationship("OrderedDessert", back_populates="dessert")


class DiscountCode(Base):
    __tablename__ = "DiscountCode"

    id = Column(Integer, primary_key=True)
    code = Column(String(255))
    type = Column(String(255))
    amount = Column(Integer)

    # orders = relationship("Order", back_populates="discount")


class DeliveryPerson(Base):
    __tablename__ = "DeliveryPerson"

    id = Column(Integer, primary_key=True)
    postcode_start = Column(Integer)
    postcode_end = Column(Integer)
    status = Column(String(255))

    # orders = relationship("Order", back_populates="delivery_person")


class Order(Base):
    __tablename__ = "Order"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("Customer.id"))
    delivery_person_id = Column(Integer, ForeignKey("DeliveryPerson.id"))
    status = Column(String(255))
    discount_id = Column(Integer, ForeignKey("DiscountCode.id"))
    timestamp = Column(TIMESTAMP)

    customer: Mapped["Customer"]= relationship(back_populates="orders")
    # delivery_person = relationship("DeliveryPerson", back_populates="orders")
    # discount = relationship("DiscountCode", back_populates="orders")
    #
    # pizzas = relationship("OrderedPizza", back_populates="order")
    # desserts = relationship("OrderedDessert", back_populates="order")
    # drinks = relationship("OrderedDrink", back_populates="order")


class OrderedPizza(Base):
    __tablename__ = "OrderedPizza"

    order_id = Column(Integer, ForeignKey("Order.id"), primary_key=True)
    pizza_id = Column(Integer, ForeignKey("Pizza.id"), primary_key=True)

    # order = relationship("Order", back_populates="pizzas")
    # pizza = relationship("Pizza", back_populates="ordered_pizzas")


class OrderedDessert(Base):
    __tablename__ = "OrderedDessert"

    order_id = Column(Integer, ForeignKey("Order.id"), primary_key=True)
    dessert_id = Column(Integer, ForeignKey("Dessert.id"), primary_key=True)

    # order = relationship("Order", back_populates="desserts")
    # dessert = relationship("Dessert", back_populates="ordered_desserts")


class OrderedDrink(Base):
    __tablename__ = "OrderedDrink"

    order_id = Column(Integer, ForeignKey("Order.id"), primary_key=True)
    drink_id = Column(Integer, ForeignKey("Drink.id"), primary_key=True)

    # order = relationship("Order", back_populates="drinks")
    # drink = relationship("Drink", back_populates="ordered_drinks")

class Customer(Base):
    __tablename__ = "Customer"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    birthday = Column(Date)
    address = Column(String(255))
    postcode = Column(Integer)

    orders: Mapped[Order] = relationship(back_populates="customer")

