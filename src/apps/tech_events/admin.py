from django.contrib import admin
from apps.tech_events.models import MeetupGroup, TechEvent, ParseError


def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
make_inactive.short_description = "Mark selected events inactive"

class MeetupGroupAdmin(admin.ModelAdmin):
    exclude      = ('name','location',)
    list_display = ('name','url') 
    list_filter  = ('is_blacklisted',)
    search_fields = ['name','url']

class TechEventAdmin(admin.ModelAdmin):
    search_fields = ['url','name']
    list_filter   = ('is_active',)
    actions       = [make_inactive]



admin.site.register(MeetupGroup, MeetupGroupAdmin)
admin.site.register(TechEvent, TechEventAdmin)
admin.site.register(ParseError)
