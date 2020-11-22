from django.contrib import admin
from import_export import resources, admin as import_export_admin
from . import models


class EventResource(resources.ModelResource):
    class Meta:
        model = models.Event
        import_id_fields = ('name', 'date')
        fields = ('name', 'date', 'street', 'city', 'country', 'link')
        widgets = {
            'date': {'format': '%Y-%m-%dT%H:%M:%S.%fZ'},
        }


class EventAdmin(import_export_admin.ImportExportModelAdmin):
    resource_class = EventResource
    list_display = ('name', 'date', 'link')
    ordering = ('-date',)


class CommuntityEventSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'source')


admin.site.register(models.Event, EventAdmin)
admin.site.register(models.CommunityEventSource, CommuntityEventSourceAdmin)
