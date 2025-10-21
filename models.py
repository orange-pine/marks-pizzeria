
from ast import In
from datetime import date, datetime
import string
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Table,
    null
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
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column()
    vegan: Mapped[bool]= mapped_column()
    vegetarian: Mapped[bool] = mapped_column()


class Pizza(Base):
    __tablename__: str = "Pizza"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    ingredients: Mapped[list[Ingredient]] = relationship(secondary=PizzaIngredient)

    # Calculate price dynamically from ingredient prices
    @property
    def price(self):
        """Compute total price based on the sum of ingredient prices."""
        if not self.ingredients:
            return 0
        return sum(ingredient.price for ingredient in self.ingredients)

    @property
    def vegetarian(self):
        vegetarian = True

        for ingredient in self.ingredients:
            if ingredient.vegetarian != True:
                vegetarian = False
        return vegetarian

    @property
    def vegan(self):
        vegan = True

        for ingredient in self.ingredients:
            if ingredient.vegan != True:
                vegan = False
        return vegan


class Drink(Base):
    __tablename__: str = "Drink"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column()
    vegan: Mapped[bool]= mapped_column()
    vegetarian: Mapped[bool] = mapped_column()


class Dessert(Base):
    __tablename__: str = "Dessert"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column()
    vegan: Mapped[bool]= mapped_column()
    vegetarian: Mapped[bool] = mapped_column()



class DiscountCode(Base):
    __tablename__: str = "DiscountCode"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    amount: Mapped[int] = mapped_column()
    order: Mapped["Order"] = relationship(back_populates="discount_code")


class DeliveryPerson(Base):
    __tablename__: str = "DeliveryPerson"

    id: Mapped[int] = mapped_column(primary_key=True)
    postcode_start: Mapped[int] = mapped_column()
    postcode_end: Mapped[int] = mapped_column()
    unavailable_before: Mapped[datetime] = mapped_column()


class Order(Base):
    __tablename__: str = "Order"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("Customer.id"))
    delivery_person_id: Mapped[int] = mapped_column(ForeignKey("DeliveryPerson.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(255))
    discount_id: Mapped[int] = mapped_column(ForeignKey("DiscountCode.id"), nullable=True)
    timestamp: Mapped[datetime]= mapped_column()

    customer: Mapped["Customer"]= relationship(back_populates="orders")
    delivery_person: Mapped[DeliveryPerson] = relationship()
    discount_code: Mapped[DiscountCode] = relationship(back_populates="order")
    pizzas: Mapped[list[Pizza]] = relationship(secondary="OrderedPizza")
    desserts: Mapped[list[Dessert]] = relationship(secondary="OrderedDessert")
    drinks: Mapped[list[Drink]] = relationship(secondary="OrderedDrink")

    @property
    def total(self):
        """Compute total price based on the sum of ingredient prices."""
        total = 0
        total += sum(pizza.price for pizza in self.pizzas)
        total += sum(drink.price for drink in self.drinks)
        total += sum(dessert.price for dessert in self.desserts)

        if(self.discount_code != None):
            if self.discount_code.type == "fixed":
                total -= self.discount_code.amount
            else:
                total *= 1 + self.discount_code.amount

        return total



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
    name: Mapped[str] = mapped_column(String(255))
    birthday: Mapped[date] = mapped_column()
    address: Mapped[str]= mapped_column(String(255))
    postcode: Mapped[int] = mapped_column()

    orders: Mapped[Order] = relationship(back_populates="customer")

