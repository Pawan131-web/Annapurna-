from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action
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

    @action(detail=False, methods=['get'], url_path='related')
    def related_products(self, request):
        p_id = request.query_params.get('id') or request.query_params.get('product_id')
        p_name = request.query_params.get('name')
        p_dept = request.query_params.get('department') or request.query_params.get('type')
        return self._get_related_response(p_id=p_id, p_name=p_name, dept=p_dept)

    @action(detail=True, methods=['get'], url_path='related')
    def related_for_product(self, request, pk=None):
        return self._get_related_response(p_id=pk)

    def _get_related_response(self, p_id=None, p_name=None, dept=None):
        """
        Return up to 6 related products according to strict business logic:
        1. Exclude current product P.
        2. Only active, published, and in-stock (quantity_in_stock > 0).
        3. Priority order without duplicates:
           a. Same sub-category as P
           b. Same main category as P (other sub-categories)
           c. Newest products from same main category
        4. NEVER include products from a different main category.
        5. If 0 matches, return empty list.
        6. Single efficient query (select_related for category, limit 6).
        7. Handle products with no category or sub-category safely without crashing.
        """
        from django.db.models import Case, When, Value, IntegerField

        p = None
        if p_name:
            clean_name = p_name.strip()
            p = Product.objects.filter(name__iexact=clean_name, is_deleted=False, status='active').select_related('category', 'category__parent').first()
            if not p:
                p = Product.objects.filter(name__icontains=clean_name, is_deleted=False, status='active').select_related('category', 'category__parent').first()

        if not p and p_id:
            try:
                candidate = Product.objects.filter(id=int(p_id), is_deleted=False, status='active').select_related('category', 'category__parent').first()
                if candidate:
                    if not p_name:
                        p = candidate
                    else:
                        c_clean = candidate.name.lower()
                        n_clean = p_name.strip().lower()
                        if c_clean in n_clean or n_clean in c_clean:
                            p = candidate
            except (ValueError, TypeError):
                p = None

        # Determine target main category ('grocery' or 'liquor')
        target_dept = dept if dept in ('grocery', 'liquor') else (p.department if (p and p.department) else None)

        # Rule 7: If main category is missing, safely return empty list to hide section
        if not target_dept:
            return Response([])

        cat_id = p.category_id if p else None

        priority_expr = None
        if cat_id:
            priority_expr = Case(
                When(category_id=cat_id, then=Value(1)),
                default=Value(2),
                output_field=IntegerField()
            )

        # Single efficient query: select_related for category + limit 6 (WCAG / no N+1)
        qs = Product.objects.filter(
            department=target_dept,
            status='active',
            is_deleted=False,
            quantity_in_stock__gt=0
        )

        if p:
            qs = qs.exclude(id=p.id)

        qs = qs.select_related('category', 'category__parent').prefetch_related('images')

        if priority_expr:
            qs = qs.annotate(match_priority=priority_expr).order_by('match_priority', '-created_at')
        else:
            qs = qs.order_by('-created_at')

        items = list(qs[:6])

        data = []
        for item in items:
            img_url = ''
            primary = item.primary_image
            if primary and primary.image:
                img_url = primary.image.url
            elif item.images.exists():
                img_url = item.images.first().image.url
            else:
                img_url = 'asstes/website-designs/grocries/R.jpg' if item.department == 'grocery' else 'asstes/website-designs/hero_liquor.png'

            price_raw = int(item.selling_price)
            data.append({
                'id': item.id,
                'name': item.name,
                'price': f"NPR. {price_raw:,}.00",
                'priceRaw': price_raw,
                'img': img_url,
                'cat': item.category.name if item.category else '',
                'department': item.department,
                'volume': item.volume or ''
            })

        return Response(data)


class SaleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sale.objects.prefetch_related('items')
    serializer_class = SaleSerializer


from rest_framework.permissions import AllowAny, IsAuthenticated


class OnlineOrderViewSet(viewsets.ModelViewSet):
    queryset = OnlineOrder.objects.prefetch_related('items').order_by('-created_at')

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

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


