from django.db import models
import random

class ProductManager(models.QuerySet):

    def get_queryset_for_new_collection_product(self):
        return self.only('title', 'price', 'photo').filter(season__season_status='new')

    def get_random_list_for_new_collection_product(self):
        products = random.sample(list(self.get_queryset_for_new_collection_product()), 3)
        return products

    def get_all_products(self):
        return self.only('title', 'price', 'photo').all()

    def get_queryset_for_recommended_product(self):
        return self.only('title', 'price', 'photo').filter(season__season_status='recommended')

class ProductDataMixin:

    def get_context(self,**kwargs):
        base_context = kwargs
        base_context['title'] = 'Man Shop'
        return base_context
