# admin.py
from django.contrib import admin, messages
from .models import ContactUs  # Adjusted the model name to ContactUs if that's correct

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'Email', 'message')

    def response_change(self, request, obj):
        messages.success(request, "This message has been viewed.")
        return super().response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        messages.success(request, "A new contact message has been received.")
        return super().response_add(request, obj, post_url_continue)

admin.site.register(ContactUs, ContactUsAdmin)
