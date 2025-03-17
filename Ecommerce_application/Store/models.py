from django.db import models
from Account.models import userData

class Category(models.Model):
    slug=models.CharField(max_length=100, null=False)
    category_name=models.CharField(max_length=100, null=False)
    category_description=models.TextField(null=False)
    category_image=models.ImageField(null=False, upload_to="images/")
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.category_name

class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    slug=models.CharField(max_length=100, null=False)
    product_name=models.CharField(max_length=100, null=False)
    product_image=models.ImageField(null=False, upload_to="images/")
    product_description=models.TextField(null=False)
    original_price = models.DecimalField(max_digits=10, decimal_places=2 ,blank=True, null=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    product_details=models.TextField(null=False)
    status=models.BooleanField(default=False, help_text="0=default , 1=Hidden")
    product_quantity=models.IntegerField(default=0)
    trending=models.BooleanField(default=False, help_text="0=default , 1=Trending")
    created_at = models.DateTimeField(auto_now_add=True)
    num_panels = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return self.product_name
    @property
    def discount_percentage(self):
        if self.original_price and self.discounted_price:
            if self.original_price > self.discounted_price:
                discount = (self.original_price - self.discounted_price) / self.original_price * 100
                return round(discount)
        return 0

      
class Cart(models.Model):
    user = models.ForeignKey(userData, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user=models.ForeignKey(userData,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100, null=False)
    last_name=models.CharField(max_length=100,null=False)
    email=models.CharField(max_length=100, null=False)
    address=models.CharField(max_length=100, null=False)
    city=models.CharField(max_length=100, null=False)
    phone_no=models.CharField(max_length=15, null=True)
    state=models.CharField(max_length=100, null=True)
    pincode=models.CharField(max_length=100, null=False)
    total_price=models.CharField(max_length=100, null=False)
    payment_mode=models.CharField(max_length=100, null=False)   
    orderstatus=(
        ('pending','pending'),
        ('cancel','cancel'),
        ('completed','completed'),
    )   
    status=models.CharField(max_length=100, choices=orderstatus, default='pending')   
    message=models.TextField(null=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now=True)
    tracking_no=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.first_name)

class OrderItem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    price=models.FloatField(null=False)
    quantity=models.IntegerField(null=False)
    
    def __str__(self):
        return '{} - {} - {}'.format(self.order.id, self.order.first_name,self.order.last_name)
    
class ReviewRating(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(userData,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=500,blank=True)
    rateing=models.IntegerField()
    status=models.BooleanField(default=False, help_text="0=default , 1=Hidden")
    updated_at=models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    