from django.contrib.admin import ModelAdmin, register
from api.models import DDT, Container, Client, User


@register(DDT)
class DDTAdmin(ModelAdmin):
    icon_name = 'local_shipping'


@register(Client)
class ClientAdmin(ModelAdmin):
    icon_name = "euro_symbol"


@register(User)
class UserAdmin(ModelAdmin):
    icon_name = "people"
