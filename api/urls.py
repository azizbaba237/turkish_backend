from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (ProductViewSet
     ,ServiceViewSet
     ,ContactViewSet
     ,CategoryViewSet
     ,TestimonialsViewSet
     ,NewsletterViewSet)
from django.urls import include



router = DefaultRouter()

router.register(r'products', ProductViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'testimonials', TestimonialsViewSet)
router.register("newsletter", NewsletterViewSet)

urlpatterns = [
     path('', include(router.urls)),
]
