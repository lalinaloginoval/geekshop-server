from django.urls import path

from authapp.views import Login, Register, profile, logout

app_name = 'authapp'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
]
