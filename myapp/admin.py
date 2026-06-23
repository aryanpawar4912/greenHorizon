from django.contrib import admin
from .models import MobileApp

@admin.register(MobileApp)
class MobileAppAdmin(admin.ModelAdmin):
    list_display = ('apk_file', 'uploaded_at')

