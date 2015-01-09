from django.contrib import admin
from apps.companies.models import Category, Company

# Register your models here.
admin.site.register(Category)
admin.site.register(Company)
