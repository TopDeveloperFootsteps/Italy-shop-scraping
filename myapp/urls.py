from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views.product import ProductViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]