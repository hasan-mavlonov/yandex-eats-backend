from django.contrib import admin

from users.models import User, PhoneVerification, Menu


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'name', 'role', 'is_active', 'created_at')


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_verification_code', 'created_at')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'branch', 'created_by', 'created_at')
    search_fields = ('name', 'branch__name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


