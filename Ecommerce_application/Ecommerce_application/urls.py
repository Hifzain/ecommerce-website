"""
URL configuration for Ecommerce_application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path  
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
  
    path('', views.base, name='base'), 
    path('', views.navbar, name='navbar'),
    path('', views.footer, name='footer'),
    path('', include('Home.urls')),
    path('', include('Store.urls')), 
    path('', include('Account.urls')),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # This is for serving media files during development