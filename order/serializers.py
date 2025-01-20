from django.db import transaction
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
    user = serializers.CharField(read_only=True)
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

        with transaction.atomic():
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

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')

        with transaction.atomic():
            instance = super().update(instance, validated_data) # Update order status (Confirmed, Cancelled)

            # Update Items
            existing_items = {item.product.id: item for item in instance.items.all()}
            new_items_data = []

            for item_data in items_data:
                product_name = item_data['product']['name']
                try:
                    product = Product.objects.get(name=product_name)
                except Product.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Product with name '{product_name}' does not exist."
                    )

                if product.id in existing_items:
                    # Update quantity of existing item
                    existing_item = existing_items[product.id]
                    existing_item.quantity = item_data.get('quantity', existing_item.quantity)
                    existing_item.save()
                else:
                    # Create new item added in the order
                    new_items_data.append(OrderItem(
                        order=instance,
                        product=product,
                        quantity=item_data.get('quantity', 1)
                    ))

            # Deleting items not included in the new list only if PUT request method
            if self.partial == False:
                items_to_delete = [
                    item for product_id, item in existing_items.items()
                    if product_id not in [Product.objects.get(name=item['product']['name']).id for item in items_data]
                ]
                for item in items_to_delete:
                    item.delete()

                # Creating new items
                OrderItem.objects.bulk_create(new_items_data)


        return instance