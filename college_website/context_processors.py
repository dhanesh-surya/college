from .models import CollegeInfo, Menu, MenuItem, ImportantLink, ScrollingNotification, SliderImage, HeaderInfo, NavbarInfo, Notice, Department
from django.db.models import Prefetch, Q
from django.utils import timezone


def college_info(request):
    """Add college info to all templates"""
    college_info = CollegeInfo.objects.filter(is_active=True).first()
    return {
        'college_info': college_info,
    }


def menu_context(request):
    """Enhanced menu context for hybrid static/CMS navbar"""
    # Get CMS menus with optimized prefetch for navbar display
    cms_menus = Menu.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            'items',
            queryset=MenuItem.objects.filter(
                is_active=True,
                parent__isnull=True  # Top-level items only for navbar
            ).prefetch_related(
                Prefetch(
                    'children',
                    queryset=MenuItem.objects.filter(is_active=True).order_by('ordering', 'title'),
                    to_attr='active_children'
                )
            ).order_by('ordering', 'title'),
            to_attr='top_level_items'
        )
    ).order_by('ordering', 'title')
    
    # Get navbar info for customization
    navbar_info = NavbarInfo.objects.filter(is_active=True).first()
    
    # Get recent notices count for notification badge
    now = timezone.now()
    recent_notices_count = Notice.objects.filter(
        is_active=True,
        publish_date__gte=now - timezone.timedelta(days=7)
    ).count()
    
    # Important and quick links
    important_links = ImportantLink.objects.filter(
        is_active=True, type='important'
    ).order_by('ordering')
    
    quick_links = ImportantLink.objects.filter(
        is_active=True, type='quick'
    ).order_by('ordering')
    
    # Current URL for active state detection
    current_url = request.get_full_path()
    
    return {
        'main_menus': cms_menus,  # Legacy support
        'cms_menus': cms_menus,   # New name for clarity
        'navbar_info': navbar_info,
        'recent_notices_count': recent_notices_count,
        'important_links': important_links,
        'quick_links': quick_links,
        'current_url': current_url,
    }


def scrolling_notifications(request):
    """Add active scrolling notifications to all templates"""
    notifications = ScrollingNotification.objects.filter(
        is_active=True
    ).order_by('display_order', '-priority', '-start_date')
    
    # Filter only currently active notifications
    active_notifications = [n for n in notifications if n.is_currently_active]
    
    return {
        'scrolling_notifications': active_notifications,
    }


def slider_images(request):
    """Add active slider images to all templates"""
    slider_images = SliderImage.objects.filter(
        is_active=True
    ).order_by('ordering', '-created_at')
    
    # Filter only currently active slides (considering scheduling)
    active_slides = [slide for slide in slider_images if slide.is_currently_active]
    
    return {
        'slider_images': active_slides,
    }


def header_info(request):
    """Add active header info to all templates"""
    header_info = HeaderInfo.objects.filter(is_active=True).first()
    
    return {
        'header_info': header_info,
    }


def menu_visibility_context(request):
    """Add menu visibility settings to all templates"""
    try:
        from .models import MenuVisibilitySettings
        menu_visibility = MenuVisibilitySettings.objects.filter(is_active=True).first()
        if not menu_visibility:
            # Create default settings if none exist
            menu_visibility = MenuVisibilitySettings.objects.create(
                show_research_menu=True,
                show_placement_menu=True,
                show_alumni_menu=True,
                show_events_menu=True,
                show_exam_timetable=True,
                show_exam_revaluation=True,
                show_exam_question_papers=True,
                show_exam_rules=True,
                show_student_portal=True,
                show_sports_cultural=True,
                show_nss_ncc=True,
                show_research_centers=True,
                show_publications=True,
                show_patents_projects=True,
                is_active=True
            )
    except Exception:
        # Fallback to default values if model doesn't exist
        menu_visibility = type('MenuVisibilitySettings', (), {
            'show_research_menu': True,
            'show_placement_menu': True,
            'show_alumni_menu': True,
            'show_events_menu': True,
            'show_exam_timetable': True,
            'show_exam_revaluation': True,
            'show_exam_question_papers': True,
            'show_exam_rules': True,
            'show_student_portal': True,
            'show_sports_cultural': True,
            'show_nss_ncc': True,
            'show_research_centers': True,
            'show_publications': True,
            'show_patents_projects': True,
        })()
    
    return {
        'menu_visibility': menu_visibility,
    }


