/**
 * Hero Banner Admin Interface Enhancement
 * Provides dynamic field visibility and real-time preview functionality
 */

document.addEventListener('DOMContentLoaded', function() {
<<<<<<< HEAD
    const heroBannerForm = document.querySelector('.hero-banner-admin form');
=======
    // Look for hero banner admin form in Django admin
    const heroBannerForm = document.querySelector('#herobanner_form, .hero-banner-admin form, form[action*="herobanner"]');
>>>>>>> a11168e (Fix)
    if (!heroBannerForm) return;

    // Initialize the interface
    initHeroBannerAdmin();
});

function initHeroBannerAdmin() {
<<<<<<< HEAD
    // Get form elements
    const backgroundTypeSelect = document.getElementById('background-type-select');
=======
    // Get form elements - try multiple selectors for Django admin
    const backgroundTypeSelect = document.getElementById('background-type-select') || 
                                document.querySelector('select[name="background_type"]');
>>>>>>> a11168e (Fix)
    const gradientFields = document.querySelector('.gradient-fields');
    const solidFields = document.querySelector('.solid-fields');
    const imageFields = document.querySelector('.image-fields');
    const videoFields = document.querySelector('.video-fields');
    
    // Initialize field visibility
    if (backgroundTypeSelect) {
        updateFieldVisibility(backgroundTypeSelect.value);
        
        // Add change event listener
        backgroundTypeSelect.addEventListener('change', function() {
            updateFieldVisibility(this.value);
        });
    }
    
    // Initialize color pickers
    initColorPickers();
    
    // Initialize opacity slider
    initOpacitySlider();
    
    // Initialize real-time preview
    initRealTimePreview();
    
    // Initialize form validation
    initFormValidation();
}

function updateFieldVisibility(backgroundType) {
    const gradientFields = document.querySelector('.gradient-fields');
    const solidFields = document.querySelector('.solid-fields');
    const imageFields = document.querySelector('.image-fields');
    const videoFields = document.querySelector('.video-fields');
    
    // Hide all background type specific fields
    [gradientFields, solidFields, imageFields, videoFields].forEach(field => {
        if (field) {
            field.style.display = 'none';
        }
    });
    
    // Show relevant fields based on background type
    switch (backgroundType) {
        case 'gradient':
            if (gradientFields) gradientFields.style.display = 'block';
            break;
        case 'solid':
            if (solidFields) solidFields.style.display = 'block';
            break;
        case 'image':
            if (imageFields) imageFields.style.display = 'block';
            break;
        case 'video':
            if (videoFields) videoFields.style.display = 'block';
            break;
    }
}

function initColorPickers() {
    const colorPickers = document.querySelectorAll('.color-picker');
    
    colorPickers.forEach(picker => {
        // Add color preview
        const preview = document.createElement('div');
        preview.className = 'color-preview';
        preview.style.cssText = `
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 2px solid #fff;
            box-shadow: 0 0 0 1px #d1d5da;
            display: inline-block;
            margin-left: 10px;
            vertical-align: middle;
        `;
        
        picker.parentNode.appendChild(preview);
        
        // Update preview on change
        picker.addEventListener('change', function() {
            preview.style.backgroundColor = this.value;
        });
        
        // Set initial preview
        preview.style.backgroundColor = picker.value;
    });
}

function initOpacitySlider() {
    const opacitySlider = document.querySelector('input[name="background_image_opacity"]');
    if (!opacitySlider) return;
    
    // Create opacity display
    const opacityDisplay = document.createElement('span');
    opacityDisplay.className = 'opacity-display';
    opacityDisplay.textContent = opacitySlider.value + '%';
    
    opacitySlider.parentNode.appendChild(opacityDisplay);
    
    // Update display on change
    opacitySlider.addEventListener('input', function() {
        opacityDisplay.textContent = this.value + '%';
    });
}

