from config import Config

def calculate_pizza_price(price) -> float:
     return round((Config.PIZZA_BASE_PRICE + price) * Config.MARGIN * Config.VAT, 2)
