# 🏔️ Annapurna — Luxury Grocery Essentials & Fine Liquors

A full-stack, unified e-commerce platform and inventory management system designed for Kathmandu's premier fine single malts, luxury spirits, vintage wines, and daily grocery essentials.

---

## 🌟 Key Features

- **🛍️ Storefront & Catalogs**:
  - **Dynamic Product Catalogs**: Dedicated portals for Fine Liquors (`liquior.html`) and Grocery Essentials (`grocries.html`).
  - **Editorial Product Detail Pages**: Dynamic showcase (`product-detail.html`) with variant selectors, thumbnail carousel, and automatic recommendation engines.
  - **Real-Time Client & API Search**: Instant multi-attribute search across categories, brands, and price tiers.
  - **Fluid Cart & Direct Ordering**: WhatsApp order generation + integrated checkout modals.
- **🎨 Luxury Aesthetics & Dual Theme System**:
  - **Light Mode**: Warm ivory and champagne gold palette with high-contrast typography.
  - **Obsidian Dark Mode**: Deep obsidian surfaces (`#0B0D11`), glowing champagne gold accents (`#E5C158`), and smooth transitions.
- **⚙️ Django Admin & Management Dashboard**:
  - Full CRUD for products, categories, suppliers, and inventory stock tracking.
  - REST API (`/api/products/`, `/api/orders/`, `/api/categories/`).
  - Session-authenticated Administrator portal.
- **🚀 Unified Single-Port Architecture**:
  - Serves static storefront, dynamic REST APIs, and Django admin dashboard concurrently on port `8000`.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Modern Web Browser (Chrome, Edge, Firefox, Safari)

### 2. Run the Application
Start the unified application with a single command:
```bash
python run.py
```
Or on Windows:
```cmd
start_server.bat
```

### 3. Application URLs
- **Storefront**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Liquor Catalog**: [http://127.0.0.1:8000/liquior.html](http://127.0.0.1:8000/liquior.html)
- **Grocery Catalog**: [http://127.0.0.1:8000/grocries.html](http://127.0.0.1:8000/grocries.html)
- **Admin Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
- **REST API**: [http://127.0.0.1:8000/api/products/](http://127.0.0.1:8000/api/products/)

---

## 📁 Repository Structure

```
Annapurna/
├── Annapurna_liquor/
│   ├── liquior/                 # Customer Storefront (HTML, CSS, JS, Assets)
│   │   ├── index.html           # Main Landing Page
│   │   ├── liquior.html         # Liquor Catalog Page
│   │   ├── grocries.html        # Grocery Catalog Page
│   │   ├── product-detail.html  # Dynamic Product Details Page
│   │   ├── theme.css            # Central Dual-Theme Styling System
│   │   ├── theme.js             # Theme Switcher Engine
│   │   ├── api-config.js        # Backend API & Authentication Layer
│   │   └── search-engine.js     # Real-Time Search & Autocomplete
│   └── shopadmin_clean/         # Django Admin & REST API Backend
│       └── shopadmin/
│           ├── manage.py
│           ├── config/          # Django Settings & URLs
│           ├── api/             # REST Framework Endpoints
│           ├── products/        # Product & Inventory Models
│           └── dashboard/       # Administrative UI
├── run.py                       # Unified Single-Port Launcher
├── start_server.bat             # Windows Quick-Start Script
├── .gitignore
└── README.md
```

---

## 📄 License
All rights reserved © Annapurna Grocery Essentials & Liquor.
