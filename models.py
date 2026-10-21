# models.py
class Product:
    def __init__(self, product_id, name, price, photo):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._photo = photo

    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def photo(self):
        return self._photo

    def get_info(self):
        return f"{self.name} - {self.price}$"

class Phone(Product):
    def get_info(self):
        return f"📱 {self.name}\n💰 {self.price}$"

class Laptop(Product):
    def get_info(self):
        return f"💻 {self.name}\n💰 {self.price}$"

class Order:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def clear(self):
        self.__products.clear()

    def get_products(self):
        return self.__products

    def total_items(self):
        return len(self.__products)

    def total_price(self):
        total = 0

        for product in self.__products:
            total += product.price

        return total