/**
 * Annapurna Store — Central API Configuration & Network Layer
 * Manages environment-aware API endpoints for seamless local dev & production deployment.
 */

(function (window) {
    'use strict';

    // Auto-detect base URL (defaults to current origin for unified single-port server)
    let defaultBaseUrl = (window.location && window.location.origin && window.location.origin !== 'null') 
        ? window.location.origin 
        : 'http://127.0.0.1:8000';

    const API_BASE_URL = window.ANNAPURNA_API_URL || defaultBaseUrl;

    const apiConfig = {
        baseUrl: API_BASE_URL,
        endpoints: {
            orders: `${API_BASE_URL}/api/orders/`,
            products: `${API_BASE_URL}/api/products/`,
            categories: `${API_BASE_URL}/api/categories/`,
            suppliers: `${API_BASE_URL}/api/suppliers/`,
            login: `${API_BASE_URL}/accounts/login/`,
            logout: `${API_BASE_URL}/accounts/logout/`,
            dashboard: `${API_BASE_URL}/dashboard/`
        },

        /**
         * Authenticate store administrator with Django backend.
         * Sets authenticated session cookie and returns user + dashboard redirect.
         * @param {string} identifier - Username or Email
         * @param {string} password - User Password
         * @returns {Promise<Object>}
         */
        async login(identifier, password) {
            try {
                const response = await fetch(this.endpoints.login, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    credentials: 'include',
                    body: JSON.stringify({ identifier, password })
                });

                const data = await response.json().catch(() => ({}));

                if (!response.ok || !data.success) {
                    return {
                        success: false,
                        message: data.message || 'Invalid username or password. Please try again.'
                    };
                }

                return {
                    success: true,
                    redirect_url: data.redirect_url || this.endpoints.dashboard,
                    dashboard_url: data.dashboard_url || this.endpoints.dashboard,
                    user: data.user,
                    message: data.message
                };
            } catch (err) {
                console.error('Admin authentication network error:', err);
                return {
                    success: false,
                    message: 'Cannot connect to backend server. Make sure the server is running on port 8000.'
                };
            }
        },

        /**
         * Terminate admin session both on server and in client storage.
         */
        async logout() {
            try {
                await fetch(this.endpoints.logout, {
                    method: 'POST',
                    headers: { 'Accept': 'application/json' },
                    credentials: 'include'
                }).catch(() => {});
            } catch (err) {
                console.warn('Logout API warning:', err);
            }
            localStorage.removeItem('annapurna_admin_user');
            localStorage.removeItem('annapurna_admin_logged_in');
        },

        /**
         * Check if URL has ?admin_login=1 and open modal automatically only if logged out.
         */
        checkAutoLoginParam() {
            try {
                const params = new URLSearchParams(window.location.search);
                const isAdminLoginParam = params.get('admin_login') === '1' || params.get('action') === 'login';
                const isLoggedIn = !!localStorage.getItem('annapurna_admin_user') || document.body.classList.contains('is-logged-in');

                if (isAdminLoginParam) {
                    if (isLoggedIn) {
                        // Already logged in: redirect straight to dashboard if next is present, otherwise clean URL
                        const nextUrl = params.get('next') || this.endpoints.dashboard;
                        window.location.href = nextUrl;
                        return;
                    }

                    setTimeout(() => {
                        if (typeof window.openAuthModal === 'function') {
                            window.openAuthModal();
                        } else {
                            const overlay = document.getElementById('authModalOverlay');
                            if (overlay) overlay.classList.add('active');
                        }

                        // Check if error was passed
                        const err = params.get('error');
                        const errorEl = document.getElementById('authModalError');
                        if (errorEl && err) {
                            errorEl.textContent = err === 'invalid_credentials'
                                ? 'Invalid username or password. Please try again.'
                                : 'Please log in with admin credentials to access the admin portal.';
                            errorEl.style.display = 'block';
                        }
                    }, 150);
                }
            } catch (e) {
                console.warn('URL check warning:', e);
            }
        },

        /**
         * Submit online order to backend API
         * @param {Object} orderData 
         * @returns {Promise<Object>}
         */
        async postOrder(orderData) {
            try {
                const response = await fetch(this.endpoints.orders, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(orderData)
                });

                if (!response.ok) {
                    const errorJson = await response.json().catch(() => ({}));
                    throw new Error(errorJson.message || `HTTP ${response.status}: Failed to submit order`);
                }

                return await response.json();
            } catch (err) {
                console.warn('Backend API order sync error:', err);
                throw err;
            }
        },

        /**
         * Fetch active products list from Django DRF API
         * @returns {Promise<Array>}
         */
        async fetchProducts(department = '') {
            try {
                let url = `${this.endpoints.products}?page_size=500`;
                if (department) {
                    url += `&department=${encodeURIComponent(department)}`;
                }
                const response = await fetch(url, {
                    method: 'GET',
                    headers: { 'Accept': 'application/json' }
                });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();
                return Array.isArray(data) ? data : (data.results || []);
            } catch (err) {
                console.warn('Backend API products fetch error:', err);
                return null;
            }
        }
    };

    window.apiConfig = apiConfig;

    // Run auto-login query checker on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => apiConfig.checkAutoLoginParam());
    } else {
        apiConfig.checkAutoLoginParam();
    }
})(window);
