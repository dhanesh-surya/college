"""
Signal handlers for college website models
"""

import logging
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib import messages
from django.utils import timezone
from .models import TopUtilityBar, ScrollingNotification
from .validators import TopUtilityBarValidator

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=TopUtilityBar)
def validate_top_utility_bar(sender, instance, **kwargs):
    """
    Comprehensive validation before saving TopUtilityBar
    """
    # Run custom validation
    validator = TopUtilityBarValidator(instance)
    validator.validate()
    
    # Clean and normalize fields
    if instance.name:
        instance.name = instance.name.strip()
    
    if instance.contact_phone:
        # Normalize phone number format
        import re
        cleaned_phone = re.sub(r'[^\d\+\-\(\)\s]', '', instance.contact_phone)
        instance.contact_phone = cleaned_phone
    
    if instance.contact_email:
        instance.contact_email = instance.contact_email.strip().lower()
    
    # Normalize URLs
    url_fields = [
        'facebook_url', 'twitter_url', 'instagram_url', 
        'youtube_url', 'linkedin_url',
        'custom_link_1_url', 'custom_link_2_url', 'custom_link_3_url'
    ]
    
    for field_name in url_fields:
        url = getattr(instance, field_name, '')
        if url:
            # Remove trailing slashes and clean URL
            url = url.strip().rstrip('/')
            setattr(instance, field_name, url)


@receiver(post_save, sender=TopUtilityBar)
def handle_top_utility_bar_save(sender, instance, created, **kwargs):
    """
    Handle post-save operations for TopUtilityBar
    """
    # Clear related cache
    cache.delete('active_utility_bar')
    cache.delete('utility_bar_config')
    
    # Log the action
    action = 'created' if created else 'updated'
    logger.info(f'TopUtilityBar "{instance.name}" was {action}. Active: {instance.is_active}')
    
    # If this utility bar is active, ensure others are deactivated
    if instance.is_active:
        deactivated_count = TopUtilityBar.objects.exclude(pk=instance.pk).filter(is_active=True).update(is_active=False)
        
        if deactivated_count > 0:
            logger.info(f'{deactivated_count} other utility bar(s) were automatically deactivated')
        
        # Cache the active utility bar
        cache.set('active_utility_bar', instance, timeout=3600)  # Cache for 1 hour
    else:
        # Remove from cache if deactivated
        cached_bar = cache.get('active_utility_bar')
        if cached_bar and cached_bar.pk == instance.pk:
            cache.delete('active_utility_bar')


@receiver(post_delete, sender=TopUtilityBar)
def handle_top_utility_bar_delete(sender, instance, **kwargs):
    """
    Handle utility bar deletion
    """
    # Clear cache
    cache.delete('active_utility_bar')
    cache.delete('utility_bar_config')
    
    logger.info(f'TopUtilityBar "{instance.name}" was deleted')


@receiver(pre_save, sender=ScrollingNotification)
def validate_scrolling_notification(sender, instance, **kwargs):
    """
    Additional validation for ScrollingNotification
    """
    # Ensure start_date is not in the past for new notifications
    if not instance.pk and instance.start_date:
        now = timezone.now()
        if instance.start_date < now:
            # Allow past dates but log a warning
            logger.warning(f'ScrollingNotification "{instance.title}" has start_date in the past')
    
    # Validate end_date is after start_date
    if instance.start_date and instance.end_date:
        if instance.end_date <= instance.start_date:
            from django.core.exceptions import ValidationError
            raise ValidationError("End date must be after start date")


def get_active_utility_bar():
    """
    Helper function to get the active utility bar with caching
    """
    cached_bar = cache.get('active_utility_bar')
    
    if cached_bar is None:
        try:
            active_bar = TopUtilityBar.objects.get(is_active=True)
            cache.set('active_utility_bar', active_bar, timeout=3600)
            return active_bar
        except TopUtilityBar.DoesNotExist:
            return None
        except TopUtilityBar.MultipleObjectsReturned:
            # Handle case where multiple are active (shouldn't happen but just in case)
            logger.warning("Multiple active utility bars found, using the most recent")
            active_bar = TopUtilityBar.objects.filter(is_active=True).order_by('-updated_at').first()
            
            # Fix the issue by deactivating all but the most recent
            TopUtilityBar.objects.filter(is_active=True).exclude(pk=active_bar.pk).update(is_active=False)
            
            cache.set('active_utility_bar', active_bar, timeout=3600)
            return active_bar
    
    return cached_bar


