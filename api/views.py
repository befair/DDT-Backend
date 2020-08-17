from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import ClientSerializer, DDTReadSerializer, DDTSerializer
from api.models import DDT, Client, Pallet, User


class DDTPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class DDTViewSet(ModelViewSet):
    queryset = DDT.objects.all()
    pagination_class = DDTPagination

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return DDTReadSerializer
        else:
            return DDTSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class PalletMapView(APIView):
    def get(self, request):
        rv = {k[0]: k[1] for k in Pallet.KIND}
        return Response(rv)
