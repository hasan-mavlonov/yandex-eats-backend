from django.contrib import admin

from business.models import Company, Branch


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
