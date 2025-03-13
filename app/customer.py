import math
import datetime
from app.car import Car
from app.shop import Shop
from app.config_loader import load_config

config = load_config()
FUEL_PRICE = config["FUEL_PRICE"]


class Customer:
    def __init__(self, name: str, product_cart: int,
                 location: int, money: int , car: Car) -> None:
        self.name = name
        self.product_cart = product_cart
        self.location = tuple(location)
        self.money = money
        self.car = Car(car["brand"], car["fuel_consumption"])

    def distance_to(self, shop: Shop) -> int:
        return math.dist(self.location, shop.location)

    def trip_cost(self, shop: Shop) -> [int, float]:
        distance = self.distance_to(shop) * 2  # round trip
        fuel_needed = (distance / 100) * self.car.fuel_consumption
        return round(fuel_needed * FUEL_PRICE, 2)

    def can_afford(self, shop: Shop) -> bool:
        trip_cost = self.trip_cost(shop)
        total_product_cost = sum(shop.products.get(p, float("inf")) * q
                                 for p, q in self.product_cart.items())
        return trip_cost + total_product_cost <= self.money

    def buy_products(self, shop: Shop) -> None:
        if not self.can_afford(shop):
            print(f"{self.name} doesn't have enough "
                  f"money to make a purchase in any shop")
            return

        trip_cost = self.trip_cost(shop)
        total_cost = sum(shop.products[p] * q
                         for p, q in self.product_cart.items())
        self.money -= (trip_cost + total_cost)
        self.location = shop.location

        print(f"{self.name} rides to {shop.name}\n")
        print(f"Date: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Thanks, {self.name}, for your purchase!")
        print("You have bought:")
        for ps, qs in self.product_cart.items():
            price = int(shop.products[ps] * qs) \
                if str(shop.products[ps] * qs)[-1] == "0" \
                else shop.products[ps] * qs
            print(f"{qs} {ps}s for {price} dollars")
        print(f"Total cost is {total_cost} dollars\nSee you again!\n")

        print(f"{self.name} rides home")
        self.location = tuple(
            config["customers"][0]["location"])  # Reset location to home
        print(f"{self.name} now has {round(self.money, 2)} dollars\n")
