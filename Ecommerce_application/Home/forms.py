from django import forms
from .models import ContactUs  # Import the model
import re

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs  # Specify the model
        fields = ['name', 'Email', 'message']  # Include all necessary fields

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match("^[A-Za-z]{3,15}$", name):  # Only letters, no spaces or numbers
            raise forms.ValidationError("Name must be 3-15 letters, without spaces or numbers.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not re.match("^[A-Za-z]{10,15}$", message):  # Only letters, no spaces or numbers
            raise forms.ValidationError("Name must be 10-15 letters, without spaces or numbers.")
        return message