def departments_context(request):
    """Add departments to navbar context for dropdown menus"""
    departments = Department.objects.filter(
        is_active=True
    ).prefetch_related(
        'programs'
    ).order_by('name')
    
    return {
        'departments': departments,
    }


def navbar_config_context(request):
    """Add comprehensive navbar configuration to all templates"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    
    if not navbar_config:
        # Create default navbar configuration if none exists
        navbar_config = NavbarInfo.objects.create(
            brand_name="Chaitanya Science and Arts College",
            brand_subtitle="Shaheed Nandkumar Patel Vishwavidyalaya, Raigarh",
            is_active=True
        )
    
    # Convert navbar config to CSS variables for easy template usage
    navbar_css_vars = {
        '--navbar-height': f'{navbar_config.navbar_height}px',
        '--navbar-padding-top': f'{navbar_config.navbar_padding_top}rem',
        '--navbar-padding-bottom': f'{navbar_config.navbar_padding_bottom}rem',
        '--navbar-padding-horizontal': f'{navbar_config.navbar_padding_horizontal}rem',
        '--menu-item-padding-vertical': f'{navbar_config.menu_item_padding_vertical}rem',
        '--menu-item-padding-horizontal': f'{navbar_config.menu_item_padding_horizontal}rem',
        '--menu-item-margin': f'{navbar_config.menu_item_margin}rem',
        '--menu-item-gap': f'{navbar_config.menu_item_gap}rem',
        '--menu-item-border-radius': f'{navbar_config.menu_item_border_radius}px',
        '--brand-font-size': f'{navbar_config.brand_font_size}rem',
        '--menu-font-size': f'{navbar_config.menu_font_size}rem',
        '--menu-line-height': f'{navbar_config.menu_line_height}',
        '--logo-height': f'{navbar_config.logo_height}px',
        '--mobile-breakpoint': f'{navbar_config.mobile_breakpoint}px',
        '--tablet-breakpoint': f'{navbar_config.tablet_breakpoint}px',
        '--mobile-navbar-height': f'{navbar_config.mobile_navbar_height}px',
        '--mobile-padding-horizontal': f'{navbar_config.mobile_padding_horizontal}rem',
        '--mobile-menu-font-size': f'{navbar_config.mobile_menu_font_size}rem',
        '--mobile-brand-font-size': f'{navbar_config.mobile_brand_font_size}rem',
        '--mobile-logo-height': f'{navbar_config.mobile_logo_height}px',
        '--dropdown-padding': f'{navbar_config.dropdown_padding}rem',
        '--dropdown-item-padding-vertical': f'{navbar_config.dropdown_item_padding_vertical}rem',
        '--dropdown-item-padding-horizontal': f'{navbar_config.dropdown_item_padding_horizontal}rem',
        '--dropdown-item-font-size': f'{navbar_config.dropdown_item_font_size}rem',
        '--dropdown-item-margin': f'{navbar_config.dropdown_item_margin}rem',
        '--mega-menu-padding': f'{navbar_config.mega_menu_padding}rem',
        '--mega-menu-columns': f'{navbar_config.mega_menu_columns}',
        '--mega-menu-width': navbar_config.mega_menu_width,
        '--transition-duration': f'{navbar_config.transition_duration}s',
        '--hover-scale': f'{navbar_config.hover_scale}',
        '--box-shadow': navbar_config.box_shadow,
        '--border-radius': f'{navbar_config.border_radius}px',
        '--navbar-background-color': navbar_config.navbar_background_color,
        '--navbar-text-color': navbar_config.navbar_text_color,
        '--navbar-hover-color': navbar_config.navbar_hover_color,
        '--navbar-border-color': navbar_config.navbar_border_color,
    }
    
    return {
        'navbar_config': navbar_config,
        'navbar_css_vars': navbar_css_vars,
    }


def menu_visibility_context(request):
    """Add menu visibility settings to all templates"""
    try:
        # Get current active menu visibility settings
        from .models import MenuVisibilitySettings
        menu_settings = MenuVisibilitySettings.get_current_settings()
        
        # Get active menu categories and submenus
        from .models import MenuCategory, MenuSubmenu
        active_categories = MenuCategory.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                'submenus',
                queryset=MenuSubmenu.objects.filter(is_active=True).order_by('order'),
                to_attr='active_submenus'
            )
        ).order_by('order')
        
        return {
            'menu_visibility': menu_settings,
            'menu_categories': active_categories,
        }
    except Exception as e:
        # Fallback if models don't exist yet (during migrations)
        return {
            'menu_visibility': None,
            'menu_categories': [],
        }
