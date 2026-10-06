import re
import json

with open('Annapurna_liquor/liquior/product-detail.html', 'r', encoding='utf-8') as f:
    text = f.read()

m_liq = re.search(r'const PRODUCTS_DATA = (\[.*?\]);', text, re.DOTALL)
liq_items = json.loads(m_liq.group(1))

names_to_check = [
    "Macallan",
    "Dom",
    "Pérignon",
    "Don Julio",
    "Blue Label",
    "Hennessy",
    "Yamazaki",
    "Glenlivet",
    "Margaux",
    "Clase Azul",
    "Glenfiddich",
    "Opihr",
    "Rémy",
    "Remy"
]

for n in names_to_check:
    matches = [p for p in liq_items if n.lower() in p['name'].lower()]
    print(f"Checking '{n}': found {len(matches)} -> {[m['name'] + ' (ID ' + str(m['id']) + ')' for m in matches]}")
