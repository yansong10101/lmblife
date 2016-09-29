from django.contrib import admin
from lmb_core.university.models import University


class UniversityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'handle', 'university_code', 'display_name', 'is_active', )
    ordering = ('handle', )

admin.site.register(University, UniversityAdmin)
