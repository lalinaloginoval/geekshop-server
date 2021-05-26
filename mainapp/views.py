from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)


class ProductView(ListView):
    model = Product
    template_name = 'mainapp/products.html'
    paginate_by = 3

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ProductView, self).get_context_data()

        context.update({'title': 'GeekShop - Каталог', 'categories': ProductCategory.objects.all()})
        category_id = self.kwargs.get('category_id')
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