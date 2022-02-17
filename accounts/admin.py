from django.contrib import admin
from . import models

class User(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'current_city')
    list_display_links = ('name', 'email')
    search_fields = ('name','email')
    list_per_page = 10

class Search(admin.ModelAdmin):
    list_display = ('id', 'city_name', 'user')
    list_display_links = ('city_name', 'id')
    search_fields = ('city_name', 'user')
    list_per_page = 10

admin.site.register(models.UserProfile, User)
admin.site.register(models.ResearchedCities, Search)