from .models import *
from django.conf import settings
from decimal import Decimal

def get_brand_queryset():
    return Brands.objects.only('img').all()[:4]

def get_cart_products_for_user(user):
    cart = Cart.objects.filter(user=user).first()
    if cart:
        return cart.product.all()

    return None

def get_cart_products_for_anonym_user(session):
    cart = session.get(settings.CART_SESSION_ID)
    if cart:
        cart_products = []
        for c in cart:
            cart_products.append(cart[c])
    else:
        cart_products = []

    return cart_products

def add_cart_quantity(user,kwargs):
    cart_product = CartProduct.objects.filter(user=user,pk=kwargs['product_id']).first()
    cart_product.quantity += 1
    cart_product.save()

def remove_cart_quantity(user,kwargs):
    cart_product = CartProduct.objects.filter(user=user,pk=kwargs['product_id']).first()
    if cart_product.quantity == 1:
        cart_product.delete()
    else:
        cart_product.quantity -= 1
        cart_product.save()

def remove_cart(user,kwargs):
    cart_product = CartProduct.objects.filter(user=user,pk=kwargs['product_id']).first()
    cart_product.delete()


class AddCartManager:

    def __init__(self,request,kwargs):
        self.__request = request
        self.__kwargs = kwargs

    def add_to_cart(self):
        self.cart, created = Cart.objects.get_or_create(
            user=self.__request.user,
        )

        if not created and self.cart.product.filter(user=self.__request.user,product__pk=self.__kwargs['product_id']).exists():
            self.add_product_in_exist_cart()
        else:
            self.create_and_add_cart_product_in_cart()

    def create_and_add_cart_product_in_cart(self):
        product = Product.objects.get(pk=self.__kwargs['product_id'])
        cart_product = CartProduct.objects.create(
            user=self.__request.user,
            product=product,
            quantity=1,
            cart=self.cart
        )
        self.cart.product.add(cart_product)

    def add_product_in_exist_cart(self):
        cart_product = self.cart.product.filter(user=self.__request.user,product__pk=self.__kwargs['product_id']).first()
        cart_product.quantity += 1
        cart_product.save()


class AnonymCartManager:

    def __init__(self,request,kwargs):
        if not request.session.session_key:
            request.session.cycle_key()
        self.__session = request.session
        self.__kwargs = kwargs
        self.__cart = request.session.get(settings.CART_SESSION_ID)
        if not self.__cart:
            self.__cart = request.session[settings.CART_SESSION_ID] = {}

    def add_to_cart(self):
        product = Product.objects.get(pk=self.__kwargs['product_id'])
        if str(product.pk) not in self.__cart:
            self.__cart[str(product.pk)] = {
                'pk': product.pk,
                'get_title': product.title,
                'quantity' : 1,
                'price': str(product.price),
                'get_photo': product.photo.url,
                'final_price': None,
            }
        else:
            self.__cart[str(product.pk)]['quantity'] += 1

        self.save()
        # self.__session.clear()

    def remove_from_cart(self):
        self.__cart.pop(str(self.__kwargs['product_id']))
        self.save()

    def add_quantity(self):
        self.__cart[str(self.__kwargs['product_id'])]['quantity'] += 1
        self.save()

    def remove_quantity(self):
        if self.__cart[str(self.__kwargs['product_id'])]['quantity'] == 1:
            self.__cart.pop(str(self.__kwargs['product_id']))
        else:
            self.__cart[str(self.__kwargs['product_id'])]['quantity'] -= 1
        self.save()

    def save(self):
        self.final_price()
        self.__session[settings.CART_SESSION_ID] = self.__cart
        self.__session.modified = True

    def final_price(self):
        for product in self.__cart:
            price = Decimal(self.__cart[product]['price']) * self.__cart[product]['quantity']
            self.__cart[product]['final_price'] = str(int(price)) if int(price) == price else str(price)



        





