from django.shortcuts import render
from rest_framework import viewsets

from . import models
from . import serializers


class DDTViewSet(viewsets.ModelViewSet):
    queryset = models.DDT.objects.all()
    serializer_class = serializers.DDTSerializer

    def post(self, request):
        print(request)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
