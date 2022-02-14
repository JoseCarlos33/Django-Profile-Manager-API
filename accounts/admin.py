from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from django.contrib import admin

class User(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'current_city')
    list_display_links = ('name', 'email')
    search_fields = ('nanme','email')
    list_per_page = 10

admin.site.register(models.UserProfile, User)
admin.site.register(models.ResearchedCities)