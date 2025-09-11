from django import template
from django.utils.safestring import mark_safe
from ..models import NavbarInfo

register = template.Library()

@register.simple_tag
def navbar_css_vars():
    """Generate CSS custom properties for navbar configuration"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    
    if not navbar_config:
        return ""
    
    css_vars = f"""
    :root {{
        --navbar-height: {navbar_config.navbar_height}px;
        --navbar-padding-top: {navbar_config.navbar_padding_top}rem;
        --navbar-padding-bottom: {navbar_config.navbar_padding_bottom}rem;
        --navbar-padding-horizontal: {navbar_config.navbar_padding_horizontal}rem;
        --menu-item-padding-vertical: {navbar_config.menu_item_padding_vertical}rem;
        --menu-item-padding-horizontal: {navbar_config.menu_item_padding_horizontal}rem;
        --menu-item-margin: {navbar_config.menu_item_margin}rem;
        --menu-item-gap: {navbar_config.menu_item_gap}rem;
        --menu-item-border-radius: {navbar_config.menu_item_border_radius}px;
        --brand-font-size: {navbar_config.brand_font_size}rem;
        --menu-font-size: {navbar_config.menu_font_size}rem;
        --menu-line-height: {navbar_config.menu_line_height};
        --logo-height: {navbar_config.logo_height}px;
        --mobile-breakpoint: {navbar_config.mobile_breakpoint}px;
        --tablet-breakpoint: {navbar_config.tablet_breakpoint}px;
        --mobile-navbar-height: {navbar_config.mobile_navbar_height}px;
        --mobile-padding-horizontal: {navbar_config.mobile_padding_horizontal}rem;
        --mobile-menu-font-size: {navbar_config.mobile_menu_font_size}rem;
        --mobile-brand-font-size: {navbar_config.mobile_brand_font_size}rem;
        --mobile-logo-height: {navbar_config.mobile_logo_height}px;
        --dropdown-padding: {navbar_config.dropdown_padding}rem;
        --dropdown-item-padding-vertical: {navbar_config.dropdown_item_padding_vertical}rem;
        --dropdown-item-padding-horizontal: {navbar_config.dropdown_item_padding_horizontal}rem;
        --dropdown-item-font-size: {navbar_config.dropdown_item_font_size}rem;
        --dropdown-item-margin: {navbar_config.dropdown_item_margin}rem;
        --mega-menu-padding: {navbar_config.mega_menu_padding}rem;
        --mega-menu-columns: {navbar_config.mega_menu_columns};
        --mega-menu-width: {navbar_config.mega_menu_width};
        --transition-duration: {navbar_config.transition_duration}s;
        --hover-scale: {navbar_config.hover_scale};
        --box-shadow: {navbar_config.box_shadow};
        --border-radius: {navbar_config.border_radius}px;
        --navbar-background-color: {navbar_config.navbar_background_color};
        --navbar-text-color: {navbar_config.navbar_text_color};
        --navbar-hover-color: {navbar_config.navbar_hover_color};
        --navbar-border-color: {navbar_config.navbar_border_color};
    }}
    """
    
    return mark_safe(css_vars)

@register.simple_tag
def navbar_config_value(field_name):
    """Get a specific navbar configuration value"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    
    if not navbar_config:
        return ""
    
    return getattr(navbar_config, field_name, "")

@register.simple_tag
def navbar_brand_name():
    """Get the navbar brand name"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    return navbar_config.brand_name if navbar_config else "College"

@register.simple_tag
def navbar_brand_subtitle():
    """Get the navbar brand subtitle"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    return navbar_config.brand_subtitle if navbar_config else ""

@register.simple_tag
def navbar_logo():
    """Get the navbar logo URL"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    if navbar_config and navbar_config.logo:
        return navbar_config.logo.url
    return ""

@register.simple_tag
def navbar_show_logo():
    """Check if logo should be shown"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    return navbar_config.show_logo if navbar_config else True

@register.simple_tag
def navbar_show_brand_text():
    """Check if brand text should be shown"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    return navbar_config.show_brand_text if navbar_config else True

@register.simple_tag
def navbar_is_sticky():
    """Check if navbar should be sticky"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    return navbar_config.is_sticky if navbar_config else False

@register.simple_tag
def navbar_enable_search():
    """Check if search should be enabled"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    return navbar_config.enable_search if navbar_config else True

@register.simple_tag
def navbar_search_placeholder():
    """Get the search placeholder text"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    return navbar_config.search_placeholder if navbar_config else "Search..."
