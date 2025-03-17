# utils.py
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_order_email_alert(customer_name, order_id, order_items, total_price, recipient_list):
    subject = f"New Order Placed: Order #{order_id}"
    message = (
        f"Dear Admin,\n\n"
        f"A new order has been placed by {customer_name}.\n"
        f"Order ID: {order_id}\n"
        f"Total Price: {total_price}\n\n"
        "Order Details:\n"
    )

    for item in order_items:
        message += f"- {item['product']} (Quantity: {item['quantity']}, Price: ${item['price']})\n"

    message += "\nPlease check the admin dashboard for more details."

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
        logger.info("Email sent successfully to %s", recipient_list)
        return True
    except Exception as e:
        logger.error("Error sending email: %s", e)
        return False



def send_order_confirmation_email(order):
    subject = 'Order Confirmation'
    message = (
        f"Dear {order.first_name} {order.last_name},\n\n"
        f"Thank you for your order!\n\n"
        f"Order ID: {order.id}\n"
        f"Total Price: {order.total_price}\n"
        f"Payment Mode: {order.payment_mode}\n"
        f"Address: {order.address}, {order.city}, {order.state}, {order.pincode}\n\n"
        f"Your order will be processed shortly.\n\n"
        f"Best regards,\n"
        f"SolarTech Green Energy Solution"
    )

    recipient_list = [order.email]  # Send to the customer's email
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Use the default sender email
            recipient_list,
            fail_silently=False
        )
    except Exception as e:
        
        print(f"Error sending email: {e}")  
