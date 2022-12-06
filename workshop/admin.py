from django.contrib import admin
from .models import Faq
from album.models import Artist


# Register your models here.
class FaqAdmin(admin.ModelAdmin):
    list_display = (
        'lang',
        'name',
        'description',
    )

admin.site.register(Faq, FaqAdmin)
