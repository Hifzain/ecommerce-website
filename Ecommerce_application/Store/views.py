from .models import *
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import random
from .forms import ReviewRatingForm
from Store.models import ReviewRating
from django.db.models import Sum, Count
from .forms import OrderFilterForm
from django.utils import timezone
from datetime import datetime
from .utils import send_order_confirmation_email
from Account.models import userData

def home(request):
    home_category=Category.objects.all()
    trending_products=Product.objects.filter(trending=1)
    context={'home_category':home_category,'trending_products':trending_products}
    return render(request,'home.html',context)

def category(request):
    category=Category.objects.all()
    context={'category':category}
    return render(request, 'category.html',context)


def products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    trending_products = Product.objects.filter(trending=1, category=category)
    
    context = {
        'category_name': category,
        'products': products,
        'trending_products': trending_products,  
    }
    return render(request, "products.html", context)


def productview(request, catg_slug, prod_slug):
    category = get_object_or_404(Category, slug=catg_slug)
    product = get_object_or_404(Product, slug=prod_slug, status=False, category=category)
    reviews = ReviewRating.objects.filter(product=product, status=0)

    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = userData.objects.get(id=user_id)
            except userData.DoesNotExist:
                messages.error(request, 'Invalid user. Please login again.')
                return redirect('login')

            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                if ReviewRating.objects.filter(product=product, user=user).exists():
                    messages.error(request, 'You have already reviewed this product.')
                    return redirect('productview', catg_slug=catg_slug, prod_slug=prod_slug)

                review = form.save(commit=False)
                review.product = product
                review.user = user
                review.save()
                messages.success(request, 'Thank you for your review!')
                return redirect('productview', catg_slug=catg_slug, prod_slug=prod_slug)
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            messages.error(request, 'You must be logged in to write a review.')
            return redirect('login')
    else:
        form = ReviewRating()

    context = {
        'prod': product,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'products_details.html', context)

