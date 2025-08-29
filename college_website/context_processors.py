from .models import CollegeInfo, Menu, MenuItem, ImportantLink, ScrollingNotification, SliderImage, HeaderInfo, NavbarInfo, Notice
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
