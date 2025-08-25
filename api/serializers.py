from rest_framework import serializers
from .models import Product, Service, Contact, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    colors = serializers.StringRelatedField(many=True)
    class Meta:
        model = Product
        fields = '__all__'
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

