from django.contrib import admin

from core.models import ApiKey


# Register your models here.


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    pass
