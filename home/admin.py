from django.contrib import admin
from .models import Prices

# Register your models here.


class PricesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'description',
    )

admin.site.register(Prices, PricesAdmin)

