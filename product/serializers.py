from rest_framework import serializers
from .models import Product


class ProductManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'name',
            'category',
            'description',
            'price',
            'stock',
            'image',
            'is_active',
            'created_at',
            'updated_at',
            'url',
        ]

    def get_url(self, obj): # For add a complete link
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(obj.get_absolute_url())

    @staticmethod
    def validate_price(value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    @staticmethod
    def validate_stock(value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class ProductVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'sku',
            'name',
            'category',
            'description',
            'price',
            'stock',
            'is_active',
            'url',
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(obj.get_absolute_url())

    @staticmethod
    def validate_price(value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    @staticmethod
    def validate_stock(value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class ProductClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'description',
            'price',
            'url',
        ]

    def get_url(self, obj): # For add a complete link
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(obj.get_absolute_url())


    def validate(self, data):
        if not self.instance.is_active:
            raise serializers.ValidationError("The product is not active.")

        if self.instance.stock <= 0:
            raise serializers.ValidationError("The product is out of stock.")

        return data

    @staticmethod
    def validate_price(value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'stock',
        )

    @staticmethod
    def validate_price(value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    @staticmethod
    def validate_stock(value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class ProductSummarySerializer(serializers.Serializer):
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
    average_price = serializers.FloatField()
    total_stock = serializers.IntegerField()
    active_product_count = serializers.IntegerField()
    inactive_product_count = serializers.IntegerField()
    out_of_stock_count = serializers.IntegerField()
    products = ProductSerializer(many=True)
