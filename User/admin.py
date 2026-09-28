from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Country, CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'get_level',
        'first_name',
        'last_name',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

    list_filter = (
        'is_superuser',
        'is_staff',
        'is_active',
    )

    def get_level(self, obj):
        if obj.is_superuser:
            return 'ADMIN'
        return 'MEMBER'

    get_level.short_description = 'Level'


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
