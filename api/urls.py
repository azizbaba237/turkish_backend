from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductViewSet
     ,ServiceViewSet
     ,ContactViewSet
     ,CategoryViewSet
     ,TestimonialsViewSet
     ,NewsletterViewSet)
from .views_auth import RegisterView, ProfileView, LogoutView
from .views_token import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView



router = DefaultRouter()

router.register(r'products', ProductViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'testimonials', TestimonialsViewSet)
router.register("newsletter", NewsletterViewSet)

urlpatterns = [
     path('', include(router.urls)),

# Auth
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', ProfileView.as_view(), name='auth_profile'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
]
