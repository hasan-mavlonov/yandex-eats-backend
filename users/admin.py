from django.contrib import admin

from users.models import User, PhoneVerification, UserManager, Delivery, OrderItem, Order, Menu, Branch, Company


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'name', 'role', 'is_active', 'created_at')


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_verification_code', 'created_at')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'manager', 'active', 'latitude', 'longitude', 'created_at')
    search_fields = ('name', 'company__name', 'manager__name')
    list_filter = ('active', 'created_at')
    ordering = ('-created_at',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'branch', 'created_by', 'created_at')
    search_fields = ('name', 'branch__name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


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


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'delivery_person', 'status', 'assigned_at', 'completed_at')
    search_fields = ('order__id', 'delivery_person__name', 'status')
    list_filter = ('status', 'assigned_at', 'completed_at')
    ordering = ('-assigned_at',)