def get_utility_bar_context():
    """
    Get utility bar context for templates with caching
    """
    context = cache.get('utility_bar_context')
    
    if context is None:
        active_bar = get_active_utility_bar()
        
        if active_bar:
            # Build context data
            context = {
                'utility_bar': active_bar,
                'show_social_icons': active_bar.show_social_icons,
                'show_contact_info': active_bar.show_contact_info,
                'show_custom_links': active_bar.show_custom_links,
                'social_links': [],
                'contact_info': {},
                'custom_links': []
            }
            
            # Collect social links
            if active_bar.show_social_icons:
                social_links = [
                    ('facebook', active_bar.facebook_url, 'fab fa-facebook-f'),
                    ('twitter', active_bar.twitter_url, 'fab fa-twitter'),
                    ('instagram', active_bar.instagram_url, 'fab fa-instagram'),
                    ('youtube', active_bar.youtube_url, 'fab fa-youtube'),
                    ('linkedin', active_bar.linkedin_url, 'fab fa-linkedin'),
                ]
                
                context['social_links'] = [
                    {'platform': platform, 'url': url, 'icon': icon}
                    for platform, url, icon in social_links if url
                ]
            
            # Collect contact info
            if active_bar.show_contact_info:
                contact_info = {}
                if active_bar.contact_phone:
                    contact_info['phone'] = active_bar.contact_phone
                if active_bar.contact_email:
                    contact_info['email'] = active_bar.contact_email
                context['contact_info'] = contact_info
            
            # Collect custom links
            if active_bar.show_custom_links:
                custom_links = []
                for i in range(1, 4):
                    text = getattr(active_bar, f'custom_link_{i}_text', '')
                    url = getattr(active_bar, f'custom_link_{i}_url', '')
                    
                    if text and url:
                        custom_links.append({'text': text, 'url': url})
                
                context['custom_links'] = custom_links
            
            # Cache for 30 minutes
            cache.set('utility_bar_context', context, timeout=1800)
        else:
            context = {'utility_bar': None}
            # Cache empty result for 5 minutes
            cache.set('utility_bar_context', context, timeout=300)
    
    return context


# Signal to clear utility bar cache when any related model changes
@receiver([post_save, post_delete], sender=TopUtilityBar)
def clear_utility_bar_cache(sender, **kwargs):
    """Clear utility bar related cache"""
    cache_keys = [
        'active_utility_bar',
        'utility_bar_context',
        'utility_bar_config'
    ]
    
    for key in cache_keys:
        cache.delete(key)


class UtilityBarManager:
    """
    Manager class for utility bar operations
    """
    
    @staticmethod
    def activate_utility_bar(utility_bar_id):
        """
        Activate a specific utility bar and deactivate others
        """
        try:
            # Get the utility bar to activate
            utility_bar = TopUtilityBar.objects.get(pk=utility_bar_id)
            
            # Deactivate all others
            TopUtilityBar.objects.exclude(pk=utility_bar_id).update(is_active=False)
            
            # Activate the selected one
            utility_bar.is_active = True
            utility_bar.save()
            
            logger.info(f'Utility bar "{utility_bar.name}" activated successfully')
            return True, f'Utility bar "{utility_bar.name}" is now active'
            
        except TopUtilityBar.DoesNotExist:
            logger.error(f'Utility bar with ID {utility_bar_id} not found')
            return False, 'Utility bar not found'
        except Exception as e:
            logger.error(f'Error activating utility bar: {str(e)}')
            return False, f'Error activating utility bar: {str(e)}'
    
    @staticmethod
    def deactivate_all_utility_bars():
        """
        Deactivate all utility bars
        """
        try:
            updated_count = TopUtilityBar.objects.filter(is_active=True).update(is_active=False)
            logger.info(f'{updated_count} utility bars deactivated')
            return True, f'{updated_count} utility bar(s) deactivated'
        except Exception as e:
            logger.error(f'Error deactivating utility bars: {str(e)}')
            return False, f'Error deactivating utility bars: {str(e)}'
    
    @staticmethod
    def get_utility_bar_stats():
        """
        Get statistics about utility bars
        """
        total = TopUtilityBar.objects.count()
        active = TopUtilityBar.objects.filter(is_active=True).count()
        inactive = total - active
        
        return {
            'total': total,
            'active': active,
            'inactive': inactive,
            'has_active': active > 0
        }
    
    @staticmethod
    def validate_all_utility_bars():
        """
        Validate all utility bars and return issues
        """
        issues = []
        
        for bar in TopUtilityBar.objects.all():
            try:
                validator = TopUtilityBarValidator(bar)
                validator.validate()
            except ValidationError as e:
                issues.append({
                    'utility_bar': bar.name,
                    'errors': e.message_dict if hasattr(e, 'message_dict') else [str(e)]
                })
        
        return issues
    
    @staticmethod
    def duplicate_utility_bar(source_id, new_name=None):
        """
        Create a duplicate of a utility bar
        """
        try:
            source = TopUtilityBar.objects.get(pk=source_id)
            
            # Create a copy
            source.pk = None
            source.name = new_name or f"{source.name} (Copy)"
            source.is_active = False  # Make copy inactive
            source.save()
            
            logger.info(f'Utility bar "{source.name}" duplicated successfully')
            return True, f'Utility bar duplicated as "{source.name}"'
            
        except TopUtilityBar.DoesNotExist:
            logger.error(f'Source utility bar with ID {source_id} not found')
            return False, 'Source utility bar not found'
        except Exception as e:
            logger.error(f'Error duplicating utility bar: {str(e)}')
            return False, f'Error duplicating utility bar: {str(e)}'
