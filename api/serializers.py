from rest_framework.serializers import ChoiceField, ModelSerializer
from . import models


class ContainerSerializer(ModelSerializer):
    class Meta:
        model = models.Container
        fields = ('type', 'count')


class DDTSerializer(ModelSerializer):
    containers = ContainerSerializer(many=True)

    class Meta:
        model = models.DDT
        fields = ('containers', 'client', 'date', 'photo')


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
