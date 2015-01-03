from django.contrib import admin
from apps.tech_events.models import MeetupGroup, TechEvent, ParseError


class MeetupGroupAdmin(admin.ModelAdmin):
    exclude      = ('name','location',)
    list_display = ('name','url') 
    list_filter  = ('is_blacklisted',)
    search_fields = ['name','url']


admin.site.register(MeetupGroup, MeetupGroupAdmin)
admin.site.register(TechEvent)
admin.site.register(ParseError)
