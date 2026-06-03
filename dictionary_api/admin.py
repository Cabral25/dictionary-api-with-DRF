from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Word


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Word)
class AdminWord(admin.ModelAdmin):
    list_display = ('word', 'meaning', 'example', 'created_by')
    search_fields = ('word', 'created_by')
    ordering = ['word']

# Register your models here.
