from django.contrib.admin import ModelAdmin, TabularInline, register
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.urls import path

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
    readonly_fields = ['creation_time']
    list_display = ['__str__', 'client', 'date', 'creation_time']

    list_filter = ('date', 'client__corporate_name')

    inlines = [PalletInline]


@register(models.AppUser)
class AppUserAdmin(ModelAdmin):
    icon_name = "people"
    list_display = ['__str__', 'email', 'user_kind']
    fields = ['first_name', 'last_name', 'email', 'user_kind']

    search_fields = ['first_name', 'last_name', 'email']


@register(models.DataExport)
class DataExportAdmin(ModelAdmin):
    icon_name = 'cloud_download'
    page_form_template = 'data_export/form_page.html'
    page_result_template = 'data_export/page.html'

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        return [
            path('', self.page_view, name='%s_%s_changelist' % info),
            path('result', self.page_result_view, name='%s_%s_result' % info),
        ]

    def page_view(self, request):
        self._check_permissions(request)
        context = self._get_context(request)
        return TemplateResponse(request, self.page_form_template, context)

    def page_result_view(self, request):
        self._check_permissions(request)
        context = self._get_context(request)
        return TemplateResponse(request, self.page_result_template, context)

    def _check_permissions(self, request):
        if not self.has_view_or_change_permission(request):
            raise PermissionDenied

    def _get_context(self, request):
        return dict(
            self.admin_site.each_context(request),
            title='Page',
        )