function initRealTimePreview() {
    const previewContainer = createPreviewContainer();
    if (!previewContainer) return;
    
<<<<<<< HEAD
    // Add preview after the form
    const form = document.querySelector('.hero-banner-admin form');
=======
    // Add preview after the form - try multiple selectors
    const form = document.querySelector('.hero-banner-admin form') || 
                 document.querySelector('#herobanner_form') ||
                 document.querySelector('form[action*="herobanner"]');
>>>>>>> a11168e (Fix)
    if (form) {
        form.parentNode.insertBefore(previewContainer, form.nextSibling);
    }
    
    // Add preview update listeners
    addPreviewListeners(previewContainer);
}

function createPreviewContainer() {
    const container = document.createElement('div');
    container.className = 'hero-banner-preview';
    container.innerHTML = `
        <h4>Live Preview</h4>
        <div id="hero-preview" style="
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
            padding: 40px 20px;
            border-radius: 8px;
            position: relative;
            overflow: hidden;
        ">
            <h1 id="preview-title" style="margin-bottom: 20px; font-size: 2.5rem; font-weight: bold;">
                Sample Title
            </h1>
            <p id="preview-subtitle" style="margin-bottom: 30px; font-size: 1.2rem; opacity: 0.9;">
                Sample subtitle text goes here
            </p>
            <div id="preview-buttons" style="display: flex; gap: 15px; flex-wrap: wrap; justify-content: center;">
                <button id="preview-primary-btn" style="
                    padding: 12px 24px;
                    border: none;
                    border-radius: 6px;
                    font-weight: 600;
                    cursor: pointer;
                ">Primary Button</button>
                <button id="preview-secondary-btn" style="
                    padding: 12px 24px;
                    border: 2px solid;
                    border-radius: 6px;
                    font-weight: 600;
                    cursor: pointer;
                    background: transparent;
                ">Secondary Button</button>
            </div>
        </div>
    `;
    
    return container;
}

