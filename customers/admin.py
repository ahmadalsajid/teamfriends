from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ("name", "date_of_birth")


admin.site.register(Customer, CustomerAdmin)
