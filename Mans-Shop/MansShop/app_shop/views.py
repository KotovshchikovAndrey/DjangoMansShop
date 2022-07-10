from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import *
from .services import get_brand_queryset, get_cart_products_for_user,AddCartManager,add_cart_quantity,remove_cart_quantity, AnonymCartManager, remove_cart\
,get_cart_products_for_anonym_user
from .utils import ProductDataMixin

class MainView(ProductDataMixin,ListView):
    template_name = 'app_shop/main.html'
    queryset = Product.get_product_queryset.get_queryset_for_new_collection_product()[:12]
    context_object_name = 'products'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        base_context = self.get_context(
            new_collection=Product.get_product_queryset.get_random_list_for_new_collection_product(),
            brands=get_brand_queryset(),
        )
        return dict(list(base_context.items()) + list(context.items()))

class ProductListView(ProductDataMixin,ListView):
    template_name = 'app_shop/list_product.html'
    queryset = Product.get_product_queryset.get_all_products()
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        base_context = self.get_context(
            products_title='ТОВАРЫ В НАЛИЧИИ',
            url=reverse('products'),
        )
        return dict(list(base_context.items()) + list(context.items()))

class ProductDetailView(ProductDataMixin,DetailView):
    model = Product
    template_name = 'app_shop/detail_product.html'
    context_object_name = 'product'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_context()
        return dict(list(base_context.items()) + list(context.items()))

class NewCollectionListView(ProductDataMixin,ListView):
    template_name = 'app_shop/list_product.html'
    queryset = Product.get_product_queryset.get_queryset_for_new_collection_product()
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_context(
            products_title='НОВОЕ ПОСТУПЛЕНИЕ',
            url=reverse('new_collection'),
        )
        return dict(list(base_context.items()) + list(context.items()))

class RecommendedProductView(ProductDataMixin,ListView):
    template_name = 'app_shop/list_product.html'
    queryset = Product.get_product_queryset.get_queryset_for_recommended_product()
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_context(
            products_title='САМАЯ ПОПУЛЯРНАЯ КОЛЛЕКЦИЯ',
            url=reverse('recommended'),
        )
        return dict(list(base_context.items()) + list(context.items()))

class CartView(ProductDataMixin,View):

    def get(self,request):
        user = request.user
        cart_products = None
        if not request.session.session_key:
            request.session.cycle_key()

        if user.is_authenticated:
            cart_products = get_cart_products_for_user(user)
        else:
            cart_products = get_cart_products_for_anonym_user(request.session)

        paginator = Paginator(cart_products,5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = self.get_context(
            cart_products=cart_products,
            url=reverse('cart'),
            page_obj=page_obj,
            num_pages=paginator.num_pages,
        )

        return render(request,'app_shop/cart.html',context)

class AddCartView(View):

    def get(self,request,**kwargs):
        if not request.user.is_authenticated:
            cart = AnonymCartManager(request,kwargs)
            cart.add_to_cart()
        else:
            cart = AddCartManager(request,kwargs)
            cart.add_to_cart()

        return redirect('cart')

def add_quantity_view(request,**kwargs):
    if not request.user.is_authenticated:
        cart = AnonymCartManager(request, kwargs)
        cart.add_quantity()
    else:
        add_cart_quantity(request.user,kwargs)
    return redirect(request.META.get('HTTP_REFERER'))

def remove_quantity_view(request,**kwargs):
    if not request.user.is_authenticated:
        cart = AnonymCartManager(request,kwargs)
        cart.remove_quantity()
    else:
        remove_cart_quantity(request.user,kwargs)
    return redirect(request.META.get('HTTP_REFERER'))

def remove_from_cart_view(request,**kwargs):
    if not request.user.is_authenticated:
        cart = AnonymCartManager(request,kwargs)
        cart.remove_from_cart()
    else:
        remove_cart(request.user,kwargs)
    return redirect(request.META.get('HTTP_REFERER'))