function addPreviewListeners(previewContainer) {
<<<<<<< HEAD
    const form = document.querySelector('.hero-banner-admin form');
=======
    const form = document.querySelector('.hero-banner-admin form') || 
                 document.querySelector('#herobanner_form') ||
                 document.querySelector('form[action*="herobanner"]');
>>>>>>> a11168e (Fix)
    if (!form) return;
    
    // Title preview
    const titleInput = form.querySelector('input[name="title"]');
    const previewTitle = previewContainer.querySelector('#preview-title');
    if (titleInput && previewTitle) {
        titleInput.addEventListener('input', function() {
            previewTitle.textContent = this.value || 'Sample Title';
        });
    }
    
    // Subtitle preview
    const subtitleInput = form.querySelector('textarea[name="subtitle"]');
    const previewSubtitle = previewContainer.querySelector('#preview-subtitle');
    if (subtitleInput && previewSubtitle) {
        subtitleInput.addEventListener('input', function() {
            previewSubtitle.textContent = this.value || 'Sample subtitle text goes here';
        });
    }
    
    // Button text preview
    const primaryBtnText = form.querySelector('input[name="primary_button_text"]');
    const previewPrimaryBtn = previewContainer.querySelector('#preview-primary-btn');
    if (primaryBtnText && previewPrimaryBtn) {
        primaryBtnText.addEventListener('input', function() {
            previewPrimaryBtn.textContent = this.value || 'Primary Button';
        });
    }
    
    const secondaryBtnText = form.querySelector('input[name="secondary_button_text"]');
    const previewSecondaryBtn = previewContainer.querySelector('#preview-secondary-btn');
    if (secondaryBtnText && previewSecondaryBtn) {
        secondaryBtnText.addEventListener('input', function() {
            previewSecondaryBtn.textContent = this.value || 'Secondary Button';
        });
    }
    
    // Color previews
    const titleColor = form.querySelector('input[name="title_color"]');
    if (titleColor && previewTitle) {
        titleColor.addEventListener('change', function() {
            previewTitle.style.color = this.value;
        });
    }
    
    const subtitleColor = form.querySelector('input[name="subtitle_color"]');
    if (subtitleColor && previewSubtitle) {
        subtitleColor.addEventListener('change', function() {
            previewSubtitle.style.color = this.value;
        });
    }
    
    const primaryBtnBgColor = form.querySelector('input[name="primary_button_bg_color"]');
    if (primaryBtnBgColor && previewPrimaryBtn) {
        primaryBtnBgColor.addEventListener('change', function() {
            previewPrimaryBtn.style.backgroundColor = this.value;
        });
    }
    
    const primaryBtnTextColor = form.querySelector('input[name="primary_button_text_color"]');
    if (primaryBtnTextColor && previewPrimaryBtn) {
        primaryBtnTextColor.addEventListener('change', function() {
            previewPrimaryBtn.style.color = this.value;
        });
    }
    
    const secondaryBtnBgColor = form.querySelector('input[name="secondary_button_bg_color"]');
    if (secondaryBtnBgColor && previewSecondaryBtn) {
        secondaryBtnBgColor.addEventListener('change', function() {
            previewSecondaryBtn.style.backgroundColor = this.value;
        });
    }
    
    const secondaryBtnTextColor = form.querySelector('input[name="secondary_button_text_color"]');
    if (secondaryBtnTextColor && previewSecondaryBtn) {
        secondaryBtnTextColor.addEventListener('change', function() {
            previewSecondaryBtn.style.color = this.value;
        });
    }
    
    const secondaryBtnBorderColor = form.querySelector('input[name="secondary_button_border_color"]');
    if (secondaryBtnBorderColor && previewSecondaryBtn) {
        secondaryBtnBorderColor.addEventListener('change', function() {
            previewSecondaryBtn.style.borderColor = this.value;
        });
    }
    
    // Background preview
    const backgroundType = form.querySelector('select[name="background_type"]');
    if (backgroundType) {
        backgroundType.addEventListener('change', function() {
            updatePreviewBackground(this.value, previewContainer);
        });
    }
    
    // Font previews
    const titleFontFamily = form.querySelector('select[name="title_font_family"]');
    if (titleFontFamily && previewTitle) {
        titleFontFamily.addEventListener('change', function() {
            previewTitle.style.fontFamily = this.value;
        });
    }
    
    const titleFontSize = form.querySelector('select[name="title_font_size"]');
    if (titleFontSize && previewTitle) {
        titleFontSize.addEventListener('change', function() {
            const sizeMap = {
                'text-4xl': '2rem',
                'text-5xl': '3rem',
                'text-6xl': '3.75rem',
                'text-7xl': '4.5rem',
                'text-8xl': '6rem'
            };
            previewTitle.style.fontSize = sizeMap[this.value] || '3.75rem';
        });
    }
    
    const titleFontWeight = form.querySelector('select[name="title_font_weight"]');
    if (titleFontWeight && previewTitle) {
        titleFontWeight.addEventListener('change', function() {
            const weightMap = {
                'font-light': '300',
                'font-normal': '400',
                'font-medium': '500',
                'font-semibold': '600',
                'font-bold': '700',
                'font-extrabold': '800'
            };
            previewTitle.style.fontWeight = weightMap[this.value] || '700';
        });
    }
}

function updatePreviewBackground(backgroundType, previewContainer) {
    const preview = previewContainer.querySelector('#hero-preview');
    if (!preview) return;
    
    switch (backgroundType) {
        case 'gradient':
            const startColor = document.querySelector('input[name="gradient_start_color"]')?.value || '#1e3a8a';
            const endColor = document.querySelector('input[name="gradient_end_color"]')?.value || '#7c3aed';
            const direction = document.querySelector('select[name="gradient_direction"]')?.value || '135deg';
            preview.style.background = `linear-gradient(${direction}, ${startColor}, ${endColor})`;
            break;
            
        case 'solid':
            const solidColor = document.querySelector('input[name="solid_background_color"]')?.value || '#1e3a8a';
            preview.style.background = solidColor;
            break;
            
        case 'image':
            const imageInput = document.querySelector('input[name="background_image"]');
            if (imageInput && imageInput.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.style.backgroundImage = `url(${e.target.result})`;
                    preview.style.backgroundSize = 'cover';
                    preview.style.backgroundPosition = 'center';
                };
                reader.readAsDataURL(imageInput.files[0]);
            }
            break;
            
        case 'video':
            preview.style.background = '#1e3a8a';
            // Add video preview placeholder
            preview.innerHTML += '<div style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px;">🎥 Video Background</div>';
            break;
    }
}

