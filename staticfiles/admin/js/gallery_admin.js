// Gallery Admin JavaScript

(function($) {
    'use strict';

    // Initialize when DOM is ready
    $(document).ready(function() {
        initGalleryAdmin();
    });

    function initGalleryAdmin() {
        // Initialize image upload handling
        initImageUpload();
        
        // Initialize image preview
        initImagePreview();
        
        // Initialize drag and drop for image ordering
        initImageSorting();
        
        // Initialize bulk actions
        initBulkActions();
        
        // Initialize image validation
        initImageValidation();
        
        // Initialize gallery statistics
        updateGalleryStats();
    }

    // Image Upload Handling
    function initImageUpload() {
        $(document).on('change', 'input[type="file"][accept*="image"]', function() {
            var $input = $(this);
            var file = this.files[0];
            
            if (file) {
                // Validate file
                if (validateImageFile(file, $input)) {
                    // Show preview
                    showImagePreview(file, $input);
                    
                    // Update file info
                    updateFileInfo(file, $input);
                }
            }
        });

        // Drag and drop file upload
        $('.gallery-image-upload').on({
            'dragover dragenter': function(e) {
                e.preventDefault();
                e.stopPropagation();
                $(this).addClass('drag-over');
            },
            'dragleave': function(e) {
                e.preventDefault();
                e.stopPropagation();
                $(this).removeClass('drag-over');
            },
            'drop': function(e) {
                e.preventDefault();
                e.stopPropagation();
                $(this).removeClass('drag-over');
                
                var files = e.originalEvent.dataTransfer.files;
                if (files.length > 0) {
                    var $input = $(this).find('input[type="file"]');
                    $input[0].files = files;
                    $input.trigger('change');
                }
            }
        });
    }

    // Image Preview
    function initImagePreview() {
        // Lightbox for image previews
        $(document).on('click', '.image-preview img', function() {
            var src = $(this).attr('src');
            var caption = $(this).closest('tr').find('input[name*="caption"]').val() || 'Gallery Image';
            
            showImageLightbox(src, caption);
        });
    }

    // Image Sorting
    function initImageSorting() {
        if ($.fn.sortable) {
            $('.gallery-images-table tbody').sortable({
                items: 'tr:not(.empty-form)',
                handle: '.sortable-handle',
                axis: 'y',
                opacity: 0.8,
                placeholder: 'ui-sortable-placeholder',
                update: function(event, ui) {
                    updateImageOrdering($(this));
                }
            });
        }
    }

    // Update image ordering after sorting
    function updateImageOrdering($container) {
        $container.find('tr:not(.empty-form)').each(function(index) {
            $(this).find('input[name*="ordering"]').val(index + 1);
        });
        
        showNotification('Image order updated', 'success');
    }

    // Bulk Actions
    function initBulkActions() {
        // Select all images
        $(document).on('change', '.select-all-images', function() {
            var checked = $(this).prop('checked');
            $('.image-checkbox').prop('checked', checked);
            updateBulkActionButtons();
        });

        // Individual image selection
        $(document).on('change', '.image-checkbox', function() {
            updateBulkActionButtons();
        });

        // Bulk delete
        $(document).on('click', '.bulk-delete-images', function() {
            var selectedImages = $('.image-checkbox:checked');
            if (selectedImages.length > 0) {
                if (confirm(`Are you sure you want to delete ${selectedImages.length} image(s)?`)) {
                    selectedImages.each(function() {
                        var $row = $(this).closest('tr');
                        $row.find('input[name*="DELETE"]').prop('checked', true);
                        $row.hide();
                    });
                    showNotification(`${selectedImages.length} image(s) marked for deletion`, 'warning');
                }
            }
        });

        // Bulk caption update
        $(document).on('click', '.bulk-update-captions', function() {
            var newCaption = prompt('Enter new caption for selected images:');
            if (newCaption !== null) {
                $('.image-checkbox:checked').each(function() {
                    var $row = $(this).closest('tr');
                    $row.find('input[name*="caption"]').val(newCaption);
                });
                showNotification('Captions updated', 'success');
            }
        });
    }

    // Update bulk action button states
    function updateBulkActionButtons() {
        var selectedCount = $('.image-checkbox:checked').length;
        var $bulkActions = $('.gallery-bulk-actions');
        
        if (selectedCount > 0) {
            $bulkActions.show();
            $bulkActions.find('.selected-count').text(selectedCount);
        } else {
            $bulkActions.hide();
        }
    }

    // Image Validation
    function initImageValidation() {
        $(document).on('change', 'input[type="file"][accept*="image"]', function() {
            var file = this.files[0];
            var $input = $(this);
            
            if (file) {
                validateImageFile(file, $input);
            }
        });
    }

    // Validate image file
    function validateImageFile(file, $input) {
        var isValid = true;
        var messages = [];
        
        // Check file type
        if (!file.type.startsWith('image/')) {
            messages.push('Please select a valid image file');
            isValid = false;
        }
        
        // Check file size (5MB limit)
        var maxSize = 5 * 1024 * 1024; // 5MB
        if (file.size > maxSize) {
            messages.push('File size too large (max 5MB)');
            isValid = false;
        }
        
        // Check dimensions (if possible)
        if (file.type.startsWith('image/')) {
            checkImageDimensions(file, function(width, height) {
                if (width < 300 || height < 300) {
                    showValidationMessage($input, 'Image resolution is low (recommended: 800x600 or larger)', 'warning');
                } else {
                    showValidationMessage($input, `Image: ${width}x${height}px`, 'valid');
                }
            });
        }
        
        // Show validation messages
        if (messages.length > 0) {
            showValidationMessage($input, messages.join(', '), 'invalid');
        }
        
        return isValid;
    }

    // Check image dimensions
    function checkImageDimensions(file, callback) {
        var img = new Image();
        img.onload = function() {
            callback(this.width, this.height);
        };
        img.src = URL.createObjectURL(file);
    }

    // Show validation message
    function showValidationMessage($input, message, type) {
        var $container = $input.closest('td, .form-group');
        var $existing = $container.find('.image-validation');
        
        if ($existing.length) {
            $existing.remove();
        }
        
        var $message = $('<div class="image-validation ' + type + '">' + message + '</div>');
        $container.append($message);
        
        // Auto-hide success messages
        if (type === 'valid') {
            setTimeout(function() {
                $message.fadeOut();
            }, 3000);
        }
    }

    // Show image preview
    function showImagePreview(file, $input) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var $preview = $input.siblings('.image-preview');
            if (!$preview.length) {
                $preview = $('<div class="image-preview"></div>');
                $input.after($preview);
            }
            
            $preview.html('<img src="' + e.target.result + '" style="max-width: 150px; max-height: 100px; border-radius: 4px; margin-top: 10px;" />');
        };
        reader.readAsDataURL(file);
    }

    // Update file info
    function updateFileInfo(file, $input) {
        var $info = $input.siblings('.file-info');
        if (!$info.length) {
            $info = $('<div class="file-info"></div>');
            $input.after($info);
        }
        
        var sizeKB = Math.round(file.size / 1024);
        var sizeText = sizeKB > 1024 ? (sizeKB / 1024).toFixed(1) + ' MB' : sizeKB + ' KB';
        
        $info.html('<small class="text-muted">File: ' + file.name + ' (' + sizeText + ')</small>');
    }

    // Show image lightbox
    function showImageLightbox(src, caption) {
        var $lightbox = $('#image-lightbox');
        if (!$lightbox.length) {
            $lightbox = $('<div id="image-lightbox" class="image-lightbox"><div class="lightbox-content"><img /><div class="lightbox-caption"></div><button class="lightbox-close">&times;</button></div></div>');
            $('body').append($lightbox);
        }
        
        $lightbox.find('img').attr('src', src);
        $lightbox.find('.lightbox-caption').text(caption);
        $lightbox.show();
        
        // Close lightbox
        $lightbox.on('click', function(e) {
            if (e.target === this || $(e.target).hasClass('lightbox-close')) {
                $(this).hide();
            }
        });
    }

    // Update gallery statistics
    function updateGalleryStats() {
        var totalGalleries = $('.gallery-item').length;
        var activeGalleries = $('.gallery-item.active').length;
        var totalImages = $('.image-item').length;
        
        var $stats = $('.gallery-stats');
        if ($stats.length) {
            $stats.find('.total-galleries').text(totalGalleries);
            $stats.find('.active-galleries').text(activeGalleries);
            $stats.find('.total-images').text(totalImages);
        }
    }

    // Show notification
    function showNotification(message, type) {
        type = type || 'info';
        var $notification = $('<div class="gallery-notification gallery-notification-' + type + '">' + message + '</div>');
        
        $('body').append($notification);
        
        setTimeout(function() {
            $notification.fadeOut(function() {
                $(this).remove();
            });
        }, 3000);
    }

    // Auto-save functionality
    var autoSaveTimer;
    $(document).on('input change', '.gallery-form input, .gallery-form select, .gallery-form textarea', function() {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(function() {
            // Auto-save logic can be implemented here
            console.log('Gallery auto-save triggered');
        }, 5000);
    });

    // Keyboard shortcuts
    $(document).on('keydown', function(e) {
        // Ctrl+S to save
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            $('input[name="_save"]').click();
        }
        
        // Delete key to remove selected images
        if (e.key === 'Delete' && $('.image-checkbox:checked').length > 0) {
            e.preventDefault();
            $('.bulk-delete-images').click();
        }
    });

    // Form submission enhancements
    $('form').on('submit', function() {
        // Show loading state
        var $submitButton = $(this).find('input[type="submit"]');
        $submitButton.prop('disabled', true).val('Saving...');
        
        // Re-enable after a delay (in case of errors)
        setTimeout(function() {
            $submitButton.prop('disabled', false).val('Save');
        }, 5000);
    });

})(django.jQuery);

