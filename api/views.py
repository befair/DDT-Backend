from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import DDT, AppUser, Client, Pallet
from api.serializers import (AppUserSerializer, ClientSerializer,
                             DDTReadSerializer, DDTSerializer)


class DDTPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class DDTViewSet(ModelViewSet):
    queryset = DDT.objects.all()
    pagination_class = DDTPagination
    filter_backends = [OrderingFilter]
    ordering = ['-date']

    def get_queryset(self):
        queryset = DDT.objects.all()

        # Filter by client
        client = self.request.query_params.get('client', None)
        if client is not None:
            queryset = queryset.filter(client_id=client)

        # Filter by operator
        operator = self.request.query_params.get('operator', None)
        if operator is not None:
            queryset = queryset.filter(operator_id=operator)

        # Filter by date
        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)
        if from_date and to_date:
            queryset = queryset.filter(date__range=[from_date, to_date])

        return queryset

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


class OTPLoginView(APIView):
    def post(self, request):
        otp = request.data.get('OTP', False)

        if otp:
            try:
                user = User.objects.get(otp=otp)
            except User.DoesNotExist:
                return Response({'error': "User not found"}, 404)

            rv = UserSerializer(user)

            # Deactivate OTP
            user.otp = ""
            user.save()

            return Response(rv.data)
        else:
            return Response({'error': "OTP not found"}, 400)
