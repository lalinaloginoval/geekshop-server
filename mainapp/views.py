from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView


def get_categories():
    if settings.LOW_CACHE:
        key = 'categories'
        categories = cache.get(key)
        if categories is None:
            categories = ProductCategory.objects.all()
            cache.set(key, categories)
        return categories
    else:
        return ProductCategory.objects.all()


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


class ProductView(ListView):
    model = Product
    template_name = 'mainapp/products.html'
    paginate_by = 3

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ProductView, self).get_context_data()

        context.update({'title': 'GeekShop - Каталог', 'categories': get_categories()})
        category_id = self.kwargs.get('category_id')

        if settings.LOW_CACHE:
            key = 'products'
            products = cache.get(key)
            if products is None:
                products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
                cache.set(key, products)
        else:
            products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

        paginator = Paginator(products, per_page=self.paginate_by)
        try:
            products_paginator = paginator.page(self.kwargs.get('page'))
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context.update({'products': products_paginator})
        return context
