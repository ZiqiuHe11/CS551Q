from django.contrib import admin
from .models import Star, Order, UserProfile

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('name', 'constellation', 'magnitude')
    search_fields = ('name', 'constellation')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name_given', 'star', 'user', 'status', 'date_ordered')
    list_filter = ('status', 'date_ordered')
    search_fields = ('name_given', 'star__name', 'user__username')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username',)

