// Menu Management Admin JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all menu admin functionality
    initMenuAdmin();
    
    function initMenuAdmin() {
        // Initialize color pickers
        initColorPickers();
        
        // Initialize quick toggles
        initQuickToggles();
        
        // Initialize menu tree visualization
        initMenuTree();
        
        // Initialize bulk actions
        initBulkActions();
        
        // Initialize form validation
        initFormValidation();
        
        // Initialize live preview
        initLivePreview();
    }
    
    // Color picker functionality
    function initColorPickers() {
        const colorInputs = document.querySelectorAll('input[type="color"]');
        
        colorInputs.forEach(input => {
            // Add color preview
            const preview = document.createElement('div');
            preview.className = 'color-preview';
            preview.style.cssText = `
                width: 20px;
                height: 20px;
                border-radius: 50%;
                border: 2px solid #fff;
                box-shadow: 0 0 0 1px #ddd;
                display: inline-block;
                margin-right: 8px;
                vertical-align: middle;
            `;
            
            // Insert preview before input
            input.parentNode.insertBefore(preview, input);
            
            // Update preview on change
            input.addEventListener('change', function() {
                preview.style.backgroundColor = this.value;
            });
            
            // Set initial preview
            preview.style.backgroundColor = input.value;
        });
    }
    
    // Enhanced checkbox and toggle functionality
    function initQuickToggles() {
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        
        checkboxes.forEach(checkbox => {
            // Find the parent form row or field container
            const container = findParentContainer(checkbox);
            if (!container) return;
            
            // Add enhanced styling
            addEnhancedStyling(checkbox, container);
            
            // Add change event
            checkbox.addEventListener('change', function() {
                updateCheckboxState(this);
                updateFormValidation(this);
            });
            
            // Set initial state
            updateCheckboxState(checkbox);
        });
    }
    
    function findParentContainer(checkbox) {
        // Look for common parent containers
        let container = checkbox.closest('.form-row, .field, .form-group, .checkbox-field');
        if (!container) {
            // Create a container if none exists
            container = document.createElement('div');
            container.className = 'enhanced-checkbox';
            checkbox.parentNode.insertBefore(container, checkbox);
            container.appendChild(checkbox);
        }
        return container;
    }
    
    function addEnhancedStyling(checkbox, container) {
        // Add enhanced checkbox class if not already present
        if (!container.classList.contains('enhanced-checkbox')) {
            container.classList.add('enhanced-checkbox');
        }
        
        // Ensure checkbox has a label
        let label = container.querySelector('label');
        if (!label) {
            // Create label if none exists
            label = document.createElement('label');
            label.textContent = checkbox.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            label.setAttribute('for', checkbox.id || checkbox.name);
            container.appendChild(label);
        }
        
        // Add status indicator
        if (!container.querySelector('.checkbox-status')) {
            const status = document.createElement('span');
            status.className = 'checkbox-status';
            label.appendChild(status);
        }
    }
    
    function updateCheckboxState(checkbox) {
        const container = checkbox.closest('.enhanced-checkbox');
        if (!container) return;
        
        const status = container.querySelector('.checkbox-status');
        if (status) {
            if (checkbox.checked) {
                status.style.backgroundColor = '#28a745';
                container.style.borderColor = '#28a745';
                container.style.backgroundColor = '#f8fff9';
            } else {
                status.style.backgroundColor = '#6c757d';
                container.style.borderColor = '#e9ecef';
                container.style.backgroundColor = 'white';
            }
        }
        
        // Update container classes
        if (checkbox.checked) {
            container.classList.add('checked');
        } else {
            container.classList.remove('checked');
        }
    }
    
    function updateFormValidation(checkbox) {
        // Add visual feedback for form validation
        const form = checkbox.closest('form');
        if (form) {
            form.classList.add('was-validated');
        }
    }
    
    // Menu tree visualization
    function initMenuTree() {
        const menuTree = document.querySelector('.menu-tree');
        if (!menuTree) return;
        
        // Add expand/collapse functionality
        const treeItems = menuTree.querySelectorAll('.menu-tree-item');
        
        treeItems.forEach(item => {
            const subitems = item.querySelectorAll('.menu-tree-subitem');
            if (subitems.length > 0) {
                // Add expand/collapse button
                const toggleBtn = document.createElement('button');
                toggleBtn.className = 'tree-toggle';
                toggleBtn.innerHTML = '<i class="fas fa-chevron-down"></i>';
                toggleBtn.style.cssText = `
                    background: none;
                    border: none;
                    color: #007bff;
                    cursor: pointer;
                    padding: 5px;
                    margin-right: 10px;
                `;
                
                item.insertBefore(toggleBtn, item.firstChild);
                
                // Add click event
                toggleBtn.addEventListener('click', function() {
                    const isExpanded = item.classList.contains('expanded');
                    if (isExpanded) {
                        item.classList.remove('expanded');
                        toggleBtn.innerHTML = '<i class="fas fa-chevron-down"></i>';
                        subitems.forEach(subitem => subitem.style.display = 'none');
                    } else {
                        item.classList.add('expanded');
                        toggleBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
                        subitems.forEach(subitem => subitem.style.display = 'block');
                    }
                });
                
                // Initially hide subitems
                subitems.forEach(subitem => subitem.style.display = 'none');
            }
        });
    }
    
    // Bulk actions functionality
    function initBulkActions() {
        const bulkForm = document.querySelector('form');
        if (!bulkForm) return;
        
        const actionSelect = bulkForm.querySelector('select[name="action"]');
        const selectedItems = bulkForm.querySelectorAll('input[name="selected_items"]');
        const executeBtn = bulkForm.querySelector('button[type="submit"]');
        
        if (actionSelect && executeBtn) {
            // Update execute button text based on action
            actionSelect.addEventListener('change', function() {
                const actionText = this.options[this.selectedIndex].text;
                executeBtn.innerHTML = `<i class="fas fa-cogs"></i>${actionText}`;
            });
            
            // Confirm destructive actions
            bulkForm.addEventListener('submit', function(e) {
                const action = actionSelect.value;
                const checkedItems = Array.from(selectedItems).filter(item => item.checked);
                
                if (checkedItems.length === 0) {
                    e.preventDefault();
                    alert('Please select at least one item to perform this action.');
                    return;
                }
                
                if (action === 'delete' || action.includes('deactivate')) {
                    if (!confirm(`Are you sure you want to ${action} ${checkedItems.length} selected item(s)? This action cannot be undone.`)) {
                        e.preventDefault();
                        return;
                    }
                }
            });
        }
        
        // Select all functionality
        const selectAllCheckbox = document.getElementById('select-all');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', function() {
                selectedItems.forEach(item => {
                    item.checked = this.checked;
                });
            });
        }
    }
    
    // Form validation
    function initFormValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Show validation errors
                    showValidationErrors(form);
                }
                
                form.classList.add('was-validated');
            });
        });
    }
    
    function showValidationErrors(form) {
        const invalidFields = form.querySelectorAll(':invalid');
        
        invalidFields.forEach(field => {
            // Add error styling
            field.classList.add('is-invalid');
            
            // Show error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            errorDiv.textContent = field.validationMessage;
            
            // Remove existing error message
            const existingError = field.parentNode.querySelector('.invalid-feedback');
            if (existingError) {
                existingError.remove();
            }
            
            field.parentNode.appendChild(errorDiv);
        });
    }
    
    // Live preview functionality
    function initLivePreview() {
        const previewContainer = document.querySelector('.menu-preview');
        if (!previewContainer) return;
        
        // Watch for changes in form fields
        const formFields = document.querySelectorAll('input, textarea, select');
        
        formFields.forEach(field => {
            field.addEventListener('input', function() {
                updateLivePreview(field);
            });
            
            field.addEventListener('change', function() {
                updateLivePreview(field);
            });
        });
    }
    
    function updateLivePreview(field) {
        const previewContainer = document.querySelector('.menu-preview');
        if (!previewContainer) return;
        
        const fieldName = field.name;
        const fieldValue = field.value;
        
        // Update preview based on field type
        if (fieldName.includes('name')) {
            const previewName = previewContainer.querySelector('.preview-name');
            if (previewName) {
                previewName.textContent = fieldValue || 'Menu Name';
            }
        }
        
        if (fieldName.includes('icon_class')) {
            const previewIcon = previewContainer.querySelector('.preview-icon');
            if (previewIcon) {
                previewIcon.className = fieldValue || 'fas fa-home';
            }
        }
        
        if (fieldName.includes('text_color')) {
            const previewText = previewContainer.querySelector('.preview-text');
            if (previewText) {
                previewText.style.color = fieldValue || '#374151';
            }
        }
        
        if (fieldName.includes('hover_color')) {
            const previewHover = previewContainer.querySelector('.preview-hover');
            if (previewHover) {
                previewHover.style.borderColor = fieldValue || '#1f2937';
            }
        }
    }
    
    // Enhanced table functionality
    function initEnhancedTable() {
        const tables = document.querySelectorAll('.results');
        
        tables.forEach(table => {
            // Add row highlighting
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                row.addEventListener('mouseenter', function() {
                    this.style.backgroundColor = '#f8f9fa';
                });
                
                row.addEventListener('mouseleave', function() {
                    this.style.backgroundColor = '';
                });
            });
            
            // Add sortable columns
            const headers = table.querySelectorAll('th.sortable');
            headers.forEach(header => {
                header.style.cursor = 'pointer';
                header.addEventListener('click', function() {
                    sortTable(table, Array.from(rows), this);
                });
            });
        });
    }
    
    function sortTable(table, rows, header) {
        const columnIndex = Array.from(header.parentNode.children).indexOf(header);
        const isAscending = header.classList.contains('asc');
        
        // Remove existing sort classes
        header.parentNode.querySelectorAll('th').forEach(th => {
            th.classList.remove('asc', 'desc');
        });
        
        // Add sort class
        header.classList.add(isAscending ? 'desc' : 'asc');
        
        // Sort rows
        rows.sort((a, b) => {
            const aValue = a.children[columnIndex].textContent.trim();
            const bValue = b.children[columnIndex].textContent.trim();
            
            if (isAscending) {
                return bValue.localeCompare(aValue);
            } else {
                return aValue.localeCompare(bValue);
            }
        });
        
        // Reorder rows
        const tbody = table.querySelector('tbody');
        rows.forEach(row => tbody.appendChild(row));
    }
    
    // Initialize enhanced table
    initEnhancedTable();
    
    // Enhanced checkbox functionality for active/inactive states
    createEnhancedCheckboxes();
    
    // Simple fallback initialization for existing checkboxes
    setTimeout(function() {
        const existingCheckboxes = document.querySelectorAll('.enhanced-checkbox input[type="checkbox"]');
        existingCheckboxes.forEach(checkbox => {
            if (!checkbox.hasAttribute('data-enhanced-initialized')) {
                const container = checkbox.closest('.enhanced-checkbox');
                if (container) {
                    initializeExistingCheckbox(checkbox, container);
                }
            }
        });
    }, 100);
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + S to save
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const saveBtn = document.querySelector('input[type="submit"], button[type="submit"]');
            if (saveBtn) {
                saveBtn.click();
            }
        }
        
        // Ctrl/Cmd + A to select all
        if ((e.ctrlKey || e.metaKey) && e.key === 'a') {
            const selectAllCheckbox = document.getElementById('select-all');
            if (selectAllCheckbox) {
                selectAllCheckbox.checked = !selectAllCheckbox.checked;
                selectAllCheckbox.dispatchEvent(new Event('change'));
            }
        }
    });
    
    // Create enhanced checkboxes for specific fields
    function createEnhancedCheckboxes() {
        // Find fields that should have enhanced styling
        const enhancedFields = document.querySelectorAll('input[name*="is_active"], input[name*="is_featured"], input[name*="show_"]');
        
        enhancedFields.forEach(field => {
            if (field.type === 'checkbox') {
                createEnhancedCheckbox(field);
            }
        });
        
        // Also find existing enhanced-checkbox containers and initialize them
        const existingContainers = document.querySelectorAll('.enhanced-checkbox');
        existingContainers.forEach(container => {
            const checkbox = container.querySelector('input[type="checkbox"]');
            if (checkbox) {
                initializeExistingCheckbox(checkbox, container);
            }
        });
    }
    
    function createEnhancedCheckbox(checkbox) {
        // Find or create container
        let container = checkbox.closest('.form-row, .field, .form-group, .enhanced-checkbox');
        if (!container) {
            container = document.createElement('div');
            container.className = 'enhanced-checkbox compact';
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
                status.style.backgroundColor = '#28a745';
            }
            
            if (statusText) {
                statusText.textContent = 'Active';
                statusText.style.backgroundColor = '#28a745';
            }
        } else {
            // Inactive state
            container.classList.remove('active');
            container.classList.add('inactive');
            
            if (status) {
                status.style.backgroundColor = '#dc3545';
            }
            
            if (statusText) {
                statusText.textContent = 'Inactive';
                statusText.style.backgroundColor = '#dc3545';
            }
        }
        
        // Update container classes
        if (checkbox.checked) {
            container.classList.add('checked');
        } else {
            container.classList.remove('checked');
        }
    }
    
    // Add tooltips
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'custom-tooltip';
            tooltip.textContent = this.title;
            tooltip.style.cssText = `
                position: absolute;
                background: #333;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 1000;
                pointer-events: none;
                white-space: nowrap;
            `;
            
            document.body.appendChild(tooltip);
            
            // Position tooltip
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
    
    // Auto-save functionality for long forms
    let autoSaveTimer;
    const longForms = document.querySelectorAll('form');
    
    longForms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                clearTimeout(autoSaveTimer);
                autoSaveTimer = setTimeout(() => {
                    // Show auto-save indicator
                    showAutoSaveIndicator();
                }, 2000);
            });
        });
    });
    
    function showAutoSaveIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'auto-save-indicator';
        indicator.textContent = 'Auto-saving...';
        indicator.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 10px 20px;
            border-radius: 4px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(indicator);
        
        // Remove after 3 seconds
        setTimeout(() => {
            indicator.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => indicator.remove(), 300);
        }, 3000);
    }
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
});
