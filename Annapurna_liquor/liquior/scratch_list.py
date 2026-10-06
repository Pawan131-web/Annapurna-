import re
import json

with open('Annapurna_liquor/liquior/product-detail.html', 'r', encoding='utf-8') as f:
    pdp_text = f.read()

m_liq = re.search(r'const PRODUCTS_DATA = (\[.*?\]);', pdp_text, re.DOTALL)
liq_items = json.loads(m_liq.group(1))

print("Total Liquor Products in PDP:", len(liq_items))
for p in liq_items:
    print(f"ID {p['id']}: '{p['name']}' ({p.get('category')}) - Price: {p.get('priceRaw')}")
