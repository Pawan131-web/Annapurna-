import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from categories.models import Category
from products.models import Product

def seed_subcategories():
    liquor, _ = Category.objects.get_or_create(
        name='Liquor',
        defaults={'description': 'Spirits, whiskies, beers, wines'}
    )

    grocery, _ = Category.objects.get_or_create(
        name='Grocery',
        defaults={'description': 'Daily grocery essentials and packaged food'}
    )

    drink_subcategories = [
        'Whisky & Single Malts',
        'Wine & Red Wines',
        'Gin & Craft Botanicals',
        'Cold Drinks & Tonics',
        'Champagne & Sparklings',
        'Vodka',
        'Tequila & Mezcal',
        'Rum & Cachaça',
        'Cognac & Brandy',
        'Craft Beer & Ciders',
        'Liqueurs & Mixers',
    ]

    grocery_subcategories = [
        'Rice & Grains',
        'Dal & Pulses',
        'Flour & Atta',
        'Cooking Oil',
        'Spices & Masala',
        'Sugar & Salt',
        'Noodles & Pasta',
        'Biscuits & Cookies',
        'Chocolates & Confectionery',
        'Snacks',
        'Tea & Coffee',
        'Soft Drinks & Beverages',
        'Packaged Foods',
        'Canned & Processed Foods',
        'Grocery Essentials'
    ]

    print("Creating/updating subcategories under Liquor and Grocery...")
    created_cats = {}
    for sub in drink_subcategories:
        cat, created = Category.objects.get_or_create(
            name=sub,
            defaults={
                'parent': liquor,
                'description': f'Subcategory of {liquor.name}'
            }
        )
        if not cat.parent:
            cat.parent = liquor
            cat.save(update_fields=['parent'])
        created_cats[sub] = cat
        print(f" - {cat.name} (Parent: {cat.parent.name})")

    for sub in grocery_subcategories:
        cat, created = Category.objects.get_or_create(
            name=sub,
            defaults={
                'parent': grocery,
                'description': f'Subcategory of {grocery.name}'
            }
        )
        if not cat.parent:
            cat.parent = grocery
            cat.save(update_fields=['parent'])
        created_cats[sub] = cat
        print(f" - {cat.name} (Parent: {cat.parent.name})")

    # Map existing products to specific subcategories
    product_mappings = {
        'Royal Stag 750ml': 'Whisky & Single Malts',
        'Blenders Pride 750ml': 'Whisky & Single Malts',
        'Kingfisher Strong 650ml': 'Craft Beer & Ciders',
    }

    for prod_name, sub_name in product_mappings.items():
        if sub_name in created_cats:
            prods = Product.objects.filter(name__icontains=prod_name, is_deleted=False)
            for p in prods:
                p.category = created_cats[sub_name]
                p.save(update_fields=['category'])
                print(f"Assigned '{p.name}' to category '{p.category.display_name}'")

    print("\nDrink subcategories successfully seeded!")

if __name__ == '__main__':
    seed_subcategories()
