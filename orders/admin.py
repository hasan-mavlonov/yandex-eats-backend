from django.contrib import admin

from orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'branch', 'status', 'created_at')
    search_fields = ('client__name', 'branch__name', 'status')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'menu', 'quantity', 'price', 'created_at')
    search_fields = ('order__id', 'menu__name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
