from django.contrib import admin
from lmb_core.permission.models import PermissionGroup


class PermissionGroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'permission', 'group_name', 'is_active', 'user_level')

admin.site.register(PermissionGroup, PermissionGroupAdmin)
