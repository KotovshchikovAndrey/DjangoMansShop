import typing as tp

from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from app_shop.models import Product

from app_shop.services.cart import ICartService, CartServiceFactory
from app_shop.services.product import ProductService

from app_shop.utils import get_faker, ProductDataMixin


class FakerView(View):
    faker = get_faker()

    def get(self, request: HttpRequest):
        if not request.user.is_superuser:
            return HttpResponse(content="Fuck you!")

        self.faker.create_seasons()
        self.faker.create_categories()
        self.faker.create_products()

        return HttpResponse(content="Fake data were created!")


class MainView(ProductDataMixin, ListView):
    template_name = "app_shop/main.html"
    queryset = ProductService.get_new_season_products(limit=12)
    context_object_name = "products"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        base_context = self.get_context(
            new_collection=ProductService.get_random_products(limit=100),
            brands=ProductService.get_product_brands(),
        )

        return dict(list(base_context.items()) + list(context.items()))


class ProductListView(ProductDataMixin, ListView):
    template_name = "app_shop/list_product.html"
    queryset = ProductService.get_all_products()
    context_object_name = "products"
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        base_context = self.get_context(
            products_title="ТОВАРЫ В НАЛИЧИИ",
            url=reverse("products"),
        )

        return dict(list(base_context.items()) + list(context.items()))


class ProductDetailView(ProductDataMixin, DetailView):
    model = Product
    template_name = "app_shop/detail_product.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_context()
        return dict(list(base_context.items()) + list(context.items()))


class NewCollectionListView(ProductDataMixin, ListView):
    template_name = "app_shop/list_product.html"
    queryset = ProductService.get_new_season_products(limit=10)
    context_object_name = "products"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_context(
            products_title="НОВОЕ ПОСТУПЛЕНИЕ",
            url=reverse("new_collection"),
        )

        return dict(list(base_context.items()) + list(context.items()))


class RecommendedProductView(ProductDataMixin, ListView):
    template_name = "app_shop/list_product.html"
    queryset = ProductService.get_recommended_product()
    context_object_name = "products"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_context(
            products_title="САМАЯ ПОПУЛЯРНАЯ КОЛЛЕКЦИЯ",
            url=reverse("recommended"),
        )

        return dict(list(base_context.items()) + list(context.items()))


class CartView(ProductDataMixin, View):
    def dispatch(
        self, request: HttpRequest, *args: tp.Any, **kwargs: tp.Any
    ) -> HttpResponse:
        user = request.user
        if user.is_authenticated:
            cart_service = CartServiceFactory.create("authenticated", user=user)
            return super().dispatch(request, cart_service, *args, **kwargs)

        if not request.session.session_key:
            request.session.cycle_key()

        cart_service = CartServiceFactory.create("anonym", session=request.session)
        return super().dispatch(request, cart_service, *args, **kwargs)

    def get(self, request: HttpRequest, service: ICartService):
        cart_products = service.get_products()

        paginator = Paginator(cart_products, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = self.get_context(
            cart_products=cart_products,
            url=reverse("cart"),
            page_obj=page_obj,
            num_pages=paginator.num_pages,
        )

        return render(request, "app_shop/cart.html", context)


def add_to_cart_view(request, **kwargs):
    if not request.user.is_authenticated:
        cart = CartServiceFactory.create("anonym", session=request.session)
    else:
        cart = CartServiceFactory.create("authenticated", user=request.user)

    cart.add_product(product_id=kwargs["product_id"])
    return redirect("cart")


def remove_from_cart_view(request, **kwargs):
    if not request.user.is_authenticated:
        cart = CartServiceFactory.create("anonym", session=request.session)
    else:
        cart = CartServiceFactory.create("authenticated", user=request.user)

    cart.remove_product(product_id=kwargs["product_id"])
    return redirect(request.META.get("HTTP_REFERER"))


def add_quantity_view(request, **kwargs):
    if not request.user.is_authenticated:
        cart = CartServiceFactory.create("anonym", session=request.session)
    else:
        cart = CartServiceFactory.create("authenticated", user=request.user)

    cart.increment_quantity(product_id=kwargs["product_id"])
    return redirect(request.META.get("HTTP_REFERER"))


def remove_quantity_view(request, **kwargs):
    if not request.user.is_authenticated:
        cart = CartServiceFactory.create("anonym", session=request.session)
    else:
        cart = CartServiceFactory.create("authenticated", user=request.user)

    cart.decrement_quantity(product_id=kwargs["product_id"])
    return redirect(request.META.get("HTTP_REFERER"))
