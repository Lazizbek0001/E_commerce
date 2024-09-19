from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name='home'),
    path("about/", views.about, name='about'),
    path("login/", views.login_user, name='login'),
    path("logout/", views.logout_user, name='logout'),
    path("register/", views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path("product/<int:pk>", views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
]
