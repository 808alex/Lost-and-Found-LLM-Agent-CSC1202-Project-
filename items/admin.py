from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "kind", "status", "colour", "location", "date")
    list_filter = ("kind", "status")
    search_fields = ("description", "object_type", "brand", "location")
