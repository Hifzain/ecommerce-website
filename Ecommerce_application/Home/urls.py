from django.urls import path
from . import views



urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search_products, name='search_products'),
    path('energy-calculator/', views.energy_calculator, name='energy_calculator'),
    path('orders', views.orders, name='orders'),
    path('ordersview/<str:created_at>', views.vieworder, name='vieworders'), #we can give any varible name in <str:##>
    path("orders/<str:status>/", views.order_list, name="order_list"),
    path("orders/", views.order_list, name="all_orders"),
   
    
]





