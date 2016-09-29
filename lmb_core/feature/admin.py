from django.contrib import admin
from lmb_core.feature.models import FeatureGroup, Feature


class FeatureGroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'feature_group_name', 'display_name', 'is_active', )
    ordering = ('feature_group_name', )

admin.site.register(FeatureGroup, FeatureGroupAdmin)
