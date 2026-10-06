import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from categories.models import Category
from inventory.models import StockMovement
from products.models import Product
from sales.models import Sale, SaleItem
from suppliers.models import Supplier

User = get_user_model()

CATEGORIES = [
    ('Groceries', 'Everyday food and pantry staples'),
    ('Beverages', 'Soft drinks, juices, and water'),
    ('Snacks', 'Chips, biscuits, and confectionery'),
    ('Household', 'Cleaning and home essentials'),
    ('Electronics', 'Small electronics and accessories'),
]

SUPPLIERS = [
    ('Himalayan Distributors', 'Suresh Gurung', '9801112233', 'suresh@himalayandist.com.np'),
    ('Pokhara Wholesale Mart', 'Anita Rai', '9812345678', 'anita@pokharawholesale.com.np'),
    ('Kathmandu FMCG Supply', 'Bikash Shrestha', '9845098450', 'bikash@ktmfmcg.com.np'),
]

PRODUCTS = [
    ('Basmati Rice 5kg', 'Groceries', 900, 1050, 'kg'),
    ('Mustard Oil 1L', 'Groceries', 260, 320, 'l'),
    ('Instant Noodles (Pack of 6)', 'Snacks', 220, 280, 'pack'),
    ('Coca-Cola 500ml', 'Beverages', 45, 65, 'piece'),
    ('Real Juice 1L', 'Beverages', 140, 190, 'l'),
    ('Potato Chips 150g', 'Snacks', 90, 130, 'piece'),
    ('Dish Wash Bar', 'Household', 30, 45, 'piece'),
    ('Detergent Powder 1kg', 'Household', 150, 195, 'kg'),
    ('USB-C Cable 1m', 'Electronics', 180, 280, 'piece'),
    ('Power Bank 10000mAh', 'Electronics', 1400, 1900, 'piece'),
    ('Wai Wai Noodles (Single)', 'Snacks', 18, 25, 'piece'),
    ('Bottled Water 1L', 'Beverages', 20, 30, 'piece'),
]


class Command(BaseCommand):
    help = 'Seeds sample data (categories, suppliers, products, sales) so the dashboard is not empty on first run.'

    def handle(self, *args, **options):
        admin_user, created = User.objects.get_or_create(
            username='admin', defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@shopadmin.local'}
        )
        if created:
            admin_user.set_password('admin12345')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created superuser "admin" / password "admin12345"'))

        cat_map = {}
        for name, desc in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'description': desc})
            cat_map[name] = cat

        suppliers = []
        for name, contact, phone, email in SUPPLIERS:
            sup, _ = Supplier.objects.get_or_create(
                name=name, defaults={'contact_person': contact, 'phone': phone, 'email': email}
            )
            suppliers.append(sup)

        products = []
        for i, (name, cat_name, cost, price, unit) in enumerate(PRODUCTS, start=1):
            sku = f'SKU{i:04d}'
            product, _ = Product.objects.get_or_create(
                sku=sku,
                defaults=dict(
                    name=name, category=cat_map[cat_name], supplier=random.choice(suppliers),
                    cost_price=Decimal(cost), selling_price=Decimal(price),
                    quantity_in_stock=random.randint(5, 120), unit=unit,
                    low_stock_threshold=15,
                ),
            )
            products.append(product)

        # A handful of sample sales spread over the last two weeks.
        if Sale.objects.count() < 5:
            for day_offset in range(14, 0, -1):
                if random.random() < 0.6:
                    continue
                sale = Sale.objects.create(
                    customer_name=random.choice(['', 'Walk-in Customer', 'Ramesh K.', 'Sita M.']),
                    payment_method=random.choice(['cash', 'esewa', 'fonepay', 'card']),
                    sold_by=admin_user,
                    sold_at=timezone.now() - timezone.timedelta(days=day_offset),
                )
                for product in random.sample(products, k=random.randint(1, 3)):
                    qty = random.randint(1, 5)
                    SaleItem.objects.create(
                        sale=sale, product=product, quantity=qty,
                        unit_price=product.selling_price, unit_cost=product.cost_price,
                    )
                    StockMovement.objects.create(
                        product=product, direction='out', reason='sale', quantity=qty,
                        quantity_before=product.quantity_in_stock + qty, quantity_after=product.quantity_in_stock,
                        note=f'Sale {sale.invoice_number}', created_by=admin_user,
                    )

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete: {Category.objects.count()} categories, {Supplier.objects.count()} suppliers, '
            f'{Product.objects.count()} products, {Sale.objects.count()} sales.'
        ))
