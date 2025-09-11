/**
 * Enhanced Checkboxes - Standalone Script
 * This script provides enhanced checkbox functionality for active/inactive states
 */

(function() {
    'use strict';
    
    // Initialize enhanced checkboxes
    function initEnhancedCheckboxes() {
        // Find existing enhanced-checkbox containers and initialize them
        const existingContainers = document.querySelectorAll('.enhanced-checkbox');
        existingContainers.forEach(container => {
            const checkbox = container.querySelector('input[type="checkbox"]');
            if (checkbox) {
                initializeExistingCheckbox(checkbox, container);
            }
        });
        
        // Find fields that should have enhanced styling
        const enhancedFields = document.querySelectorAll('input[name*="is_active"], input[name*="is_featured"], input[name*="show_"]');
        enhancedFields.forEach(field => {
            if (field.type === 'checkbox') {
                createEnhancedCheckbox(field);
            }
        });
    }
    
    function createEnhancedCheckbox(checkbox) {
        // Find or create container
        let container = checkbox.closest('.form-row, .field, .form-group, .enhanced-checkbox');
        if (!container) {
            container = document.createElement('div');
            container.className = 'enhanced-checkbox admin-compact';
            checkbox.parentNode.insertBefore(container, checkbox);
            container.appendChild(checkbox);
        }
        
        // Add enhanced checkbox class if not already present
        if (!container.classList.contains('enhanced-checkbox')) {
            container.classList.add('enhanced-checkbox', 'admin-compact');
        }
        
        // Ensure checkbox has a label
        let label = container.querySelector('label');
        if (!label) {
            // Create label if none exists
            label = document.createElement('label');
            label.textContent = getFieldDisplayName(checkbox.name);
            label.setAttribute('for', checkbox.id || checkbox.name);
            container.appendChild(label);
        }
        
        // Add status indicator
        if (!container.querySelector('.checkbox-status')) {
            const status = document.createElement('span');
            status.className = 'checkbox-status';
            label.appendChild(status);
        }
        
        // Add status text
        if (!container.querySelector('.status-text')) {
            const statusText = document.createElement('span');
            statusText.className = 'status-text';
            statusText.textContent = checkbox.checked ? 'Active' : 'Inactive';
            label.appendChild(statusText);
        }
        
        // Add change event
        checkbox.addEventListener('change', function() {
            updateEnhancedCheckbox(this);
        });
        
        // Set initial state
        updateEnhancedCheckbox(checkbox);
    }
    
    function initializeExistingCheckbox(checkbox, container) {
        // Ensure status elements exist
        let label = container.querySelector('label');
        if (!label) return;
        
        // Add status indicator if missing
        if (!container.querySelector('.checkbox-status')) {
            const status = document.createElement('span');
            status.className = 'checkbox-status';
            label.appendChild(status);
        }
        
        // Add status text if missing
        if (!container.querySelector('.status-text')) {
            const statusText = document.createElement('span');
            statusText.className = 'status-text';
            statusText.textContent = checkbox.checked ? 'Active' : 'Inactive';
            label.appendChild(statusText);
        }
        
        // Add change event if not already added
        if (!checkbox.hasAttribute('data-enhanced-initialized')) {
            checkbox.addEventListener('change', function() {
                updateEnhancedCheckbox(this);
            });
            checkbox.setAttribute('data-enhanced-initialized', 'true');
        }
        
        // Set initial state
        updateEnhancedCheckbox(checkbox);
    }
    
    function getFieldDisplayName(fieldName) {
        // Convert field name to display name
        const nameMap = {
            'is_active': 'Active Status',
            'is_featured': 'Featured Item',
            'show_research_menu': 'Show Research Menu',
            'show_placement_menu': 'Show Placement Menu',
            'show_alumni_menu': 'Show Alumni Menu',
            'show_events_menu': 'Show Events Menu',
            'show_exam_timetable': 'Show Exam Timetable',
            'show_exam_revaluation': 'Show Exam Revaluation',
            'show_exam_question_papers': 'Show Question Papers',
            'show_exam_rules': 'Show Exam Rules',
            'show_student_portal': 'Show Student Portal',
            'show_sports_cultural': 'Show Sports & Cultural',
            'show_nss_ncc': 'Show NSS & NCC',
            'show_research_centers': 'Show Research Centers',
            'show_publications': 'Show Publications',
            'show_patents_projects': 'Show Patents & Projects'
        };
        
        return nameMap[fieldName] || fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
    
    function updateEnhancedCheckbox(checkbox) {
        const container = checkbox.closest('.enhanced-checkbox');
        if (!container) return;
        
        const status = container.querySelector('.checkbox-status');
        const statusText = container.querySelector('.status-text');
        
        if (checkbox.checked) {
            // Active state
            container.classList.remove('inactive');
            container.classList.add('active');
            
            if (status) {
                status.style.backgroundColor = '#007bff';
            }
            
            if (statusText) {
                statusText.textContent = 'Active';
                statusText.style.backgroundColor = '#007bff';
            }
        } else {
            // Inactive state
            container.classList.remove('active');
            container.classList.add('inactive');
            
            if (status) {
                status.style.backgroundColor = '#6c757d';
            }
            
            if (statusText) {
                statusText.textContent = 'Inactive';
                statusText.style.backgroundColor = '#6c757d';
            }
        }
        
        // Update container classes
        if (checkbox.checked) {
            container.classList.add('checked');
        } else {
            container.classList.remove('checked');
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initEnhancedCheckboxes);
    } else {
        initEnhancedCheckboxes();
    }
    
    // Also initialize after a short delay to catch any dynamically added elements
    setTimeout(initEnhancedCheckboxes, 100);
    
    // Make functions globally available
    window.initEnhancedCheckboxes = initEnhancedCheckboxes;
    window.createEnhancedCheckbox = createEnhancedCheckbox;
    window.updateEnhancedCheckbox = updateEnhancedCheckbox;
    
})();
