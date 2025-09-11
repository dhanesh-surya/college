# Navbar Configuration System

## Overview

The Navbar Configuration System allows you to dynamically manage all aspects of your website's navigation bar through Django's admin interface. This system provides comprehensive control over navbar appearance, behavior, and responsiveness.

## Features

### 🎨 **Visual Customization**
- **Colors**: Background, text, hover, and border colors
- **Typography**: Font sizes, line heights, and brand styling
- **Spacing**: Padding, margins, and gaps between elements
- **Dimensions**: Navbar height, logo size, and border radius
- **Shadows**: Custom box shadows and visual effects

### 📱 **Responsive Design**
- **Breakpoints**: Customizable mobile and tablet breakpoints
- **Mobile Settings**: Separate configuration for mobile devices
- **Adaptive Sizing**: Auto-adjusting font sizes and spacing
- **Touch Optimization**: Mobile-friendly interactions

### 🎯 **Advanced Features**
- **Mega Menu**: Configurable multi-column dropdown menus
- **Animation**: Customizable transitions and hover effects
- **Search**: Optional search functionality with custom placeholder
- **Sticky Navigation**: Option to make navbar stick to top
- **Logo Management**: Upload and configure brand logos

## Quick Start

### 1. Access Navbar Configuration

**Option A: Django Admin Interface**
```
http://127.0.0.1:8000/admin/college_website/navbarinfo/
```

**Option B: Custom Configuration Page**
```
http://127.0.0.1:8000/admin/navbar-config/
```

### 2. Create Default Configuration

If no configuration exists, run:
```bash
python manage.py create_default_navbar_config
```

### 3. Configure Your Navbar

1. Navigate to the navbar configuration page
2. Adjust settings in organized sections:
   - **Brand Information**: Name, subtitle, logo
   - **Dimensions & Spacing**: Size and spacing controls
   - **Typography**: Font settings and line heights
   - **Colors & Styling**: Color scheme and visual effects
   - **Navigation Behavior**: Sticky, search, positioning
   - **Mobile Settings**: Mobile-specific configurations
   - **Dropdown & Mega Menu**: Submenu configurations
   - **Animation & Effects**: Transitions and hover effects

## Configuration Sections

### 🏢 Brand Information
- **Brand Name**: Main college/institution name
- **Brand Subtitle**: Secondary text or affiliation
- **Logo**: Upload institution logo
- **Show Logo**: Toggle logo visibility
- **Show Brand Text**: Toggle text visibility

### 📏 Navbar Dimensions & Spacing
- **Navbar Height**: Overall navbar height (20-100px)
- **Padding**: Top, bottom, and horizontal padding
- **Menu Item Spacing**: Vertical and horizontal padding
- **Margins**: Spacing between menu items
- **Border Radius**: Rounded corners for menu items

### 🔤 Typography & Logo
- **Brand Font Size**: Institution name font size
- **Menu Font Size**: Navigation menu font size
- **Line Height**: Text line spacing
- **Logo Height**: Logo dimensions

### 🎨 Colors & Styling
- **Background Color**: Navbar background
- **Text Color**: Menu item text color
- **Hover Color**: Hover state color
- **Border Color**: Border and divider colors
- **Box Shadow**: Drop shadow effects
- **Border Radius**: Overall navbar rounding

### 📱 Responsive Breakpoints
- **Mobile Breakpoint**: Screen width for mobile layout (default: 992px)
- **Tablet Breakpoint**: Screen width for tablet layout (default: 768px)

### 📱 Mobile Settings
- **Mobile Navbar Height**: Height for mobile devices
- **Mobile Padding**: Horizontal padding for mobile
- **Mobile Font Sizes**: Separate font sizes for mobile
- **Mobile Logo Height**: Logo size for mobile devices

### 📋 Dropdown & Mega Menu
- **Dropdown Padding**: Spacing inside dropdown menus
- **Dropdown Item Spacing**: Individual item padding
- **Dropdown Font Size**: Text size in dropdowns
- **Mega Menu Columns**: Number of columns (1-6)
- **Mega Menu Width**: Width control (auto, 100%, custom)

### ⚡ Animation & Effects
- **Transition Duration**: Animation speed (0.1-2 seconds)
- **Hover Scale**: Scale effect on hover (1-1.5x)

### ⚙️ Navigation Behavior
- **Sticky Navigation**: Make navbar stick to top
- **Show Below Header**: Position relative to header
- **Enable Search**: Toggle search functionality
- **Search Placeholder**: Custom search placeholder text

## Template Usage

### Using Context Variables

The navbar configuration is automatically available in all templates through context processors:

```html
<!-- Access navbar configuration -->
{{ navbar_config.brand_name }}
{{ navbar_config.navbar_height }}
{{ navbar_config.menu_font_size }}

<!-- Use CSS variables -->
<style>
.navbar {
    height: var(--navbar-height);
    padding: var(--navbar-padding-top) var(--navbar-padding-horizontal);
    background-color: var(--navbar-background-color);
    color: var(--navbar-text-color);
}
</style>
```

### Using Template Tags

Load and use the navbar template tags:

```html
{% load navbar_tags %}

<!-- Generate CSS variables -->
{% navbar_css_vars %}

<!-- Get specific values -->
{% navbar_brand_name %}
{% navbar_config_value 'menu_font_size' %}
{% navbar_logo %}
{% navbar_show_logo %}
```

