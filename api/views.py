import os

from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.exporter import export_xlsx
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

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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


class PalletMapView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rv = {k[0]: k[1] for k in Pallet.KIND}
        return Response(rv)


class ClientViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class OperatorsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        operators = AppUser.objects.filter(user_kind='OP')
        rv = AppUserSerializer(operators, many=True).data
        return Response(rv)


class OperatorDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            operator = AppUser.objects.get(pk=pk)
            rv = AppUserSerializer(operator).data
            return Response(rv)
        except AppUser.DoesNotExist:
            return Response({"error": "Operator not found"}, 404)


class ExportDDTView(APIView):
    def get(self, request):
        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)

        if from_date and to_date:
            # Ensure 'report' directory exists
            if not os.path.exists('reports'):
                os.mkdir('reports')

            filename = f"reports/report_{from_date}_{to_date}.xlsx"

            # Retrive DDTS
            queryset = DDT.objects.filter(date__range=[from_date, to_date]).order_by('pk')

            # Create XLSX
            export_xlsx(queryset, filename)

            with open(filename, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = f"inline; filename={os.path.basename(filename)}"
                return response
        else:
            return Response({'error': "Invalid date"}, 401)


class RegistrationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # If email is not used by another account
        if not AppUser.objects.filter(email=request.data['email']):
            # Validate fields
            s = AppUserSerializer(data=request.data)
            s.is_valid(raise_exception=True)

            try:
                # Create account
                user = AppUser.objects.create(
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    email=request.data['email']
                )
            except KeyError:
                return Response({'error': "Invalid request"}, 401)

            # Send OTP through mail to new user
            print(user.otp)
            return Response({'success': "Account created"})
        else:
            return Response({'error': "Email already in use"}, 401)


class LoginView(APIView):
    def post(self, request):
        try:
            user = AppUser.objects.get(otp=request.data.get('OTP', ''))
        except AppUser.DoesNotExist:
            return Response({'error': "User not found"}, 404)

        if user and not user.otp_used:
            # Get serialized data to a JSON
            s = AppUserSerializer(user).data
            rv = {a: s[a] for a in s}

            # Create authentication token
            try:
                token = Token.objects.create(user=user)
            except IntegrityError:
                token = Token.objects.get(user=user)
                token.delete()
                token = Token.objects.create(user=user)

            rv['auth_token'] = token.key

            # Deactivate OTP
            user.otp_used = True
            user.save()

            return Response(rv)
        else:
            return Response({'error': "OTP already used"}, 401)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'success': "Token revoked"})


class TokenCheckView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = AppUser.objects.get(pk=request.user.pk)
        except AppUser.DoesNotExist:
            return Response({'error': "Invalid token"})
        else:
            rv = {"error"}
            s = AppUserSerializer(user).data
            rv = {a: s[a] for a in s}

            return Response(rv)


class OTPResetView(APIView):
    def post(self, request):
        for user in AppUser.objects.filter(email=request.data.get('email')):
            user.reset_otp()

        return Response({'success': "Email sent"})
