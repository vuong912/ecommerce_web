from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.get_cart, name='get_cart'),
]