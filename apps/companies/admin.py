from django.contrib import admin
from apps.companies.models import Category, Company, Stage

class CompanyAdmin(admin.ModelAdmin):
    filter_horizontal = ('cities',)

# Register your models here.
admin.site.register(Category)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Stage)
