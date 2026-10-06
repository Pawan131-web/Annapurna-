/**
 * Annapurna Store - Dark / Light Theme Engine
 * Default: Light Mode (as currently designed)
 * Dark Mode: Obsidian Luxury Palette
 */

(function () {
    // 1. Immediately apply saved theme on initial execution to prevent flash
    const savedTheme = localStorage.getItem('annapurna_theme') || 'light';
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark-theme');
        if (document.body) document.body.classList.add('dark-theme');
    } else {
        document.documentElement.classList.remove('dark-theme');
        if (document.body) document.body.classList.remove('dark-theme');
    }

    // 2. Initialize toggle buttons when DOM is ready
    function setupThemeToggle() {
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        } else {
            document.body.classList.remove('dark-theme');
        }
        updateThemeToggleIcons();

        // Attach click listener to all theme toggle buttons
        document.querySelectorAll('#themeToggleBtn, .theme-toggle-btn').forEach(btn => {
            btn.onclick = function (e) {
                e.preventDefault();
                e.stopPropagation();
                
                const isCurrentlyDark = document.body.classList.contains('dark-theme');
                if (isCurrentlyDark) {
                    document.body.classList.remove('dark-theme');
                    document.documentElement.classList.remove('dark-theme');
                    localStorage.setItem('annapurna_theme', 'light');
                } else {
                    document.body.classList.add('dark-theme');
                    document.documentElement.classList.add('dark-theme');
                    localStorage.setItem('annapurna_theme', 'dark');
                }
                
                updateThemeToggleIcons();
            };
        });
    }

    function updateThemeToggleIcons() {
        const isDark = document.body ? document.body.classList.contains('dark-theme') : (localStorage.getItem('annapurna_theme') === 'dark');
        document.querySelectorAll('#themeToggleBtn, .theme-toggle-btn').forEach(btn => {
            if (isDark) {
                // In Dark Mode -> Show Sun icon to switch back to Light Mode
                btn.innerHTML = `
                    <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="pointer-events: none;">
                        <circle cx="12" cy="12" r="5"></circle>
                        <line x1="12" y1="1" x2="12" y2="3"></line>
                        <line x1="12" y1="21" x2="12" y2="23"></line>
                        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                        <line x1="1" y1="12" x2="3" y2="12"></line>
                        <line x1="21" y1="12" x2="23" y2="12"></line>
                        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                    </svg>
                `;
                btn.title = "Switch to Light Theme";
                btn.setAttribute('aria-label', 'Switch to Light Theme');
            } else {
                // In Light Mode -> Show Moon icon to switch to Dark Mode
                btn.innerHTML = `
                    <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="pointer-events: none;">
                        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                    </svg>
                `;
                btn.title = "Switch to Dark Theme";
                btn.setAttribute('aria-label', 'Switch to Dark Theme');
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupThemeToggle);
    } else {
        setupThemeToggle();
    }

    // Expose globally
    window.AnnapurnaTheme = {
        toggle: function () {
            const btn = document.getElementById('themeToggleBtn');
            if (btn) btn.click();
        },
        isDark: function () {
            return document.body.classList.contains('dark-theme');
        }
    };
})();
