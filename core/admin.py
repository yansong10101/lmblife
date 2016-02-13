from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from core.models import University, FeatureGroup, Customer, OrgAdmin, PermissionGroup
from core.forms import OrgAdminCreateForm, CustomerCreationForm

admin.site.site_header = _('留美帮')
admin.site.site_title = _('留美帮')


class UniversityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'university_name', 'university_code', )
    ordering = ('university_name', )


class OrgUserAdmin(UserAdmin):
    add_form = OrgAdminCreateForm

    list_display = ('username', 'is_active', 'is_president', 'first_name', 'last_name', )
    list_filter = ('is_president', )
    fieldsets = (
        (None, {'fields': ('username', 'password', ), }),
        ('Personal info', {'fields': ('is_active', 'first_name', 'last_name', ), }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('university', 'username', 'password1', 'password2', 'first_name', 'last_name', )
        }),
    )
    search_fields = ('username', )
    ordering = ('username', )
    filter_horizontal = ()


class CustomerAdmin(UserAdmin):
    # form = CustomerChangeForm
    add_form = CustomerCreationForm

    list_display = ('pk', 'email', 'is_active', 'is_admin', 'first_name', 'last_name', )
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('email', 'password', ), }),
        ('Personal info', {'fields': ('first_name', 'last_name', ), }),
        # ('Permissions', {'fields': ('is_admin', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', )
        }),
    )
    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()


class PermissionGroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'group_name', 'is_org_admin', 'is_active', 'user_level', )
    filter_horizontal = ('permission', )
    ordering = ('group_name', )


class FeatureGroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'feature_name', )
    ordering = ('feature_name', )


admin.site.register(University, UniversityAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(OrgAdmin, OrgUserAdmin)
admin.site.register(PermissionGroup, PermissionGroupAdmin)
admin.site.register(FeatureGroup, FeatureGroupAdmin)
