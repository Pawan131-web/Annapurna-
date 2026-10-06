# ShopAdmin — Shop / Inventory Management System (Phase 1: Admin Backend)

A custom-built Django admin dashboard for managing products, categories, suppliers,
inventory, sales, and reports — built as Phase 1 of a two-phase project. A public
customer-facing site (Phase 2) will read data from this backend through the included
REST API.

## Tech stack

- Python 3 + Django 5/6
- SQLite (zero-config, file-based database)
- Django Templates + Bootstrap 5 + Bootstrap Icons for the dashboard UI (not default Django admin)
- Chart.js for analytics charts
- django-crispy-forms (Bootstrap 5 pack) for form rendering
- Django REST Framework for the API layer
- Pillow for image handling
- python-decouple for environment variables
- openpyxl for Excel report exports

## Project structure

```
config/          project settings, root urls
accounts/        auth (login/logout/password reset), Profile (Admin/Staff roles)
dashboard/       home dashboard, stat cards, charts, sidebar low-stock context processor
categories/      Category CRUD
suppliers/       Supplier CRUD
products/        Product CRUD, images, price history, quick-price AJAX endpoint, seed_data command
inventory/       stock in/out movement log
sales/           point-of-sale style sale entry + printable receipt
reports/         sales / inventory / performance / profit reports with CSV & Excel export
api/             DRF read-only endpoints for the future public frontend
templates/       all HTML templates (base.html holds the shared sidebar/navbar shell)
static/css/      shopadmin.css — the dashboard's design system
```

## Setup

1. **Create a virtual environment and install dependencies**

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set a real `SECRET_KEY`. The database is SQLite by default and
   needs no extra setup — it will be created as `db.sqlite3` in the project root the
   first time you run migrations. Optionally set `DB_NAME` to point at a different
   file path.

3. **Run migrations**

   ```bash
   python manage.py migrate
   ```

4. **Create a superuser** (or use the seed command below, which creates one for you)

   ```bash
   python manage.py createsuperuser
   ```

5. **Load sample data** so the dashboard isn't empty on first run

   ```bash
   python manage.py seed_data
   ```

   This creates 5 categories, 3 suppliers, 12 products, a handful of sample sales over
   the last two weeks, and a superuser: **username `admin`, password `admin12345`**
   (only if a user named `admin` doesn't already exist — change this password immediately
   in a real deployment).

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/` — you'll be redirected to the dashboard (or the login
   page if you're not signed in yet).

   The underlying Django admin is still available at `/django-admin/` if you ever need
   raw database access.

## Where things live

- **Dashboard**: `/dashboard/`
- **Products / Categories / Suppliers**: `/products/`, `/categories/`, `/suppliers/`
- **Inventory log**: `/inventory/`
- **Sales & receipts**: `/sales/`
- **Reports** (with CSV/Excel export): `/reports/sales/`, `/reports/inventory/`,
  `/reports/performance/`, `/reports/profit/`
- **REST API** (for the future public site): `/api/products/`, `/api/categories/`,
  `/api/suppliers/`, `/api/sales/` — read-only, session-authenticated for now

## Notes on design decisions

- **Soft delete**: deleting a product sets `is_deleted=True` rather than removing the
  row, so sales history and reports stay intact.
- **Price history**: editing a product's cost or selling price (via the edit form or the
  quick-price modal on the product list) automatically logs the change — who changed it
  and when.
- **Stock movements**: every stock in/out and every sale writes a `StockMovement` row,
  so you get a full audit trail of inventory changes, not just a running total.
- **Frontend-ready API**: `ProductSerializer` nests category, supplier, and images
  directly so the future public site can render a product page from a single API call.
- **Reports export**: CSV export uses Python's standard library (no extra dependency);
  Excel export uses `openpyxl`. PDF export isn't wired up as a one-click button yet —
  the report pages are print-friendly, so "Print to PDF" from the browser works today,
  and a dedicated PDF export (e.g. via WeasyPrint) is a natural next addition if you want
  a literal PDF button later.

## Next steps for Phase 2

The API layer (`/api/...`) is intentionally read-only and already returns
frontend-ready, nested JSON. The public site can be built against these endpoints
without touching this backend's models.
