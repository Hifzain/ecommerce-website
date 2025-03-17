from Store.models import *
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from Store.models import Order, OrderItem
from Account.models import userData
from Store.models import Cart 



def about(request):
    return render(request,'about_us.html')

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            subject = "New Contact Form Submission"
            message = f"""
            You have a new message from your website:
            
            Name: {form.cleaned_data['name']}
            Email: {form.cleaned_data['Email']}
            Message: {form.cleaned_data['message']}
            """
            admin_email = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home') 
        else:
            messages.error(request, 'Please correct the errors below.')  
    return render(request, 'contact.html', {'form': form})



def search_products(request):
    query = request.GET.get('q')  # 'q' is the name of the search input field
    if query: 
        products = Product.objects.filter(product_name__icontains=query) # Partial match
        if products.exists(): 
            context = {'products': products}
            return render(request, 'search.html', context)
        else: 
            context = {'products': [], 'message': 'No products found for your search.'}
            return render(request, 'search.html', context)
    else:  
        context = {'products': [], 'message': 'Please enter a search term.'}
        return render(request, 'home.html', context)


   

def energy_calculator(request):
    return render(request, 'energy_calculator.html')


def orders(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = userData.objects.get(id=user_id)
        except userData.DoesNotExist:
            return JsonResponse({"status": "Invalid user. Please login again."})
        myorder = Order.objects.filter(user=user)
    else:
        myorder = None

    context = {'myorder': myorder}
    return render(request, 'orders.html', context)


def vieworder(request, created_at):
    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = userData.objects.get(id=user_id)
        except userData.DoesNotExist:
            return JsonResponse({"status": "Invalid user. Please login again."})
        order = Order.objects.filter(created_at=created_at, user=user).first()
        if order:
            orderitem = OrderItem.objects.filter(order=order)
            context = {'order': order, 'orderitem': orderitem}
            return render(request, 'vieworders.html', context)
        else:
            return JsonResponse({"status": "Order not found"}, status=404)
    else:
        return JsonResponse({"status": "Login to continue"}, status=401)  # User is not logged in


def order_list(request, status=None):
    if status == "completed":
        orders = Order.objects.filter(status="completed")
    elif status == "pending":
        orders = Order.objects.filter(status="pending")
    elif status == "cancel":
        orders = Order.objects.filter(status="cancel")
    else:
        orders = Order.objects.all()

    context = {
        "orders": orders,
        "status": status,
    }
    return render(request, "order_list.html", context)

def navbar(request):
    if request.user.is_authenticated: 
        cart_count = Cart.objects.filter(user=request.user)or 0
    else:
        cart_count = 0  
    context = {'cart_count': cart_count} 
    return render(request, 'nav.html', context)  





