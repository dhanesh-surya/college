"""
Custom validators for the college website models
"""

import re
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _


def validate_phone_number(phone):
    """
    Validate phone number format with country code support
    """
    if not phone:
        return
    
    # Remove all spaces and special characters for validation
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check basic format: optional +, followed by country code and number
    if not re.match(r'^\+?[1-9]\d{8,15}$', clean_phone):
        raise ValidationError(
            _('Please enter a valid phone number. Examples: +91-9425540666, (555) 123-4567'),
            code='invalid_phone'
        )


def validate_social_media_url(url, platform):
    """
    Validate social media URLs for specific platforms
    """
    if not url:
        return
    
    # First, validate as a general URL
    url_validator = URLValidator()
    try:
        url_validator(url)
    except ValidationError:
        raise ValidationError(
            _(f'Please enter a valid URL for {platform}.'),
            code='invalid_url'
        )
    
    # Then check platform-specific domain
    parsed = urlparse(url)
    platform_domains = {
        'facebook': ['facebook.com', 'fb.com', 'm.facebook.com'],
        'twitter': ['twitter.com', 'x.com', 'm.twitter.com'],
        'instagram': ['instagram.com', 'instagr.am', 'm.instagram.com'],
        'youtube': ['youtube.com', 'youtu.be', 'm.youtube.com'],
        'linkedin': ['linkedin.com', 'm.linkedin.com']
    }
    
    if platform.lower() in platform_domains:
        valid_domains = platform_domains[platform.lower()]
        if not any(domain in parsed.netloc.lower() for domain in valid_domains):
            raise ValidationError(
                _(f'Please enter a valid {platform.title()} URL. Expected domains: {", ".join(valid_domains)}'),
                code='invalid_platform_url'
            )


def validate_facebook_url(url):
    """Validate Facebook URL"""
    validate_social_media_url(url, 'facebook')


def validate_twitter_url(url):
    """Validate Twitter URL"""
    validate_social_media_url(url, 'twitter')


def validate_instagram_url(url):
    """Validate Instagram URL"""
    validate_social_media_url(url, 'instagram')


def validate_youtube_url(url):
    """Validate YouTube URL"""
    validate_social_media_url(url, 'youtube')


def validate_linkedin_url(url):
    """Validate LinkedIn URL"""
    validate_social_media_url(url, 'linkedin')


def validate_custom_link_url(url):
    """
    Validate custom link URLs (can be relative paths or absolute URLs)
    """
    if not url:
        return
    
    url = url.strip()
    
    # Allow relative paths starting with /
    if url.startswith('/'):
        if not re.match(r'^/[\w\-\./]*$', url):
            raise ValidationError(
                _('Please enter a valid path. Example: /admissions/ or /results/'),
                code='invalid_path'
            )
        return
    
    # Validate absolute URLs
    url_validator = URLValidator()
    try:
        url_validator(url)
    except ValidationError:
        raise ValidationError(
            _('Please enter either a relative path (e.g., /admissions/) or a complete URL (e.g., https://example.com)'),
            code='invalid_link_url'
        )


def validate_hex_color(color):
    """
    Validate hex color code format
    """
    if not color:
        return
    
    if not re.match(r'^#[0-9A-Fa-f]{6}$', color):
        raise ValidationError(
            _('Please enter a valid hex color code. Example: #FF5733'),
            code='invalid_hex_color'
        )


def validate_utility_bar_height(height):
    """
    Validate utility bar height with UX considerations
    """
    if height is not None:
        if height < 20:
            raise ValidationError(
                _('Utility bar height must be at least 20 pixels for proper visibility and touch accessibility.'),
                code='height_too_small'
            )
        
        if height > 100:
            raise ValidationError(
                _('Utility bar height should not exceed 100 pixels to avoid taking too much screen real estate.'),
                code='height_too_large'
            )


def validate_color_contrast(background_color, text_color):
    """
    Basic color contrast validation for accessibility
    """
    if background_color and text_color:
        # Convert hex to RGB for basic contrast calculation
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def get_luminance(rgb):
            # Simplified luminance calculation
            r, g, b = [x / 255.0 for x in rgb]
            return 0.299 * r + 0.587 * g + 0.114 * b
        
        try:
            bg_rgb = hex_to_rgb(background_color)
            text_rgb = hex_to_rgb(text_color)
            
            bg_luminance = get_luminance(bg_rgb)
            text_luminance = get_luminance(text_rgb)
            
            # Calculate contrast ratio
            if bg_luminance > text_luminance:
                contrast = (bg_luminance + 0.05) / (text_luminance + 0.05)
            else:
                contrast = (text_luminance + 0.05) / (bg_luminance + 0.05)
            
            # WCAG AA standard recommends at least 4.5:1 for normal text
            # Using very lenient 2.0 for utility bars to avoid blocking saves
            if contrast < 2.0:
                raise ValidationError(
                    _('The color combination has very poor contrast. Consider using darker text on light backgrounds or lighter text on dark backgrounds for better accessibility.'),
                    code='poor_contrast'
                )
                
        except (ValueError, TypeError):
            # If color parsing fails, skip contrast validation
            pass


