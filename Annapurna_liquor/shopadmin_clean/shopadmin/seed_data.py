import os
from decimal import Decimal

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from categories.models import Category
from suppliers.models import Supplier
from products.models import Product, ProductImage
from sales.models import Sale, SaleItem
from inventory.models import StockMovement

User = get_user_model()


def run_seeding():
    print("Cleaning sales and inventory movements...")
    
    # Clear sales and stock movements
    SaleItem.objects.all().delete()
    Sale.objects.all().delete()
    StockMovement.objects.all().delete()

    # Admin user
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@shopadmin.local', 'admin123')

    # Categories
    cat_liquor, _ = Category.objects.get_or_create(name='Liquor', defaults={'department': 'liquor', 'description': 'Spirits, whiskies, beers, wines'})
    cat_grocery, _ = Category.objects.get_or_create(name='Grocery', defaults={'department': 'grocery', 'description': 'Craft mixers, tonics, and bar accessories'})

    # Suppliers
    sup_apex, _ = Supplier.objects.get_or_create(name='Apex Distributors', defaults={'contact_person': 'Ramesh Shrestha', 'phone': '9841234567'})
    sup_global, _ = Supplier.objects.get_or_create(name='Global Spirits Co.', defaults={'contact_person': 'Sanjay Thapa', 'phone': '9851098765'})
    sup_quality, _ = Supplier.objects.get_or_create(name='Quality Foods Ltd.', defaults={'contact_person': 'Anita Sharma', 'phone': '9801122334'})

    # Rich Products data: (name, sku, cat, sup, dept, brand, vol, abv, origin, rating, cost, sell, stock, low)
    products_data = [
        ("The Macallan 18 Year Double Cask", "LIQ-001", cat_liquor, sup_global, "liquor", "The Macallan", "750ML", 43.0, "Scotland", 5.0, 40000, 48600, 15, 5),
        ("Dom Pérignon Vintage 2013", "LIQ-002", cat_liquor, sup_global, "liquor", "Dom Pérignon", "750ML", 12.5, "France", 4.9, 30000, 37000, 10, 3),
        ("Jack Daniel's Old No. 7", "LIQ-003", cat_liquor, sup_global, "liquor", "Jack Daniel's", "750ML", 40.0, "USA", 4.9, 5800, 7450, 25, 5),
        ("Premium Himalayan Aged Basmati Rice (5kg)", "GRO-001", cat_grocery, sup_quality, "grocery", "Goldstar Pantry", "5KG", None, "Nepal", 5.0, 1150, 1450, 60, 10),
        ("Jeera Masino Premium Rice (20kg)", "GRO-002", cat_grocery, sup_quality, "grocery", "Annapurna Pantry", "20KG", None, "Nepal", 4.9, 2100, 2450, 40, 10),
        ("Polished Red Masoor Dal (1kg)", "GRO-003", cat_grocery, sup_quality, "grocery", "Quality Foods", "1KG", None, "Nepal", 4.8, 140, 180, 100, 10),
        ("Organic Yellow Moong Dal (1kg)", "GRO-004", cat_grocery, sup_quality, "grocery", "Himalayan Organics", "1KG", None, "Nepal", 4.9, 160, 210, 85, 10),
        ("Whole Wheat Chakki Fresh Atta (5kg)", "GRO-005", cat_grocery, sup_quality, "grocery", "Goldstar Pantry", "5KG", None, "Nepal", 4.9, 320, 410, 70, 10),
        ("Cold Pressed Extra Virgin Mustard Oil (2L)", "GRO-006", cat_grocery, sup_quality, "grocery", "Goldstar Pantry", "2L", None, "Nepal", 4.7, 620, 780, 50, 10),
        ("Pure Himalayan Clarified Ghee (500g)", "GRO-007", cat_grocery, sup_quality, "grocery", "Himalayan Organics", "500G", None, "Nepal", 5.0, 1350, 1650, 35, 10),
        ("Pure Kashmiri Saffron & Cardamom Pack", "GRO-008", cat_grocery, sup_quality, "grocery", "Himalayan Organics", "50G", None, "Nepal", 5.0, 1750, 2200, 30, 5),
        ("Organic Turmeric & Chili Powder Combo (500g)", "GRO-009", cat_grocery, sup_quality, "grocery", "Himalayan Organics", "500G", None, "Nepal", 4.8, 210, 280, 90, 10),
        ("Refined Crystal Sugar & Iodized Salt Set", "GRO-010", cat_grocery, sup_quality, "grocery", "Quality Foods", "2KG", None, "Nepal", 4.8, 150, 200, 120, 15),
        ("Organic Whole Leaf Ilam Green Tea (200g)", "GRO-011", cat_grocery, sup_quality, "grocery", "Himalayan Organics", "200G", None, "Nepal", 4.8, 360, 480, 65, 10),
        ("Handcrafted Dark Chocolate Truffles Box", "GRO-012", cat_grocery, sup_quality, "grocery", "Annapurna Bakery", "250G", None, "Nepal", 4.9, 680, 890, 45, 10),
        ("Packaged Danish Pastries & Biscuits Box", "GRO-013", cat_grocery, sup_quality, "grocery", "Annapurna Bakery", "500G", None, "Nepal", 5.0, 430, 580, 55, 10),
        ("Natural Sparkling Glacier Mineral Water (Case of 12)", "GRO-014", cat_grocery, sup_quality, "grocery", "Himalayan Organics", "12x500ML", None, "Nepal", 4.8, 720, 960, 80, 15),
        ("Gourmet Roasted Nuts & Dried Fruits Pack (1kg)", "GRO-015", cat_grocery, sup_quality, "grocery", "Annapurna Pantry", "1KG", None, "Nepal", 4.9, 490, 650, 75, 10),
    ]

    for name, sku, cat, sup, dept, brand, vol, abv, origin, rat, cost, sell, stock, low in products_data:
        p, _ = Product.objects.get_or_create(
            sku=sku,
            defaults={
                'name': name,
                'category': cat,
                'supplier': sup,
                'department': dept,
                'brand': brand,
                'volume': vol,
                'alcohol_percentage': Decimal(str(abv)) if abv is not None else None,
                'origin': origin,
                'rating': Decimal(str(rat)),
                'quantity_in_stock': stock,
                'low_stock_threshold': low,
                'cost_price': Decimal(str(cost)),
                'selling_price': Decimal(str(sell)),
                'is_deleted': False,
                'status': 'active',
            }
        )

    # Re-link existing media files if available
    media_dir = os.path.join(os.path.dirname(__file__), 'media', 'products', '2026', '08')
    if os.path.exists(media_dir):
        files = sorted([f for f in os.listdir(media_dir) if not f.startswith('.')])
        products = list(Product.objects.filter(is_deleted=False))
        for idx, prod in enumerate(products):
            if idx < len(files) and not prod.images.exists():
                img_filename = f"products/2026/08/{files[idx]}"
                ProductImage.objects.create(product=prod, image=img_filename, is_primary=True)

    print("Seeding finished cleanly. Uploaded photos preserved!")


if __name__ == '__main__':
    run_seeding()
