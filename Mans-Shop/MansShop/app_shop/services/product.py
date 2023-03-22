import random
from app_shop.models import Product, Brands


class ProductService:
    @staticmethod
    def get_new_season_products(limit: int):
        products = Product.objects.only("title", "price", "photo").filter(
            season__season_status="new"
        )[:limit]

        return products

    @classmethod
    def get_random_products(cls, limit: int):
        products = cls.get_new_season_products(limit)
        random_limit = limit if limit <= len(products) else len(products)
        random_products = random.choices(products, k=random_limit)

        return random_products

    @staticmethod
    def get_all_products():
        return Product.objects.only("title", "price", "photo").all()

    @staticmethod
    def get_recommended_product():
        return Product.objects.only("title", "price", "photo").filter(
            season__season_status="recommended"
        )

    @staticmethod
    def get_product_brands():
        return Brands.objects.only("img").all()[:4]
