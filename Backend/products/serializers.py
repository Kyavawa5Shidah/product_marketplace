from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'status',
            'created_by',
            'created_at',
        ]
        read_only_fields = ['created_by', 'status']

    def update(self, instance, validated_data):

        # Prevent editing approved products
        if instance.status == 'APPROVED':
            raise serializers.ValidationError(
                "Approved products cannot be edited."
            )

        return super().update(instance, validated_data)
