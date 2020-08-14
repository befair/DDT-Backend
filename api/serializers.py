from rest_framework.serializers import ModelSerializer, ListSerializer
from rest_framework import serializers
from api.models import Pallet, DDT, User


class PalletSerializer(ModelSerializer):
    class Meta:
        model = Pallet
        fields = ['type', 'count']

    def to_representation(self, instance):
        """Convert pallet type from key to String"""
        ret = super().to_representation(instance)
        ret['type'] = Pallet.KIND[ret['type']-1][1]
        return ret


class DDTSerializer(ModelSerializer):
    pallets = serializers.JSONField()

    class Meta:
        model = DDT
        fields = ['pallets', 'operator', 'client', 'date', 'photo']

    def create(self, validated_data):
        pallets = validated_data.pop('pallets')
        ddt = DDT.objects.create(**validated_data)

        for pallet in pallets:
            p = PalletSerializer(data=pallet)
            p.is_valid(raise_exception=True)
            Pallet.objects.create(
                ddt_id=ddt.pk,
                type=pallet['type'],
                count=pallet['count']
            )

        return ddt

    def to_representation(self, instance):
        """Convert pallets to JSON"""
        # a = []
        ret = super().to_representation(instance)
        # for c in ret['pallets'].all():
        #     a.append({"type": c.type, "count": c.count})
        ret['pallets'] = [{"type": p.type, "count": p.count} for p in ret['pallets'].all()]
        return ret


class DDTReadSerializer(ModelSerializer):
    pallets = PalletSerializer(many=True, read_only=True)

    class Meta:
        model = DDT
        fields = ['pallets', 'operator', 'client', 'date', 'photo']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
