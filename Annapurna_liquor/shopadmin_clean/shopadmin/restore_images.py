import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, ProductImage

# Find uploaded files in media/products/2026/08
media_dir = os.path.join(os.path.dirname(__file__), 'media', 'products', '2026', '08')
if os.path.exists(media_dir):
    files = sorted([f for f in os.listdir(media_dir) if not f.startswith('.')])
    print(f"Found {len(files)} uploaded image files in media:")
    for f in files:
        print(" -", f)

    products = list(Product.objects.filter(is_deleted=False))
    print(f"\nLinking image files to {len(products)} products...")

    for idx, prod in enumerate(products):
        # Pick images for each product
        if idx < len(files):
            img_filename = f"products/2026/08/{files[idx]}"
            pi, created = ProductImage.objects.get_or_create(
                product=prod,
                image=img_filename,
                defaults={'is_primary': True}
            )
            print(f"Attached {files[idx]} to product '{prod.name}' (ID: {prod.pk})")

    print("\nAll product photos successfully re-linked in database!")
else:
    print("Media directory not found.")
