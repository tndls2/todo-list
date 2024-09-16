from django.contrib import admin
from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('user_name',)


admin.site.register(User, UserAdmin)
