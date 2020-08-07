from django.contrib import admin
from api.models import DDT, Container, Client, User


class DDTAdmin(admin.ModelAdmin):
    pass


class ClientAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(DDT, DDTAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(User, UserAdmin)