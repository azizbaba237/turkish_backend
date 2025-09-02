from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ServiceViewSet, ContactViewSet, CategoryViewSet, TestimonialsViewSet
from django.urls import include



router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'testimonials', TestimonialsViewSet)

urlpatterns = [
     path('', include(router.urls)),
]
