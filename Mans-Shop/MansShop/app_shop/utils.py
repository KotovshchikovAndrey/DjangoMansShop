import random

from decimal import Decimal
from string import ascii_letters

from functools import cache
from app_shop.models import Product, Category, Season


class ProductDataMixin:
    def get_context(self, **kwargs):
        base_context = kwargs
        base_context["title"] = "Man Shop"
        return base_context


class Faker:
    def create_seasons(self, count: int = 5):
        seasons = []
        for _ in range(count):
            name = self.__get_random_string()
            description = self.__get_random_string(length=100)
            seasons.append(Season(name=name, description=description))

        Season.objects.bulk_create(seasons)

    def create_categories(self, count: int = 5):
        categories = []
        for _ in range(count):
            name = self.__get_random_string()
            categories.append(Category(name=name))

        Category.objects.bulk_create(categories)

    def create_products(self, count: int = 5):
        products = []
        for _ in range(count):
            title = self.__get_random_string()
            description = self.__get_random_string(length=100)
            price = self.__get_random_number()
            category = Category.objects.first()
            season = Season.objects.first()

            product = Product(
                title=title,
                description=description,
                price=Decimal(price),
                category=category,
                season=season,
            )

            products.append(product)

        Product.objects.bulk_create(products)

    def __get_random_string(self, length: int = 10) -> str:
        string = ""
        for _ in range(length):
            string += random.choice(ascii_letters)

        return string

    def __get_random_number(self) -> int:
        return random.randint(1, 1000)


@cache
def get_faker() -> Faker:
    return Faker()
