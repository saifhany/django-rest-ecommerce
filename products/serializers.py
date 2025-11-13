from rest_framework import serializers
from .models import Product
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Product
        fields = '__all__'