def addtocart(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({"status": "Login to continue"})

        try:
            user = userData.objects.get(id=user_id)
        except userData.DoesNotExist:
            return JsonResponse({"status": "Invalid user. Please login again."})

        prod_id = request.POST.get('product_id')
        prod_qty = request.POST.get('product_qty')

        try:
            prod_id = int(prod_id)
            prod_qty = int(prod_qty)
        except (ValueError, TypeError):
            return JsonResponse({"status": "Invalid product ID or quantity"})
        if prod_qty <= 0:
            return JsonResponse({"status": "Quantity must be at least 1"})
        try:
            product_check = Product.objects.get(id=prod_id)
        except Product.DoesNotExist:
            return JsonResponse({"status": "No such product found"})

        if product_check.product_quantity == 0:
            return JsonResponse({"status": "This product is out of stock!"})

        if Cart.objects.filter(user=user, product_id=prod_id).exists():
            return JsonResponse({"status": "Product already in cart"})

        if product_check.product_quantity >= prod_qty:
            Cart.objects.create(user=user, product=product_check, product_qty=prod_qty)
            return JsonResponse({"status": "Product added successfully"})
        else:
            return JsonResponse({"status": f"Only {product_check.product_quantity} quantity left"})

    return JsonResponse({"status": "Invalid request method"})



def viewcart(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = userData.objects.get(id=user_id)
        except userData.DoesNotExist:
            messages.error(request, "Invalid user session. Please login again.")
            return redirect('login')
        
        cart = Cart.objects.filter(user=user)
        context = {'cart': cart}
        return render(request, 'viewcart.html', context)
    else:
        messages.error(request, "You need to login to view your cart.")
        return redirect('login')

def updatecart(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return JsonResponse({'status': 'Login to continue'}, status=401)

    try:
        user = userData.objects.get(id=user_id)
    except userData.DoesNotExist:
        return JsonResponse({"status": "Invalid user. Please login again."}, status=400)

    if request.method == 'POST':
        try:
            prod_id = int(request.POST.get('product_id', 0))  
            prod_qty = int(request.POST.get('product_qty', 1))  
        except ValueError:
            return JsonResponse({'status': 'Invalid product data'}, status=400)

        cart = get_object_or_404(Cart, product_id=prod_id, user=user)

        if cart.product.product_quantity >= prod_qty:
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status': 'Quantity updated', 'new_quantity': cart.product_qty})
        else:
            return JsonResponse({'status': f'Only {cart.product.product_quantity} items available'}, status=400)

    return JsonResponse({'status': 'Invalid request'}, status=400)

def deletecartitem(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = userData.objects.get(id=user_id)
        except userData.DoesNotExist:
            return JsonResponse({"status": "Invalid user. Please login again."})

        if request.method == 'POST':
            prod_id = int(request.POST.get('product_id'))
            
            if Cart.objects.filter(user=user, product_id=prod_id).exists():
                cartitem = Cart.objects.get(product_id=prod_id, user=user)
                cartitem.delete()
                return JsonResponse({'status': 'deleted successfully'})
            else:
                return JsonResponse({'status': 'Product not found in cart'}, status=404)
    else:
        return JsonResponse({'status': 'Login to continue'}, status=401)  

    return JsonResponse({'status': 'Invalid request'}, status=400)

from decimal import Decimal

def checkout(request):
    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = userData.objects.get(id=user_id)
        except userData.DoesNotExist:
            return JsonResponse({"status": "Invalid user. Please login again."})

        cart = Cart.objects.filter(user=user)

        if not cart.exists():
            messages.error(request, "Your cart is empty. Please add items to the cart.")
            return redirect('home')

        total_price = Decimal(0)
        items_to_delete = []

        for item in cart:
            if item.product_qty > item.product.product_quantity:
                items_to_delete.append(item.id)
            else:
                total_price += item.product.discounted_price * Decimal(item.product_qty)
        if items_to_delete:
            Cart.objects.filter(id__in=items_to_delete).delete()

        tax_rate = Decimal('0.05') 
        tax_amount = total_price * tax_rate
        total_price_with_tax = total_price + tax_amount

        context = {
            'cartitems': cart,
            'total_price': total_price.quantize(Decimal('0.01')), 
            'tax_amount': tax_amount.quantize(Decimal('0.01')),
            'total_price_with_tax': total_price_with_tax.quantize(Decimal('0.01')),
            'first_name': user.first_name,
            'email': user.email,
            'Phone': user.Phone,
            'last_name': user.last_name,
        }
        return render(request, 'checkout.html', context)

    else:
        messages.error(request, "Please log in to continue to checkout.")
        return redirect('login')



def placeorder(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "Please log in to place an order.")
            return redirect('login')
        try:
            user = userData.objects.get(id=user_id)
        except userData.DoesNotExist:
            messages.error(request, "Invalid user. Please log in again.")
            return redirect('login')

        neworder = Order()
        neworder.user = user
        neworder.first_name = request.POST.get('first_name')
        neworder.last_name = request.POST.get('last_name')
        neworder.email = request.POST.get('email')
        neworder.phone_no = request.POST.get('phone_no')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')
        neworder.message = request.POST.get('message')
       
        cart_items = Cart.objects.filter(user=user)
        cart_total_price = sum(item.product.discounted_price * item.product_qty for item in cart_items)
        neworder.total_price = cart_total_price    

        neworder.save()  
        # This creates a new entry in the OrderItem table for each product in the cart.
        for item in cart_items:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.discounted_price,
                quantity=item.product_qty
            )
            product = Product.objects.get(id=item.product.id)
            product.product_quantity -= item.product_qty
            product.save()

        # Clear the user's cart after placing the order
        Cart.objects.filter(user=user).delete()

        messages.success(request, "Your order has been placed successfully.")
        
        send_order_confirmation_email(neworder)

        return redirect('home')  
    return redirect('home')

from django.db.models.functions import TruncDate


from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
     return user.is_superuser  

@login_required  
@user_passes_test(is_admin)  

def dashboard(request):
    form = OrderFilterForm(request.GET or None)
    orders = Order.objects.all()
    product=Product.objects.all()
    status = request.GET.get('status', 'all')

    total_quantity = sum(product.product_quantity for product in product)
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        if status and status != 'all':
            orders = orders.filter(status=status)
        if start_date:
            orders = orders.filter(created_at__gte=timezone.make_aware(datetime.combine(start_date, datetime.min.time())))
        if end_date:
            orders = orders.filter(created_at__lte=timezone.make_aware(datetime.combine(end_date, datetime.max.time())))

    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status='completed').count()
    pending_orders = Order.objects.filter(status='pending').count()
    cancel_orders = Order.objects.filter(status='cancel').count()

    today = timezone.now()
    sales_today = orders.filter(created_at__date=today.date()).count()
    sales_this_week = orders.filter(created_at__gte=today - timezone.timedelta(days=7)).count()
    sales_this_month = orders.filter(created_at__month=today.month, created_at__year=today.year).count()
    sales_this_year = orders.filter(created_at__year=today.year).count()

    revenue_today = orders.filter(created_at__date=today.date()).aggregate(Sum('total_price'))['total_price__sum'] or 0
    revenue_this_week = orders.filter(created_at__gte=today - timezone.timedelta(days=7)).aggregate(Sum('total_price'))['total_price__sum'] or 0
    revenue_this_month = orders.filter(created_at__month=today.month, created_at__year=today.year).aggregate(Sum('total_price'))['total_price__sum'] or 0
    revenue_this_year = orders.filter(created_at__year=today.year).aggregate(Sum('total_price'))['total_price__sum'] or 0

    context = {
        'form': form,
        'orders': orders,  
        'status': status,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'cancel_orders': cancel_orders,
        'sales_today': sales_today,
        'sales_this_week': sales_this_week,
        'sales_this_month': sales_this_month,
        'sales_this_year': sales_this_year,
        'revenue_today': revenue_today,
        'revenue_this_week': revenue_this_week,
        'revenue_this_month': revenue_this_month,
        'revenue_this_year': revenue_this_year,
        'product': product,
        'total_quantity':total_quantity
    }
    return render(request, 'sales_report.html', context)
