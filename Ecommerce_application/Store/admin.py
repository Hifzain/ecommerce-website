from django.contrib import admin
from .models import Category, Product, Order, OrderItem, ReviewRating

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','email','city', 'address','total_price']


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order,ProductAdmin)  # ✅ Register OrderAdmin for custom order display
admin.site.register(OrderItem)  # ✅ Register OrderItemAdmin for list view
admin.site.register(ReviewRating)
