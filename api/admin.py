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
    search_fields = ['serial']
    list_display = ['__str__', 'client', 'date']

    list_filter = ('date', 'client__corporate_name')

    inlines = [PalletInline]


@register(models.User)
class UserAdmin(ModelAdmin):
    icon_name = "people"
    list_display = ['__str__', 'email', 'user_kind']
    exclude = ['id']

    search_fields = ['name', 'surname', 'email']
