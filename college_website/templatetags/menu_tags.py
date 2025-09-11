from django import template
from django.utils.safestring import mark_safe
from ..models import MenuVisibilitySettings, MenuCategory, MenuSubmenu

register = template.Library()


@register.simple_tag
def get_menu_visibility():
    """Get current menu visibility settings"""
    return MenuVisibilitySettings.get_current_settings()


@register.simple_tag
def get_active_menus():
    """Get all active menu categories with their submenus"""
    return MenuCategory.objects.filter(is_active=True).prefetch_related(
        'submenus'
    ).order_by('order')


@register.simple_tag
def is_menu_visible(menu_name):
    """Check if a specific menu is visible based on settings"""
    settings = MenuVisibilitySettings.get_current_settings()
    if not settings:
        return True  # Default to visible if no settings
    
    # Map menu names to settings fields
    menu_mapping = {
        'research': 'show_research_menu',
        'placement': 'show_placement_menu',
        'alumni': 'show_alumni_menu',
        'events': 'show_events_menu',
        'exam_timetable': 'show_exam_timetable',
        'exam_revaluation': 'show_exam_revaluation',
        'exam_question_papers': 'show_exam_question_papers',
        'exam_rules': 'show_exam_rules',
        'student_portal': 'show_student_portal',
        'sports_cultural': 'show_sports_cultural',
        'nss_ncc': 'show_nss_ncc',
        'research_centers': 'show_research_centers',
        'publications': 'show_publications',
        'patents_projects': 'show_patents_projects',
    }
    
    setting_field = menu_mapping.get(menu_name.lower())
    if setting_field:
        return getattr(settings, setting_field, True)
    
    return True  # Default to visible


@register.simple_tag
def render_menu_item(menu_item, is_active=False):
    """Render a single menu item with proper styling"""
    active_class = 'active' if is_active else ''
    
    html = f'''
    <a class="dropdown-item tw-transition-all tw-duration-200 {active_class}" 
       href="{menu_item.url}" 
       style="color: {menu_item.text_color};">
        <i class="{menu_item.icon_class} me-3 tw-text-blue-500 tw-w-4"></i>
        {menu_item.name}
    </a>
    '''
    
    return mark_safe(html)


@register.simple_tag
def render_menu_category(category, current_url=''):
    """Render a complete menu category with submenus"""
    if not category.is_active:
        return ''
    
    # Check if current page matches this category
    is_current = current_url.startswith(category.slug) if category.slug != 'home' else current_url == '/'
    
    html = f'''
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle {"active" if is_current else ""}" 
           href="#" role="button" data-bs-toggle="dropdown" 
           aria-expanded="false" id="{category.slug}Dropdown"
           style="color: {category.text_color};">
            <i class="{category.icon_class} me-2 tw-text-sm"></i>{category.name}
        </a>
        <ul class="dropdown-menu tw-animate-pulse">
    '''
    
    # Group submenus by group_header
    submenus_by_group = {}
    for submenu in category.submenus.filter(is_active=True).order_by('order'):
        group = submenu.group_header or 'General'
        if group not in submenus_by_group:
            submenus_by_group[group] = []
        submenus_by_group[group].append(submenu)
    
    # Render submenus by group
    for group_name, submenus in submenus_by_group.items():
        if group_name != 'General':
            html += f'<li><h6 class="dropdown-header tw-text-red-600 tw-font-bold">{group_name}</h6></li>'
        
        for submenu in submenus:
            html += render_menu_item(submenu)
            
            if submenu.show_divider:
                html += '<li><hr class="dropdown-divider tw-border-gray-200"></li>'
    
    html += '''
        </ul>
    </li>
    '''
    
    return mark_safe(html)


@register.filter
def filter_visible_menus(menus, visibility_settings):
    """Filter menus based on visibility settings"""
    if not visibility_settings:
        return menus
    
    visible_menus = []
    for menu in menus:
        if is_menu_visible(menu.slug):
            visible_menus.append(menu)
    
    return visible_menus


@register.simple_tag
def get_menu_stats():
    """Get statistics about the menu system"""
    total_categories = MenuCategory.objects.count()
    active_categories = MenuCategory.objects.filter(is_active=True).count()
    total_submenus = MenuSubmenu.objects.count()
    active_submenus = MenuSubmenu.objects.filter(is_active=True).count()
    
    return {
        'total_categories': total_categories,
        'active_categories': active_categories,
        'total_submenus': total_submenus,
        'active_submenus': active_submenus,
        'hidden_categories': total_categories - active_categories,
        'hidden_submenus': total_submenus - active_submenus,
    }
