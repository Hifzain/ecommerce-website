from django import forms
from .models import *
from django.core.exceptions import ValidationError


class ReviewRatingForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rateing']  
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review here...'}),
            'rateing': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }


class OrderFilterForm(forms.Form):
    ORDER_STATUS_CHOICES = [
        ('all', 'All'),
        ('pending', 'Pending'),
        ('cancel', 'cancel'),
        ('completed', 'Completed'),
    ]
    status = forms.ChoiceField(choices=ORDER_STATUS_CHOICES, required=False)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone_no = forms.CharField(max_length=12, required=True)
    address = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.ChoiceField(
        choices=[
            ("", "Select State/Province"),
            ("Punjab", "Punjab"),
            ("KPK", "KPK"),
            ("Balochistan", "Balochistan"),
            ("Sindh", "Sindh"),
            ("AJK", "AJK"),
            ("GB", "GB"),
        ],
        required=True,
    )
    pincode = forms.CharField(max_length=6, required=True)
    payment_mode = forms.ChoiceField(
        choices=[
            ("", "Select Payment Mode"),
            ("COD", "Cash on Delivery"),
        ],
        required=True,
    )

   