function initFormValidation() {
<<<<<<< HEAD
    const form = document.querySelector('.hero-banner-admin form');
=======
    const form = document.querySelector('.hero-banner-admin form') || 
                 document.querySelector('#herobanner_form') ||
                 document.querySelector('form[action*="herobanner"]');
>>>>>>> a11168e (Fix)
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            showValidationErrors();
        }
    });
}

function validateForm() {
    let isValid = true;
<<<<<<< HEAD
    const form = document.querySelector('.hero-banner-admin form');
=======
    const form = document.querySelector('.hero-banner-admin form') || 
                 document.querySelector('#herobanner_form') ||
                 document.querySelector('form[action*="herobanner"]');
>>>>>>> a11168e (Fix)
    
    // Clear previous validation
    clearValidationErrors();
    
    // Required field validation
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            markFieldAsError(field, 'This field is required');
            isValid = false;
        }
    });
    
    // Background type specific validation
    const backgroundType = form.querySelector('select[name="background_type"]')?.value;
    
    if (backgroundType === 'gradient') {
        const startColor = form.querySelector('input[name="gradient_start_color"]');
        const endColor = form.querySelector('input[name="gradient_end_color"]');
        
        if (!startColor.value || !endColor.value) {
            markFieldAsError(startColor, 'Gradient colors are required');
            markFieldAsError(endColor, 'Gradient colors are required');
            isValid = false;
        }
    }
    
    if (backgroundType === 'image') {
        const imageInput = form.querySelector('input[name="background_image"]');
        if (!imageInput.files[0]) {
            markFieldAsError(imageInput, 'Background image is required');
            isValid = false;
        }
    }
    
    if (backgroundType === 'video') {
        const videoUrl = form.querySelector('input[name="background_video_url"]');
        if (!videoUrl.value.trim()) {
            markFieldAsError(videoUrl, 'Video URL is required');
            isValid = false;
        }
    }
    
    // Button validation
    const primaryBtnText = form.querySelector('input[name="primary_button_text"]');
    const primaryBtnUrl = form.querySelector('input[name="primary_button_url"]');
    
    if (primaryBtnText.value.trim() && !primaryBtnUrl.value.trim()) {
        markFieldAsError(primaryBtnUrl, 'Primary button URL is required when button text is provided');
        isValid = false;
    }
    
    const secondaryBtnText = form.querySelector('input[name="secondary_button_text"]');
    const secondaryBtnUrl = form.querySelector('input[name="secondary_button_url"]');
    
    if (secondaryBtnText.value.trim() && !secondaryBtnUrl.value.trim()) {
        markFieldAsError(secondaryBtnUrl, 'Secondary button URL is required when button text is provided');
        isValid = false;
    }
    
    return isValid;
}

function markFieldAsError(field, message) {
    if (!field) return;
    
    field.classList.add('field-error');
    
    // Create error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    // Insert after field
    field.parentNode.insertBefore(errorDiv, field.nextSibling);
}

function clearValidationErrors() {
    // Remove error classes
    document.querySelectorAll('.field-error').forEach(field => {
        field.classList.remove('field-error');
    });
    
    // Remove error messages
    document.querySelectorAll('.error-message').forEach(msg => {
        msg.remove();
    });
}

function showValidationErrors() {
    // Scroll to first error
    const firstError = document.querySelector('.field-error');
    if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    // Show alert
    alert('Please fix the validation errors before submitting the form.');
}

// Add utility functions
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

// Export functions for global access
window.HeroBannerAdmin = {
    init: initHeroBannerAdmin,
    updateFieldVisibility: updateFieldVisibility,
    validateForm: validateForm
};
