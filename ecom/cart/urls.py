from . import views
from django.urls import path

urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('add/', views.cart_add, name='cart_add'),
    path('update/', views.cart_update, name='cart_update'),
]