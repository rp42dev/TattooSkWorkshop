from django.contrib import admin
from .models import About, AddMember, Faq
from album.models import Artist

# Register your models here.

class AddMemberAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class AboutAdmin(admin.ModelAdmin):
    list_display = (
        'member',
        'name',
        'order',
        'image',
    )


admin.site.register(About, AboutAdmin)
admin.site.register(AddMember, AddMemberAdmin)

# Register your models here.
class FaqAdmin(admin.ModelAdmin):
    list_display = (
        'lang',
        'name',
        'description',
    )

admin.site.register(Faq, FaqAdmin)
