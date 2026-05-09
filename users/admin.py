from django.contrib import admin

from .models import User, ClientMessage

@admin.register(User)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('phone', 'full_name', "updated_at")
    search_fields = ('full_name', 'phone')

@admin.register(ClientMessage)
class LineUpAdmin(admin.ModelAdmin):
    list_display = ('status', "client", "title", "updated_at", "deadline_at")
    search_fields = ("status", "client", "title")
