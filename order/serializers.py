from rest_framework import serializers

from order.models import OrderItem, Order


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price')

    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal'
        )



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total')

    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'updated_at',
            'user',
            'status',
            'items',
            'total_price',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        return representation

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
