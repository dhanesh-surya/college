/**
 * Top Utility Bar Admin JavaScript
 * Provides interactive functionality for the admin interface
 */

(function($) {
    'use strict';

    // Initialize when DOM is ready
    $(document).ready(function() {
        initializeTopUtilityBarForm();
        initializeColorPickers();
        initializeConditionalFields();
        initializeValidation();
        initializePreviewFunctionality();
        initializeTooltips();
    });

    /**
     * Initialize the main form functionality
     */
    function initializeTopUtilityBarForm() {
        // Add form wrapper class
        $('.top-utility-bar-form').closest('form').addClass('utility-bar-admin-form');
        
        // Enhance fieldsets
        $('.top-utility-bar-form fieldset').each(function() {
            const $fieldset = $(this);
            const $legend = $fieldset.find('h2');
            
            if ($legend.length) {
                $legend.addClass('fieldset-header').prepend('<i class="fas fa-chevron-down fieldset-toggle"></i>');
                
                // Make fieldsets collapsible
                $legend.css('cursor', 'pointer').on('click', function() {
                    const $content = $fieldset.find('.form-row');
                    const $icon = $(this).find('.fieldset-toggle');
                    
                    $content.slideToggle(300);
                    $icon.toggleClass('fa-chevron-down fa-chevron-up');
                });
            }
        });

        // Add helpful indicators
        addFormIndicators();
    }

    /**
     * Initialize enhanced color pickers
     */
    function initializeColorPickers() {
        $('input[type="color"]').each(function() {
            const $input = $(this);
            const $wrapper = $('<div class="color-picker-wrapper"></div>');
            
            $input.wrap($wrapper);
            
            // Add color preview and reset button
            $input.after(`
                <div class="color-picker-controls">
                    <div class="color-preview" style="background-color: ${$input.val()}"></div>
                    <button type="button" class="btn btn-sm btn-outline-secondary reset-color" title="Reset to default">
                        <i class="fas fa-undo"></i>
                    </button>
                </div>
            `);
            
            // Update preview when color changes
            $input.on('change', function() {
                $(this).siblings('.color-picker-controls').find('.color-preview')
                    .css('background-color', this.value);
                validateColorContrast();
            });
            
            // Reset to default color
            $input.siblings('.color-picker-controls').find('.reset-color').on('click', function() {
                const defaultColor = $input.data('default') || '#ffffff';
                $input.val(defaultColor).trigger('change');
            });
        });
    }

    /**
     * Initialize conditional field visibility
     */
    function initializeConditionalFields() {
        // Social media fields
        const $showSocialIcons = $('#id_show_social_icons');
        const $socialFields = $('.social-media-fields');
        
        function toggleSocialFields() {
            if ($showSocialIcons.is(':checked')) {
                $socialFields.removeClass('hidden').addClass('visible');
            } else {
                $socialFields.removeClass('visible').addClass('hidden');
            }
        }
        
        $showSocialIcons.on('change', toggleSocialFields);
        toggleSocialFields(); // Initial state

        // Contact info fields
        const $showContactInfo = $('#id_show_contact_info');
        const $contactFields = $('.contact-info-fields');
        
        function toggleContactFields() {
            if ($showContactInfo.is(':checked')) {
                $contactFields.removeClass('hidden').addClass('visible');
            } else {
                $contactFields.removeClass('visible').addClass('hidden');
            }
        }
        
        $showContactInfo.on('change', toggleContactFields);
        toggleContactFields(); // Initial state

        // Custom links fields
        const $showCustomLinks = $('#id_show_custom_links');
        const $customLinksFields = $('.custom-links-fields');
        
        function toggleCustomLinksFields() {
            if ($showCustomLinks.is(':checked')) {
                $customLinksFields.removeClass('hidden').addClass('visible');
            } else {
                $customLinksFields.removeClass('visible').addClass('hidden');
            }
        }
        
        $showCustomLinks.on('change', toggleCustomLinksFields);
        toggleCustomLinksFields(); // Initial state

        // Custom link pair validation
        initializeCustomLinkPairs();
    }

    /**
     * Initialize custom link pair functionality
     */
    function initializeCustomLinkPairs() {
        for (let i = 1; i <= 3; i++) {
            const $textField = $(`#id_custom_link_${i}_text`);
            const $urlField = $(`#id_custom_link_${i}_url`);
            
            // Add real-time validation
            $textField.add($urlField).on('input blur', function() {
                validateCustomLinkPair(i);
            });
        }
    }

    /**
     * Validate custom link pairs
     */
    function validateCustomLinkPair(linkNumber) {
        const $textField = $(`#id_custom_link_${linkNumber}_text`);
        const $urlField = $(`#id_custom_link_${linkNumber}_url`);
        
        const text = $textField.val().trim();
        const url = $urlField.val().trim();
        
        // Remove previous validation
        $textField.add($urlField).removeClass('is-valid is-invalid');
        
        if (text || url) {
            if (text && url) {
                // Both provided - valid
                $textField.add($urlField).addClass('is-valid');
            } else {
                // Only one provided - invalid
                $textField.addClass(text ? 'is-valid' : 'is-invalid');
                $urlField.addClass(url ? 'is-valid' : 'is-invalid');
            }
        }
    }

    /**
     * Initialize form validation
     */
    function initializeValidation() {
        // Phone number validation
        $('#id_contact_phone').on('input', function() {
            const phone = this.value.trim();
            const phoneRegex = /^[\+]?[1-9][\d\s\-\(\)]{8,15}$/;
            
            $(this).removeClass('is-valid is-invalid');
            
            if (phone && !phoneRegex.test(phone)) {
                $(this).addClass('is-invalid');
                showFieldError($(this), 'Please enter a valid phone number');
            } else if (phone) {
                $(this).addClass('is-valid');
                clearFieldError($(this));
            }
        });

        // Email validation
        $('#id_contact_email').on('input', function() {
            const email = this.value.trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            $(this).removeClass('is-valid is-invalid');
            
            if (email && !emailRegex.test(email)) {
                $(this).addClass('is-invalid');
                showFieldError($(this), 'Please enter a valid email address');
            } else if (email) {
                $(this).addClass('is-valid');
                clearFieldError($(this));
            }
        });

        // URL validation for social media
        $('input[data-validation="url"]').on('input', function() {
            const url = this.value.trim();
            const urlRegex = /^https?:\/\/.+/;
            
            $(this).removeClass('is-valid is-invalid');
            
            if (url && !urlRegex.test(url)) {
                $(this).addClass('is-invalid');
                showFieldError($(this), 'Please enter a complete URL starting with http:// or https://');
            } else if (url) {
                $(this).addClass('is-valid');
                clearFieldError($(this));
            }
        });

        // Height validation
        $('#id_height').on('input', function() {
            const height = parseInt(this.value);
            
            $(this).removeClass('is-valid is-invalid');
            
            if (height && (height < 20 || height > 100)) {
                $(this).addClass('is-invalid');
                showFieldError($(this), 'Height should be between 20 and 100 pixels');
            } else if (height) {
                $(this).addClass('is-valid');
                clearFieldError($(this));
            }
        });
    }

    /**
     * Show field error
     */
    function showFieldError($field, message) {
        const $wrapper = $field.closest('.field-wrapper');
        if ($wrapper.length === 0) {
            $field.wrap('<div class="field-wrapper"></div>');
        }
        
        $field.closest('.field-wrapper').find('.field-error').remove();
        $field.after(`<div class="field-error text-danger small mt-1">${message}</div>`);
    }

    /**
     * Clear field error
     */
    function clearFieldError($field) {
        $field.closest('.field-wrapper').find('.field-error').remove();
    }

    /**
     * Validate color contrast
     */
    function validateColorContrast() {
        const bgColor = $('#id_background_color').val();
        const textColor = $('#id_text_color').val();
        
        if (bgColor && textColor && bgColor.toLowerCase() === textColor.toLowerCase()) {
            showColorContrastWarning();
        } else {
            clearColorContrastWarning();
        }
    }

    /**
     * Show color contrast warning
     */
    function showColorContrastWarning() {
        const $textColorField = $('#id_text_color');
        const $warning = $(`
            <div class="color-contrast-warning alert alert-warning alert-dismissible fade show mt-2" role="alert">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Background and text colors are the same. This will make text unreadable.
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        
        $textColorField.closest('.form-row').find('.color-contrast-warning').remove();
        $textColorField.closest('.form-row').append($warning);
    }

    /**
     * Clear color contrast warning
     */
    function clearColorContrastWarning() {
        $('.color-contrast-warning').remove();
    }

    /**
     * Initialize preview functionality
     */
    function initializePreviewFunctionality() {
        // Add preview panel if not exists
        if ($('#utility-bar-preview').length === 0) {
            $('body').append(`
                <div id="utility-bar-preview" class="utility-bar-preview-panel">
                    <div class="preview-header">
                        <h4>Utility Bar Preview</h4>
                        <button type="button" class="close-preview">&times;</button>
                    </div>
                    <div class="preview-content">
                        <div id="preview-utility-bar"></div>
                    </div>
                </div>
            `);
            
            $('.close-preview').on('click', function() {
                $('#utility-bar-preview').hide();
            });
        }

        // Live preview updates
        $('input, select').on('change input', debounce(updatePreview, 300));
    }

    /**
     * Update preview panel
     */
    function updatePreview() {
        const $preview = $('#preview-utility-bar');
        
        const config = {
            name: $('#id_name').val(),
            backgroundColor: $('#id_background_color').val(),
            textColor: $('#id_text_color').val(),
            height: $('#id_height').val() + 'px',
            position: $('#id_position').val(),
            showSocialIcons: $('#id_show_social_icons').is(':checked'),
            showContactInfo: $('#id_show_contact_info').is(':checked'),
            showCustomLinks: $('#id_show_custom_links').is(':checked'),
            showOnMobile: $('#id_show_on_mobile').is(':checked')
        };

        let previewHtml = `
            <div class="utility-bar-demo" style="
                background-color: ${config.backgroundColor}; 
                color: ${config.textColor}; 
                height: ${config.height};
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 20px;
                font-size: 14px;
            ">
        `;

        // Add social icons
        if (config.showSocialIcons) {
            previewHtml += `
                <div class="social-icons">
                    <i class="fab fa-facebook-f"></i>
                    <i class="fab fa-twitter"></i>
                    <i class="fab fa-instagram"></i>
                    <i class="fab fa-youtube"></i>
                    <i class="fab fa-linkedin"></i>
                </div>
            `;
        }

        // Add contact info
        if (config.showContactInfo) {
            const phone = $('#id_contact_phone').val();
            const email = $('#id_contact_email').val();
            
            previewHtml += `<div class="contact-info">`;
            if (phone) previewHtml += `<span><i class="fas fa-phone"></i> ${phone}</span>`;
            if (email) previewHtml += `<span><i class="fas fa-envelope"></i> ${email}</span>`;
            previewHtml += `</div>`;
        }

        // Add custom links
        if (config.showCustomLinks) {
            previewHtml += `<div class="custom-links">`;
            for (let i = 1; i <= 3; i++) {
                const text = $(`#id_custom_link_${i}_text`).val();
                if (text) {
                    previewHtml += `<a href="#">${text}</a>`;
                }
            }
            previewHtml += `</div>`;
        }

        previewHtml += '</div>';
        
        $preview.html(previewHtml);
    }

    /**
     * Preview utility bar (called from admin list)
     */
    window.previewUtilityBar = function(utilityBarId) {
        // Show preview panel
        $('#utility-bar-preview').show();
        
        // You could load actual data via AJAX here
        // For now, just show the preview panel
        updatePreview();
    };

    /**
     * Initialize tooltips
     */
    function initializeTooltips() {
        // Add tooltips to help icons
        $('[data-toggle="tooltip"]').each(function() {
            $(this).tooltip();
        });

        // Add info icons to complex fields
        const complexFields = [
            'background_color',
            'text_color', 
            'height',
            'custom_link_1_url',
            'custom_link_2_url', 
            'custom_link_3_url'
        ];

        complexFields.forEach(fieldName => {
            const $field = $(`#id_${fieldName}`);
            if ($field.length) {
                $field.after('<i class="fas fa-info-circle tooltip-trigger ml-2"></i>');
            }
        });
    }

    /**
     * Add form indicators
     */
    function addFormIndicators() {
        // Add progress indicator for form completion
        const $progressBar = $(`
            <div class="form-progress-wrapper">
                <div class="form-progress-bar">
                    <div class="progress-fill" style="width: 0%"></div>
                </div>
                <small class="progress-text">Form completion: 0%</small>
            </div>
        `);
        
        $('.top-utility-bar-form').prepend($progressBar);

        // Update progress on field changes
        $('input, select, textarea').on('input change', updateFormProgress);
        updateFormProgress(); // Initial calculation
    }

    /**
     * Update form completion progress
     */
    function updateFormProgress() {
        const totalFields = $('input[required], select[required], textarea[required]').length || $('input, select, textarea').not('[type="hidden"]').length;
        const completedFields = $('input, select, textarea').not('[type="hidden"]').filter(function() {
            return $(this).val() && $(this).val().trim() !== '';
        }).length;

        const percentage = totalFields > 0 ? Math.round((completedFields / totalFields) * 100) : 0;
        
        $('.progress-fill').css('width', percentage + '%');
        $('.progress-text').text(`Form completion: ${percentage}%`);
        
        // Color coding
        if (percentage < 30) {
            $('.progress-fill').css('background-color', '#dc3545');
        } else if (percentage < 70) {
            $('.progress-fill').css('background-color', '#ffc107');
        } else {
            $('.progress-fill').css('background-color', '#28a745');
        }
    }

    /**
     * Real-time URL validation
     */
    function validateURL(url, expectedDomain = null) {
        try {
            const urlObj = new URL(url);
            
            if (expectedDomain && !urlObj.hostname.includes(expectedDomain)) {
                return false;
            }
            
            return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
        } catch (e) {
            return false;
        }
    }

    /**
     * Initialize real-time validation for all fields
     */
    function initializeValidation() {
        // Social media URL validation
        const socialFields = {
            'facebook_url': 'facebook.com',
            'twitter_url': 'twitter.com',
            'instagram_url': 'instagram.com',
            'youtube_url': 'youtube.com',
            'linkedin_url': 'linkedin.com'
        };

        Object.entries(socialFields).forEach(([fieldName, domain]) => {
            $(`#id_${fieldName}`).on('blur', function() {
                const url = this.value.trim();
                if (url && !validateURL(url, domain)) {
                    $(this).addClass('is-invalid');
                    showFieldError($(this), `Please enter a valid ${domain} URL`);
                } else if (url) {
                    $(this).addClass('is-valid');
                    clearFieldError($(this));
                }
            });
        });

        // Form submission validation
        $('.utility-bar-admin-form').on('submit', function(e) {
            let isValid = true;
            
            // Check required fields if any feature is enabled
            if ($('#id_show_social_icons').is(':checked')) {
                const hasSocialUrl = Object.keys(socialFields).some(field => 
                    $(`#id_${field}`).val().trim()
                );
                
                if (!hasSocialUrl) {
                    isValid = false;
                    showFormError('Please provide at least one social media URL when social icons are enabled.');
                }
            }
            
            if ($('#id_show_contact_info').is(':checked')) {
                const hasContactInfo = $('#id_contact_phone').val().trim() || $('#id_contact_email').val().trim();
                
                if (!hasContactInfo) {
                    isValid = false;
                    showFormError('Please provide at least one contact method when contact info is enabled.');
                }
            }
            
            if (!isValid) {
                e.preventDefault();
                $('html, body').animate({
                    scrollTop: $('.form-error').first().offset().top - 100
                }, 500);
            }
        });
    }

    /**
     * Show form-level error
     */
    function showFormError(message) {
        $('.form-error').remove();
        $('.top-utility-bar-form').prepend(`
            <div class="form-error alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fas fa-exclamation-circle me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
    }

    /**
     * Debounce function for performance
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
     * Auto-save functionality (draft)
     */
    function initializeAutoSave() {
        let autoSaveTimeout;
        
        $('input, select, textarea').on('change', function() {
            clearTimeout(autoSaveTimeout);
            
            autoSaveTimeout = setTimeout(() => {
                saveDraft();
            }, 2000);
        });
    }

    /**
     * Save form as draft
     */
    function saveDraft() {
        const formData = $('.utility-bar-admin-form').serialize();
        
        // You could implement AJAX draft saving here
        console.log('Auto-saving draft...', formData);
        
        // Show save indicator
        showSaveIndicator('Draft saved');
    }

    /**
     * Show save indicator
     */
    function showSaveIndicator(message) {
        $('.save-indicator').remove();
        
        const $indicator = $(`
            <div class="save-indicator alert alert-success alert-dismissible fade show position-fixed" 
                 style="top: 20px; right: 20px; z-index: 9999; min-width: 250px;">
                <i class="fas fa-check-circle me-2"></i>
                ${message}
            </div>
        `);
        
        $('body').append($indicator);
        
        setTimeout(() => {
            $indicator.fadeOut(300, function() {
                $(this).remove();
            });
        }, 3000);
    }

    /**
     * Initialize keyboard shortcuts
     */
    function initializeKeyboardShortcuts() {
        $(document).on('keydown', function(e) {
            // Ctrl/Cmd + S to save
            if ((e.ctrlKey || e.metaKey) && e.keyCode === 83) {
                e.preventDefault();
                $('.utility-bar-admin-form').submit();
            }
            
            // Ctrl/Cmd + P to preview
            if ((e.ctrlKey || e.metaKey) && e.keyCode === 80) {
                e.preventDefault();
                $('#utility-bar-preview').toggle();
                updatePreview();
            }
        });
    }

    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();

})(django.jQuery || jQuery);
