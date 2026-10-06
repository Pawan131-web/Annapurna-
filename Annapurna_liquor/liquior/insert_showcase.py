
import re
import json

pdp_path = 'Annapurna_liquor/liquior/product-detail.html'
with open(pdp_path, 'r', encoding='utf-8') as f:
    content = f.read()

showcase_liquors = """
    ,
    {
        "id": 201,
        "name": "The Macallan 18 Year Double Cask",
        "category": "Whisky",
        "brand": "The Macallan",
        "country": "Scotland (Speyside)",
        "img": "asstes/website-designs/hero_liquor.png",
        "priceRaw": 48600,
        "minPrice": 48600,
        "maxPrice": 48600,
        "priceDisplay": "Rs. 48,600",
        "sizeDisplay": "750ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "The Macallan 18 Year Double Cask 750ML",
                "label": "750ML",
                "volume": "750ML",
                "priceRaw": 48600,
                "priceFormatted": "Rs. 48,600",
                "img": "asstes/website-designs/hero_liquor.png",
                "sku": "MAC18DC"
            }
        ],
        "desc": "Matured in a combination of hand-picked sherry seasoned American and European oak casks for 18 years. Rich dried fruit, ginger, and toffee notes with a warm, lingering oak finish.",
        "rating": "5.0",
        "reviews": 68,
        "gallery": [
            "asstes/website-designs/hero_liquor.png"
        ]
    },
    {
        "id": 202,
        "name": "Dom Pérignon Vintage 2013",
        "category": "Champagne",
        "brand": "Dom Pérignon",
        "country": "France (Champagne)",
        "img": "asstes/website-designs/alcohol design/wine_closeup.jpg",
        "priceRaw": 37000,
        "minPrice": 37000,
        "maxPrice": 37000,
        "priceDisplay": "Rs. 37,000",
        "sizeDisplay": "750ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "Dom Pérignon Vintage 2013 750ML",
                "label": "750ML",
                "volume": "750ML",
                "priceRaw": 37000,
                "priceFormatted": "Rs. 37,000",
                "img": "asstes/website-designs/alcohol design/wine_closeup.jpg",
                "sku": "DOM2013"
            }
        ],
        "desc": "A masterpiece of champagne craftsmanship with aromas of eucalyptus, mint, and vetiver, followed by mirabelle plum and apricot, culminating in an elegant, saline finish.",
        "rating": "4.9",
        "reviews": 52,
        "gallery": [
            "asstes/website-designs/alcohol design/wine_closeup.jpg"
        ]
    },
    {
        "id": 203,
        "name": "Don Julio 1942 Añejo Tequila",
        "category": "Tequila",
        "brand": "Don Julio",
        "country": "Mexico (Jalisco)",
        "img": "asstes/website-designs/alcohol design/red_wine_grapes.jpg",
        "priceRaw": 28350,
        "minPrice": 28350,
        "maxPrice": 28350,
        "priceDisplay": "Rs. 28,350",
        "sizeDisplay": "750ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "Don Julio 1942 Añejo Tequila 750ML",
                "label": "750ML",
                "volume": "750ML",
                "priceRaw": 28350,
                "priceFormatted": "Rs. 28,350",
                "img": "asstes/website-designs/alcohol design/red_wine_grapes.jpg",
                "sku": "DJ1942"
            }
        ],
        "desc": "Handcrafted in small batches and aged for a minimum of two and a half years in American white oak barrels. Rich aromas of caramel, chocolate, and warm oak.",
        "rating": "4.9",
        "reviews": 46,
        "gallery": [
            "asstes/website-designs/alcohol design/red_wine_grapes.jpg"
        ]
    },
    {
        "id": 204,
        "name": "Johnnie Walker Blue Label",
        "category": "Whisky",
        "brand": "Johnnie Walker",
        "country": "Scotland",
        "img": "asstes/website-designs/hero_liquor.png",
        "priceRaw": 33000,
        "minPrice": 33000,
        "maxPrice": 33000,
        "priceDisplay": "Rs. 33,000",
        "sizeDisplay": "750ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "Johnnie Walker Blue Label 750ML",
                "label": "750ML",
                "volume": "750ML",
                "priceRaw": 33000,
                "priceFormatted": "Rs. 33,000",
                "img": "asstes/website-designs/hero_liquor.png",
                "sku": "JWBL750"
            }
        ],
        "desc": "An exquisite blend of Scotland’s rarest and most exceptional whiskies. Velvety smooth with layers of honey, rich fruit, and a signature gentle smokiness.",
        "rating": "5.0",
        "reviews": 89,
        "gallery": [
            "asstes/website-designs/hero_liquor.png"
        ]
    },
    {
        "id": 205,
        "name": "Hennessy XO Cognac",
        "category": "Cognac & Brandy",
        "brand": "Hennessy",
        "country": "France (Cognac)",
        "img": "asstes/website-designs/alcohol design/wine_closeup.jpg",
        "priceRaw": 29700,
        "minPrice": 29700,
        "maxPrice": 29700,
        "priceDisplay": "Rs. 29,700",
        "sizeDisplay": "700ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "Hennessy XO Cognac 700ML",
                "label": "700ML",
                "volume": "700ML",
                "priceRaw": 29700,
                "priceFormatted": "Rs. 29,700",
                "img": "asstes/website-designs/alcohol design/wine_closeup.jpg",
                "sku": "HNXO700"
            }
        ],
        "desc": "The original Extra Old Cognac created in 1870. Complex aromas of candied fruit, wild cocoa, and black pepper with a harmonious, long-lasting finish.",
        "rating": "4.9",
        "reviews": 41,
        "gallery": [
            "asstes/website-designs/alcohol design/wine_closeup.jpg"
        ]
    },
    {
        "id": 206,
        "name": "Yamazaki 12 Year Single Malt",
        "category": "Whisky",
        "brand": "Yamazaki",
        "country": "Japan",
        "img": "asstes/website-designs/alcohol design/red_wine_grapes.jpg",
        "priceRaw": 26300,
        "minPrice": 26300,
        "maxPrice": 26300,
        "priceDisplay": "Rs. 26,300",
        "sizeDisplay": "700ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "Yamazaki 12 Year Single Malt 700ML",
                "label": "700ML",
                "volume": "700ML",
                "priceRaw": 26300,
                "priceFormatted": "Rs. 26,300",
                "img": "asstes/website-designs/alcohol design/red_wine_grapes.jpg",
                "sku": "YMZ12"
            }
        ],
        "desc": "Japan's premier single malt whisky aged in American, Spanish, and Japanese Mizunara oak. Notes of peach, pineapple, candied orange, and delicate Mizunara spice.",
        "rating": "5.0",
        "reviews": 57,
        "gallery": [
            "asstes/website-designs/alcohol design/red_wine_grapes.jpg"
        ]
    },
    {
        "id": 207,
        "name": "The Glenlivet 21 Year Archive",
        "category": "Whisky",
        "brand": "The Glenlivet",
        "country": "Scotland (Speyside)",
        "img": "asstes/website-designs/hero_liquor.png",
        "priceRaw": 39000,
        "minPrice": 39000,
        "maxPrice": 39000,
        "priceDisplay": "Rs. 39,000",
        "sizeDisplay": "700ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "The Glenlivet 21 Year Archive 700ML",
                "label": "700ML",
                "volume": "700ML",
                "priceRaw": 39000,
                "priceFormatted": "Rs. 39,000",
                "img": "asstes/website-designs/hero_liquor.png",
                "sku": "GLV21"
            }
        ],
        "desc": "Matured in a combination of hand-selected American oak and ex-sherry casks. Notes of dried fruit, cinnamon, ginger, and rich dark chocolate.",
        "rating": "4.9",
        "reviews": 33,
        "gallery": [
            "asstes/website-designs/hero_liquor.png"
        ]
    },
    {
        "id": 208,
        "name": "Château Margaux Grand Cru 2015",
        "category": "Wine",
        "brand": "Château Margaux",
        "country": "France (Bordeaux)",
        "img": "asstes/website-designs/alcohol design/wine_closeup.jpg",
        "priceRaw": 98000,
        "minPrice": 98000,
        "maxPrice": 98000,
        "priceDisplay": "Rs. 98,000",
        "sizeDisplay": "750ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "Château Margaux Grand Cru 2015 750ML",
                "label": "750ML",
                "volume": "750ML",
                "priceRaw": 98000,
                "priceFormatted": "Rs. 98,000",
                "img": "asstes/website-designs/alcohol design/wine_closeup.jpg",
                "sku": "MARG2015"
            }
        ],
        "desc": "Legendary Premier Grand Cru Classé wine boasting aromas of crushed blackberries, violet perfume, cedarwood, and fine-grained velvety tannins.",
        "rating": "5.0",
        "reviews": 19,
        "gallery": [
            "asstes/website-designs/alcohol design/wine_closeup.jpg"
        ]
    },
    {
        "id": 209,
        "name": "Clase Azul Reposado Tequila",
        "category": "Tequila",
        "brand": "Clase Azul",
        "country": "Mexico (Jalisco)",
        "img": "asstes/website-designs/alcohol design/red_wine_grapes.jpg",
        "priceRaw": 30300,
        "minPrice": 30300,
        "maxPrice": 30300,
        "priceDisplay": "Rs. 30,300",
        "sizeDisplay": "750ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "Clase Azul Reposado Tequila 750ML",
                "label": "750ML",
                "volume": "750ML",
                "priceRaw": 30300,
                "priceFormatted": "Rs. 30,300",
                "img": "asstes/website-designs/alcohol design/red_wine_grapes.jpg",
                "sku": "CAZULREP"
            }
        ],
        "desc": "Handcrafted in iconic hand-painted ceramic decanters. 100% Blue Weber Agave aged for 8 months in bourbon casks with notes of hazelnut, vanilla, and agave syrup.",
        "rating": "5.0",
        "reviews": 75,
        "gallery": [
            "asstes/website-designs/alcohol design/red_wine_grapes.jpg"
        ]
    },
    {
        "id": 210,
        "name": "Glenfiddich 18 Year Small Batch",
        "category": "Whisky",
        "brand": "Glenfiddich",
        "country": "Scotland (Speyside)",
        "img": "asstes/website-designs/hero_liquor.png",
        "priceRaw": 19500,
        "minPrice": 19500,
        "maxPrice": 19500,
        "priceDisplay": "Rs. 19,500",
        "sizeDisplay": "750ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "Glenfiddich 18 Year Small Batch 750ML",
                "label": "750ML",
                "volume": "750ML",
                "priceRaw": 19500,
                "priceFormatted": "Rs. 19,500",
                "img": "asstes/website-designs/hero_liquor.png",
                "sku": "GLEN18"
            }
        ],
        "desc": "Aged in Spanish Oloroso wood and American oak before marrying in small batches for at least three months. Baked apple, cinnamon, and rich oak.",
        "rating": "4.9",
        "reviews": 64,
        "gallery": [
            "asstes/website-designs/hero_liquor.png"
        ]
    },
    {
        "id": 211,
        "name": "Opihr Oriental Spiced Gin",
        "category": "Gin",
        "brand": "Opihr",
        "country": "United Kingdom",
        "img": "asstes/website-designs/alcohol design/classics_gin.png",
        "priceRaw": 6500,
        "minPrice": 6500,
        "maxPrice": 6500,
        "priceDisplay": "Rs. 6,500",
        "sizeDisplay": "700ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "Opihr Oriental Spiced Gin 700ML",
                "label": "700ML",
                "volume": "700ML",
                "priceRaw": 6500,
                "priceFormatted": "Rs. 6,500",
                "img": "asstes/website-designs/alcohol design/classics_gin.png",
                "sku": "OPHR700"
            }
        ],
        "desc": "London Dry Gin crafted with exotic hand-picked botanicals from the Ancient Spice Route including Indonesian Cubeb berries, Indian Tellicherry black pepper, and Moroccan coriander.",
        "rating": "4.8",
        "reviews": 38,
        "gallery": [
            "asstes/website-designs/alcohol design/classics_gin.png"
        ]
    },
    {
        "id": 212,
        "name": "Rémy Martin XO Excellence",
        "category": "Cognac & Brandy",
        "brand": "Rémy Martin",
        "country": "France (Cognac)",
        "img": "asstes/website-designs/alcohol design/wine_closeup.jpg",
        "priceRaw": 29000,
        "minPrice": 29000,
        "maxPrice": 29000,
        "priceDisplay": "Rs. 29,000",
        "sizeDisplay": "700ML",
        "hasMultipleSizes": false,
        "variants": [
            {
                "original_name": "Rémy Martin XO Excellence 700ML",
                "label": "700ML",
                "volume": "700ML",
                "priceRaw": 29000,
                "priceFormatted": "Rs. 29,000",
                "img": "asstes/website-designs/alcohol design/wine_closeup.jpg",
                "sku": "RMXO700"
            }
        ],
        "desc": "Cognac Fine Champagne blended with hundreds of aged eaux-de-vie. Opulent flavors of juicy plums, ripe figs, candied oranges, and cinnamon.",
        "rating": "5.0",
        "reviews": 51,
        "gallery": [
            "asstes/website-designs/alcohol design/wine_closeup.jpg"
        ]
    }
"""

