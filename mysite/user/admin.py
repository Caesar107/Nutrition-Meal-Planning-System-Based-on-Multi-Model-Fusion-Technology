from django.contrib import admin
from app.admin import BaseAdmin
from .models import *

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(BaseAdmin):
    list_display = ('user', 'gender', 'age')
    list_filter = ('user',)


@admin.register(HealthIndex)
class HealthIndexAdmin(BaseAdmin):
    list_display = (
        'id',
        'user',
        'date',
        'weight',
        'blood_sugar',
        'blood_pressure',
        'heart_rate',
    )
    list_filter = ('date', )