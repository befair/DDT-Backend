from rest_framework.serializers import JSONField, ListSerializer, ModelSerializer
from api.models import Client, DDT, User, Pallet


class PalletSerializer(ModelSerializer):
    class Meta:
        model = Pallet
        fields = ['type', 'received', 'returned', 'moved']

    def to_representation(self, instance):
        """Convert pallet type from key to String"""
        ret = super().to_representation(instance)
        ret['human_type'] = Pallet.KIND[ret['type']-1][1]
        return ret


class DDTSerializer(ModelSerializer):
    pallets = JSONField()

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
                received=pallet.get('received', 0),
                returned=pallet.get('returned', 0),
                moved=pallet.get('moved', 0)
            )

        return ddt

    def to_representation(self, instance):
        """Convert pallets to JSON"""
        ret = super().to_representation(instance)
        ret['pallets'] = [
            {
                "type": p.type,
                "received": p.received,
                "returned": p.returned,
                "moved": p.moved
            }
            for p in ret['pallets'].all()]
        return ret


class DDTReadSerializer(ModelSerializer):
    pallets = PalletSerializer(many=True, read_only=True)

    class Meta:
        model = DDT
        fields = ['pallets', 'operator', 'client', 'date', 'photo']


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['pk', 'corporate_name']