# Replace end of PRODUCTS_DATA
content = content.replace('"sku": "179014"\n            }\n        ],\n        "desc": "375ML Yeti Vodka 375ml is a premium spirit from the Yeti Vodka manufacturer, Yeti Distillery. Quadruple-distilled using Swiss technology and triple-platinum filtered, it reflects its authentic Yeti Vodka origin in Nepal.",\n        "rating": "4.9",\n        "reviews": 132,\n        "gallery": [\n            "asstes/darumandu_products/yeti-vodka-375ml.png",\n            "asstes/darumandu_products/yeti-vodka-750ml.png"\n        ]\n    }\n];', '"sku": "179014"\n            }\n        ],\n        "desc": "375ML Yeti Vodka 375ml is a premium spirit from the Yeti Vodka manufacturer, Yeti Distillery. Quadruple-distilled using Swiss technology and triple-platinum filtered, it reflects its authentic Yeti Vodka origin in Nepal.",\n        "rating": "4.9",\n        "reviews": 132,\n        "gallery": [\n            "asstes/darumandu_products/yeti-vodka-375ml.png",\n            "asstes/darumandu_products/yeti-vodka-750ml.png"\n        ]\n    }' + showcase_liquors + '\n];')

print("Showcase liquors inserted!")
with open(pdp_path, 'w', encoding='utf-8') as f:
    f.write(content)
