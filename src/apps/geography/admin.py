from django.contrib import admin
from apps.geography.models import Country, City, Attribution


class AttributionInline(admin.TabularInline):
    model = Attribution


class CityAdmin(admin.ModelAdmin):
    inlines = [AttributionInline, ]
    list_display = ('long_name',)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
