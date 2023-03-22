import typing as tp

from abc import ABC, abstractmethod
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.sessions.backends.base import SessionBase

from app_shop.models import Cart, Product, CartProduct, Brands


class ICartService(ABC):
    @abstractmethod
    def get_products(self) -> tp.Iterable[CartProduct]:
        raise NotImplementedError()

    @abstractmethod
    def add_product(self, product_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def remove_product(self, product_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def increment_quantity(self, product_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def decrement_quantity(self, product_id: int) -> None:
        raise NotImplementedError()


class AuthCartService(ICartService):
    __user: AbstractBaseUser

    def __init__(self, user: AbstractBaseUser) -> None:
        self.__user = user

    def get_products(self):
        cart = Cart.objects.prefetch_related("product").filter(user=self.__user).first()
        if cart:
            return cart.product.all()

    def add_product(self, product_id: int):
        cart, created = Cart.objects.prefetch_related("product").get_or_create(
            user=self.__user
        )

        if not created:
            cart_product = cart.product.filter(
                user=self.__user, product__pk=product_id
            ).first()

            cart_product.quantity += 1
            cart_product.save()
            return

        product = Product.objects.get(pk=product_id)
        cart_product = CartProduct.objects.create(
            user=self.__user,
            product=product,
            quantity=1,
            cart=cart,
        )

        cart.product.add(cart_product)

    def remove_product(self, product_id: int):
        cart_product = CartProduct.objects.filter(
            user=self.__user, pk=product_id
        ).first()

        cart_product.delete()

    def increment_quantity(self, product_id: int):
        cart_product = CartProduct.objects.filter(
            user=self.__user, pk=product_id
        ).first()

        cart_product.quantity += 1
        cart_product.save()

    def decrement_quantity(self, product_id: int):
        cart_product = CartProduct.objects.filter(
            user=self.__user, pk=product_id
        ).first()

        if cart_product.quantity == 1:
            cart_product.delete()
        else:
            cart_product.quantity -= 1
            cart_product.save()


class AnonymCartService(ICartService):
    __session: SessionBase

    def __init__(self, session: SessionBase) -> None:
        self.__session = session

    def get_products(self):
        cart = self.__session.get(settings.CART_SESSION_ID)
        if cart is None:
            return []

        cart_products = []
        for c in cart:
            cart_products.append(cart[c])

        return cart_products

    def add_product(self, product_id: int):
        product = Product.objects.filter(pk=product_id).first()
        if product is None:
            # ApiError
            raise

        cart = self.__get_session_cart()
        cart_product_id = str(product.pk)

        if cart_product_id not in cart:
            cart[cart_product_id] = {
                "pk": product.pk,
                "get_title": product.title,
                "quantity": 1,
                "price": str(product.price),
                "get_photo": product.photo.url,
                "final_price": None,
            }
        else:
            cart[cart_product_id]["quantity"] += 1

        self.__save_session_cart(cart)

    def remove_product(self, product_id: int):
        cart = self.__get_session_cart()
        cart.pop(str(product_id))

        self.__save_session_cart(cart)

    def increment_quantity(self, product_id: int):
        cart = self.__get_session_cart()
        cart[str(product_id)]["quantity"] += 1

        self.__save_session_cart(cart)

    def decrement_quantity(self, product_id: int):
        cart = self.__get_session_cart()

        _product_id = str(product_id)
        if cart[_product_id]["quantity"] == 1:
            cart.pop(_product_id)
        else:
            cart[str(_product_id)]["quantity"] -= 1

        self.__save_session_cart(cart)

    def __get_session_cart(self):
        cart = self.__session.get(settings.CART_SESSION_ID)
        if cart is None:
            cart = self.__session[settings.CART_SESSION_ID] = {}

        return cart

    def __save_session_cart(self, cart: tp.Dict[str, str]) -> None:
        self.__set_final_price_for_products(cart)

        self.__session[settings.CART_SESSION_ID] = cart
        self.__session.modified = True

    def __set_final_price_for_products(self, cart: tp.Dict[str, tp.Any]):
        for cart_product in cart:
            product_price = Decimal(cart[cart_product]["price"])
            product_quantity = cart[cart_product]["quantity"]
            price = product_price * product_quantity

            # убирает нули после запятой, если сумма целая
            final_price = str(int(price)) if int(price) == price else str(price)
            cart[cart_product]["final_price"] = final_price


CartType = tp.Literal["anonym", "authenticated"]


class CartServiceFactory:
    __cart_services: tp.Dict[CartType, tp.Type[ICartService]] = {
        "anonym": AnonymCartService,
        "authenticated": AuthCartService,
    }

    @classmethod
    def create(cls, name: CartType, *args, **kwargs) -> ICartService:
        cart_service = cls.__cart_services[name]
        return cart_service(*args, **kwargs)  # type: ignore
