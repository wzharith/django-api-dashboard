from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'state', 'paid_amount']

# class OrderSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     phone = serializers.CharField(max_length=100)
#     state = serializers.CharField(max_length=100)
#     paid_amount = serializers.FloatField(blank=True, null=True)
#
#     def create(self, validated_data):
#         return Order.objects.create(validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('name', instance.name)
#         instance.phone = validated_data.get('phone', instance.phone)
#         instance.state = validated_data.get('state', instance.state)
#         instance.paid_amount = validated_data.get('paid_amount', instance.paid_amount)
#         instance.save()
#         return instance