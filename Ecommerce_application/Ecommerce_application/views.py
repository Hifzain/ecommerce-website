from django.shortcuts import render
from . import views
from Account.models import *


def navbar(request):
    cart_count=userData.objects.all()
    context={'cart_count':cart_count}
    return render(request,'nav.html',context)

def footer(request):
    return render(request,'footer.html')
    
def base(request):
    return render(request, 'base.html')






