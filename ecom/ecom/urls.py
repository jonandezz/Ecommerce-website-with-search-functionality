"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name= 'register'),
    path('login/', auth_view.LoginView.as_view(template_name='registration/login.html'), name= 'login'),
    path('products/', views.product_list_view, name='products'),
    path('updateItem/', views.updateItem, name='updateItem' ),
    path('checkout/', views.checkout, name='checkout' ),
    path('processOrder/', views.processOrder, name='processOrder' ),
    path('cart/', views.cart, name= 'cart'),
    
    path('accounts/', include('django_registration.backends.activation.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

