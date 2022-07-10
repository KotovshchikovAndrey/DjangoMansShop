from django.db import models
from django.urls import reverse
from .utils import ProductManager
from app_user.models import User
from django.db.models import Count

class Category(models.Model):
    name = models.CharField(max_length=50,verbose_name='Название Категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Season(models.Model):
    choice = (
        ('new','Новая Коллекция'),
        ('recommended','Рекомендуемая К Покупке Коллекция'),
        ('default','Обычная Коллекция')
    )

    name = models.CharField(max_length=50,verbose_name='Название Сезона')
    description = models.TextField(verbose_name='Описание Сезона')
    season_status = models.CharField(max_length=11,choices=choice,default='default',verbose_name='Статус Коллекции')


    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название Товара')
    description = models.TextField(verbose_name='Описание Товара')
    price = models.DecimalField(max_digits=10,decimal_places=3,verbose_name='Цена Товара',default=0)
    cat = models.ForeignKey('Category',on_delete=models.CASCADE,verbose_name='Категория Товара')
    photo = models.ImageField(upload_to='product_photos',verbose_name='Фото Товара')
    season = models.ForeignKey('Season',on_delete=models.CASCADE,verbose_name='Сезон Продукта',default=None)

    objects = models.Manager()
    get_product_queryset = ProductManager.as_manager()


    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def get_price(self):
        price = int(self.price) if int(self.price) == self.price else self.price
        return price

class Brands(models.Model):
    name = models.CharField(max_length=100,verbose_name='Наименование Бренда')
    img = models.ImageField(verbose_name='Логотип Бренда',upload_to='brand_photos',default=None)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

class Images(models.Model):
    image = models.ImageField(upload_to='product_photos',verbose_name='Фото Товара')
    product = models.ForeignKey('Product',verbose_name='Продукт',on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f'фото для товара {self.product.title}'

class CartProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Пользователь товара в корзине')
    product = models.ForeignKey('Product',on_delete=models.CASCADE,verbose_name='Продукт в корзине')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара в штуках')
    cart = models.ForeignKey('Cart',on_delete=models.CASCADE,verbose_name='Корзина Пользователя',related_name='product_for_cart')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'Товар {self.product.title} пользователя {self.user.username}'

    def final_price(self):
        price = self.product.get_price() * self.quantity
        return int(price) if int(price) == price else price

    def get_photo(self):
        return self.product.photo.url

    def get_title(self):
        return self.product.title

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Пользователь корзины')
    product = models.ManyToManyField('CartProduct',verbose_name='Товары в карзине',related_name='cart_for_cart_product',blank=True)

    class Meta:
        verbose_name = 'Корзина Пользователя'
        verbose_name_plural = 'Корзины Пользователей'

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

    def count_product_in_cart(self):
        count_product = self.product.count()
        return count_product

    def final_price(self):
        price = 0
        for product in self.product.all():
            price += product.final_price()

        return int(price) if int(price) == price else price



