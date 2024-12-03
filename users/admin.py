from django.contrib import admin

from users.models import User, PhoneVerification, UserManager


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'name', 'role', 'is_active', 'created_at')


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_verification_code', 'created_at')


