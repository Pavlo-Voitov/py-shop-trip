class Shop:
    def __init__(self, name: str, location: int, products: dict) -> None:
        self.name = name
        self.location = tuple(location)
        self.products = products
