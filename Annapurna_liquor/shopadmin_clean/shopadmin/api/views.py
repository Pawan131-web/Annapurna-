from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from categories.models import Category
from products.models import Product
from sales.models import Sale, OnlineOrder
from suppliers.models import Supplier

from .serializers import (
    CategorySerializer, ProductSerializer, SaleSerializer,
    SupplierSerializer, OnlineOrderSerializer, OnlineOrderCreateSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department']


class SupplierViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Supplier.objects.filter(is_active=True)
    serializer_class = SupplierSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.filter(is_deleted=False, status='active').select_related('category', 'supplier').prefetch_related('images')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'supplier', 'department', 'brand']
    search_fields = ['name', 'sku', 'brand', 'tags', 'description']
    ordering_fields = ['selling_price', 'created_at', 'rating']


class SaleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sale.objects.prefetch_related('items')
    serializer_class = SaleSerializer


class OnlineOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = OnlineOrder.objects.prefetch_related('items')

    def get_serializer_class(self):
        if self.action == 'create':
            return OnlineOrderCreateSerializer
        return OnlineOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {
                    'status': 'success',
                    'message': 'Order successfully created',
                    'order': OnlineOrderSerializer(order).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

