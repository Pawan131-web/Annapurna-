import os
from pathlib import Path
from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.static import serve as django_static_serve

# Path to the customer storefront directory
STOREFRONT_DIR = (settings.BASE_DIR.parent.parent / 'liquior').resolve()

def serve_storefront(request, path=''):
    """
    Unified single-port handler: Serves the customer-facing storefront files
    (HTML pages, CSS, JS, images, videos) directly through Django on port 8000.
    """
    path = path.strip('/')
    
    # Default route: serve index.html
    if not path or path in ('index.html', 'idex.html'):
        path = 'index.html'
    elif path == 'favicon.ico':
        fav = STOREFRONT_DIR / 'asstes' / 'website-designs' / 'annapurna_icon_gold.png'
        if fav.exists():
            return django_static_serve(request, 'asstes/website-designs/annapurna_icon_gold.png', document_root=str(STOREFRONT_DIR))
        return HttpResponse(status=204)
        
    file_path = (STOREFRONT_DIR / path).resolve()
    
    # Security check: prevent directory traversal attacks
    try:
        file_path.relative_to(STOREFRONT_DIR)
    except ValueError:
        raise Http404("File not found")
        
    if not file_path.exists() or file_path.is_dir():
        raise Http404(f"File '{path}' not found")
        
    response = django_static_serve(request, path, document_root=str(STOREFRONT_DIR))
    
    # Zero-cache headers for dev iteration
    if path.endswith(('.html', '.js', '.css')):
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
    return response
