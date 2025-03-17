# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderItem
from .utils import send_order_email_alert
@receiver(post_save, sender=Order)
def send_order_alert(sender, instance, created, **kwargs):
    if created:
        customer_name = f"{instance.first_name} {instance.last_name}"
        order_id = instance.id
        total_price = instance.total_price

        order_items = [
            {"name": item.product.product_name, "quantity": item.quantity, "price": item.price}
            for item in OrderItem.objects.filter(order=instance)
        ]

        recipient_list = ['syedhifzain124213@gmail.com']  # Replace with the admin email
        success = send_order_email_alert(customer_name, order_id, order_items, total_price, recipient_list)

        if success:
            print("Email sent successfully")
        else:
            print("Failed to send email")

