from django.contrib.admin import ModelAdmin, TabularInline, register
from api import models


class PalletInline(TabularInline):
    model = models.Pallet


@register(models.Client)
class ClientAdmin(ModelAdmin):
    icon_name = "euro_symbol"
    search_fields = ['corporate_name']


@register(models.DDT)
class DDTAdmin(ModelAdmin):
    icon_name = 'local_shipping'
    search_fields = ['date']
    list_filter = ['client']

    inlines = [PalletInline]


@register(models.User)
class UserAdmin(ModelAdmin):
    icon_name = "people"
    search_fields = ['name', 'surname', 'email']
    exclude = ['id']
