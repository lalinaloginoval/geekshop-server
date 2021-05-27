from django.urls import path

from mainapp.views import ProductView

app_name = 'mainapp'

urlpatterns = [
    path('', ProductView.as_view(), name='index'),
    path('<int:category_id>/', ProductView.as_view(), name='product'),
    path('page/<int:page>/', ProductView.as_view(), name='page')
]