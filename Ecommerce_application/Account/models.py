from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from Store.models import *
from django.db.models import Sum


class userData(models.Model):
   first_name = models.CharField(max_length=40)
   last_name=models.CharField(max_length=40)
   Phone = models.CharField(max_length=20)
   email = models.CharField(max_length=30,unique=True)
   password = models.CharField(max_length=128, default="")
   last_login = models.DateTimeField(null=True, blank=True)  



   def get_cart_count(self):
        return Cart.objects.filter(user=self).aggregate(total_items=Sum('product_qty'))['total_items'] or 0

   @staticmethod
   def get_email_field_name():
        """Return the name of the email field."""
        return 'Email'
   def set_password(self, raw_password):
        """Hash the password manually."""
        self.password = make_password(raw_password)

   def check_password(self, raw_password):
        """Check the hashed password."""
       
        return check_password(raw_password, self.password)
   def __str__(self):
        return self.email
  
