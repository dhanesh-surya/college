// Enhanced Menu Admin JavaScript

(function($) {
    'use strict';

    // Initialize when DOM is ready
    $(document).ready(function() {
        initMenuAdmin();
    });

    function initMenuAdmin() {
        // Initialize path type conditional fields
        initPathTypeConditionals();
        
        // Initialize form validation
        initFormValidation();
        
        // Initialize drag and drop for sortable items
        initSortableItems();
        
        // Initialize URL preview
        initUrlPreview();
        
        // Initialize menu item counters
        updateMenuItemCounters();
    }

    // Path Type Conditional Field Display
    function initPathTypeConditionals() {
        $(document).on('change', 'select[name*="path_type"]', function() {
            var $select = $(this);
            var pathType = $select.val();
            var $row = $select.closest('.form-row, .inline-related, tr');
            
            var $externalUrlField = $row.find('.field-external_url, [class*="external_url"]');
            var $pageField = $row.find('.field-page, [class*="page"]');
            
            if (pathType === 'external') {
                $externalUrlField.show().removeClass('hidden');
                $pageField.hide().addClass('hidden');
                $externalUrlField.find('input').prop('required', true);
                $pageField.find('select').prop('required', false);
            } else if (pathType === 'internal') {
                $pageField.show().removeClass('hidden');
                $externalUrlField.hide().addClass('hidden');
                $pageField.find('select').prop('required', true);
                $externalUrlField.find('input').prop('required', false);
            } else {
                $externalUrlField.hide().addClass('hidden');
                $pageField.hide().addClass('hidden');
                $externalUrlField.find('input').prop('required', false);
                $pageField.find('select').prop('required', false);
            }
        });

        // Trigger on page load for existing forms
        $('select[name*="path_type"]').trigger('change');
    }

    // Form Validation
    function initFormValidation() {
        $('form').on('submit', function(e) {
            var isValid = true;
            var errors = [];

            // Validate menu items
            $('.inline-related:not(.empty-form)').each(function() {
                var $item = $(this);
                var pathType = $item.find('select[name*="path_type"]').val();
                var externalUrl = $item.find('input[name*="external_url"]').val();
                var page = $item.find('select[name*="page"]').val();
                var title = $item.find('input[name*="title"]').val();

                if (title) { // Only validate if title is filled
                    if (pathType === 'external' && !externalUrl) {
                        errors.push('External URL is required when path type is External');
                        $item.find('input[name*="external_url"]').addClass('error');
                        isValid = false;
                    }
                    
                    if (pathType === 'internal' && !page) {
                        errors.push('Page selection is required when path type is Internal');
                        $item.find('select[name*="page"]').addClass('error');
                        isValid = false;
                    }
                }
            });

            if (!isValid) {
                e.preventDefault();
                showValidationErrors(errors);
            }
        });

        // Clear error styling on input
        $(document).on('input change', 'input.error, select.error', function() {
            $(this).removeClass('error');
        });
    }

    // Show validation errors
    function showValidationErrors(errors) {
        var errorHtml = '<div class="errorlist"><ul>';
        errors.forEach(function(error) {
            errorHtml += '<li>' + error + '</li>';
        });
        errorHtml += '</ul></div>';

        // Remove existing error messages
        $('.errorlist').remove();
        
        // Add new error message at the top of the form
        $('form').prepend(errorHtml);
        
        // Scroll to top
        $('html, body').animate({ scrollTop: 0 }, 300);
    }

    // Initialize sortable items
    function initSortableItems() {
        if ($.fn.sortable) {
            $('.inline-group').sortable({
                items: '.inline-related:not(.empty-form)',
                handle: '.sortable-handle, .drag-handle',
                axis: 'y',
                opacity: 0.8,
                placeholder: 'sortable-placeholder',
                update: function(event, ui) {
                    updateOrderingFields($(this));
                }
            });
        }
    }

    // Update ordering fields after sorting
    function updateOrderingFields($container) {
        $container.find('.inline-related:not(.empty-form)').each(function(index) {
            $(this).find('input[name*="ordering"]').val(index + 1);
        });
    }

    // URL Preview functionality
    function initUrlPreview() {
        $(document).on('input', 'input[name*="external_url"]', function() {
            var $input = $(this);
            var url = $input.val();
            var $preview = $input.siblings('.url-preview');
            
            if (!$preview.length) {
                $preview = $('<div class="url-preview"></div>');
                $input.after($preview);
            }
            
            if (url) {
                $preview.html('<small class="url-display">Preview: <a href="' + url + '" target="_blank">' + url + '</a></small>');
            } else {
                $preview.empty();
            }
        });

        // Trigger on page load
        $('input[name*="external_url"]').trigger('input');
    }

    // Update menu item counters
    function updateMenuItemCounters() {
        $('.inline-group').each(function() {
            var $group = $(this);
            var totalItems = $group.find('.inline-related:not(.empty-form)').length;
            var activeItems = $group.find('.inline-related:not(.empty-form) input[name*="is_active"]:checked').length;
            
            var $counter = $group.find('.menu-items-counter');
            if (!$counter.length) {
                $counter = $('<span class="menu-items-counter"></span>');
                $group.find('h2').append($counter);
            }
            
            $counter.html('<span class="menu-items-count">' + activeItems + '/' + totalItems + ' active</span>');
        });

        // Update counters when items are added/removed/changed
        $(document).on('change', 'input[name*="is_active"], input[name*="DELETE"]', function() {
            setTimeout(updateMenuItemCounters, 100);
        });
    }

    // Add new inline form functionality
    $(document).on('click', '.add-row a', function(e) {
        setTimeout(function() {
            initPathTypeConditionals();
            updateMenuItemCounters();
        }, 100);
    });

    // Delete inline form functionality
    $(document).on('click', '.delete-row', function() {
        setTimeout(updateMenuItemCounters, 100);
    });

    // Auto-generate slug from title
    $(document).on('input', 'input[name*="title"]:not([name*="meta_title"])', function() {
        var $titleInput = $(this);
        var $slugInput = $titleInput.closest('.form-row, .inline-related, tr').find('input[name*="slug"]');
        
        if ($slugInput.length && !$slugInput.val()) {
            var slug = generateSlug($titleInput.val());
            $slugInput.val(slug);
        }
    });

    // Generate URL-friendly slug
    function generateSlug(text) {
        return text
            .toLowerCase()
            .replace(/[^\w\s-]/g, '') // Remove special characters
            .replace(/[\s_-]+/g, '-') // Replace spaces and underscores with hyphens
            .replace(/^-+|-+$/g, ''); // Remove leading/trailing hyphens
    }

    // Keyboard shortcuts
    $(document).on('keydown', function(e) {
        // Ctrl+S to save
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            $('input[name="_save"]').click();
        }
        
        // Ctrl+Shift+A to add new menu item
        if (e.ctrlKey && e.shiftKey && e.key === 'A') {
            e.preventDefault();
            $('.add-row a').first().click();
        }
    });

    // Enhanced UI feedback
    function showNotification(message, type) {
        type = type || 'success';
        var $notification = $('<div class="notification notification-' + type + '">' + message + '</div>');
        
        $('body').append($notification);
        
        setTimeout(function() {
            $notification.fadeOut(function() {
                $(this).remove();
            });
        }, 3000);
    }

    // Form auto-save (optional)
    var autoSaveTimer;
    $(document).on('input change', 'form input, form select, form textarea', function() {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(function() {
            // Auto-save logic can be implemented here if needed
            console.log('Auto-save triggered');
        }, 5000);
    });

})(django.jQuery);

// CSS for notifications
var notificationCSS = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 4px;
        color: white;
        font-weight: 500;
        z-index: 9999;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .notification-success {
        background: #28a745;
    }
    .notification-error {
        background: #dc3545;
    }
    .notification-warning {
        background: #ffc107;
        color: #212529;
    }
    .sortable-placeholder {
        height: 60px;
        background: #f8f9fa;
        border: 2px dashed #dee2e6;
        margin: 5px 0;
    }
    input.error, select.error {
        border-color: #dc3545 !important;
        box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25) !important;
    }
`;

// Inject CSS
var style = document.createElement('style');
style.textContent = notificationCSS;
document.head.appendChild(style);
