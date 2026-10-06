/**
 * Annapurna Store — Intelligent Product Search & Autocomplete Engine
 * Dynamic, debounced search suggestions with match highlighting,
 * liquor & grocery catalog indexing, keyboard navigation, and direct routing.
 */

(function () {
    // 1. UNIFIED STORE CATALOG (Liquor & Groceries)
    let STORE_CATALOG = [
        // --- LIQUOR PRODUCTS (140 Clean Compact Catalog Items) ---
        {"id": 1, "name": "1768 Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,200", "priceRaw": 2200, "rating": "4.9", "img": "asstes/darumandu_products/1768-vodka-750ml.webp", "brand": "1768", "tags": ["1768 vodka", "vodka", "1768", "liquor", "drinks", "alcohol", "international", "750ml"]},
        {"id": 2, "name": "2 Share Natural Sweet Red", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,400", "priceRaw": 1400, "rating": "4.9", "img": "asstes/darumandu_products/2-share-natural-sweet-red-750ml.png", "brand": "2 Share", "tags": ["2 share natural sweet red", "wine", "2 share", "liquor", "drinks", "alcohol", "international", "750ml", "share", "natural", "sweet", "red"]},
        {"id": 3, "name": "2 Share Natural Sweet White", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,500", "priceRaw": 1500, "rating": "5.0", "img": "asstes/darumandu_products/2-share-natural-sweet-white-750ml.png", "brand": "2 Share", "tags": ["2 share natural sweet white", "wine", "2 share", "liquor", "drinks", "alcohol", "south africa", "750ml", "share", "natural", "sweet", "white"]},
        {"id": 4, "name": "8 Peaks Himalayan Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 610", "priceRaw": 610, "rating": "4.9", "img": "asstes/darumandu_products/8-peaks-himalayan-vodka-375ml.webp", "brand": "8 Peaks", "tags": ["8 peaks himalayan vodka", "vodka", "8 peaks", "liquor", "drinks", "alcohol", "international", "375ml", "peaks", "himalayan"]},
        {"id": 5, "name": "8848 Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,190", "priceRaw": 1190, "rating": "4.9", "img": "asstes/darumandu_products/8848-vodka-375ml.png", "brand": "8848", "tags": ["8848 vodka", "vodka", "8848", "liquor", "drinks", "alcohol", "international", "375ml", "750ml"]},
        {"id": 6, "name": "Absolut Blue", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 6,600", "priceRaw": 6600, "rating": "5.0", "img": "asstes/darumandu_products/absolut-blue-1l.png", "brand": "Absolut", "tags": ["absolut blue", "vodka", "absolut", "liquor", "drinks", "alcohol", "international", "1l", "blue"]},
        {"id": 7, "name": "Absolut Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 7,120", "priceRaw": 7120, "rating": "4.9", "img": "asstes/darumandu_products/absolute-vodka-1ltr.jpg", "brand": "Absolut", "tags": ["absolut vodka", "vodka", "absolut", "liquor", "drinks", "alcohol", "sweden", "1l"]},
        {"id": 8, "name": "Aristocrat Classic Nepalese Blend Whisky", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 630", "priceRaw": 630, "rating": "4.9", "img": "asstes/darumandu_products/aristocrat-classic-nepalese-blend-whisky-375ml.png", "brand": "Aristocrat", "tags": ["aristocrat classic nepalese blend whisky", "whisky", "aristocrat", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml", "classic", "nepalese", "blend"]},
        {"id": 9, "name": "Arna 8 Premium Lager", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 370", "priceRaw": 370, "rating": "5.0", "img": "asstes/darumandu_products/arna-8-premium-lager-650ml.png", "brand": "Arna", "tags": ["arna 8 premium lager", "beer", "arna", "liquor", "drinks", "alcohol", "nepal", "650ml", "premium", "lager"]},
        {"id": 10, "name": "Arna Beer", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 200", "priceRaw": 200, "rating": "4.9", "img": "asstes/darumandu_products/arna-beer-300ml.jpg", "brand": "Arna", "tags": ["arna beer", "beer", "arna", "liquor", "drinks", "alcohol", "nepal", "300ml", "500ml"]},
        {"id": 11, "name": "Baileys Irish Cream", "category": "Liqueur", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 3,900", "priceRaw": 3900, "rating": "4.9", "img": "asstes/darumandu_products/baileys-irish-cream-500ml.jpg", "brand": "Baileys", "tags": ["baileys irish cream", "liqueur", "baileys", "liquor", "drinks", "alcohol", "ireland", "500ml", "1l", "irish", "cream"]},
        {"id": 12, "name": "Bandipur Whisky", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 6,000", "priceRaw": 6000, "rating": "5.0", "img": "asstes/darumandu_products/bandipur-whisky-750ml.webp", "brand": "Bandipur", "tags": ["bandipur whisky", "whisky", "bandipur", "liquor", "drinks", "alcohol", "nepal", "750ml"]},
        {"id": 13, "name": "Barahsinghe Craft Dunkelweizen Dark Wheat", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 455", "priceRaw": 455, "rating": "4.9", "img": "asstes/darumandu_products/barahsinghe-craft-dunkelweizen-dark-wheat-bottle-650ml.png", "brand": "Barahsinghe", "tags": ["barahsinghe craft dunkelweizen dark wheat", "beer", "barahsinghe", "liquor", "drinks", "alcohol", "international", "650ml (bottle)", "650ml", "craft", "dunkelweizen", "dark", "wheat"]},
        {"id": 14, "name": "Barahsinghe Craft Hazy IPA", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 490", "priceRaw": 490, "rating": "4.9", "img": "asstes/darumandu_products/barahsinghe-craft-hazy-ipa-bottle-650ml.png", "brand": "Barahsinghe", "tags": ["barahsinghe craft hazy ipa", "beer", "barahsinghe", "liquor", "drinks", "alcohol", "nepal", "650ml (bottle)", "650ml", "craft", "hazy", "ipa"]},
        {"id": 15, "name": "Barahsinghe Craft Pilsner", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 455", "priceRaw": 455, "rating": "5.0", "img": "asstes/darumandu_products/barahsinghe-craft-pilsner-650ml.webp", "brand": "Barahsinghe", "tags": ["barahsinghe craft pilsner", "beer", "barahsinghe", "liquor", "drinks", "alcohol", "nepal", "650ml", "craft", "pilsner"]},
        {"id": 16, "name": "Barasinghe Belgian", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 225", "priceRaw": 225, "rating": "4.9", "img": "asstes/darumandu_products/barasinghe-belgian-330ml.webp", "brand": "Barahsinghe", "tags": ["barasinghe belgian", "beer", "barahsinghe", "liquor", "drinks", "alcohol", "nepal", "330ml", "barasinghe", "belgian"]},
        {"id": 17, "name": "Barasinghe Hazy", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 510", "priceRaw": 510, "rating": "4.9", "img": "asstes/darumandu_products/barasinghe-hazy-650ml.jpg", "brand": "Barahsinghe", "tags": ["barasinghe hazy", "beer", "barahsinghe", "liquor", "drinks", "alcohol", "nepal", "650ml", "barasinghe", "hazy"]},
        {"id": 18, "name": "Barasinghe Pale Ale", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 500", "priceRaw": 500, "rating": "5.0", "img": "asstes/darumandu_products/barasinghe-pale-ale-650ml.png", "brand": "Barahsinghe", "tags": ["barasinghe pale ale", "beer", "barahsinghe", "liquor", "drinks", "alcohol", "nepal", "650ml", "barasinghe", "pale", "ale"]},
        {"id": 19, "name": "Barasinghe Pilsner", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 235", "priceRaw": 235, "rating": "4.9", "img": "asstes/darumandu_products/barasinghe-pilsner-330ml.jpg", "brand": "Barahsinghe", "tags": ["barasinghe pilsner", "beer", "barahsinghe", "liquor", "drinks", "alcohol", "nepal", "330ml", "500ml", "barasinghe", "pilsner"]},
        {"id": 20, "name": "Barasinghe Strong", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 270", "priceRaw": 270, "rating": "4.9", "img": "asstes/darumandu_products/barasinghe-strong-500ml.jpg", "brand": "Barahsinghe", "tags": ["barasinghe strong", "beer", "barahsinghe", "liquor", "drinks", "alcohol", "nepal", "500ml", "650ml", "barasinghe", "strong"]},
        {"id": 21, "name": "Baron D'Arignac", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,710", "priceRaw": 1710, "rating": "5.0", "img": "asstes/darumandu_products/baron-darignac-750ml.jpg", "brand": "Baron DArignac", "tags": ["baron d'arignac", "wine", "baron darignac", "liquor", "drinks", "alcohol", "france", "750ml", "baron", "arignac"]},
        {"id": 22, "name": "Beefeater London Dry Gin", "category": "Gin", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 5,380", "priceRaw": 5380, "rating": "4.9", "img": "asstes/darumandu_products/beefeater-london-dry-gin-1l.webp", "brand": "Beefeater London", "tags": ["beefeater london dry gin", "gin", "beefeater london", "liquor", "drinks", "alcohol", "england", "750ml", "beefeater", "london", "dry"]},
        {"id": 23, "name": "Berries & Blues", "category": "Gin", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,386", "priceRaw": 1386, "rating": "4.9", "img": "asstes/darumandu_products/berries-blues-750-ml.webp", "brand": "Berries and Blues", "tags": ["berries & blues", "gin", "berries and blues", "liquor", "drinks", "alcohol", "international", "750ml", "berries", "blues"]},
        {"id": 24, "name": "Big Master Box", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 3,779", "priceRaw": 3779, "rating": "5.0", "img": "asstes/darumandu_products/big-master-box-4ltr.jpg", "brand": "Big Master", "tags": ["big master box", "wine", "big master", "liquor", "drinks", "alcohol", "nepal", "4ltr", "big", "master", "box"]},
        {"id": 25, "name": "Big Master Regular", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 900", "priceRaw": 900, "rating": "4.9", "img": "asstes/darumandu_products/big-master-regular-750ml.png", "brand": "Big Master", "tags": ["big master regular", "wine", "big master", "liquor", "drinks", "alcohol", "nepal", "750ml", "big", "master", "regular"]},
        {"id": 26, "name": "Big Master Sweet Red Box", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 3,780", "priceRaw": 3780, "rating": "4.9", "img": "asstes/darumandu_products/big-master-sweet-red-4l-box.png", "brand": "Big Master", "tags": ["big master sweet red box", "wine", "big master", "liquor", "drinks", "alcohol", "&nbsp;nepal", "4l", "big", "master", "sweet", "red", "box"]},
        {"id": 27, "name": "Big Master Sweet Red Wine", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 900", "priceRaw": 900, "rating": "5.0", "img": "asstes/darumandu_products/big-master-sweet-red-750ml.png", "brand": "Big Master", "tags": ["big master sweet red wine", "wine", "big master", "liquor", "drinks", "alcohol", "&nbsp;nepal", "750ml", "big", "master", "sweet", "red"]},
        {"id": 28, "name": "Black & White Blended Scotch Whisky", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 8,280", "priceRaw": 8280, "rating": "4.9", "img": "asstes/darumandu_products/black-white-blended-scotch-whisky-1l.webp", "brand": "Black & White", "tags": ["black & white blended scotch whisky", "whisky", "black & white", "liquor", "drinks", "alcohol", "scotland", "1l", "black", "white", "blended", "scotch"]},
        {"id": 29, "name": "Black Oak", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 760", "priceRaw": 760, "rating": "4.9", "img": "asstes/darumandu_products/black-oak-375ml.jpg", "brand": "black oak", "tags": ["black oak", "whisky", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml", "black", "oak"]},
        {"id": 30, "name": "Blue Diamond", "category": "Gin", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 630", "priceRaw": 630, "rating": "5.0", "img": "asstes/darumandu_products/blue-diamond-375ml.png", "brand": "Blue Diamond", "tags": ["blue diamond", "gin", "liquor", "drinks", "alcohol", "&nbsp;nepal", "375ml", "blue", "diamond"]},
        {"id": 31, "name": "Blue Nature", "category": "Spirits & Liquor", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 620", "priceRaw": 620, "rating": "4.9", "img": "asstes/darumandu_products/blue-nature-reserved-master-spirit-375ml.webp", "brand": "Blue Nature", "tags": ["blue nature", "spirits & liquor", "liquor", "drinks", "alcohol", "international", "375ml", "750ml", "blue", "nature"]},
        {"id": 32, "name": "Calvet Sauvicnon blanc", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,550", "priceRaw": 2550, "rating": "4.9", "img": "asstes/darumandu_products/calvet-sauvicnon-blanc-750ml.jpg", "brand": "Calvet Sauvicnon", "tags": ["calvet sauvicnon blanc", "wine", "calvet sauvicnon", "liquor", "drinks", "alcohol", "france", "750ml", "calvet", "sauvicnon", "blanc"]},
        {"id": 33, "name": "Carlsberg", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 410", "priceRaw": 410, "rating": "5.0", "img": "asstes/darumandu_products/carlsberg-500ml.jpg", "brand": "Carlsberg", "tags": ["carlsberg", "beer", "liquor", "drinks", "alcohol", "nepal", "500ml", "650ml"]},
        {"id": 34, "name": "Carlsberg Danish Pilsner", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 410", "priceRaw": 410, "rating": "4.9", "img": "asstes/darumandu_products/carlsberg-danish-pilsner-can-500ml.png", "brand": "Carlsberg", "tags": ["carlsberg danish pilsner", "beer", "carlsberg", "liquor", "drinks", "alcohol", "nepal", "500ml (can)", "500ml", "650ml (bottle)", "650ml", "danish", "pilsner"]},
        {"id": 35, "name": "Challenger Whisky", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 630", "priceRaw": 630, "rating": "4.9", "img": "asstes/darumandu_products/challenger-whisky-375ml.png", "brand": "Challenger", "tags": ["challenger whisky", "whisky", "challenger", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml"]},
        {"id": 36, "name": "Chivas Regal 12 Years", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 8,200", "priceRaw": 8200, "rating": "5.0", "img": "asstes/darumandu_products/chivas-regal-12-years-750ml.png", "brand": "Chivas Regal", "tags": ["chivas regal 12 years", "whisky", "chivas regal", "liquor", "drinks", "alcohol", "scotland", "750ml", "1l", "chivas", "regal", "years"]},
        {"id": 37, "name": "Cruzares Airen", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,530", "priceRaw": 1530, "rating": "4.9", "img": "asstes/darumandu_products/cruzares-airen-750ml.jpg", "brand": "Cruzares", "tags": ["cruzares airen", "wine", "cruzares", "liquor", "drinks", "alcohol", "spain", "750ml", "airen"]},
        {"id": 38, "name": "Cruzares Tempranillo Red Wine", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,530", "priceRaw": 1530, "rating": "4.9", "img": "asstes/darumandu_products/cruzares-tempranillo-red-wine-750ml.jpg", "brand": "Cruzares", "tags": ["cruzares tempranillo red wine", "wine", "cruzares", "liquor", "drinks", "alcohol", "spain", "750ml", "tempranillo", "red"]},
        {"id": 39, "name": "Divine White Wine", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 810", "priceRaw": 810, "rating": "5.0", "img": "asstes/darumandu_products/divine-wine-white-750ml.png", "brand": "Divine", "tags": ["divine white wine", "wine", "divine", "liquor", "drinks", "alcohol", "&nbsp;nepal", "750ml", "white"]},
        {"id": 40, "name": "Gilbey's Gin", "category": "Gin", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 6,570", "priceRaw": 6570, "rating": "4.9", "img": "asstes/darumandu_products/gilbeys-gin-1ltr.jpg", "brand": "Gilbeys", "tags": ["gilbey's gin", "gin", "gilbeys", "liquor", "drinks", "alcohol", "united kingdom", "1l", "gilbey"]},
        {"id": 41, "name": "Glenmorangie 10 Years Original Single Malt Whisky", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 9,500", "priceRaw": 9500, "rating": "4.9", "img": "asstes/darumandu_products/glenmorangie-10-years-original-single-malt-whisky-750ml.png", "brand": "Glenmorangie", "tags": ["glenmorangie 10 years original single malt whisky", "whisky", "glenmorangie", "liquor", "drinks", "alcohol", "scotland", "750ml", "years", "original", "single", "malt"]},
        {"id": 42, "name": "Glenmorangie 12yrs Original", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 11,000", "priceRaw": 11000, "rating": "5.0", "img": "asstes/darumandu_products/glenmorangie-12yrs-original-750ml.webp", "brand": "Glenmorangie", "tags": ["glenmorangie 12yrs original", "whisky", "glenmorangie", "liquor", "drinks", "alcohol", "scotland", "750ml", "12yrs", "original"]},
        {"id": 43, "name": "Golden Oak", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 660", "priceRaw": 660, "rating": "4.9", "img": "asstes/darumandu_products/golden-oak-375ml.png", "brand": "Golden Oak", "tags": ["golden oak", "whisky", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml", "golden", "oak"]},
        {"id": 44, "name": "Gorkha Extra Strong Beer", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 200", "priceRaw": 200, "rating": "4.9", "img": "asstes/darumandu_products/gorkha-extra-strong-beer-330ml.png", "brand": "Gorkha", "tags": ["gorkha extra strong beer", "beer", "gorkha", "liquor", "drinks", "alcohol", "nepal", "330ml", "extra", "strong"]},
        {"id": 45, "name": "Gorkha Strong Beer", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 295", "priceRaw": 295, "rating": "5.0", "img": "asstes/darumandu_products/gorkha-strong-beer-can-500ml.png", "brand": "Gorkha", "tags": ["gorkha strong beer", "beer", "gorkha", "liquor", "drinks", "alcohol", "international", "500ml (can)", "500ml", "650ml (bottle)", "650ml", "strong"]},
        {"id": 46, "name": "Grey Wolf Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,386", "priceRaw": 1386, "rating": "4.9", "img": "asstes/darumandu_products/grey-wolf-750ml-vodka.webp", "brand": "Grey Wolf", "tags": ["grey wolf vodka", "vodka", "grey wolf", "liquor", "drinks", "alcohol", "international", "750ml", "grey", "wolf"]},
        {"id": 47, "name": "Gurkhas & Guns", "category": "Spirits & Liquor", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,620", "priceRaw": 1620, "rating": "4.9", "img": "asstes/darumandu_products/gurkhas-guns-375ml.png", "brand": "Gurkhas and Guns", "tags": ["gurkhas & guns", "spirits & liquor", "gurkhas and guns", "liquor", "drinks", "alcohol", "&nbsp;nepal", "375ml", "750ml", "gurkhas", "guns"]},
        {"id": 48, "name": "Hardys Merlot", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,200", "priceRaw": 2200, "rating": "5.0", "img": "asstes/darumandu_products/hardys-merlot-750ml.webp", "brand": "Hardys", "tags": ["hardys merlot", "wine", "hardys", "liquor", "drinks", "alcohol", "australia", "750ml", "merlot"]},
        {"id": 49, "name": "Hardys Moscato", "category": "Spirits & Liquor", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,980", "priceRaw": 1980, "rating": "4.9", "img": "asstes/darumandu_products/hardys-moscato-750ml.jpg", "brand": "Hardys", "tags": ["hardys moscato", "spirits & liquor", "hardys", "liquor", "drinks", "alcohol", "international", "750ml", "moscato"]},
        {"id": 50, "name": "Highlander Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 630", "priceRaw": 630, "rating": "4.9", "img": "asstes/darumandu_products/highlander-vodka-375ml.png", "brand": "Highlander", "tags": ["highlander vodka", "vodka", "highlander", "liquor", "drinks", "alcohol", "international", "375ml", "750ml"]},
        {"id": 51, "name": "Himalayan Honey Hunter 4 Years Rum", "category": "Rum", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,345", "priceRaw": 2345, "rating": "5.0", "img": "asstes/darumandu_products/himalayan-honey-hunter-4-years-rum-750ml.png", "brand": "Himalayan Honey Hunter", "tags": ["himalayan honey hunter 4 years rum", "rum", "himalayan honey hunter", "liquor", "drinks", "alcohol", "international", "750ml", "himalayan", "honey", "hunter", "years"]},
        {"id": 52, "name": "Himalayan Honey Hunter", "category": "Rum", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,340", "priceRaw": 2340, "rating": "4.9", "img": "asstes/darumandu_products/himalayan-honey-hunter-750ml.jpg", "brand": "Himalayan Honey Hunter", "tags": ["himalayan honey hunter", "rum", "liquor", "drinks", "alcohol", "nepal", "750ml", "himalayan", "honey", "hunter"]},
        {"id": 53, "name": "Himalayen Reserve", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 3,780", "priceRaw": 3780, "rating": "4.9", "img": "asstes/darumandu_products/himalayen-reserve-750ml.png", "brand": "Himalayan", "tags": ["himalayen reserve", "whisky", "himalayan", "liquor", "drinks", "alcohol", "nepal", "750ml", "himalayen", "reserve"]},
        {"id": 54, "name": "J P Chenet Medium Sweet Red", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,205", "priceRaw": 2205, "rating": "5.0", "img": "asstes/darumandu_products/j-p-chenet-medium-sweet-red-750ml.jpg", "brand": "JP Chenet", "tags": ["j p chenet medium sweet red", "wine", "jp chenet", "liquor", "drinks", "alcohol", "france", "750ml", "chenet", "medium", "sweet", "red"]},
        {"id": 55, "name": "J P Chenet Medium Sweet White", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,205", "priceRaw": 2205, "rating": "4.9", "img": "asstes/darumandu_products/j-p-chenet-medium-sweet-white-750ml.jpg", "brand": "JP Chenet", "tags": ["j p chenet medium sweet white", "wine", "jp chenet", "liquor", "drinks", "alcohol", "france", "750ml", "chenet", "medium", "sweet", "white"]},
        {"id": 56, "name": "J&B Rare", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 6,550", "priceRaw": 6550, "rating": "4.9", "img": "asstes/darumandu_products/jb-rare-1l.png", "brand": "JB", "tags": ["j&b rare", "whisky", "jb", "liquor", "drinks", "alcohol", "scotland", "1l", "rare"]},
        {"id": 57, "name": "J&B Rare Blended Scotch Whisky", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 7,550", "priceRaw": 7550, "rating": "5.0", "img": "asstes/darumandu_products/jb-rare-blended-scotch-whisky-750ml.webp", "brand": "JB", "tags": ["j&b rare blended scotch whisky", "whisky", "jb", "liquor", "drinks", "alcohol", "scotland", "750ml", "rare", "blended", "scotch"]},
        {"id": 58, "name": "JP Chenet Cabernet Sauvignon", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,350", "priceRaw": 2350, "rating": "4.9", "img": "asstes/darumandu_products/jp-chenet-cabernet-sauvignon-750ml.png", "brand": "JP Chenet", "tags": ["jp chenet cabernet sauvignon", "wine", "jp chenet", "liquor", "drinks", "alcohol", "international", "750ml", "chenet", "cabernet", "sauvignon"]},
        {"id": 59, "name": "JP Chenet Sweet White", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,350", "priceRaw": 2350, "rating": "4.9", "img": "asstes/darumandu_products/jp-chenet-sweet-white-750ml.png", "brand": "JP Chenet", "tags": ["jp chenet sweet white", "wine", "jp chenet", "liquor", "drinks", "alcohol", "france", "750ml", "chenet", "sweet", "white"]},
        {"id": 60, "name": "Jack Daniel's", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,955", "priceRaw": 1955, "rating": "5.0", "img": "asstes/darumandu_products/jack-deniels-200ml.jpg", "brand": "Jack Daniels", "tags": ["jack daniel's", "whisky", "jack daniels", "liquor", "drinks", "alcohol", "united states", "200ml", "500ml", "750ml", "1l", "jack", "daniel"]},
        {"id": 61, "name": "Jack Daniel's Sinatra Select", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 24,240", "priceRaw": 24240, "rating": "4.9", "img": "asstes/darumandu_products/jack-daniels-sinatra-select-1l.png", "brand": "Jack Daniels", "tags": ["jack daniel's sinatra select", "whisky", "jack daniels", "liquor", "drinks", "alcohol", "united states of america", "1l", "jack", "daniel", "sinatra", "select"]},
        {"id": 62, "name": "Jacob's Creek Classic Merlot", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,350", "priceRaw": 2350, "rating": "4.9", "img": "asstes/darumandu_products/jacobs-creek-classic-merlot-750ml.png", "brand": "Jacobs Creek", "tags": ["jacob's creek classic merlot", "wine", "jacobs creek", "liquor", "drinks", "alcohol", "australia", "750ml", "jacob", "creek", "classic", "merlot"]},
        {"id": 63, "name": "Jacob's Creek Chardonnay", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,350", "priceRaw": 2350, "rating": "5.0", "img": "asstes/darumandu_products/jacobs-creek-chardonnay-750ml.jpg", "brand": "Jacobs Creek", "tags": ["jacob's creek chardonnay", "wine", "jacobs creek", "liquor", "drinks", "alcohol", "australia", "750ml", "jacob", "creek", "chardonnay"]},
        {"id": 64, "name": "Jacob's Creek Merlot Shiraz", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,350", "priceRaw": 2350, "rating": "4.9", "img": "asstes/darumandu_products/jacobs-creek-merlot-shiraz-750ml.jpg", "brand": "Jacobs Creek", "tags": ["jacob's creek merlot shiraz", "wine", "jacobs creek", "liquor", "drinks", "alcohol", "australia", "750ml", "jacob", "creek", "merlot", "shiraz"]},
        {"id": 65, "name": "Jacob's Creek Shiraz Cabernet", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,350", "priceRaw": 2350, "rating": "4.9", "img": "asstes/darumandu_products/jacobs-creek-shiraz-cabernet-750ml.jpg", "brand": "Jacobs Creek", "tags": ["jacob's creek shiraz cabernet", "wine", "jacobs creek", "liquor", "drinks", "alcohol", "australia", "750ml", "jacob", "creek", "shiraz", "cabernet"]},
        {"id": 66, "name": "Jagermeister Herbal Liqueur", "category": "Liqueur", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 8,400", "priceRaw": 8400, "rating": "5.0", "img": "asstes/darumandu_products/jagermeister-herbal-liqueur-1-ltr.webp", "brand": "Jagermeister", "tags": ["jagermeister herbal liqueur", "liqueur", "jagermeister", "liquor", "drinks", "alcohol", "germany", "1l", "herbal"]},
        {"id": 67, "name": "Jameson Irish Whiskey", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,850", "priceRaw": 1850, "rating": "4.9", "img": "asstes/darumandu_products/jameson-irish-whiskey-200ml.webp", "brand": "Jameson", "tags": ["jameson irish whiskey", "whisky", "jameson", "liquor", "drinks", "alcohol", "ireland", "200ml", "500ml", "1l", "irish", "whiskey"]},
        {"id": 68, "name": "Johnnie Walker Black Label", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 9,950", "priceRaw": 9950, "rating": "4.9", "img": "asstes/darumandu_products/johnnie-walker-black-label-1l.png", "brand": "Johnnie Walker", "tags": ["johnnie walker black label", "whisky", "johnnie walker", "liquor", "drinks", "alcohol", "scotland", "1l", "johnnie", "walker", "black", "label"]},
        {"id": 69, "name": "Johnnie Walker Double Black", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 8,900", "priceRaw": 8900, "rating": "5.0", "img": "asstes/darumandu_products/double-black-750ml.jpg", "brand": "Johnnie Walker", "tags": ["johnnie walker double black", "whisky", "johnnie walker", "liquor", "drinks", "alcohol", "international", "750ml", "1l", "johnnie", "walker", "double", "black"]},
        {"id": 70, "name": "Johnnie Walker Red Label", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 7,050", "priceRaw": 7050, "rating": "4.9", "img": "asstes/darumandu_products/johnnie-walker-red-label-1l.png", "brand": "Johnnie Walker", "tags": ["johnnie walker red label", "whisky", "johnnie walker", "liquor", "drinks", "alcohol", "scotland", "1l", "johnnie", "walker", "red", "label"]},
        {"id": 71, "name": "Kala Patthar", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,440", "priceRaw": 1440, "rating": "4.9", "img": "asstes/darumandu_products/kala-patthar-375ml.png", "brand": "Kala Patthar", "tags": ["kala patthar", "whisky", "liquor", "drinks", "alcohol", "nepal", "375ml", "kala", "patthar"]},
        {"id": 72, "name": "Kala Patthar Blended Reserve", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,880", "priceRaw": 2880, "rating": "5.0", "img": "asstes/darumandu_products/kala-patthar-blended-reserve-750ml.png", "brand": "Kala Patthar", "tags": ["kala patthar blended reserve", "whisky", "kala patthar", "liquor", "drinks", "alcohol", "nepal", "750ml", "kala", "patthar", "blended", "reserve"]},
        {"id": 73, "name": "Khukri Coronation Rum", "category": "Rum", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 9,000", "priceRaw": 9000, "rating": "4.9", "img": "asstes/darumandu_products/khukri-coronation-rum-375ml.png", "brand": "Khukri", "tags": ["khukri coronation rum", "rum", "khukri", "liquor", "drinks", "alcohol", "nepal", "375ml", "coronation"]},
        {"id": 74, "name": "Khukri Rum", "category": "Rum", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,140", "priceRaw": 1140, "rating": "4.9", "img": "asstes/darumandu_products/khukri-rum-375ml.png", "brand": "Khukri", "tags": ["khukri rum", "rum", "khukri", "liquor", "drinks", "alcohol", "international", "375ml", "750ml"]},
        {"id": 75, "name": "Khukri Spice Rum", "category": "Rum", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,224", "priceRaw": 1224, "rating": "5.0", "img": "asstes/darumandu_products/khukuri-rum-spice-375ml.jpg", "brand": "Khukri", "tags": ["khukri spice rum", "rum", "khukri", "liquor", "drinks", "alcohol", "international", "375ml", "750ml", "spice"]},
        {"id": 76, "name": "King's Hill", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 850", "priceRaw": 850, "rating": "4.9", "img": "asstes/darumandu_products/kings-hill-750ml.jpg", "brand": "Kings Hill", "tags": ["king's hill", "wine", "kings hill", "liquor", "drinks", "alcohol", "nepal", "750ml", "king", "hill"]},
        {"id": 77, "name": "King's Hill Red sweet wine", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 865", "priceRaw": 865, "rating": "4.9", "img": "asstes/darumandu_products/kings-hill-red-sweet-wine-750ml.png", "brand": "Kings Hill", "tags": ["king's hill red sweet wine", "wine", "kings hill", "liquor", "drinks", "alcohol", "international", "750ml", "king", "hill", "red", "sweet"]},
        {"id": 78, "name": "Lindeman's Cawarra Semillon Chardonnay", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,250", "priceRaw": 2250, "rating": "5.0", "img": "asstes/darumandu_products/lindemans-cawarra-semillon-chardonnay-750ml.webp", "brand": "Lindeman", "tags": ["lindeman's cawarra semillon chardonnay", "wine", "lindeman", "liquor", "drinks", "alcohol", "international", "750ml", "cawarra", "semillon", "chardonnay"]},
        {"id": 79, "name": "Lindeman's Sweet Red", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,070", "priceRaw": 2070, "rating": "4.9", "img": "asstes/darumandu_products/lindemans-sweet-red-750ml.jpg", "brand": "Lindeman", "tags": ["lindeman's sweet red", "wine", "lindeman", "liquor", "drinks", "alcohol", "australia", "750ml", "sweet", "red"]},
        {"id": 80, "name": "Lindeman's Cawarra Shiraz Cabernet", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,250", "priceRaw": 2250, "rating": "4.9", "img": "asstes/darumandu_products/lindemans-cawarra-shiraz-cabernet-750ml.webp", "brand": "Lindeman", "tags": ["lindeman's cawarra shiraz cabernet", "wine", "lindeman", "liquor", "drinks", "alcohol", "australia", "750ml", "cawarra", "shiraz", "cabernet"]},
        {"id": 81, "name": "MAXX Premium Blended Reserve", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 570", "priceRaw": 570, "rating": "5.0", "img": "asstes/darumandu_products/maxx-premium-blended-reserve-375ml.webp", "brand": "MAXX", "tags": ["maxx premium blended reserve", "whisky", "maxx", "liquor", "drinks", "alcohol", "international", "375ml", "750ml", "premium", "blended", "reserve"]},
        {"id": 82, "name": "Macallan", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 12,060", "priceRaw": 12060, "rating": "4.9", "img": "asstes/darumandu_products/macallan-750ml.jpg", "brand": "The Macallan", "tags": ["macallan", "whisky", "the macallan", "liquor", "drinks", "alcohol", "scotland", "750ml"]},
        {"id": 83, "name": "Manang Valley Premium Dry White Wine", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,250", "priceRaw": 1250, "rating": "4.9", "img": "asstes/darumandu_products/manang-valley-premium-dry-white-wine-750ml.png", "brand": "Manang Valley", "tags": ["manang valley premium dry white wine", "wine", "manang valley", "liquor", "drinks", "alcohol", "international", "750ml", "manang", "valley", "premium", "dry", "white"]},
        {"id": 84, "name": "Manang Valley Premium Rose Wine", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,239", "priceRaw": 1239, "rating": "5.0", "img": "asstes/darumandu_products/manang-valley-premium-rose-750ml.png", "brand": "Manang Valley", "tags": ["manang valley premium rose wine", "wine", "manang valley", "liquor", "drinks", "alcohol", "&nbsp;nepal", "750ml", "manang", "valley", "premium", "rose"]},
        {"id": 85, "name": "Medinate Sweet Wine", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,835", "priceRaw": 1835, "rating": "4.9", "img": "asstes/darumandu_products/medinate-sweet-750ml.webp", "brand": "Medinet", "tags": ["medinate sweet wine", "wine", "medinet", "liquor", "drinks", "alcohol", "international", "750ml", "medinate", "sweet"]},
        {"id": 86, "name": "Medinet Sweet Red", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,629", "priceRaw": 1629, "rating": "4.9", "img": "asstes/darumandu_products/medinet-sweet-red-750ml.webp", "brand": "Medinet", "tags": ["medinet sweet red", "wine", "medinet", "liquor", "drinks", "alcohol", "france", "750ml", "sweet", "red"]},
        {"id": 87, "name": "Moet & Chandon", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 16,500", "priceRaw": 16500, "rating": "5.0", "img": "asstes/darumandu_products/moet-chandon-750ml.webp", "brand": "Moet Chandon", "tags": ["moet & chandon", "wine", "moet chandon", "liquor", "drinks", "alcohol", "france", "750ml", "moet", "chandon"]},
        {"id": 88, "name": "Mustang Black Whisky", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 720", "priceRaw": 720, "rating": "4.9", "img": "asstes/darumandu_products/mustang-black-375ml.png", "brand": "Mustang", "tags": ["mustang black whisky", "whisky", "mustang", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml", "black"]},
        {"id": 89, "name": "Mustang Gold", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 630", "priceRaw": 630, "rating": "4.9", "img": "asstes/darumandu_products/mustang-gold-375ml.png", "brand": "Mustang", "tags": ["mustang gold", "whisky", "mustang", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml", "gold"]},
        {"id": 90, "name": "Mustang Pure Perfection Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,160", "priceRaw": 1160, "rating": "5.0", "img": "asstes/darumandu_products/mustang-pure-perfection-vodka-750ml.webp", "brand": "Mustang", "tags": ["mustang pure perfection vodka", "vodka", "mustang", "liquor", "drinks", "alcohol", "nepal", "750ml", "pure", "perfection"]},
        {"id": 91, "name": "Nepal Ice", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 190", "priceRaw": 190, "rating": "4.9", "img": "asstes/darumandu_products/nepal-ice-330ml.jpg", "brand": "Nepal Ice Beer", "tags": ["nepal ice", "beer", "nepal ice beer", "liquor", "drinks", "alcohol", "nepal", "330ml", "500ml", "650ml", "ice"]},
        {"id": 92, "name": "Nepse Bulls", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 4,900", "priceRaw": 4900, "rating": "4.9", "img": "asstes/darumandu_products/nepse-bulls-750ml.webp", "brand": "Nepse Bulls", "tags": ["nepse bulls", "whisky", "liquor", "drinks", "alcohol", "international", "750ml", "nepse", "bulls"]},
        {"id": 93, "name": "Nude Superior Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,180", "priceRaw": 1180, "rating": "5.0", "img": "asstes/darumandu_products/nude-superior-vodka-375ml.png", "brand": "Nude", "tags": ["nude superior vodka", "vodka", "nude", "liquor", "drinks", "alcohol", "international", "375ml", "750ml", "superior"]},
        {"id": 94, "name": "Oasis", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 620", "priceRaw": 620, "rating": "4.9", "img": "asstes/darumandu_products/oasis-375-ml.webp", "brand": "Oasis", "tags": ["oasis", "vodka", "liquor", "drinks", "alcohol", "international", "375ml", "750ml"]},
        {"id": 95, "name": "Old Durbar 12 Years", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 6,045", "priceRaw": 6045, "rating": "4.9", "img": "asstes/darumandu_products/old-durbar-12-years-750ml.png", "brand": "Old Durbar", "tags": ["old durbar 12 years", "whisky", "old durbar", "liquor", "drinks", "alcohol", "nepal", "750ml", "old", "durbar", "years"]},
        {"id": 96, "name": "Old Durbar Black Chimney", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,980", "priceRaw": 1980, "rating": "5.0", "img": "asstes/darumandu_products/old-durbar-black-chimney-375ml.png", "brand": "Old Durbar", "tags": ["old durbar black chimney", "whisky", "old durbar", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml", "1l", "old", "durbar", "black", "chimney"]},
        {"id": 97, "name": "Old Durbar Regular", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,529", "priceRaw": 1529, "rating": "4.9", "img": "asstes/darumandu_products/old-durbar-regular-375ml.png", "brand": "Old Durbar", "tags": ["old durbar regular", "whisky", "old durbar", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml", "1l", "old", "durbar", "regular"]},
        {"id": 98, "name": "Old Durbar Reserve", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 3,050", "priceRaw": 3050, "rating": "4.9", "img": "asstes/darumandu_products/old-durbar-reserve-750ml.png", "brand": "Old Durbar", "tags": ["old durbar reserve", "whisky", "old durbar", "liquor", "drinks", "alcohol", "nepal", "750ml", "old", "durbar", "reserve"]},
        {"id": 99, "name": "Old Monk The Legend Rum", "category": "Rum", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,600", "priceRaw": 2600, "rating": "5.0", "img": "asstes/darumandu_products/old-monk-the-legend-rum-750ml.png", "brand": "Old Monk", "tags": ["old monk the legend rum", "rum", "old monk", "liquor", "drinks", "alcohol", "nepal", "750ml", "old", "monk", "the", "legend"]},
        {"id": 100, "name": "Old Monk XXX Rum", "category": "Rum", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,090", "priceRaw": 1090, "rating": "4.9", "img": "asstes/darumandu_products/old-monk-xxx-375ml.jpg", "brand": "Old Monk", "tags": ["old monk xxx rum", "rum", "old monk", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml", "old", "monk", "xxx"]},
        {"id": 101, "name": "Pataleban Red Kaule", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,200", "priceRaw": 1200, "rating": "4.9", "img": "asstes/darumandu_products/pataleban-red-kaule-750ml.webp", "brand": "Pataleban", "tags": ["pataleban red kaule", "wine", "pataleban", "liquor", "drinks", "alcohol", "nepal", "750ml", "red", "kaule"]},
        {"id": 102, "name": "Pataleban Rose Koshu", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,200", "priceRaw": 1200, "rating": "5.0", "img": "asstes/darumandu_products/pataleban-rose-koshu-750ml.webp", "brand": "Pataleban", "tags": ["pataleban rose koshu", "wine", "pataleban", "liquor", "drinks", "alcohol", "nepal", "750ml", "rose", "koshu"]},
        {"id": 103, "name": "Pataleban White Ashish", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,200", "priceRaw": 1200, "rating": "4.9", "img": "asstes/darumandu_products/pataleban-white-ashish-750ml.webp", "brand": "Pataleban", "tags": ["pataleban white ashish", "wine", "pataleban", "liquor", "drinks", "alcohol", "nepal", "750ml", "white", "ashish"]},
        {"id": 104, "name": "Porto Ruby WIne", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 3,375", "priceRaw": 3375, "rating": "4.9", "img": "asstes/darumandu_products/porto-ruby-wine-750ml.jpg", "brand": "Porto", "tags": ["porto ruby wine", "wine", "porto", "liquor", "drinks", "alcohol", "portugal", "750ml", "ruby"]},
        {"id": 105, "name": "Porto White", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 3,375", "priceRaw": 3375, "rating": "5.0", "img": "asstes/darumandu_products/porto-white-750ml.jpg", "brand": "Porto", "tags": ["porto white", "wine", "porto", "liquor", "drinks", "alcohol", "portugal", "750ml", "white"]},
        {"id": 106, "name": "Rara Blues", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,260", "priceRaw": 1260, "rating": "4.9", "img": "asstes/darumandu_products/rara-blues-750ml.jpg", "brand": "Rara Blues", "tags": ["rara blues", "whisky", "liquor", "drinks", "alcohol", "nepal", "750ml", "rara", "blues"]},
        {"id": 107, "name": "Red Nature Whiskey", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 620", "priceRaw": 620, "rating": "4.9", "img": "asstes/darumandu_products/red-nature-master-blenders-reserve-selection-375ml.webp", "brand": "Red Nature", "tags": ["red nature whiskey", "whisky", "red nature", "liquor", "drinks", "alcohol", "international", "375ml", "red", "nature", "whiskey"]},
        {"id": 108, "name": "Red Nature Whisky", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,240", "priceRaw": 1240, "rating": "5.0", "img": "asstes/darumandu_products/red-nature-blended-whisky-750-ml.webp", "brand": "Red Nature", "tags": ["red nature whisky", "whisky", "red nature", "liquor", "drinks", "alcohol", "international", "750ml", "red", "nature"]},
        {"id": 109, "name": "Robertson Winery Sweet Red", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,835", "priceRaw": 1835, "rating": "4.9", "img": "asstes/darumandu_products/robertson-winery-sweet-red-750ml.png", "brand": "Robertson Winery", "tags": ["robertson winery sweet red", "wine", "robertson winery", "liquor", "drinks", "alcohol", "south africa", "750ml", "robertson", "winery", "sweet", "red"]},
        {"id": 110, "name": "Robertson Winery Sweet White", "category": "Wine", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,835", "priceRaw": 1835, "rating": "4.9", "img": "asstes/darumandu_products/robertson-winery-sweet-white-750ml.png", "brand": "Robertson Winery", "tags": ["robertson winery sweet white", "wine", "robertson winery", "liquor", "drinks", "alcohol", "south africa", "750ml", "robertson", "winery", "sweet", "white"]},
        {"id": 111, "name": "Royal Blue Whiskey", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 620", "priceRaw": 620, "rating": "5.0", "img": "asstes/darumandu_products/royal-blue-375-ml.webp", "brand": "Royal Blue", "tags": ["royal blue whiskey", "whisky", "royal blue", "liquor", "drinks", "alcohol", "international", "375ml", "750ml", "royal", "blue", "whiskey"]},
        {"id": 112, "name": "Ruslan Lemon Iced Tea", "category": "Liqueur", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 225", "priceRaw": 225, "rating": "4.9", "img": "asstes/darumandu_products/ruslan-lemon-iced-tea-275ml.webp", "brand": "Ruslan", "tags": ["ruslan lemon iced tea", "liqueur", "ruslan", "liquor", "drinks", "alcohol", "international", "275ml", "lemon", "iced", "tea"]},
        {"id": 113, "name": "Ruslan Peach Iced Tea", "category": "Liqueur", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 225", "priceRaw": 225, "rating": "4.9", "img": "asstes/darumandu_products/ruslan-peach-iced-tea-275ml.webp", "brand": "Ruslan", "tags": ["ruslan peach iced tea", "liqueur", "ruslan", "liquor", "drinks", "alcohol", "international", "275ml", "peach", "iced", "tea"]},
        {"id": 114, "name": "Ruslan Premium Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,180", "priceRaw": 1180, "rating": "5.0", "img": "asstes/darumandu_products/ruslan-premium-vodka-375ml.png", "brand": "Ruslan", "tags": ["ruslan premium vodka", "vodka", "ruslan", "liquor", "drinks", "alcohol", "international", "375ml", "750ml", "premium"]},
        {"id": 115, "name": "Seto Bagh Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,140", "priceRaw": 1140, "rating": "4.9", "img": "asstes/darumandu_products/seto-bagh-vodka-375ml.png", "brand": "Seto Bagh", "tags": ["seto bagh vodka", "vodka", "seto bagh", "liquor", "drinks", "alcohol", "&nbsp;nepal", "375ml", "750ml", "seto", "bagh"]},
        {"id": 116, "name": "Shikhar vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,260", "priceRaw": 1260, "rating": "4.9", "img": "asstes/darumandu_products/shikhar-vodka-750ml.jpg", "brand": "Shikhar", "tags": ["shikhar vodka", "vodka", "shikhar", "liquor", "drinks", "alcohol", "nepal", "750ml"]},
        {"id": 117, "name": "Signature Green", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,395", "priceRaw": 1395, "rating": "5.0", "img": "asstes/darumandu_products/signature-green-375ml.png", "brand": "Signature", "tags": ["signature green", "whisky", "signature", "liquor", "drinks", "alcohol", "nepal", "375ml", "green"]},
        {"id": 118, "name": "Signature Premier Grain Whisky", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,465", "priceRaw": 1465, "rating": "4.9", "img": "asstes/darumandu_products/signature-premier-375ml.png", "brand": "Signature", "tags": ["signature premier grain whisky", "whisky", "signature", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml", "premier", "grain"]},
        {"id": 119, "name": "Signature Rare Aged", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,790", "priceRaw": 2790, "rating": "4.9", "img": "asstes/darumandu_products/signature-rare-aged-750ml.png", "brand": "Signature", "tags": ["signature rare aged", "whisky", "signature", "liquor", "drinks", "alcohol", "nepal", "750ml", "rare", "aged"]},
        {"id": 120, "name": "Silver Oak Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 630", "priceRaw": 630, "rating": "5.0", "img": "asstes/darumandu_products/silver-oak-vodka-375ml.png", "brand": "Silver Oak", "tags": ["silver oak vodka", "vodka", "silver oak", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml", "silver", "oak"]},
        {"id": 121, "name": "Singleton Premium Whisky", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 11,000", "priceRaw": 11000, "rating": "4.9", "img": "asstes/darumandu_products/singleton-premium-whisky-700ml.webp", "brand": "The Singleton", "tags": ["singleton premium whisky", "whisky", "the singleton", "liquor", "drinks", "alcohol", "scotland", "700ml", "singleton", "premium"]},
        {"id": 122, "name": "Smirnoff Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,170", "priceRaw": 1170, "rating": "4.9", "img": "asstes/darumandu_products/smirnoff-375ml.png", "brand": "Smirnoff", "tags": ["smirnoff vodka", "vodka", "smirnoff", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml"]},
        {"id": 123, "name": "Stallion Whiskey", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 630", "priceRaw": 630, "rating": "5.0", "img": "asstes/darumandu_products/stallion-whiskey-375ml.jpeg", "brand": "Smirnoff", "tags": ["stallion whiskey", "whisky", "smirnoff", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml", "stallion", "whiskey"]},
        {"id": 124, "name": "Teacher's Highland Cream", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 6,450", "priceRaw": 6450, "rating": "4.9", "img": "asstes/darumandu_products/teachers-highland-cream-1l.png", "brand": "teachers", "tags": ["teacher's highland cream", "whisky", "teachers", "liquor", "drinks", "alcohol", "scotland", "1l", "teacher", "highland", "cream"]},
        {"id": 125, "name": "The Governor Smokewood Cask", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 2,980", "priceRaw": 2980, "rating": "4.9", "img": "asstes/darumandu_products/the-governor-smokewood-cask-750ml.webp", "brand": "The Governor", "tags": ["the governor smokewood cask", "whisky", "the governor", "liquor", "drinks", "alcohol", "international", "750ml", "the", "governor", "smokewood", "cask"]},
        {"id": 126, "name": "The Himalayan Reserve", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 3,780", "priceRaw": 3780, "rating": "5.0", "img": "asstes/darumandu_products/the-himalayan-reserve-750ml.png", "brand": "Himalayan", "tags": ["the himalayan reserve", "whisky", "himalayan", "liquor", "drinks", "alcohol", "nepal", "750ml", "the", "reserve"]},
        {"id": 127, "name": "The Macallan 12yrs Triple Cask Matured", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 12,190", "priceRaw": 12190, "rating": "4.9", "img": "asstes/darumandu_products/the-macallan-12yrs-triple-cask-matured-700ml.png", "brand": "The Macallan", "tags": ["the macallan 12yrs triple cask matured", "whisky", "the macallan", "liquor", "drinks", "alcohol", "scotland", "700ml", "the", "macallan", "12yrs", "triple", "cask", "matured"]},
        {"id": 128, "name": "Tuborg Beer", "category": "Beer", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 355", "priceRaw": 355, "rating": "4.9", "img": "asstes/darumandu_products/tuborg-beer-can-500ml.png", "brand": "Tuborg", "tags": ["tuborg beer", "beer", "tuborg", "liquor", "drinks", "alcohol", "nepal", "500ml (can)", "500ml", "650ml (bottle)", "650ml"]},
        {"id": 129, "name": "Two Keys Finest Blended Reserve", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 1,260", "priceRaw": 1260, "rating": "5.0", "img": "asstes/darumandu_products/two-keys-finest-blended-reserve-750ml.png", "brand": "Two Keys", "tags": ["two keys finest blended reserve", "whisky", "two keys", "liquor", "drinks", "alcohol", "nepal", "750ml", "two", "keys", "finest", "blended", "reserve"]},
        {"id": 130, "name": "Two Kyes", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 630", "priceRaw": 630, "rating": "4.9", "img": "asstes/darumandu_products/two-kyes-375ml.png", "brand": "Two Keys", "tags": ["two kyes", "whisky", "two keys", "liquor", "drinks", "alcohol", "nepal", "375ml", "two", "kyes"]},
        {"id": 131, "name": "Vat 69", "category": "Whisky", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 4,725", "priceRaw": 4725, "rating": "4.9", "img": "asstes/darumandu_products/vat-69-750ml.jpg", "brand": "Vat 69", "tags": ["vat 69", "whisky", "liquor", "drinks", "alcohol", "scotland", "750ml", "1l", "vat"]},
        {"id": 132, "name": "Yarchagumba Golden Sapphire", "category": "Spirits & Liquor", "dept": "Liquor", "deptKey": "liquor", "price": "Rs. 11,000", "priceRaw": 11000, "rating": "5.0", "img": "asstes/darumandu_products/yarchagumba-golden-sapphire-750ml.png", "brand": "Yarchagumba", "tags": ["yarchagumba golden sapphire", "spirits & liquor", "yarchagumba", "liquor", "drinks", "alcohol", "nepal", "750ml", "golden", "sapphire"]},
        {"id": 133, "name": "Yeti Vodka", "category": "Vodka", "dept": "Liquor", "deptKey": "liquor", "price": "From Rs. 1,188", "priceRaw": 1188, "rating": "4.9", "img": "asstes/darumandu_products/yeti-vodka-375ml.png", "brand": "Yeti", "tags": ["yeti vodka", "vodka", "yeti", "liquor", "drinks", "alcohol", "nepal", "375ml", "750ml"]},
        // --- GROCERY PRODUCTS ---
        {
            id: 101,
            name: "Organic Wild Himalayan Honey (500g)",
            category: "Organic Speciality",
            dept: "Groceries",
            deptKey: "grocery",
            price: "Rs. 1,850",
            priceRaw: 1850,
            rating: "5.0",
            img: "asstes/website-designs/grocries/gm-23ed737a-a2a5-4ce4-995e-9426e7bacf3a-groceries.jpeg",
            brand: "Himalayan Organics",
            tags: ["honey", "himalayan honey", "wild honey", "organic honey", "sweetener", "raw honey", "organic"]
        },
        {
            id: 102,
            name: "Gourmet Roasted Nuts & Dried Fruit Pack (1kg)",
            category: "Snacks",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 650",
            priceRaw: 650,
            rating: "4.9",
            img: "asstes/website-designs/alcohol design/classics_tobacco.png",
            brand: "Annapurna Pantry",
            tags: ["nuts", "cashews", "almonds", "dried fruit", "snacks", "pantry", "grocery"]
        },
        {
            id: 103,
            name: "Premium Packaged Breakfast Cereal & Oats",
            category: "Packaged Foods",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 420",
            priceRaw: 420,
            rating: "4.8",
            img: "asstes/website-designs/alcohol design/classics_gin.png",
            brand: "Goldstar Pantry",
            tags: ["cereal", "oats", "breakfast", "packaged food", "pantry", "groceries"]
        },
        {
            id: 104,
            name: "Artisanal Whole Wheat Toast & Sourdough Crackers",
            category: "Biscuits & Cookies",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 350",
            priceRaw: 350,
            rating: "4.9",
            img: "asstes/website-designs/alcohol design/classics_spirits.png",
            brand: "Annapurna Bakery",
            tags: ["biscuits", "cookies", "toast", "crackers", "sourdough", "bakery", "snacks", "chips"]
        },
        {
            id: 105,
            name: "Premium Himalayan Aged Basmati Rice (5kg)",
            category: "Rice & Grains",
            dept: "Groceries",
            deptKey: "grocery",
            price: "Rs. 1,450",
            priceRaw: 1450,
            rating: "5.0",
            img: "asstes/website-designs/grocries/R.jpg",
            brand: "Goldstar Pantry",
            tags: ["rice", "basmati rice", "grains", "himalayan rice", "pantry", "aged rice"]
        },
        {
            id: 106,
            name: "Organic Kashmiri Saffron & Cardamom Pack",
            category: "Spices & Masala",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 2,200",
            priceRaw: 2200,
            rating: "5.0",
            img: "asstes/website-designs/grocries/supermarket_cart.jpeg",
            brand: "Himalayan Organics",
            tags: ["saffron", "cardamom", "spices", "kashmiri saffron", "gourmet", "elaichi", "kesar"]
        },
        {
            id: 107,
            name: "Cold Pressed Extra Virgin Mustard Oil (2L)",
            category: "Cooking Oil",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 780",
            priceRaw: 780,
            rating: "4.7",
            img: "asstes/website-designs/grocries/R.jpg",
            brand: "Goldstar Pantry",
            tags: ["mustard oil", "cooking oil", "cold pressed", "spices", "tori ko tel", "pure"]
        },
        {
            id: 108,
            name: "Dried Fruit & Nut Mix Family Pack (1.5kg)",
            category: "Snacks",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 520",
            priceRaw: 520,
            rating: "4.9",
            img: "asstes/website-designs/alcohol design/classics_tobacco.png",
            brand: "Annapurna Pantry",
            tags: ["nuts", "dried fruit", "cashews", "raisins", "family pack", "pantry", "groceries"]
        },
        {
            id: 109,
            name: "Himalayan Whole Grain Oatmeal & Cereal Pack",
            category: "Packaged Foods",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 550",
            priceRaw: 550,
            rating: "4.9",
            img: "asstes/website-designs/alcohol design/wine_closeup.jpg",
            brand: "Annapurna Pantry",
            tags: ["oats", "oatmeal", "cereal", "breakfast", "whole grain", "groceries"]
        },
        {
            id: 110,
            name: "Pure Yak Ghee Himalayan Tradition (500g)",
            category: "Cooking Oil",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 1,650",
            priceRaw: 1650,
            rating: "5.0",
            img: "asstes/website-designs/grocries/gm-23ed737a-a2a5-4ce4-995e-9426e7bacf3a-groceries.jpeg",
            brand: "Himalayan Organics",
            tags: ["ghee", "yak ghee", "clarified butter", "cooking oil", "oil", "traditional", "pantry"]
        },
        {
            id: 111,
            name: "Natural Sparkling Spring Water (Case of 12)",
            category: "Soft Drinks & Beverages",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 960",
            priceRaw: 960,
            rating: "4.8",
            img: "asstes/website-designs/grocries/gm-23ed737a-a2a5-4ce4-995e-9426e7bacf3a-groceries.jpeg",
            brand: "Himalayan Organics",
            tags: ["water", "sparkling water", "spring water", "beverage", "mineral water", "case"]
        },
        {
            id: 112,
            name: "Handcrafted Dark Chocolate Truffles (250g)",
            category: "Chocolates & Confectionery",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 890",
            priceRaw: 890,
            rating: "4.9",
            img: "asstes/website-designs/grocries/supermarket_cart.jpeg",
            brand: "Annapurna Bakery",
            tags: ["chocolate", "truffles", "sweets", "snacks", "dark chocolate", "gourmet", "artisan"]
        },
        {
            id: 113,
            name: "Organic Green Tea Leaves & Himalayan Coffee Blend (200g)",
            category: "Tea & Coffee",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 480",
            priceRaw: 480,
            rating: "4.8",
            img: "asstes/website-designs/grocries/gm-23ed737a-a2a5-4ce4-995e-9426e7bacf3a-groceries.jpeg",
            brand: "Himalayan Organics",
            tags: ["tea", "green tea", "coffee", "instant coffee", "chamomile", "organic tea", "beverages", "herbal"]
        },
        {
            id: 114,
            name: "Organic Dried Herb & Spice Seasoning Pack",
            category: "Spices & Masala",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 280",
            priceRaw: 280,
            rating: "4.7",
            img: "asstes/website-designs/alcohol design/red_wine_grapes.jpg",
            brand: "Himalayan Organics",
            tags: ["spices", "herbs", "seasoning", "cooking", "groceries", "pantry"]
        },
        {
            id: 115,
            name: "Packaged Danish Biscuits & Cookies Box (500g)",
            category: "Biscuits & Cookies",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 580",
            priceRaw: 580,
            rating: "5.0",
            img: "asstes/website-designs/hero_groceries.png",
            brand: "Annapurna Bakery",
            tags: ["biscuits", "cookies", "danish cookies", "wafers", "bakery", "snacks"]
        },
        {
            id: 116,
            name: "Premium Organic Quinoa, Dal & Oats (1kg)",
            category: "Rice & Grains",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 920",
            priceRaw: 920,
            rating: "4.8",
            img: "asstes/website-designs/grocries/R.jpg",
            brand: "Goldstar Pantry",
            tags: ["quinoa", "dal", "oats", "rice", "grains", "healthy", "superfood", "pulses"]
        },
        {
            id: 117,
            name: "Instant Noodles & Macaroni Pasta Family Pack",
            category: "Noodles & Pasta",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 320",
            priceRaw: 320,
            rating: "4.9",
            img: "asstes/website-designs/grocries/supermarket_cart.jpeg",
            brand: "Goldstar Pantry",
            tags: ["noodles", "instant noodles", "pasta", "macaroni", "ramen", "packaged food", "chips"]
        },
        {
            id: 118,
            name: "Polished Red Masoor & Yellow Moong Dal Pack (1kg)",
            category: "Dal & Pulses",
            dept: "Grocery Essentials",
            deptKey: "grocery",
            price: "Rs. 180",
            priceRaw: 180,
            rating: "4.8",
            img: "asstes/website-designs/grocries/R.jpg",
            brand: "Quality Foods",
            tags: ["dal", "masoor dal", "moong dal", "chana dal", "pulses", "black lentils", "lentils"]
        }
    ];

    // 2. SEARCH MATCHING & SCORING ALGORITHM
    function searchCatalog(query) {
        if (!query || !query.trim()) return [];

        const cleanQuery = query.trim().toLowerCase();
        const tokens = cleanQuery.split(/\s+/).filter(Boolean);

        const scoredResults = STORE_CATALOG.map(item => {
            let score = 0;
            const lowerName = item.name.toLowerCase();
            const lowerBrand = (item.brand || '').toLowerCase();
            const lowerCat = (item.category || '').toLowerCase();
            const lowerTags = (item.tags || []).join(' ').toLowerCase();

            // 1. Exact or prefix match on name (Highest priority)
            if (lowerName.startsWith(cleanQuery)) {
                score += 150;
            } else if (lowerName.includes(cleanQuery)) {
                score += 90;
            }

            // 2. Brand match
            if (lowerBrand.startsWith(cleanQuery)) {
                score += 120;
            } else if (lowerBrand.includes(cleanQuery)) {
                score += 70;
            }

            // 3. Category match
            if (lowerCat.includes(cleanQuery)) {
                score += 50;
            }

            // 4. Token-by-token matching across tags, category, name
            let matchedAllTokens = true;
            for (const token of tokens) {
                if (lowerName.includes(token)) {
                    score += 30;
                } else if (lowerBrand.includes(token)) {
                    score += 25;
                } else if (lowerCat.includes(token)) {
                    score += 20;
                } else if (lowerTags.includes(token)) {
                    score += 15;
                } else {
                    matchedAllTokens = false;
                }
            }

            if (tokens.length > 1 && matchedAllTokens) {
                score += 40;
            }

            return { item, score };
        });

        // Filter items with positive score and sort descending
        return scoredResults
            .filter(res => res.score > 0)
            .sort((a, b) => b.score - a.score)
            .map(res => res.item)
            .slice(0, 7); // Max 7 suggestions
    }

    // Helper: Highlight matching substring in text
    function highlightMatch(text, query) {
        if (!query || !query.trim()) return escapeHTML(text);
        const cleanQuery = query.trim();
        const escaped = cleanQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`(${escaped})`, 'gi');
        return escapeHTML(text).replace(regex, '<mark class="search-highlight">$1</mark>');
    }

    function escapeHTML(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // 3. AUTOCOMPLETE UI CONTROLLER
    class IntelligentSearchController {
        constructor(searchWrapperEl, inputEl) {
            this.wrapper = searchWrapperEl;
            this.input = inputEl;
            this.dropdown = null;
            this.debounceTimer = null;
            this.currentIndex = -1;
            this.currentResults = [];
            this.isOpen = false;

            this.init();
        }

        init() {
            if (!this.wrapper || !this.input) return;

            // Ensure wrapper is positioned relative
            this.wrapper.style.position = 'relative';

            // Create dropdown element
            this.dropdown = document.createElement('div');
            this.dropdown.className = 'search-autocomplete-dropdown';
            this.dropdown.setAttribute('role', 'listbox');
            this.wrapper.appendChild(this.dropdown);

            // Bind Event Listeners
            this.input.addEventListener('input', (e) => this.handleInput(e));
            this.input.addEventListener('focus', () => this.handleFocus());
            this.input.addEventListener('keydown', (e) => this.handleKeydown(e));

            // Close when clicking outside
            document.addEventListener('click', (e) => {
                if (!this.wrapper.contains(e.target)) {
                    this.close();
                }
            });

            // Prevent form submit if wrapped in form
            const parentForm = this.input.closest('form');
            if (parentForm) {
                parentForm.addEventListener('submit', (e) => {
                    e.preventDefault();
                    this.executeSearch(this.input.value);
                });
            }
        }

        handleInput(e) {
            clearTimeout(this.debounceTimer);
            const query = this.input.value.trim();

            this.debounceTimer = setTimeout(() => {
                if (query.length === 0) {
                    this.close();
                } else {
                    const results = searchCatalog(query);
                    this.renderResults(results, query);
                }
            }, 100);
        }

        handleFocus() {
            const query = this.input.value.trim();
            if (query.length === 0) {
                // Do not show anything on tap/focus when input is empty
                this.close();
            } else {
                const results = searchCatalog(query);
                this.renderResults(results, query);
            }
        }

        handleKeydown(e) {
            if (!this.isOpen) {
                return;
            }

            const items = this.dropdown.querySelectorAll('.search-item');
            if (!items.length) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.executeSearch(this.input.value);
                }
                return;
            }

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.currentIndex = (this.currentIndex + 1) % items.length;
                this.updateActiveItem(items);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.currentIndex = (this.currentIndex - 1 + items.length) % items.length;
                this.updateActiveItem(items);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (this.currentIndex >= 0 && items[this.currentIndex]) {
                    items[this.currentIndex].click();
                } else {
                    this.executeSearch(this.input.value);
                }
            } else if (e.key === 'Escape') {
                this.close();
            }
        }

        updateActiveItem(items) {
            items.forEach((item, idx) => {
                const isActive = idx === this.currentIndex;
                item.classList.toggle('is-selected', isActive);
                if (isActive) {
                    item.scrollIntoView({ block: 'nearest' });
                }
            });
        }

        renderResults(results, query) {
            this.currentIndex = -1;
            this.currentResults = results;

            if (!results.length) {
                this.dropdown.innerHTML = `
                    <div class="search-empty-state">
                        <div class="search-empty-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                        </div>
                        <p class="search-empty-text">No products found for <strong>"${escapeHTML(query)}"</strong></p>
                        <p class="search-empty-hint">Try searching for Jack Daniel's, Macallan, Whiskey, Honey, or Wine</p>
                    </div>
                `;
                this.open();
                return;
            }

            let html = `
                <div class="search-dropdown-header">
                    <span class="search-dropdown-title">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                        Suggestions for "${escapeHTML(query)}" (${results.length})
                    </span>
                </div>
                <div class="search-results-list">
            `;

            results.forEach((item, idx) => {
                const highlightedName = highlightMatch(item.name, query);

                html += `
                    <div class="search-item" data-id="${item.id}" data-type="${item.deptKey}" role="option">
                        <div class="search-item-thumb">
                            <img src="${escapeHTML(item.img)}" alt="${escapeHTML(item.name)}" onerror="this.src='asstes/website-designs/hero_liquor.png'" />
                        </div>
                        <div class="search-item-details">
                            <div class="search-item-headline">
                                <span class="search-item-name">${highlightedName}</span>
                            </div>
                            <div class="search-item-meta">
                                <span class="search-item-category">${escapeHTML(item.category)}</span>
                                <span class="search-item-dot">•</span>
                                <span class="search-item-brand">${escapeHTML(item.brand || '')}</span>
                            </div>
                        </div>
                        <div class="search-item-action">
                            <span class="search-item-price">${escapeHTML(item.price)}</span>
                            <span class="search-item-arrow">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </span>
                        </div>
                    </div>
                `;
            });

            html += `
                </div>
                <div class="search-dropdown-footer search-footer-interactive" data-query="${escapeHTML(query)}">
                    <span>Press <strong>Enter</strong> or click to browse all results for "${escapeHTML(query)}"</span>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                </div>
            `;

            this.dropdown.innerHTML = html;
            this.attachItemEvents();
            this.open();
        }

        attachItemEvents() {
            // Click on Product Item
            const items = this.dropdown.querySelectorAll('.search-item');
            items.forEach(item => {
                item.addEventListener('click', () => {
                    const id = item.getAttribute('data-id');
                    const type = item.getAttribute('data-type');
                    this.navigateToProduct(id, type);
                });
            });

            // Click on Footer "Browse all results"
            const footer = this.dropdown.querySelector('.search-footer-interactive');
            if (footer) {
                footer.addEventListener('click', () => {
                    const query = footer.getAttribute('data-query');
                    this.executeSearch(query);
                });
            }
        }

        navigateToProduct(productId, productType) {
            this.close();
            const pIdNum = parseInt(productId);
            const found = STORE_CATALOG.find(p => p.id === pIdNum && (!productType || p.deptKey === productType)) || STORE_CATALOG.find(p => p.id === pIdNum);
            const type = (found && found.deptKey) || productType || 'liquor';
            const name = found ? found.name : '';
            if (found) {
                try {
                    localStorage.setItem('annapurna_selected_product', JSON.stringify({
                        id: found.id,
                        type: type,
                        name: found.name,
                        price: found.price,
                        priceRaw: found.priceRaw,
                        img: found.img
                    }));
                } catch (e) {}
            }
            const nameParam = name ? `&name=${encodeURIComponent(name)}` : '';
            window.location.href = `product-detail.html?id=${productId}&type=${type}${nameParam}`;
        }

        executeSearch(query) {
            this.close();
            if (!query || !query.trim()) return;

            const cleanQ = encodeURIComponent(query.trim());
            const results = searchCatalog(query);
            const liquorCount = results.filter(r => r.deptKey === 'liquor').length;
            const groceryCount = results.filter(r => r.deptKey === 'grocery').length;

            if (groceryCount > liquorCount) {
                window.location.href = `grocries.html?search=${cleanQ}`;
            } else {
                window.location.href = `liquior.html?search=${cleanQ}`;
            }
        }

        open() {
            this.dropdown.classList.add('is-open');
            this.isOpen = true;
        }

        close() {
            this.dropdown.classList.remove('is-open');
            this.isOpen = false;
            this.currentIndex = -1;
        }
    }

    // 4. AUTO-INITIALIZE ENGINE ON LOAD
    async function syncBackendCatalog() {
        if (!window.apiConfig) return;
        try {
            const apiProducts = await window.apiConfig.fetchProducts();
            if (Array.isArray(apiProducts) && apiProducts.length > 0) {
                const mappedProducts = apiProducts.map(p => {
                    const primaryImg = (p.images && p.images.length > 0) ? p.images[0].image : 'asstes/website-designs/hero_liquor.png';
                    const categoryName = (typeof p.category === 'object' && p.category) ? p.category.name : (p.category || '');
                    return {
                        id: p.id,
                        name: p.name,
                        category: categoryName || 'Store Product',
                        dept: p.department === 'grocery' ? 'Grocery' : 'Liquor',
                        deptKey: p.department === 'grocery' ? 'grocery' : 'liquor',
                        price: `Rs. ${parseFloat(p.selling_price || 0).toLocaleString()}`,
                        priceRaw: parseFloat(p.selling_price || 0),
                        rating: p.rating ? String(p.rating) : "5.0",
                        img: primaryImg,
                        brand: p.brand || "Annapurna",
                        tags: [
                            (p.name || '').toLowerCase(),
                            (p.brand || '').toLowerCase(),
                            (categoryName || '').toLowerCase(),
                            (p.tags || '').toLowerCase()
                        ].filter(Boolean)
                    };
                });
                STORE_CATALOG = mappedProducts;
                if (window.AnnapurnaSearch) window.AnnapurnaSearch.catalog = STORE_CATALOG;
            }
        } catch (e) {
            console.log('Using default static search catalog fallback.');
        }
    }

    function initSearchEngine() {
        syncBackendCatalog();

        // Find all search containers across pages
        const searchWrappers = document.querySelectorAll('.header-nav-search, .main-search-wrapper, .header-search-bar, .search-container');
        
        searchWrappers.forEach(wrapper => {
            const input = wrapper.querySelector('.search-input-field, .search-input, input[type="text"], input[type="search"]');
            if (input && !wrapper.dataset.searchInitialized) {
                wrapper.dataset.searchInitialized = "true";
                new IntelligentSearchController(wrapper, input);
            }
        });
    }

    // Export Global API
    window.AnnapurnaSearch = {
        catalog: STORE_CATALOG,
        search: searchCatalog,
        searchLiquor: (q) => { window.location.href = `liquior.html?search=${q}`; },
        searchGroceries: (q) => { window.location.href = `grocries.html?search=${q}`; }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSearchEngine);
    } else {
        initSearchEngine();
    }
})();
