from django.contrib import admin
from .models import TrafficDivider, Experiment

class TrafficDividerAdmin(admin.ModelAdmin):
    fields = ('page_title',)

class ExperimentAdmin(admin.ModelAdmin):
    list_display = ['page_title', 'divider', 'is_active']
    list_filter = ['page_title', 'divider', 'is_active']
    fieldsets = (
        ('Default page', {
            'fields': ('сonversion', 'entered', 'success'),
        }),
        ('Alternative page', {
            'fields': ('alternative_сonversion', 'alternative_entered', 'alternative_success'),
        }),
        ('Settings', {
            'classes': ('collapse',),
            'fields': ('page_title', 'divider', 'is_editable', 'is_active')
        }),
    )
    readonly_fields = ('page_title', 'entered', 'success', 'сonversion', 'alternative_entered', 'alternative_success', 'alternative_сonversion', 'divider')

    # toggle editable
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.is_editable == False:
                return ['page_title', 'entered', 'success', 'сonversion', 'alternative_entered', 'alternative_success', 'alternative_сonversion', 'divider']
            else:
                return []
        else:
            return ['entered', 'success', 'сonversion', 'alternative_entered', 'alternative_success', 'alternative_сonversion', 'is_editable']


admin.site.register(TrafficDivider, TrafficDividerAdmin)
admin.site.register(Experiment, ExperimentAdmin)
