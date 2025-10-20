
-- Customers
INSERT INTO Customer (id, name, birthday, address, postcode) VALUES
(1, 'Alice Johnson', '1990-05-14', '123 Elm Street', 1001),
(2, 'Bob Smith', '1985-08-23', '45 Oak Avenue', 1002),
(3, 'Charlie Lee', '2000-11-09', '78 Maple Road', 1003),
(4, 'Diana Torres', '1998-02-17', '9 Pine Boulevard', 1004),
(5, 'Ethan Brown', '1975-06-30', '56 Birch Lane', 1005);

-- Pizzas
INSERT INTO Pizza (id, name) VALUES
(1, 'Margherita'),
(2, 'Pepperoni'),
(3, 'Vegetarian Delight'),
(4, 'BBQ Chicken'),
(5, 'Vegan Special');

-- Ingredients
INSERT INTO Ingredient (id, name, price, vegan, vegetarian) VALUES
(1, 'Tomato Sauce', 1, TRUE, TRUE),
(2, 'Mozzarella', 2, FALSE, TRUE),
(3, 'Pepperoni', 3, FALSE, FALSE),
(4, 'Bell Peppers', 1, TRUE, TRUE),
(5, 'Onions', 1, TRUE, TRUE),
(6, 'BBQ Sauce', 1, TRUE, TRUE),
(7, 'Chicken', 3, FALSE, FALSE),
(8, 'Vegan Cheese', 2, TRUE, TRUE),
(9, 'Olives', 1, TRUE, TRUE),
(10, 'Mushrooms', 1, TRUE, TRUE);

-- PizzaIngredients (link pizzas to ingredients)
INSERT INTO PizzaIngredient (pizza_id, ingredient_id) VALUES
-- Margherita
(1, 1), (1, 2),
-- Pepperoni
(2, 1), (2, 2), (2, 3),
-- Vegetarian Delight
(3, 1), (3, 2), (3, 4), (3, 5), (3, 9), (3, 10),
-- BBQ Chicken
(4, 6), (4, 7), (4, 2), (4, 5),
-- Vegan Special
(5, 1), (5, 8), (5, 4), (5, 9), (5, 10);

-- Drinks
INSERT INTO Drink (id, name, price, vegan, vegetarian) VALUES
(1, 'Coca-Cola', 2, TRUE, TRUE),
(2, 'Orange Juice', 3, TRUE, TRUE),
(3, 'Water', 1, TRUE, TRUE),
(4, 'Beer', 4, TRUE, TRUE),
(5, 'Milkshake', 4, FALSE, TRUE);

-- Desserts
INSERT INTO Dessert (id, name, price, vegan, vegetarian) VALUES
(1, 'Chocolate Cake', 5, FALSE, TRUE),
(2, 'Vegan Brownie', 4, TRUE, TRUE),
(3, 'Ice Cream', 3, FALSE, TRUE),
(4, 'Fruit Salad', 3, TRUE, TRUE),
(5, 'Cheesecake', 5, FALSE, TRUE);

-- Discount Codes
INSERT INTO DiscountCode (id, code, type, amount) VALUES
(1, 'WELCOME10', 'percentage', 10),
(2, 'FREEDRINK', 'fixed', 2),
(3, 'PIZZA20', 'percentage', 20);

-- Delivery Personnel
INSERT INTO DeliveryPerson (id, postcode_start, postcode_end, status) VALUES
(1, 1000, 1002, 'available'),
(2, 1003, 1005, 'available'),
(3, 1006, 1010, 'off-duty');

-- Orders
INSERT INTO Order (id, customer_id, delivery_person_id, status, discount_id, timestamp) VALUES
(1, 1, 1, 'delivered', 1, '2025-10-18 18:45:00'),
(2, 2, 1, 'preparing', NULL, '2025-10-19 19:10:00'),
(3, 3, 2, 'delivered', 2, '2025-10-19 20:05:00'),
(4, 4, 2, 'delivered', 3, '2025-10-20 12:00:00'),
(5, 5, 1, 'pending', NULL, '2025-10-20 14:30:00');

-- Ordered Pizzas
INSERT INTO OrderedPizza (order_id, pizza_id) VALUES
(1, 2),
(1, 1),
(2, 3),
(3, 5),
(3, 1),
(4, 4),
(5, 2);

-- Ordered Drinks
INSERT INTO OrderedDrink (order_id, drink_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 1);

-- Ordered Desserts
INSERT INTO OrderedDessert (order_id, dessert_id) VALUES
(1, 1),
(2, 4),
(3, 2),
(4, 3),
(5, 5);