// CSS for gallery notifications and lightbox
var galleryCSS = `
    .gallery-notification {
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
    .gallery-notification-success {
        background: #28a745;
    }
    .gallery-notification-error {
        background: #dc3545;
    }
    .gallery-notification-warning {
        background: #ffc107;
        color: #212529;
    }
    .gallery-notification-info {
        background: #17a2b8;
    }
    
    .image-lightbox {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.9);
        z-index: 10000;
        display: none;
        align-items: center;
        justify-content: center;
    }
    
    .lightbox-content {
        position: relative;
        max-width: 90%;
        max-height: 90%;
        text-align: center;
    }
    
    .lightbox-content img {
        max-width: 100%;
        max-height: 80vh;
        border-radius: 8px;
    }
    
    .lightbox-caption {
        color: white;
        padding: 10px;
        font-size: 16px;
    }
    
    .lightbox-close {
        position: absolute;
        top: -40px;
        right: -40px;
        background: none;
        border: none;
        color: white;
        font-size: 30px;
        cursor: pointer;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(255,255,255,0.2);
    }
    
    .drag-over {
        border-color: #28a745 !important;
        background: #f0f8f0 !important;
    }
    
    .gallery-bulk-actions {
        display: none;
        background: #e9ecef;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    
    .ui-sortable-placeholder {
        height: 60px;
        background: #f0f8f0;
        border: 2px dashed #28a745;
        margin: 5px 0;
    }
`;

// Inject CSS
var style = document.createElement('style');
style.textContent = galleryCSS;
document.head.appendChild(style);
