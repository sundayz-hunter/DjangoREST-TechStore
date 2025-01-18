from django.db.models import Max, Avg, Sum, StdDev
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductManagerSerializer, ProductVendorSerializer, ProductClientSerializer, \
    ProductSummarySerializer
from user.permissions import IsStaffOrReadOnly, IsAuthenticatedStaff



# ProductViewSet : Handles CRUD operations on Product objects
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    #lookup_field = 'name'

    filterset_fields = ['name', 'category', 'sku']
    search_fields = ['name', 'category', 'sku']

    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        """
        Determines the appropriate serializer class based on the user's permission level.
        - Superusers get ProductManagerSerializer.
        - Staff users get ProductVendorSerializer.
        - Regular clients get ProductClientSerializer.
        """
        if self.request.user.is_superuser:
            return ProductManagerSerializer
        elif self.request.user.is_staff and not self.request.user.is_superuser:
            return ProductVendorSerializer
        else:
            return ProductClientSerializer

    def get_queryset(self):
        """
        Returns the queryset based on the user's permission.
        - If the user is not a staff member, only include products that are active and have stock available.
        """
        qs = super().get_queryset()

        if not self.request.user.is_staff:
            qs = qs.filter(is_active=True, stock__gt=0)
        return qs

    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """
        Endpoint out of stock products
        URL : /api/products/out_of_stock/
        """
        products = Product.objects.filter(stock=0)  # Filtrer les produits hors stock
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        """
        Override to set permissions for specific actions.
        - Admin users can access the `out_of_stock` endpoint.
        """
        if self.action == 'out_of_stock':
            return [permissions.IsAdminUser()]
        return super().get_permissions()


class ProductSummaryViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSummarySerializer

    permission_classes = [IsAuthenticatedStaff]

    def list(self, request, *args, **kwargs):
        """
        Custom list view to retrieve aggregated product statistics.
        """
        queryset = self.get_queryset()

        data = {
            'count': queryset.count(),
            'max_price': queryset.aggregate(max_price=Max('price'))['max_price'],
            'average_price': round(queryset.aggregate(average_price=Avg('price'))['average_price'], 2),
            'total_stock': queryset.aggregate(total_stock=Sum('stock'))['total_stock'],
            'std_dev_price': queryset.aggregate(std_dev_price=StdDev('price'))['std_dev_price'],
            'active_product_count': queryset.filter(is_active=True).count(),
            'inactive_product_count': queryset.filter(is_active=False).count(),
            'out_of_stock_count': queryset.filter(stock=0).count(),
            'products': queryset
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data)