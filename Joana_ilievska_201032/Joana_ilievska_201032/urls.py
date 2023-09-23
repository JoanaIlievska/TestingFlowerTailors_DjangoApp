"""Joana_ilievska_201032 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView

from FlowerShopApp.views import index,products,basket,delete_order,customer_registration_view,customer_login_view,ordered,notavailable,AboutUs

urlpatterns = [
    path('', customer_registration_view, name='register'),
    path('admin/', admin.site.urls),

    path('index/',index,name='index'),
    path('index/products/',products,name='products'),
    path('products/', products, name='products'),
    path('basket/', basket, name='basket'),
    path('delete_order/<int:order_id>/', delete_order, name='delete_order'),
    path('registration/', customer_registration_view, name='registration'),
    path('login/', customer_login_view, name='login'),
    path('basket/thankyou/',ordered,name='thankyou'),
    path('basket/Notavailable/', notavailable, name='Notavailable'),
    path('AboutUs/',AboutUs,name='AboutUs'),

              ]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
