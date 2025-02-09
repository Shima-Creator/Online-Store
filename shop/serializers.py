from rest_framework import serializers
from shop.models import *


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)


class SubCategorySerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return SubCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    price = serializers.IntegerField()
    subcategory_id = serializers.IntegerField()
    shop_id = serializers.IntegerField()
    stock = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)


class SalesmanSerializer(serializers.Serializer):
    shop = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=40)
    category_id = serializers.IntegerField()

    def create(self, validated_data):
        return Salesman.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)


class BasketSerializer(serializers.Serializer):
    username_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def create(self, validated_data):
        return Basket.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)