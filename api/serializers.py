from rest_framework.serializers import (JSONField, ListSerializer,
                                        ModelSerializer)

from api.models import DDT, Client, Pallet, User


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
        fields = ['serial', 'pallets', 'operator', 'client', 'date', 'photo']

    def create(self, validated_data):
        pallets = validated_data.pop('pallets')
        ddt = DDT.objects.create(**validated_data)

        for pallet in pallets:
            # Validate data
            p = PalletSerializer(data=pallet)
            p.is_valid(raise_exception=True)

            # Create entry
            Pallet.objects.create(
                ddt_id=ddt.pk,
                type=pallet['type'],
                received=pallet.get('received', 0),
                returned=pallet.get('returned', 0),
                moved=pallet.get('moved', 0)
            )

        return ddt

    def update(self, instance, validated_data):
        pallets = validated_data.pop('pallets', [])
        rv = super().update(instance=instance, validated_data=validated_data)

        # Remove old entries
        if pallets:
            for pallet in Pallet.objects.filter(ddt_id=instance.pk):
                pallet.delete()

        # Create entries with new data
        for pallet in pallets:
            # Validate data
            p = PalletSerializer(data=pallet)
            p.is_valid(raise_exception=True)

            # Create entry
            Pallet.objects.create(
                ddt_id=instance.pk,
                type=pallet['type'],
                received=pallet.get('received', 0),
                returned=pallet.get('returned', 0),
                moved=pallet.get('moved', 0)
            )

        return rv

    def to_representation(self, instance):
        """Convert pallets to JSON"""
        rv = super().to_representation(instance)
        rv['pallets'] = [
            {
                "type": p.type,
                "received": p.received,
                "returned": p.returned,
                "moved": p.moved
            }
            for p in rv['pallets'].all()]
        return rv


class DDTReadSerializer(ModelSerializer):
    pallets = PalletSerializer(many=True, read_only=True)

    class Meta:
        model = DDT
        fields = ['pk', 'serial', 'pallets', 'operator', 'client', 'date', 'photo']


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['pk', 'corporate_name']
