from django.contrib import admin
from .models import Flower, Order,PaidOrder


# Register your models here.

class FlowerAdmin(admin.ModelAdmin):
    list_display = ["name", "color", "quantity", "price"]




admin.site.register(Flower, FlowerAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['flower', 'user', ]

class PiadOrderAdmin(admin.ModelAdmin):
    list_display = ['id','flower','date' ,'user',]

admin.site.register(Order, OrderAdmin)
admin.site.register(PaidOrder, PiadOrderAdmin)


