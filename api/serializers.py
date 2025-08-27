from rest_framework import serializers
from .models import Product, Service, Contact, Category, Color, CategoryService, ServiceImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class CategoryServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryService
        fields = ['id', 'name']

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id', 'image', 'order']
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    colors = serializers.StringRelatedField(many=True)
    class Meta:
        model = Product
        fields = '__all__'
        
class ServiceSerializer(serializers.ModelSerializer):
    category = CategoryServiceSerializer(read_only=True)  # afficher catégorie
    images = ServiceImageSerializer(many=True, read_only=True)  # afficher images liées
    features = serializers.ListField(child=serializers.CharField(), required=False)  # affichage JSON clean

    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'price', 'category', 'features', 'images']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']
        
class CategoryServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryService
        fields = ['id', 'name']

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id', 'image', 'order']