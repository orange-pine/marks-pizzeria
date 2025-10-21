
from ast import In
from datetime import date, datetime
import string
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Table
)
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, declarative_base, Mapped

class Base(DeclarativeBase):
    pass

PizzaIngredient = Table(
    'PizzaIngredient',
    Base.metadata,
    Column('pizza_id', Integer, ForeignKey('Pizza.id')),
    Column('ingredient_id', Integer, ForeignKey('Ingredient.id'))
    )

class Ingredient(Base):
    __tablename__: str = "Ingredient"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    vegan: Mapped[bool]= mapped_column()
    vegetarian: Mapped[bool] = mapped_column()


class Pizza(Base):
    __tablename__: str = "Pizza"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    ingredients: Mapped[list[Ingredient]] = relationship(secondary=PizzaIngredient)

    # Calculate price dynamically from ingredient prices
    @property
    def price(self):
        """Compute total price based on the sum of ingredient prices."""
        if not self.ingredients:
            return 0
        return sum(ingredient.price for ingredient in self.ingredients)



class Drink(Base):
    __tablename__: str = "Drink"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    vegan: Mapped[bool]= mapped_column()
    vegetarian: Mapped[bool] = mapped_column()


class Dessert(Base):
    __tablename__: str = "Dessert"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    vegan: Mapped[bool]= mapped_column()
    vegetarian: Mapped[bool] = mapped_column()



class DiscountCode(Base):
    __tablename__: str = "DiscountCode"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    amount: Mapped[int] = mapped_column()
    order: Mapped["Order"] = relationship(back_populates="discount_code")


class DeliveryPerson(Base):
    __tablename__: str = "DeliveryPerson"

    id: Mapped[int] = mapped_column(primary_key=True)
    postcode_start: Mapped[int] = mapped_column()
    postcode_end: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column()


class Order(Base):
    __tablename__: str = "Order"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("Customer.id"))
    delivery_person_id: Mapped[int] = mapped_column(ForeignKey("DeliveryPerson.id"))
    status: Mapped[str] = mapped_column()
    discount_id: Mapped[int] = mapped_column(ForeignKey("DiscountCode.id"))
    timestamp: Mapped[datetime]= mapped_column()

    customer: Mapped["Customer"]= relationship(back_populates="orders")
    delivery_person: Mapped[DeliveryPerson] = relationship()
    discount_code: Mapped[DiscountCode] = relationship(back_populates="order")
    pizzas: Mapped[list[Pizza]] = relationship(secondary="OrderedPizza")
    desserts: Mapped[list[Dessert]] = relationship(secondary="OrderedDessert")
    drinks: Mapped[list[Drink]] = relationship(secondary="OrderedDrink")


class OrderedPizza(Base):
    __tablename__: str = "OrderedPizza"

    order_id: Mapped[int] = mapped_column(ForeignKey("Order.id"), primary_key=True)
    pizza_id: Mapped[int] = mapped_column(ForeignKey("Pizza.id"), primary_key=True)


class OrderedDessert(Base):
    __tablename__: str = "OrderedDessert"

    order_id: Mapped[int] = mapped_column(ForeignKey("Order.id"), primary_key=True)
    dessert_id: Mapped[int] = mapped_column(ForeignKey("Dessert.id"), primary_key=True)

class OrderedDrink(Base):
    __tablename__: str = "OrderedDrink"

    order_id: Mapped[int] = mapped_column(ForeignKey("Order.id"), primary_key=True)
    drink_id: Mapped[int] = mapped_column(ForeignKey("Drink.id"), primary_key=True)

class Customer(Base):
    __tablename__: str = "Customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    birthday: Mapped[date] = mapped_column()
    address: Mapped[str]= mapped_column()
    postcode: Mapped[int] = mapped_column()

    orders: Mapped[Order] = relationship(back_populates="customer")

