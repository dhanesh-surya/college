/**
 * Clean Professional Navbar JavaScript
 * Bootstrap 5 compatible dropdown and responsive navbar functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeNavbar();
    initializeDropdowns();
    initializeMobileNavbar();
    initializeUtilities();
});

/**
 * Initialize main navbar functionality
 */
function initializeNavbar() {
    const navbar = document.querySelector('#mainNavbar');
    const mobileNavbar = document.querySelector('#mobileNavbar');
    
    // Ensure navbar visibility
    if (navbar) {
        navbar.style.display = 'block';
        navbar.style.visibility = 'visible';
        navbar.style.opacity = '1';
        navbar.style.position = 'relative';
        navbar.style.width = '100%';
        navbar.style.zIndex = '1030';
    }
    
    // Handle responsive display
    function handleResponsiveDisplay() {
        const screenWidth = window.innerWidth;
        
        if (screenWidth >= 992) {
            // Desktop: show main navbar, hide mobile
            if (navbar) {
                navbar.style.display = 'block';
                navbar.classList.remove('d-lg-none');
            }
            if (mobileNavbar) {
                mobileNavbar.style.display = 'none';
                mobileNavbar.classList.add('d-lg-none');
            }
        } else {
            // Mobile: hide main navbar, show mobile
            if (navbar) {
                navbar.style.display = 'none';
                navbar.classList.add('d-lg-none');
            }
            if (mobileNavbar) {
                mobileNavbar.style.display = 'block';
                mobileNavbar.classList.remove('d-lg-none');
            }
        }
    }
    
    // Initial setup and resize handling
    handleResponsiveDisplay();
    window.addEventListener('resize', debounce(handleResponsiveDisplay, 250));
    
    // Active link highlighting
    highlightActiveLinks();
}

/**
 * Initialize Bootstrap 5 dropdown functionality
 */
function initializeDropdowns() {
    const dropdownElementList = document.querySelectorAll('.dropdown-toggle');
    
    dropdownElementList.forEach(function (dropdownToggleEl) {
        // Initialize Bootstrap dropdown
        const dropdown = new bootstrap.Dropdown(dropdownToggleEl, {
            autoClose: true,
            boundary: 'viewport',
            popperConfig: null
        });
        
        const dropdownMenu = dropdownToggleEl.nextElementSibling;
        const parentDropdown = dropdownToggleEl.closest('.dropdown');
        
        if (!dropdownMenu || !parentDropdown) return;
        
        // Desktop hover behavior
        if (window.innerWidth > 991) {
            let hoverTimeout;
            
            parentDropdown.addEventListener('mouseenter', function() {
                clearTimeout(hoverTimeout);
                
                // Close other open dropdowns first
                closeOtherDropdowns(dropdownMenu);
                
                // Show current dropdown
                dropdown.show();
            });
            
            parentDropdown.addEventListener('mouseleave', function() {
                hoverTimeout = setTimeout(() => {
                    if (!parentDropdown.matches(':hover')) {
                        dropdown.hide();
                    }
                }, 150);
            });
        }
        
        // Click behavior for all screen sizes
        dropdownToggleEl.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Close other dropdowns first
            closeOtherDropdowns(dropdownMenu);
            
            // Toggle current dropdown
            if (dropdownMenu.classList.contains('show')) {
                dropdown.hide();
            } else {
                dropdown.show();
            }
        });
        
        // Handle dropdown item clicks
        dropdownMenu.addEventListener('click', function(e) {
            if (e.target.classList.contains('dropdown-item')) {
                const href = e.target.getAttribute('href');
                if (href && href !== '#' && href !== '') {
                    dropdown.hide();
                }
            }
        });
        
        // Ensure proper positioning
        dropdownToggleEl.addEventListener('shown.bs.dropdown', function() {
            dropdownMenu.style.display = 'block';
            dropdownMenu.style.visibility = 'visible';
            dropdownMenu.style.opacity = '1';
            
            // Position dropdown to prevent viewport overflow
            positionDropdown(dropdownMenu);
        });
        
        dropdownToggleEl.addEventListener('hidden.bs.dropdown', function() {
            dropdownMenu.style.display = 'none';
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            closeAllDropdowns();
        }
    });
}

/**
 * Initialize mobile navbar functionality
 */
