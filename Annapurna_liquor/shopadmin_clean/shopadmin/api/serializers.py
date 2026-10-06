from rest_framework import serializers

from categories.models import Category
from products.models import Product, ProductImage
from sales.models import Sale, SaleItem, OnlineOrder, OnlineOrderItem
from suppliers.models import Supplier


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'department', 'description', 'icon', 'is_active', 'product_count', 'created_at']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_person', 'phone', 'email', 'address', 'is_active']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']


class ProductSerializer(serializers.ModelSerializer):
    """Frontend-ready representation: nested category/supplier + image list."""
    category = CategorySerializer(read_only=True)
    supplier = SupplierSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'category', 'supplier', 'department', 'brand',
            'volume', 'alcohol_percentage', 'origin', 'rating', 'original_price', 'tags',
            'description', 'cost_price', 'selling_price', 'quantity_in_stock', 'unit',
            'status', 'is_low_stock', 'images', 'created_at', 'updated_at',
        ]


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'unit_cost']


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id', 'invoice_number', 'customer_name', 'customer_phone',
            'payment_method', 'sold_at', 'items', 'total_amount',
        ]


class OnlineOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineOrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'line_total']


class OnlineOrderSerializer(serializers.ModelSerializer):
    items = OnlineOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = OnlineOrder
        fields = [
            'id', 'order_number', 'customer_name', 'customer_phone',
            'delivery_address', 'payment_method', 'status', 'total_amount',
            'created_at', 'updated_at', 'notes', 'items'
        ]


class OnlineOrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(max_length=200)
    qty = serializers.IntegerField(min_value=1)
    priceRaw = serializers.DecimalField(max_digits=12, decimal_places=2)


class OnlineOrderCreateSerializer(serializers.Serializer):
    orderId = serializers.CharField(max_length=32)
    customer = serializers.DictField()
    items = OnlineOrderItemCreateSerializer(many=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
    paymentMethod = serializers.CharField(max_length=50, default='Cash on Delivery (COD)')

    def create(self, validated_data):
        customer = validated_data['customer']
        order_number = validated_data['orderId']

        order = OnlineOrder.objects.create(
            order_number=order_number,
            customer_name=customer.get('name', 'Guest Customer'),
            customer_phone=customer.get('phone', ''),
            delivery_address=customer.get('address', ''),
            payment_method=validated_data.get('paymentMethod', 'Cash on Delivery (COD)'),
            total_amount=validated_data['total'],
            status=OnlineOrder.Status.PENDING
        )

        for item_data in validated_data['items']:
            prod_obj = None
            if item_data.get('product_id'):
                prod_obj = Product.objects.filter(id=item_data['product_id']).first()

            OnlineOrderItem.objects.create(
                order=order,
                product=prod_obj,
                product_name=item_data['name'],
                quantity=item_data['qty'],
                unit_price=item_data['priceRaw']
            )

            # Deduct inventory stock if product exists
            if prod_obj and prod_obj.quantity_in_stock >= item_data['qty']:
                prod_obj.quantity_in_stock -= item_data['qty']
                prod_obj.save(update_fields=['quantity_in_stock'])

        return order

