from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView

from api.models import Container, DDT, User
from api import serializers


class DDTViewSet(viewsets.ModelViewSet):
    queryset = DDT.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return serializers.DDTReadSerializer
        else:
            return serializers.DDTSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
