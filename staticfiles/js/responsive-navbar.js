/**
 * Enhanced Responsive Navbar JavaScript
 * Bootstrap 5 Compatible with Hover Effects and Mobile Support
 * Professional implementation with accessibility features
 */

class ResponsiveNavbar {
    constructor() {
        this.desktopNavbar = document.getElementById('desktopNavbar');
        this.mobileNavbar = document.getElementById('mobileNavbar');
        this.mobileNavbarContent = document.getElementById('mobileNavbarContent');
        this.isInitialized = false;
        this.hoverTimeouts = new Map();
        this.activeDropdown = null;
        
        this.init();
    }

    /**
     * Initialize the navbar functionality
     */
    init() {
        if (this.isInitialized) return;
        
        this.setupEventListeners();
        this.initializeDropdowns();
        this.handleResponsiveDisplay();
        this.initializeMobileNavigation();
        this.initializeSearch();
        this.initializeAccessibility();
        
        this.isInitialized = true;
        
        // Add fade-in animation
        if (this.desktopNavbar) {
            this.desktopNavbar.classList.add('navbar-fade-in');
        }
        if (this.mobileNavbar) {
            this.mobileNavbar.classList.add('navbar-fade-in');
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Window resize handling
        window.addEventListener('resize', this.debounce(() => {
            this.handleResponsiveDisplay();
        }, 250));

        // Window scroll handling for navbar shadow
        window.addEventListener('scroll', this.throttle(() => {
            this.handleScrollEffect();
        }, 16));

        // Document click handling for dropdown closure
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.dropdown')) {
                this.closeAllDropdowns();
            }
        });

        // Escape key handling
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllDropdowns();
                this.closeMobileMenu();
            }
        });
    }

    /**
     * Initialize Bootstrap dropdowns with hover effects
     */
    initializeDropdowns() {
        const dropdownElements = document.querySelectorAll('.dropdown');
        
        dropdownElements.forEach((dropdown) => {
            const toggle = dropdown.querySelector('.dropdown-toggle');
            const menu = dropdown.querySelector('.dropdown-menu');
            
            if (!toggle || !menu) return;

            // Initialize Bootstrap dropdown
            const bsDropdown = new bootstrap.Dropdown(toggle, {
                autoClose: 'outside',
                boundary: 'viewport'
            });

            // Desktop hover behavior
            if (window.innerWidth >= 992) {
                this.setupDesktopHover(dropdown, toggle, menu, bsDropdown);
            }

            // Click behavior for all screen sizes
            this.setupClickBehavior(toggle, menu, bsDropdown);

            // Keyboard navigation
            this.setupKeyboardNavigation(dropdown, toggle, menu);
        });
    }

    /**
     * Setup desktop hover behavior
     */
    setupDesktopHover(dropdown, toggle, menu, bsDropdown) {
        dropdown.addEventListener('mouseenter', () => {
            // Clear any existing timeout
            if (this.hoverTimeouts.has(dropdown)) {
                clearTimeout(this.hoverTimeouts.get(dropdown));
                this.hoverTimeouts.delete(dropdown);
            }

            // Close other dropdowns
            this.closeOtherDropdowns(menu);

            // Show current dropdown
            bsDropdown.show();
            this.activeDropdown = bsDropdown;
        });

        dropdown.addEventListener('mouseleave', () => {
            // Set timeout to close dropdown
            const timeout = setTimeout(() => {
                if (!dropdown.matches(':hover')) {
                    bsDropdown.hide();
                    if (this.activeDropdown === bsDropdown) {
                        this.activeDropdown = null;
                    }
                }
            }, 150);

            this.hoverTimeouts.set(dropdown, timeout);
        });

        // Prevent dropdown from closing when hovering over menu
        menu.addEventListener('mouseenter', () => {
            if (this.hoverTimeouts.has(dropdown)) {
                clearTimeout(this.hoverTimeouts.get(dropdown));
                this.hoverTimeouts.delete(dropdown);
            }
        });
    }

    /**
     * Setup click behavior for dropdowns
     */
    setupClickBehavior(toggle, menu, bsDropdown) {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();

            if (menu.classList.contains('show')) {
                bsDropdown.hide();
                this.activeDropdown = null;
            } else {
                this.closeOtherDropdowns(menu);
                bsDropdown.show();
                this.activeDropdown = bsDropdown;
            }
        });

        // Handle dropdown item clicks
        menu.addEventListener('click', (e) => {
            const dropdownItem = e.target.closest('.dropdown-item');
            if (dropdownItem) {
                const href = dropdownItem.getAttribute('href');
                if (href && href !== '#' && href !== '') {
                    // Add loading state
                    dropdownItem.classList.add('loading');
                    
                    // Close dropdown after short delay
                    setTimeout(() => {
                        bsDropdown.hide();
                        this.activeDropdown = null;
                    }, 100);
                }
            }
        });

        // Bootstrap dropdown events
        toggle.addEventListener('shown.bs.dropdown', () => {
            menu.style.display = 'block';
            menu.style.visibility = 'visible';
            menu.style.opacity = '1';
            
            // Add glow effect to toggle
            toggle.classList.add('nav-link-glow');
            
            // Position dropdown properly
            this.positionDropdown(menu);
        });

        toggle.addEventListener('hidden.bs.dropdown', () => {
            menu.style.display = 'none';
            
            // Remove glow effect
            toggle.classList.remove('nav-link-glow');
        });
    }

    /**
     * Setup keyboard navigation for dropdowns
     */
    setupKeyboardNavigation(dropdown, toggle, menu) {
        dropdown.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                if (e.target === toggle) {
                    e.preventDefault();
                    toggle.click();
                }
            } else if (e.key === 'ArrowDown') {
                if (menu.classList.contains('show')) {
                    e.preventDefault();
                    const firstItem = menu.querySelector('.dropdown-item');
                    if (firstItem) firstItem.focus();
                }
            } else if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
                if (menu.classList.contains('show')) {
                    e.preventDefault();
                    const items = menu.querySelectorAll('.dropdown-item');
                    const currentIndex = Array.from(items).indexOf(e.target);
                    
                    if (e.key === 'ArrowDown' && currentIndex < items.length - 1) {
                        items[currentIndex + 1].focus();
                    } else if (e.key === 'ArrowUp' && currentIndex > 0) {
                        items[currentIndex - 1].focus();
                    }
                }
            }
        });
    }

    /**
     * Handle responsive display changes
     */
    handleResponsiveDisplay() {
        const screenWidth = window.innerWidth;
        
        if (screenWidth >= 992) {
            // Desktop: show desktop navbar, hide mobile
            if (this.desktopNavbar) {
                this.desktopNavbar.style.display = 'block';
                this.desktopNavbar.classList.remove('d-lg-none');
            }
            if (this.mobileNavbar) {
                this.mobileNavbar.style.display = 'none';
                this.mobileNavbar.classList.add('d-lg-none');
            }
            
            // Reinitialize dropdowns for desktop
            this.initializeDropdowns();
        } else {
            // Mobile: hide desktop navbar, show mobile
            if (this.desktopNavbar) {
                this.desktopNavbar.style.display = 'none';
                this.desktopNavbar.classList.add('d-lg-none');
            }
            if (this.mobileNavbar) {
                this.mobileNavbar.style.display = 'block';
                this.mobileNavbar.classList.remove('d-lg-none');
            }
            
            // Close any open dropdowns
            this.closeAllDropdowns();
        }
    }

    /**
     * Initialize mobile navigation
     */
    initializeMobileNavigation() {
        const mobileToggler = this.mobileNavbar?.querySelector('.navbar-toggler');
        
        if (mobileToggler && this.mobileNavbarContent) {
            mobileToggler.addEventListener('click', (e) => {
                e.preventDefault();
                const bsCollapse = bootstrap.Collapse.getOrCreateInstance(this.mobileNavbarContent);
                bsCollapse.toggle();
            });

            // Close mobile nav when clicking nav links
            const mobileNavLinks = this.mobileNavbarContent.querySelectorAll('.nav-link:not(.dropdown-toggle)');
            mobileNavLinks.forEach(link => {
                link.addEventListener('click', () => {
                    if (window.innerWidth < 992) {
                        const bsCollapse = bootstrap.Collapse.getOrCreateInstance(this.mobileNavbarContent);
                        bsCollapse.hide();
                    }
                });
            });

            // Handle mobile dropdown toggles
            const mobileDropdownToggles = this.mobileNavbarContent.querySelectorAll('.dropdown-toggle');
            mobileDropdownToggles.forEach(toggle => {
                toggle.addEventListener('click', (e) => {
                    e.preventDefault();
                    const dropdown = bootstrap.Dropdown.getOrCreateInstance(toggle);
                    dropdown.toggle();
                });
            });
        }
    }

    /**
     * Initialize search functionality
     */
    initializeSearch() {
        const searchForms = document.querySelectorAll('form[role="search"]');
        
        searchForms.forEach(form => {
            const searchInput = form.querySelector('input[type="search"]');
            
            if (searchInput) {
                // Search input validation
                form.addEventListener('submit', (e) => {
                    const query = searchInput.value.trim();
                    if (!query) {
                        e.preventDefault();
                        searchInput.focus();
                        searchInput.classList.add('is-invalid');
                        
                        setTimeout(() => {
                            searchInput.classList.remove('is-invalid');
                        }, 3000);
                    } else {
                        // Add loading state to submit button
                        const submitBtn = form.querySelector('button[type="submit"]');
                        if (submitBtn) {
                            submitBtn.disabled = true;
                            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                        }
                    }
                });

                // Search suggestions (placeholder for future implementation)
                let searchTimeout;
                searchInput.addEventListener('input', (e) => {
                    clearTimeout(searchTimeout);
                    searchTimeout = setTimeout(() => {
                        this.handleSearchSuggestions(e.target.value);
                    }, 300);
                });
            }
        });
    }

    /**
     * Initialize accessibility features
     */
    initializeAccessibility() {
        // ARIA live regions for announcements
        this.createAriaLiveRegion();

        // Focus management
        this.setupFocusManagement();

        // High contrast mode detection
        this.detectHighContrastMode();
    }

    /**
     * Handle scroll effect for navbar shadow
     */
    handleScrollEffect() {
        const scrollY = window.scrollY;
        
        if (scrollY > 10) {
            if (this.desktopNavbar) {
                this.desktopNavbar.classList.add('navbar-scrolled');
            }
            if (this.mobileNavbar) {
                this.mobileNavbar.classList.add('navbar-scrolled');
            }
        } else {
            if (this.desktopNavbar) {
                this.desktopNavbar.classList.remove('navbar-scrolled');
            }
            if (this.mobileNavbar) {
                this.mobileNavbar.classList.remove('navbar-scrolled');
            }
        }
    }

    /**
     * Close all open dropdowns
     */
    closeAllDropdowns() {
        const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
        openDropdowns.forEach(menu => {
            const toggle = menu.previousElementSibling;
            const dropdown = bootstrap.Dropdown.getInstance(toggle);
            if (dropdown) {
                dropdown.hide();
            }
        });
        this.activeDropdown = null;
    }

    /**
     * Close other dropdowns except the specified one
     */
    closeOtherDropdowns(currentMenu) {
        const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
        openDropdowns.forEach(menu => {
            if (menu !== currentMenu) {
                const toggle = menu.previousElementSibling;
                const dropdown = bootstrap.Dropdown.getInstance(toggle);
                if (dropdown) {
                    dropdown.hide();
                }
            }
        });
    }

    /**
     * Close mobile menu
     */
    closeMobileMenu() {
        if (this.mobileNavbarContent && this.mobileNavbarContent.classList.contains('show')) {
            const bsCollapse = bootstrap.Collapse.getInstance(this.mobileNavbarContent);
            if (bsCollapse) {
                bsCollapse.hide();
            }
        }
    }

    /**
     * Position dropdown to prevent viewport overflow
     */
    positionDropdown(menu) {
        const rect = menu.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        // Reset positioning
        menu.style.left = '';
        menu.style.right = '';
        menu.style.transform = '';

        // Horizontal positioning
        if (rect.right > viewportWidth - 20) {
            menu.style.left = 'auto';
            menu.style.right = '0';
            menu.style.transform = 'none';
        } else if (rect.left < 20) {
            menu.style.left = '0';
            menu.style.right = 'auto';
            menu.style.transform = 'none';
        }

        // Vertical positioning for bottom overflow
        if (rect.bottom > viewportHeight - 20) {
            menu.style.top = 'auto';
            menu.style.bottom = '100%';
            menu.style.marginTop = '0';
            menu.style.marginBottom = '0.5rem';
        }
    }

    /**
     * Handle search suggestions
     */
    handleSearchSuggestions(query) {
        // Placeholder for search suggestions implementation
        if (query.length >= 2) {
            console.log('Search suggestions for:', query);
            // Implementation would go here
        }
    }

    /**
     * Create ARIA live region for announcements
     */
    createAriaLiveRegion() {
        if (!document.getElementById('navbar-announcements')) {
            const liveRegion = document.createElement('div');
            liveRegion.id = 'navbar-announcements';
            liveRegion.setAttribute('aria-live', 'polite');
            liveRegion.setAttribute('aria-atomic', 'true');
            liveRegion.style.position = 'absolute';
            liveRegion.style.left = '-10000px';
            liveRegion.style.width = '1px';
            liveRegion.style.height = '1px';
            liveRegion.style.overflow = 'hidden';
            document.body.appendChild(liveRegion);
        }
    }

    /**
     * Setup focus management
     */
    setupFocusManagement() {
        // Trap focus in mobile menu when open
        this.mobileNavbarContent?.addEventListener('keydown', (e) => {
            if (e.key === 'Tab' && this.mobileNavbarContent.classList.contains('show')) {
                const focusableElements = this.mobileNavbarContent.querySelectorAll(
                    'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
                );
                const firstElement = focusableElements[0];
                const lastElement = focusableElements[focusableElements.length - 1];

                if (e.shiftKey && document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                } else if (!e.shiftKey && document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        });
    }

    /**
     * Detect high contrast mode
     */
    detectHighContrastMode() {
        if (window.matchMedia('(prefers-contrast: high)').matches) {
            document.documentElement.classList.add('high-contrast');
        }
    }

    /**
     * Utility: Debounce function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Utility: Throttle function
     */
    throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * Public API: Reinitialize navbar
     */
    reinitialize() {
        this.isInitialized = false;
        this.init();
    }

    /**
     * Public API: Close all dropdowns
     */
    closeDropdowns() {
        this.closeAllDropdowns();
    }

    /**
     * Public API: Toggle mobile menu
     */
    toggleMobileMenu() {
        if (this.mobileNavbarContent) {
            const bsCollapse = bootstrap.Collapse.getOrCreateInstance(this.mobileNavbarContent);
            bsCollapse.toggle();
        }
    }

    /**
     * Public API: Announce message to screen readers
     */
    announce(message) {
        const liveRegion = document.getElementById('navbar-announcements');
        if (liveRegion) {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    }

    /**
     * Cleanup: Remove event listeners and clear timeouts
     */
    destroy() {
        // Clear all timeouts
        this.hoverTimeouts.forEach(timeout => clearTimeout(timeout));
        this.hoverTimeouts.clear();

        // Remove event listeners would go here
        this.isInitialized = false;
    }
}

/**
 * Auto-initialize when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Check if Bootstrap is loaded
    if (typeof bootstrap === 'undefined') {
        console.warn('Bootstrap 5 is required for the responsive navbar');
        return;
    }

    // Initialize the responsive navbar
    window.ResponsiveNavbar = new ResponsiveNavbar();
    
    // Make it globally accessible
    window.NavbarAPI = {
        reinitialize: () => window.ResponsiveNavbar.reinitialize(),
        closeDropdowns: () => window.ResponsiveNavbar.closeDropdowns(),
        toggleMobileMenu: () => window.ResponsiveNavbar.toggleMobileMenu(),
        announce: (message) => window.ResponsiveNavbar.announce(message)
    };
});

/**
 * Performance: Clean up on page unload
 */
window.addEventListener('beforeunload', function() {
    if (window.ResponsiveNavbar) {
        window.ResponsiveNavbar.destroy();
    }
});

/**
 * Handle page visibility changes
 */
document.addEventListener('visibilitychange', function() {
    if (document.hidden && window.ResponsiveNavbar) {
        window.ResponsiveNavbar.closeDropdowns();
    }
});

/**
 * Export for module systems
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ResponsiveNavbar;
}
