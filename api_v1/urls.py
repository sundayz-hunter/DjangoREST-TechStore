from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from order.views import OrdersViewSet
from product.views import ProductViewSet, ProductSummaryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrdersViewSet, basename='order')
router.register(r'products-summary', ProductSummaryViewSet, basename='product-summary')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/get-token', obtain_auth_token, name='get-token'),
]