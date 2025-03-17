from django.db import models

class ContactUs(models.Model):
    name=models.CharField(max_length=100)
    Email=models.EmailField()
    message=models.TextField()

    def __str__(self):
        return self.name
    

# Create your models here.
# models.py