## API Reference

### Model: NavbarInfo

```python
from college_website.models import NavbarInfo

# Get active configuration
config = NavbarInfo.objects.filter(is_active=True).first()

# Access configuration values
height = config.navbar_height
font_size = config.menu_font_size
background_color = config.navbar_background_color
```

### Form: NavbarInfoForm

```python
from college_website.forms import NavbarInfoForm

# Create form instance
form = NavbarInfoForm(instance=navbar_config)

# Validate and save
if form.is_valid():
    form.save()
```

### Context Processor: navbar_config_context

Automatically provides:
- `navbar_config`: NavbarInfo instance
- `navbar_css_vars`: Dictionary of CSS variables

## Advanced Usage

### Custom CSS Integration

Use the generated CSS variables in your stylesheets:

```css
/* Custom navbar styling using configuration */
.navbar {
    height: var(--navbar-height);
    background: linear-gradient(135deg, var(--navbar-background-color), var(--navbar-hover-color));
    padding: var(--navbar-padding-top) var(--navbar-padding-horizontal);
    box-shadow: var(--box-shadow);
    border-radius: var(--border-radius);
}

.navbar .nav-link {
    padding: var(--menu-item-padding-vertical) var(--menu-item-padding-horizontal);
    margin: var(--menu-item-margin);
    font-size: var(--menu-font-size);
    line-height: var(--menu-line-height);
    border-radius: var(--menu-item-border-radius);
    transition: all var(--transition-duration) ease;
}

.navbar .nav-link:hover {
    transform: scale(var(--hover-scale));
    color: var(--navbar-hover-color);
}

/* Responsive design */
@media (max-width: var(--mobile-breakpoint)) {
    .navbar {
        height: var(--mobile-navbar-height);
        padding: 0 var(--mobile-padding-horizontal);
    }
    
    .navbar .nav-link {
        font-size: var(--mobile-menu-font-size);
    }
    
    .navbar-brand {
        font-size: var(--mobile-brand-font-size);
    }
    
    .navbar-brand img {
        height: var(--mobile-logo-height);
    }
}
```

### JavaScript Integration

Access configuration values in JavaScript:

```javascript
// Get configuration from template
const navbarConfig = {
    height: {{ navbar_config.navbar_height }},
    fontSize: {{ navbar_config.menu_font_size }},
    transitionDuration: {{ navbar_config.transition_duration }},
    hoverScale: {{ navbar_config.hover_scale }},
    mobileBreakpoint: {{ navbar_config.mobile_breakpoint }}
};

// Apply dynamic styling
document.documentElement.style.setProperty('--navbar-height', navbarConfig.height + 'px');
document.documentElement.style.setProperty('--menu-font-size', navbarConfig.fontSize + 'rem');
```

## Management Commands

### Create Default Configuration
```bash
python manage.py create_default_navbar_config
```

This command creates a default navbar configuration with optimal settings for a college website.

## Best Practices

### 🎯 **Design Guidelines**
1. **Consistency**: Use consistent spacing and typography
2. **Accessibility**: Ensure sufficient color contrast
3. **Performance**: Keep animations smooth but not excessive
4. **Responsiveness**: Test on multiple device sizes

### 📱 **Mobile Optimization**
1. **Touch Targets**: Ensure menu items are large enough for touch
2. **Readability**: Use appropriate font sizes for mobile
3. **Performance**: Optimize for mobile performance
4. **Usability**: Keep mobile navigation simple and intuitive

### 🎨 **Visual Design**
1. **Brand Alignment**: Match navbar colors with brand identity
2. **Visual Hierarchy**: Use typography to create clear hierarchy
3. **Spacing**: Maintain consistent spacing throughout
4. **Shadows**: Use subtle shadows for depth without distraction

## Troubleshooting

### Common Issues

**Configuration Not Applied**
- Check if `navbar_config_context` is in `TEMPLATES['OPTIONS']['context_processors']`
- Verify that a NavbarInfo instance exists with `is_active=True`

**CSS Variables Not Working**
- Ensure CSS variables are generated using `{% navbar_css_vars %}`
- Check browser developer tools for CSS variable values

**Mobile Layout Issues**
- Verify mobile breakpoints are set correctly
- Check mobile-specific configuration values
- Test responsive design on actual devices

**Form Validation Errors**
- Check field constraints in the model
- Verify form validation rules
- Ensure proper data types for numeric fields

### Debug Mode

Enable debug mode to see configuration values:

```python
# In Django settings
DEBUG = True

# In template
{% if debug %}
    <pre>{{ navbar_config|pprint }}</pre>
{% endif %}
```

## Support

For additional support or customization requests:

1. Check the Django admin interface for configuration options
2. Review the model fields and form validation rules
3. Test changes in a development environment first
4. Use browser developer tools to inspect CSS variables

## Version History

- **v1.0**: Initial navbar configuration system
- **v1.1**: Added responsive breakpoints and mobile settings
- **v1.2**: Enhanced mega menu configuration
- **v1.3**: Added animation and effects controls
- **v1.4**: Improved template tags and context processors

---

**Note**: This system is designed to work seamlessly with the existing college website structure. All configurations are automatically applied to the navbar without requiring code changes.
