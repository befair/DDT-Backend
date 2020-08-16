from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from api.models import Client, DDT, User, Pallet
from api import serializers


class DDTPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class DDTViewSet(ModelViewSet):
    queryset = DDT.objects.all()
    pagination_class = DDTPagination

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return serializers.DDTReadSerializer
        else:
            return serializers.DDTSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
