from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from lmb_core.customer.forms import Customer, CustomerCreationForm


class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm

    list_display = ('pk', 'email', 'is_active', 'is_email_verified', 'first_name', 'last_name', )
    list_filter = ('is_active', 'is_email_verified')
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

admin.site.register(Customer, CustomerAdmin)
