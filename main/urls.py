from django.urls import path
from .import views

urlpatterns = [
    path('', views.home),
    path('create', views.home_create),
    path('dashboard', views.dashboard),
    path('log', views.log_user),
    path('logout', views.logout),
    path('profile/<int:user_id>', views.profile),
    path('add_drink', views.add_drink),
    path('update_drinks/<int:drink_id>', views.update_drinks),
    path('update/<int:drink_id>', views.update),
    path('delete/<int:drink_id>', views.delete),
    path('cart', views.cart),
    path('add_cart', views.add_cart),
    path('checkout', views.checkout),
    path('success', views.success)
]