class TopUtilityBarValidator:
    """
    Comprehensive validator for TopUtilityBar instances
    """
    
    def __init__(self, instance):
        self.instance = instance
        self.errors = {}
    
    def validate(self):
        """
        Run all validations and return errors
        """
        self._validate_basic_fields()
        self._validate_appearance()
        self._validate_social_media()
        self._validate_contact_info()
        self._validate_custom_links()
        self._validate_mobile_settings()
        self._validate_business_rules()
        
        if self.errors:
            raise ValidationError(self.errors)
    
    def _validate_basic_fields(self):
        """Validate basic required fields"""
        if not self.instance.name or len(self.instance.name.strip()) < 3:
            self.errors['name'] = _('Configuration name must be at least 3 characters long.')
    
    def _validate_appearance(self):
        """Validate appearance settings"""
        try:
            validate_hex_color(self.instance.background_color)
        except ValidationError as e:
            self.errors['background_color'] = e.message
        
        try:
            validate_hex_color(self.instance.text_color)
        except ValidationError as e:
            self.errors['text_color'] = e.message
        
        try:
            validate_utility_bar_height(self.instance.height)
        except ValidationError as e:
            self.errors['height'] = e.message
        
        # Validate color contrast (disabled to prevent blocking saves)
        # try:
        #     validate_color_contrast(self.instance.background_color, self.instance.text_color)
        # except ValidationError as e:
        #     self.errors['text_color'] = e.message
    
    def _validate_social_media(self):
        """Validate social media configuration"""
        if self.instance.show_social_icons:
            social_urls = [
                (self.instance.facebook_url, 'facebook'),
                (self.instance.twitter_url, 'twitter'),
                (self.instance.instagram_url, 'instagram'),
                (self.instance.youtube_url, 'youtube'),
                (self.instance.linkedin_url, 'linkedin'),
            ]
            
            has_valid_url = False
            
            for url, platform in social_urls:
                if url:
                    try:
                        validate_social_media_url(url, platform)
                        has_valid_url = True
                    except ValidationError as e:
                        self.errors[f'{platform}_url'] = e.message
            
            if not has_valid_url:
                self.errors['show_social_icons'] = _(
                    'At least one valid social media URL must be provided when social icons are enabled.'
                )
    
    def _validate_contact_info(self):
        """Validate contact information"""
        if self.instance.show_contact_info:
            has_contact = False
            
            if self.instance.contact_phone:
                try:
                    validate_phone_number(self.instance.contact_phone)
                    has_contact = True
                except ValidationError as e:
                    self.errors['contact_phone'] = e.message
            
            if self.instance.contact_email:
                # Email validation is handled by EmailField, but we can add custom logic
                has_contact = True
            
            if not has_contact:
                self.errors['show_contact_info'] = _(
                    'At least one contact method (phone or email) must be provided when contact info is enabled.'
                )
    
    def _validate_custom_links(self):
        """Validate custom links configuration"""
        if self.instance.show_custom_links:
            has_valid_link = False
            
            for i in range(1, 4):
                text = getattr(self.instance, f'custom_link_{i}_text', '')
                url = getattr(self.instance, f'custom_link_{i}_url', '')
                
                if text or url:
                    if not text:
                        self.errors[f'custom_link_{i}_text'] = _(f'Link text is required for custom link {i}.')
                    
                    if not url:
                        self.errors[f'custom_link_{i}_url'] = _(f'URL is required for custom link {i}.')
                    
                    if url:
                        try:
                            validate_custom_link_url(url)
                        except ValidationError as e:
                            self.errors[f'custom_link_{i}_url'] = e.message
                    
                    if text and url:
                        has_valid_link = True
            
            if not has_valid_link:
                self.errors['show_custom_links'] = _(
                    'At least one complete custom link (both text and URL) must be provided when custom links are enabled.'
                )
    
    def _validate_mobile_settings(self):
        """Validate mobile-specific settings"""
        if not self.instance.show_on_mobile and self.instance.mobile_collapsed:
            self.errors['mobile_collapsed'] = _(
                'Mobile collapse option is only relevant when utility bar is shown on mobile devices.'
            )
    
    def _validate_business_rules(self):
        """Validate business logic rules"""
        # Check for duplicate active utility bars
        if self.instance.is_active:
            from .models import TopUtilityBar
            existing_active = TopUtilityBar.objects.filter(is_active=True)
            
            if self.instance.pk:
                existing_active = existing_active.exclude(pk=self.instance.pk)
            
            if existing_active.exists():
                # This is more of a warning than an error since the model handles it
                pass  # The model's clean method and admin save method handle this
