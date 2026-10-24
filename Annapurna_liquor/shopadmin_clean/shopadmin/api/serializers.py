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
    image_url = serializers.CharField(source='get_image_url', read_only=True)

    class Meta:
        model = OnlineOrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'image_url', 'quantity', 'unit_price', 'line_total']


class OnlineOrderSerializer(serializers.ModelSerializer):
    items = OnlineOrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_badge_class = serializers.CharField(source='get_status_badge_class', read_only=True)
    whatsapp_url = serializers.CharField(source='get_whatsapp_url', read_only=True)

    class Meta:
        model = OnlineOrder
        fields = [
            'id', 'order_number', 'customer_name', 'customer_phone', 'customer_email',
            'delivery_address', 'payment_method', 'status', 'status_display', 'status_badge_class',
            'whatsapp_url', 'total_amount', 'created_at', 'updated_at', 'notes', 'items'
        ]


class OnlineOrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(max_length=200)
    qty = serializers.IntegerField(min_value=1, default=1)
    priceRaw = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    price = serializers.CharField(max_length=100, required=False, allow_blank=True)
    img = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')


class OnlineOrderCreateSerializer(serializers.Serializer):
    orderId = serializers.CharField(max_length=64, required=False, allow_blank=True)
    order_number = serializers.CharField(max_length=64, required=False, allow_blank=True)
    customer = serializers.DictField()
    items = OnlineOrderItemCreateSerializer(many=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    paymentMethod = serializers.CharField(max_length=50, default='WhatsApp Order / Direct', required=False)
    payment_method = serializers.CharField(max_length=50, default='WhatsApp Order / Direct', required=False)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')

    def create(self, validated_data):
        import random
        from decimal import Decimal

        customer = validated_data.get('customer', {})
        order_number = validated_data.get('orderId') or validated_data.get('order_number')
        if not order_number:
            order_number = f"#ANN-{random.randint(100000, 999999)}"

        items_data = validated_data.get('items', [])
        computed_total = Decimal('0')
        for item in items_data:
            qty = item.get('qty', 1)
            raw_p = item.get('priceRaw')
            if raw_p is None:
                # Try parsing price string
                p_str = item.get('price', '')
                import re
                nums = re.findall(r'\d+', p_str)
                raw_p = Decimal(nums[0]) if nums else Decimal('0')
            computed_total += (raw_p * qty)

        total_amount = validated_data.get('total')
        if total_amount is None or total_amount <= Decimal('0'):
            total_amount = computed_total

        order = OnlineOrder.objects.create(
            order_number=order_number,
            customer_name=customer.get('name') or 'Customer',
            customer_phone=customer.get('phone', ''),
            customer_email=customer.get('email', ''),
            delivery_address=customer.get('address', ''),
            payment_method=validated_data.get('paymentMethod') or validated_data.get('payment_method', 'WhatsApp Order / Direct'),
            total_amount=total_amount,
            notes=validated_data.get('notes', ''),
            status=OnlineOrder.Status.NEW
        )

        for item_data in items_data:
            prod_obj = None
            if item_data.get('product_id'):
                prod_obj = Product.objects.filter(id=item_data['product_id']).first()

            qty = item_data.get('qty', 1)
            raw_p = item_data.get('priceRaw')
            if raw_p is None:
                if prod_obj:
                    raw_p = prod_obj.selling_price
                else:
                    raw_p = Decimal('0')

            img_url = item_data.get('img') or ''
            if not img_url and prod_obj and prod_obj.primary_image:
                img_url = prod_obj.primary_image.url

            OnlineOrderItem.objects.create(
                order=order,
                product=prod_obj,
                product_name=item_data.get('name', 'Product'),
                product_image=img_url,
                quantity=qty,
                unit_price=raw_p
            )

            # Deduct inventory stock if product exists
            if prod_obj and prod_obj.quantity_in_stock >= qty:
                prod_obj.quantity_in_stock -= qty
                prod_obj.save(update_fields=['quantity_in_stock'])

        return order


