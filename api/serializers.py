from rest_framework.serializers import ModelSerializer, ListSerializer
from rest_framework import serializers
from api.models import Container, DDT, User


class ContainerSerializer(ModelSerializer):
    class Meta:
        model = Container
        fields = ['type', 'count']

    def to_representation(self, instance):
        """Convert container type from key to String"""
        ret = super().to_representation(instance)
        ret['type'] = Container.KIND[ret['type']-1][1]
        return ret


class DDTSerializer(ModelSerializer):
    containers = serializers.JSONField()

    class Meta:
        model = DDT
        fields = ['containers', 'operator', 'client', 'date', 'photo']

    def create(self, validated_data):
        containers = validated_data.pop('containers')
        ddt = DDT.objects.create(**validated_data)

        for container in containers:
            c = ContainerSerializer(data=container)
            c.is_valid(raise_exception=True)
            Container.objects.create(
                ddt_id=ddt.pk,
                type=container['type'],
                count=container['count']
            )

        return ddt

    def to_representation(self, instance):
        """Convert containers to JSON"""
        a = []
        ret = super().to_representation(instance)

        for c in ret['containers'].all():
            a.append({"type": c.type, "count": c.count})
        ret['containers'] = a
        return ret


class DDTReadSerializer(ModelSerializer):
    containers = ContainerSerializer(many=True, read_only=True)

    class Meta:
        model = DDT
        fields = ['containers', 'operator', 'client', 'date', 'photo']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
