CREATE TABLE Customers (
  id integer PRIMARY KEY,
  name VARCHAR(255),
  birtday DATE,
  address VARCHAR(255),
  postcode integer
);

CREATE TABLE Pizzas (
  id integer PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE Ingredients (
  id integer PRIMARY KEY,
  name VARCHAR(255),
  price integer,
  vegan bool,
  vegetarian bool
);

CREATE TABLE PizzaIngredients (
  PizzaId integer,
  IngredientId integer,
  FOREIGN KEY (PizzaId) REFERENCES Pizzas (id),
  FOREIGN KEY (IngredientId) REFERENCES Ingredients (id)
);

CREATE TABLE Drinks (
  id integer PRIMARY KEY,
  name VARCHAR(255),
  price integer,
  vegan bool,
  vegetarian bool
);

CREATE TABLE Desserts (
  id integer PRIMARY KEY,
  name VARCHAR(255),
  price integer,
  vegan bool,
  vegetarian bool
);

CREATE TABLE DiscountCodes (
  id integer PRIMARY KEY,
  code VARCHAR(255),
  type VARCHAR(255),
  amount integer
);

CREATE TABLE DeliveryPersonnel (
  id integer PRIMARY KEY,
  postcodeStart integer,
  postcodeEnd integer,
  status VARCHAR(255)
);

CREATE TABLE Orders (
  id integer PRIMARY KEY,
  customerId integer,
  deliveryPersonId integer,
  status VARCHAR(255),
  discountId integer,
  timestamp timestamp,
  FOREIGN KEY (customerId) REFERENCES Customers (id),
  FOREIGN KEY (deliveryPersonId) REFERENCES DeliveryPersonnel (id),
  FOREIGN KEY (discountId) REFERENCES DiscountCodes (id)
);

CREATE TABLE OrderedPizza (
  orderId integer,
  pizzaId integer,
  FOREIGN KEY (orderId) REFERENCES Orders (id),
  FOREIGN KEY (pizzaId) REFERENCES Pizzas (id)
);

CREATE TABLE OrderedDessert (
  orderId integer,
  dessertId integer,
  FOREIGN KEY (orderId) REFERENCES Orders (id),
  FOREIGN KEY (dessertId) REFERENCES Desserts (id)
);

CREATE TABLE OrderedDrink (
  orderId integer,
  drinkId integer,
  FOREIGN KEY (orderId) REFERENCES Orders (id),
  FOREIGN KEY (drinkId) REFERENCES Drinks (id)
);