function initializeMobileNavbar() {
    const mobileToggler = document.querySelector('#mobileNavbar .navbar-toggler');
    const mobileCollapse = document.querySelector('#mobileNavbarContent');
    
    if (mobileToggler && mobileCollapse) {
        // Handle mobile toggle click
        mobileToggler.addEventListener('click', function(e) {
            e.preventDefault();
            const bsCollapse = bootstrap.Collapse.getOrCreateInstance(mobileCollapse);
            bsCollapse.toggle();
        });
        
        // Close mobile nav when clicking nav links
        const mobileNavLinks = mobileCollapse.querySelectorAll('.nav-link');
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 992 && !this.classList.contains('dropdown-toggle')) {
                    const bsCollapse = bootstrap.Collapse.getOrCreateInstance(mobileCollapse);
                    bsCollapse.hide();
                }
            });
        });
    }
}

/**
 * Initialize utility functions
 */
function initializeUtilities() {
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert.alert-dismissible');
        alerts.forEach(alert => {
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (e) {
                // Silently handle if alert is already closed
            }
        });
    }, 5000);
    
    // Handle search form validation
    const searchForms = document.querySelectorAll('form[role="search"]');
    searchForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[name="q"]');
            if (searchInput && !searchInput.value.trim()) {
                e.preventDefault();
                searchInput.focus();
                searchInput.classList.add('is-invalid');
                setTimeout(() => {
                    searchInput.classList.remove('is-invalid');
                }, 3000);
            }
        });
    });
    
    // Smooth anchor scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || href === '') {
                e.preventDefault();
                return;
            }
            
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start',
                    inline: 'nearest'
                });
            }
        });
    });
    
    // Scrolling notification bar pause on hover
    const scrollingContainer = document.querySelector('.scrolling-notification-container');
    if (scrollingContainer) {
        scrollingContainer.addEventListener('mouseenter', function() {
            this.style.animationPlayState = 'paused';
        });
        
        scrollingContainer.addEventListener('mouseleave', function() {
            this.style.animationPlayState = 'running';
        });
    }
    
    // Prevent double-click issues
    let clickTimeout;
    document.addEventListener('click', function(e) {
        if (e.target.matches('a, button, .btn, .dropdown-toggle, .nav-link')) {
            if (clickTimeout) {
                e.preventDefault();
                return false;
            }
            clickTimeout = setTimeout(() => {
                clickTimeout = null;
            }, 500);
        }
    });
}

/**
 * Helper function to close other open dropdowns
 */
function closeOtherDropdowns(currentMenu) {
    document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
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
 * Helper function to close all dropdowns
 */
function closeAllDropdowns() {
    document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
        const toggle = menu.previousElementSibling;
        const dropdown = bootstrap.Dropdown.getInstance(toggle);
        if (dropdown) {
            dropdown.hide();
        }
    });
}

/**
 * Position dropdown to prevent viewport overflow
 */
function positionDropdown(menu) {
    const rect = menu.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    
    // Reset positioning
    menu.style.left = '';
    menu.style.right = '';
    menu.style.transform = '';
    
    // Check if dropdown extends beyond viewport
    if (rect.right > viewportWidth) {
        menu.style.left = 'auto';
        menu.style.right = '0';
        menu.style.transform = 'none';
    } else if (rect.left < 0) {
        menu.style.left = '0';
        menu.style.right = 'auto';
        menu.style.transform = 'none';
    }
}

/**
 * Highlight active navigation links
 */
function highlightActiveLinks() {
    const currentLocation = location.pathname;
    const menuItems = document.querySelectorAll('.navbar-nav .nav-link');
    
    menuItems.forEach(item => {
        if (item.getAttribute('href') === currentLocation) {
            item.classList.add('active');
        }
    });
}

/**
 * Debounce utility function
 */
function debounce(func, wait) {
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
 * Public API for external access
 */
window.NavbarEnhancements = {
    reinitialize: function() {
        initializeNavbar();
        initializeDropdowns();
        initializeMobileNavbar();
    },
    closeAllDropdowns: closeAllDropdowns,
    highlightActiveLinks: highlightActiveLinks
};

/**
 * Performance: Clean up on page unload
 */
window.addEventListener('beforeunload', function() {
    // Clean up any remaining timeouts
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        if (toggle) {
            const bsDropdown = bootstrap.Dropdown.getInstance(toggle);
            if (bsDropdown) {
                bsDropdown.dispose();
            }
        }
    });
});
