import re

with open('Annapurna_liquor/liquior/grocries.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.findall(r'id:\s*(\d+),\s*name:\s*"([^"]+)",\s*catName:\s*"([^"]+)",\s*priceRaw:\s*(\d+)', text)
print(f"Total products in grocries.html: {len(m)}")
for p in m:
    print(f"ID {p[0]}: '{p[1]}' ({p[2]}) - Rs. {p[3]}")
