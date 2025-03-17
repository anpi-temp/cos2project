from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_admin')
    list_filter = ('is_staff', 'is_active', 'is_admin')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_admin', 'phone_number')}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request)

admin.site.register(CustomUser, CustomUserAdmin)