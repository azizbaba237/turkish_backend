from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
     Product
    ,Service
    ,Contact
    ,Category
    ,Testimonials
    ,NewsletterSubscriber
    ,Cart
    ,CartItem
    ,Product)
from .serializers import (
     ProductSerializer
    ,ServiceSerializer
    ,ContactSerializer
    ,CategorySerializer
    ,TestimonialsSerializer
    ,NewsletterSerializer
    ,CartSerializer
    ,CartItemSerializer)
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

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    def list(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=200)

    # POST /api/cart/add/
    @action(detail=False, methods=["post"], url_path="add")
    def add(self, request):
        cart = self.get_cart(request)

        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))
        color = request.data.get("color", "")
        size = request.data.get("size", "")

        product = get_object_or_404(Product, id=product_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity, "color": color, "size": size},
        )

        if not created:
            item.quantity += quantity
            item.color = color
            item.size = size
            item.save()

        return Response(CartSerializer(cart).data, status=200)

    # POST /api/cart/update/
    @action(detail=False, methods=["post"], url_path="update_item")
    def update_item(self, request):
        cart = self.get_cart(request)

        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity", 1))

        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        item.quantity = quantity
        item.save()

        return Response(CartSerializer(cart).data, status=200)

    # POST /api/cart/remove/
    @action(detail=False, methods=["post"], url_path="remove")
    def remove(self, request):
        cart = self.get_cart(request)

        item_id = request.data.get("item_id")
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        return Response(CartSerializer(cart).data, status=200)

    # POST /api/cart/clear/
    @action(detail=False, methods=["post"], url_path="clear")
    def clear(self, request):
        cart = self.get_cart(request)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data, status=200)

    # POST /api/cart/sync/
    @action(detail=False, methods=["post"], url_path="sync")
    def sync(self, request):
        cart = self.get_cart(request)
        guest_items = request.data.get("items", [])

        for gi in guest_items:
            product_id = gi.get("product")
            qty = gi.get("quantity", 1)
            color = gi.get("color", "")
            size = gi.get("size", "")

            product = get_object_or_404(Product, id=product_id)

            item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={"quantity": qty, "color": color, "size": size},
            )

            if not created:
                item.quantity += qty
                item.save()

        return Response(CartSerializer(cart).data, status=200)

