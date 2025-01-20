from rest_framework import viewsets

from order.models import Order
from order.serializers import OrderSerializer
from user.permissions import IsAuthenticatedStaff


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticatedStaff]

    def get_queryset(self):
        """
        Returns the queryset based on the user's permission level.
        - Staff users (excluding superusers) will only view their own orders.
        """
        qs = super().get_queryset()

        if self.request.user.is_staff and not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)