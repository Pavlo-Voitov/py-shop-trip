import json
from app.customer import Customer
from app.shop import Shop


def shop_trip() -> None:
    with open("app/config.json", "r") as file:
        config = json.load(file)

    customers = []
    for cas in config["customers"]:
        customers.append(Customer(
            name=cas["name"],
            product_cart=cas["product_cart"],
            location=tuple(cas["location"]),
            money=cas["money"],
            car=cas["car"]
        ))
    shops = []
    for sh in config["shops"]:
        shops.append(Shop(name=sh["name"],
                          location=sh["location"], products=sh["products"]))

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")
        best_shop = None
        best_price = float("inf")

        for shop in shops:
            trip_cost = customer.trip_cost(shop)
            total_cost = sum(shop.products.get(p, float("inf")) * q
                             for p, q in customer.product_cart.items())
            total_trip_cost = trip_cost + total_cost

            print(f"{customer.name}'s trip to the "
                  f"{shop.name} costs {total_trip_cost}")

            if total_trip_cost < best_price and customer.can_afford(shop):
                best_shop = shop
                best_price = total_trip_cost

        if best_shop:
            customer.buy_products(best_shop)
        else:
            print(f"{customer.name} doesn't have "
                  f"enough money to make a purchase in any shop")
