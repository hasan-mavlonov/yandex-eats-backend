from django.contrib import admin

from business.models import Company, Branch

from django.contrib import admin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by_name', 'manager_name', 'created_at', 'updated_at')


admin.site.register(Company, CompanyAdmin)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'manager', 'active', 'latitude', 'longitude', 'created_at')
    search_fields = ('name', 'company__name', 'manager__name')
    list_filter = ('active', 'created_at')
    ordering = ('-created_at',)
