from rest_framework.serializers import JSONField, ModelSerializer

from api.models import DDT, AppUser, Client, Pallet


class PalletSerializer(ModelSerializer):
    class Meta:
        model = Pallet
        fields = ['kind', 'received', 'returned', 'moved']

    def to_representation(self, instance):
        """Convert pallet kind from key to String"""
        ret = super().to_representation(instance)
        ret['human_kind'] = instance.kind_to_human(ret['kind'])
        return ret


class DDTSerializer(ModelSerializer):
    pallets = JSONField()

    class Meta:
        model = DDT
        fields = ['serial', 'pallets', 'client', 'date', 'photo']

    def create(self, validated_data):
        pallets = validated_data.pop('pallets')
        
        # Get current user from context (token auth)
        user = AppUser.objects.get(pk=self.context['request'].user.pk)
        validated_data['operator'] = user

        # Validate received pallets
        for pallet in pallets:
            p = PalletSerializer(data=pallet)
            p.is_valid(raise_exception=True)

        # Create DDT
        ddt = DDT.objects.create(**validated_data)

        # Add pallets objects to DDT
        for pallet in pallets:
            # Create entry
            Pallet.objects.create(
                ddt_id=ddt.pk,
                kind=pallet['kind'],
                received=pallet.get('received', 0),
                returned=pallet.get('returned', 0),
                moved=pallet.get('moved', 0)
            )

        return ddt

    def update(self, instance, validated_data):
        pallets = validated_data.pop('pallets', [])
        
        # Get current user from context (token auth)
        user = AppUser.objects.get(pk=self.context['request'].user.pk)
        validated_data['operator'] = user

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
                kind=pallet['kind'],
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
                "kind": p.kind,
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
        fields = ['pk', 'serial', 'pallets', 'operator', 'client', 'date', 'time', 'photo']


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['pk', 'corporate_name']


class AppUserSerializer(ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['pk', 'first_name', 'last_name', 'email', 'user_kind']
