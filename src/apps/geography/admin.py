from django.contrib import admin
from apps.geography.models import Country, City, Attribution


class AttributionInline(admin.TabularInline):
    model = Attribution


class CityAdmin(admin.ModelAdmin):
    inlines = [AttributionInline, ]

admin.site.register(Country)
admin.site.register(City, CityAdmin)
