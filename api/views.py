from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, Service, Contact, Category, Testimonials, NewsletterSubscriber
from .serializers import ProductSerializer, ServiceSerializer, ContactSerializer, CategorySerializer, TestimonialsSerializer, NewsletterSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEmployee

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class TestimonialsViewSet(viewsets.ModelViewSet):
    queryset = Testimonials.objects.all()
    serializer_class = TestimonialsSerializer

class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")

        if NewsletterSubscriber.objects.filter(email=email).exists():
            return Response(
                {"message": "Cet email est déjà inscrit."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)


class SomeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsEmployee]

