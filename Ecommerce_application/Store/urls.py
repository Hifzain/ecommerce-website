# cart/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'), 
    path('category/', views.category, name='category'),
    path('products/<str:slug>/', views.products, name='products'),
    path('products/<str:catg_slug>/<str:prod_slug>', views.productview, name='productview'),
    path('add-to-cart', views.addtocart, name='addtocart'),
    path('cart', views.viewcart, name='cart'),
    path('delete-cart-item', views.deletecartitem, name='deletecartitem'),
    path('checkout', views.checkout, name='checkout'),
    path('placeorder', views.placeorder, name="placeorder"),
    path('update-cart', views.updatecart, name="updatecart"),
    path('dashboard/', views.dashboard, name='dashboard'),
]
