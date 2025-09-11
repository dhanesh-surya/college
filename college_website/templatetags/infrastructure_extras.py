from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtract arg from value"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def get_photo_count(facility):
    """Get the count of photos for a facility"""
    return facility.photos.count()

@register.filter
def get_featured_photos(facility, count=4):
    """Get featured photos for a facility"""
    return facility.photos.filter(is_featured=True, is_active=True)[:count]

@register.filter
def get_active_photos(facility, count=4):
    """Get active photos for a facility"""
    return facility.photos.filter(is_active=True)[:count]
