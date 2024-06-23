from django.contrib import admin
from django.contrib.auth.models import User
from mysite.settings import ADMIN_SITE_HEADER, ADMIN_SITE_TITLE
from django.utils.html import format_html
from django.urls import reverse
from django.db import connection as conn
from .models import *

admin.site.site_header = ADMIN_SITE_HEADER
admin.site.site_title = ADMIN_SITE_TITLE

# Register your models here.

class BaseAdmin(admin.ModelAdmin):
    """
    Base admin class to be inherited by other admin classes
    """
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            if request.user.is_superuser:
                kwargs['queryset'] = User.objects.all()
            else:
                kwargs['queryset'] = User.objects.filter(id=request.user.id)
                kwargs['initial'] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.user != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.user != request.user:
            return False
        return super().has_delete_permission(request, obj)

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'rating',
        'calories',
        'protein',
        'fat',
        'sodium',
        'categories',
    )

