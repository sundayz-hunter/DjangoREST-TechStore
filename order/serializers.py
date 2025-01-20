from rest_framework import serializers

from order.models import OrderItem, Order
from product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price', read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal'
        )



class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True)
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

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product_name = item_data['product']['name']
            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Product with name '{product_name}' does not exist."
                )

            OrderItem.objects.create(order=order, product=product, quantity=item_data.get('quantity'))

        return order