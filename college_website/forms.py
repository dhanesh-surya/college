import os
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import (
    ScrollingNotification, HeaderInfo, NavbarInfo, CollegeInfo, Program, Event, Notice, SocialInitiative, 
    StudentTestimonial, ImportantLink, ContactMessage,
    Menu, MenuItem, Page, BlockRichText, BlockImageGallery,
    BlockVideoEmbed, BlockDownloadList, BlockTableHTML, BlockForm,
    GalleryImage, DownloadFile, TopUtilityBar, CustomLink,
    IQACInfo, IQACReport, NAACInfo, NIRFInfo, AccreditationInfo, IQACFeedback, 
    QualityInitiative, SideMenu, SideMenuItem
)


class TopUtilityBarForm(forms.ModelForm):
    """Enhanced form for managing top utility bar with comprehensive validation and user experience improvements"""
    
    # Custom fields for better UX
    enable_auto_hide = forms.BooleanField(
        required=False,
        initial=False,
        label="Auto-hide on scroll",
        help_text="Automatically hide utility bar when user scrolls down",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = TopUtilityBar
        fields = '__all__'
        widgets = {
            # General Settings
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a descriptive name for this utility bar configuration',
                'maxlength': '100'
            }),
            
            # Appearance Settings
            'background_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color',
                'title': 'Choose background color'
            }),
            'text_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color',
                'title': 'Choose text color'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '20',
                'max': '100',
                'placeholder': '40'
            }),
            
            # Position Settings
            'position': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            # Social Media Enable Checkboxes
            'enable_facebook': forms.CheckboxInput(attrs={
                'class': 'form-check-input social-enable-checkbox',
                'data-target': 'facebook_url'
            }),
            'enable_twitter': forms.CheckboxInput(attrs={
                'class': 'form-check-input social-enable-checkbox',
                'data-target': 'twitter_url'
            }),
            'enable_instagram': forms.CheckboxInput(attrs={
                'class': 'form-check-input social-enable-checkbox',
                'data-target': 'instagram_url'
            }),
            'enable_youtube': forms.CheckboxInput(attrs={
                'class': 'form-check-input social-enable-checkbox',
                'data-target': 'youtube_url'
            }),
            'enable_linkedin': forms.CheckboxInput(attrs={
                'class': 'form-check-input social-enable-checkbox',
                'data-target': 'linkedin_url'
            }),
            
            # Social Media URLs
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/yourpage',
                'data-social-field': 'facebook'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://twitter.com/yourpage',
                'data-social-field': 'twitter'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/yourpage',
                'data-social-field': 'instagram'
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/yourchannel',
                'data-social-field': 'youtube'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/company/yourpage',
                'data-social-field': 'linkedin'
            }),
            
            # Contact Information
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91-XXXXXXXXXX',
                'pattern': r'^[\+]?[1-9][\d\s\-\(\)]{8,15}$'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact@example.com'
            }),
            
            # Custom Links
            'custom_link_1_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link 1 text (e.g., Admissions)',
                'maxlength': '50'
            }),
            'custom_link_1_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link 1 URL or path (e.g., /admissions/)'
            }),
            'custom_link_2_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link 2 text (e.g., Results)',
                'maxlength': '50'
            }),
            'custom_link_2_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link 2 URL or path (e.g., /results/)'
            }),
            'custom_link_3_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link 3 text (e.g., Library)',
                'maxlength': '50'
            }),
            'custom_link_3_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link 3 URL or path (e.g., /library/)'
            }),
            
            # Boolean fields with better styling
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'show_social_icons': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'data-toggle-target': '.social-media-fields'
            }),
            'show_contact_info': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'data-toggle-target': '.contact-info-fields'
            }),
            'show_custom_links': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'data-toggle-target': '.custom-links-fields'
            }),
            'show_on_mobile': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'mobile_collapsed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        help_texts = {
            'name': 'A descriptive name for this utility bar configuration (for admin reference)',
            'is_active': 'Only one utility bar can be active at a time. Activating this will deactivate others.',
            'background_color': 'Background color for the utility bar (supports hex colors)',
            'text_color': 'Text color for all text elements in the utility bar',
            'height': 'Height of the utility bar in pixels (recommended: 30-50px)',
            'position': 'Where to display the utility bar on the page',
            'show_social_icons': 'Display social media icons in the utility bar',
            'facebook_url': 'Complete URL to your Facebook page',
            'twitter_url': 'Complete URL to your Twitter profile',
            'instagram_url': 'Complete URL to your Instagram profile',
            'youtube_url': 'Complete URL to your YouTube channel',
            'linkedin_url': 'Complete URL to your LinkedIn company page',
            'show_contact_info': 'Display contact information (phone/email)',
            'contact_phone': 'Primary contact phone number with country code',
            'contact_email': 'Primary contact email address',
            'show_custom_links': 'Display custom quick links',
            'custom_link_1_text': 'Display text for the first custom link',
            'custom_link_1_url': 'URL or path for the first custom link',
            'custom_link_2_text': 'Display text for the second custom link',
            'custom_link_2_url': 'URL or path for the second custom link',
            'custom_link_3_text': 'Display text for the third custom link',
            'custom_link_3_url': 'URL or path for the third custom link',
            'show_on_mobile': 'Display utility bar on mobile devices',
            'mobile_collapsed': 'Collapse to icon on mobile to save space',
        }
        
        labels = {
            'is_active': 'Active Configuration',
            'background_color': 'Background Color',
            'text_color': 'Text Color',
            'show_social_icons': 'Show Social Media Icons',
            'show_contact_info': 'Show Contact Information',
            'show_custom_links': 'Show Custom Quick Links',
            'show_on_mobile': 'Display on Mobile',
            'mobile_collapsed': 'Collapse on Mobile',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes to form for better styling
        self.helper_attrs = {'class': 'top-utility-bar-form'}
        
        # Add required indicators to required fields
        for field_name, field in self.fields.items():
            if field.required and field_name != 'is_active':
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' required'
                else:
                    field.widget.attrs['class'] = 'required'
        
        # Add validation indicators
        self.fields['contact_phone'].widget.attrs.update({
            'title': 'Please enter a valid phone number with country code',
            'data-validation': 'phone'
        })
        
        self.fields['contact_email'].widget.attrs.update({
            'data-validation': 'email'
        })
        
        # Add URL validation for social media fields
        for field_name in ['facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'linkedin_url']:
            self.fields[field_name].widget.attrs.update({
                'data-validation': 'url',
                'pattern': 'https?://.+'
            })
        
        # Add special handling for custom link URLs (can be relative or absolute)
        for i in range(1, 4):
            url_field = f'custom_link_{i}_url'
            self.fields[url_field].widget.attrs.update({
                'data-validation': 'custom-url',
                'title': 'Enter a complete URL (https://...) or relative path (/page/)'
            })
    
    def clean_name(self):
        """Validate and clean the name field"""
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 3:
                raise forms.ValidationError('Name must be at least 3 characters long.')
        return name
    
    def clean_height(self):
        """Validate utility bar height"""
        height = self.cleaned_data.get('height')
        if height:
            if height < 20:
                raise forms.ValidationError('Height must be at least 20 pixels for proper visibility.')
            if height > 100:
                raise forms.ValidationError('Height should not exceed 100 pixels to avoid taking too much screen space.')
        return height
    
    def clean_contact_phone(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('contact_phone')
        if phone:
            phone = phone.strip()
            # Basic phone validation
            import re
            if not re.match(r'^[\+]?[1-9][\d\s\-\(\)]{8,15}$', phone):
                raise forms.ValidationError(
                    'Please enter a valid phone number. '
                    'Example: +91-9425540666 or (555) 123-4567'
                )
        return phone
    
    def clean_contact_email(self):
        """Validate email format"""
        email = self.cleaned_data.get('contact_email')
        if email:
            email = email.strip().lower()
        return email
    
    def _validate_url_field(self, url, field_name, domain_hint=None):
        """Helper method to validate URL fields"""
        if url:
            url = url.strip()
            if not url.startswith(('http://', 'https://')):
                raise forms.ValidationError(
                    f'Please enter a complete URL starting with http:// or https://'
                )
            
            # Optional domain validation for social media URLs
            if domain_hint and domain_hint not in url.lower():
                raise forms.ValidationError(
                    f'Please enter a valid {domain_hint.title()} URL'
                )
        return url
    
    def clean_facebook_url(self):
        return self._validate_url_field(
            self.cleaned_data.get('facebook_url'), 
            'facebook_url', 
            'facebook.com'
        )
    
    def clean_twitter_url(self):
        return self._validate_url_field(
            self.cleaned_data.get('twitter_url'), 
            'twitter_url', 
            'twitter.com'
        )
    
    def clean_instagram_url(self):
        return self._validate_url_field(
            self.cleaned_data.get('instagram_url'), 
            'instagram_url', 
            'instagram.com'
        )
    
    def clean_youtube_url(self):
        return self._validate_url_field(
            self.cleaned_data.get('youtube_url'), 
            'youtube_url', 
            'youtube.com'
        )
    
    def clean_linkedin_url(self):
        return self._validate_url_field(
            self.cleaned_data.get('linkedin_url'), 
            'linkedin_url', 
            'linkedin.com'
        )
    
    def _validate_custom_link_url(self, url):
        """Validate custom link URLs (can be relative or absolute)"""
        if url:
            url = url.strip()
            # Allow relative URLs starting with / or absolute URLs
            if not (url.startswith('/') or url.startswith(('http://', 'https://'))):
                raise forms.ValidationError(
                    'Enter either a relative path (e.g., /admissions/) or '
                    'a complete URL (e.g., https://example.com)'
                )
        return url
    
    def clean_custom_link_1_url(self):
        return self._validate_custom_link_url(self.cleaned_data.get('custom_link_1_url'))
    
    def clean_custom_link_2_url(self):
        return self._validate_custom_link_url(self.cleaned_data.get('custom_link_2_url'))
    
    def clean_custom_link_3_url(self):
        return self._validate_custom_link_url(self.cleaned_data.get('custom_link_3_url'))
    
    def clean(self):
        """Comprehensive form validation with improved error messages"""
        cleaned_data = super().clean()
        
        # Validate social media configuration
        if cleaned_data.get('show_social_icons'):
            social_urls = [
                cleaned_data.get('facebook_url'),
                cleaned_data.get('twitter_url'),
                cleaned_data.get('instagram_url'),
                cleaned_data.get('youtube_url'),
                cleaned_data.get('linkedin_url')
            ]
            
            if not any(social_urls):
                self.add_error('show_social_icons', 
                    'At least one social media URL must be provided when social icons are enabled. '
                    'Please provide at least one social media URL below.'
                )
        
        # Validate contact information configuration
        if cleaned_data.get('show_contact_info'):
            contact_phone = cleaned_data.get('contact_phone')
            contact_email = cleaned_data.get('contact_email')
            
            if not contact_phone and not contact_email:
                self.add_error('show_contact_info', 
                    'At least one contact method (phone or email) must be provided '
                    'when contact info display is enabled.'
                )
        
        # Validate custom links configuration
        if cleaned_data.get('show_custom_links'):
            has_valid_link = False
            
            for i in range(1, 4):
                text_field = f'custom_link_{i}_text'
                url_field = f'custom_link_{i}_url'
                text = cleaned_data.get(text_field)
                url = cleaned_data.get(url_field)
                
                if text or url:  # If either is provided
                    if not text:
                        self.add_error(text_field, 
                            f'Link text is required when URL is provided for custom link {i}.'
                        )
                    if not url:
                        self.add_error(url_field, 
                            f'URL is required when text is provided for custom link {i}.'
                        )
                    
                    if text and url:
                        has_valid_link = True
            
            if not has_valid_link:
                self.add_error('show_custom_links', 
                    'At least one complete custom link (both text and URL) must be provided '
                    'when custom links display is enabled.'
                )
        
        # Validate color contrast for accessibility
        bg_color = cleaned_data.get('background_color')
        text_color = cleaned_data.get('text_color')
        
        if bg_color and text_color:
            # Basic color contrast validation (simplified)
            if bg_color.lower() == text_color.lower():
                self.add_error('text_color', 
                    'Text color should be different from background color for better readability.'
                )
        
        # Validate mobile settings
        if not cleaned_data.get('show_on_mobile') and cleaned_data.get('mobile_collapsed'):
            self.add_error('mobile_collapsed', 
                'Mobile collapse option is only relevant when utility bar is shown on mobile devices.'
            )
        
        return cleaned_data
    
    def save(self, commit=True):
        """Enhanced save method with additional processing"""
        instance = super().save(commit=False)
        
        # If this instance is being set as active, deactivate others
        if instance.is_active:
            TopUtilityBar.objects.exclude(pk=instance.pk).update(is_active=False)
        
        if commit:
            instance.save()
        
        return instance


class CustomLinkForm(forms.ModelForm):
    """Form for managing dynamic custom links"""
    
    class Meta:
        model = CustomLink
        fields = ['text', 'url', 'icon_class', 'tooltip', 'open_in_new_tab', 'ordering', 'is_active']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link text (e.g., Admissions, Results, Library)',
                'maxlength': '50',
                'required': True
            }),
            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL or path (e.g., /admissions/ or https://example.com)',
                'maxlength': '200',
                'required': True,
                'data-validation': 'custom-url'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional icon (e.g., fas fa-graduation-cap)',
                'maxlength': '50'
            }),
            'tooltip': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional tooltip text',
                'maxlength': '100'
            }),
            'open_in_new_tab': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '999',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        help_texts = {
            'text': 'Display text for the link (keep it short and descriptive)',
            'url': 'URL or path - can be relative (/page/) or absolute (https://example.com)',
            'icon_class': 'Optional FontAwesome icon class to display before the link text',
            'tooltip': 'Optional tooltip text that appears when hovering over the link',
            'open_in_new_tab': 'Check to open this link in a new tab/window',
            'ordering': 'Display order (lower numbers appear first)',
            'is_active': 'Enable/disable this link'
        }
        
        labels = {
            'text': 'Link Text',
            'url': 'Link URL',
            'icon_class': 'Icon Class',
            'tooltip': 'Tooltip',
            'open_in_new_tab': 'Open in New Tab',
            'ordering': 'Display Order',
            'is_active': 'Active'
        }
    
    def clean_text(self):
        """Validate link text"""
        text = self.cleaned_data.get('text')
        if text:
            text = text.strip()
            if len(text) < 1:
                raise forms.ValidationError('Link text is required.')
            if len(text) > 50:
                raise forms.ValidationError('Link text must be 50 characters or less.')
        return text
    
    def clean_url(self):
        """Validate URL (can be relative or absolute)"""
        url = self.cleaned_data.get('url')
        if url:
            url = url.strip()
            # Allow relative URLs starting with / or # or absolute URLs
            if not (url.startswith('/') or url.startswith('#') or url.startswith(('http://', 'https://'))):
                raise forms.ValidationError(
                    'Enter a valid URL. Examples: /admissions/, #section, https://example.com'
                )
        return url
    
    def clean_icon_class(self):
        """Validate icon class format"""
        icon_class = self.cleaned_data.get('icon_class')
        if icon_class:
            icon_class = icon_class.strip()
            # Basic validation for FontAwesome format
            if icon_class and not (icon_class.startswith(('fa ', 'fas ', 'far ', 'fab ', 'fal ')) or 
                                  'fa-' in icon_class):
                raise forms.ValidationError(
                    'Please enter a valid FontAwesome icon class. '
                    'Examples: fas fa-graduation-cap, far fa-file-pdf'
                )
        return icon_class
    
    def clean_ordering(self):
        """Validate ordering value"""
        ordering = self.cleaned_data.get('ordering')
        if ordering is not None and ordering < 0:
            raise forms.ValidationError('Ordering must be a non-negative number.')
        return ordering


class ScrollingNotificationForm(forms.ModelForm):
    """Form for managing scrolling notifications"""
    class Meta:
        model = ScrollingNotification
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter notification title',
                'maxlength': '200'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter detailed notification message',
                'rows': 3
            }),
            'link_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Read More, Apply Now',
                'maxlength': '50'
            }),
            'link_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/link'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'color_theme': forms.Select(attrs={
                'class': 'form-select'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-bullhorn, fas fa-info-circle',
                'maxlength': '50'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'scroll_speed': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '10',
                'max': '120',
                'placeholder': '50'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
        }
        help_texts = {
            'title': 'Brief, attention-grabbing notification title',
            'message': 'Detailed message content for the notification',
            'link_text': 'Optional action button text (leave empty for no button)',
            'link_url': 'URL to redirect when notification or button is clicked',
            'priority': 'Higher priority notifications appear first',
            'color_theme': 'Visual theme color for the notification bar',
            'icon_class': 'FontAwesome icon class (e.g., fas fa-bullhorn)',
            'start_date': 'When to start displaying this notification',
            'end_date': 'When to stop displaying (leave empty for permanent)',
            'scroll_speed': 'Speed in seconds for complete scroll cycle (lower = faster)',
            'display_order': 'Lower numbers appear first in the sequence',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        link_text = cleaned_data.get('link_text')
        link_url = cleaned_data.get('link_url')
        
        # Validate date range
        if start_date and end_date and start_date >= end_date:
            raise ValidationError({
                'end_date': 'End date must be after start date.'
            })
        
        # Validate link consistency
        if link_text and not link_url:
            raise ValidationError({
                'link_url': 'Link URL is required when link text is provided.'
            })
        
        return cleaned_data


class HeaderInfoForm(forms.ModelForm):
    """Comprehensive form for HeaderInfo model with Bootstrap 5 and Tailwind CSS styling"""
    
    class Meta:
        model = HeaderInfo
        fields = '__all__'
        widgets = {
            # Basic Info
            'college_full_name': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'Enter full college name'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'Complete address of the institution'
            }),
            'affiliations': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'University affiliations or accreditations'
            }),
            'contact_info': forms.EmailInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'contact@college.edu'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': '+91-XXXXXXXXXX'
            }),
            'additional_text_1': forms.Textarea(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'Additional information line 1',
                'rows': 2
            }),
            'additional_text_2': forms.Textarea(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'Additional information line 2',
                'rows': 2
            }),
            
            # Typography
            'font_family': forms.Select(attrs={
                'class': 'form-select tw-rounded-lg'
            }),
            'font_size': forms.NumberInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'min': '12',
                'max': '72',
                'placeholder': '24'
            }),
            'font_weight': forms.Select(attrs={
                'class': 'form-select tw-rounded-lg'
            }),
            'font_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color tw-rounded-lg'
            }),
            
            # Logo Configuration
            'logo_max_height': forms.NumberInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'min': '20',
                'max': '200',
                'placeholder': '80'
            }),
            'logo_max_width': forms.NumberInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'min': '50',
                'max': '500',
                'placeholder': '200'
            }),
            
            # Social Media Links
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'https://facebook.com/yourpage'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'https://twitter.com/yourpage'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'https://instagram.com/yourpage'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'https://linkedin.com/company/yourpage'
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'https://youtube.com/yourchannel'
            }),
            
            # Header Layout & Styling
            'layout': forms.Select(attrs={
                'class': 'form-select tw-rounded-lg'
            }),
            'header_background_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color tw-rounded-lg'
            }),
            'header_gradient_colors': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)'
            }),
            'header_border_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color tw-rounded-lg'
            }),
            'header_shadow': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': '0 4px 6px rgba(0, 0, 0, 0.1)'
            }),
            'header_border_radius': forms.NumberInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'min': '0',
                'max': '50',
                'placeholder': '0'
            }),
            'header_padding': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': '2rem 0'
            }),
            'header_margin': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': '0'
            }),
            'text_shadow': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'none or 1px 1px 2px rgba(0,0,0,0.1)'
            }),
            
            # Top Bar
            'top_bar_background_class': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'bg-dark or bg-primary'
            }),
            
            # Responsive & Animation
            'animation_type': forms.Select(attrs={
                'class': 'form-select tw-rounded-lg'
            }),
            'animation_duration': forms.NumberInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'min': '0.1',
                'max': '5.0',
                'step': '0.1',
                'placeholder': '0.5'
            }),
        }
        
        help_texts = {
            'college_full_name': 'The complete official name of your institution',
            'address': 'Full address including city, state, and country',
            'affiliations': 'University affiliation, accreditation bodies, etc.',
            'contact_info': 'Primary email address for contact',
            'phone': 'Main phone number with country code',
            'additional_text_1': 'Extra information line 1 (supports HTML)',
            'additional_text_2': 'Extra information line 2 (supports HTML)',
            'font_family': 'Choose from popular Google Fonts',
            'font_size': 'Font size in pixels for the main college name',
            'font_weight': 'Font weight (boldness) for the main text',
            'font_color': 'Color for the main text elements',
            'logo_max_height': 'Maximum height for logos in pixels',
            'logo_max_width': 'Maximum width for logos in pixels',
            'facebook_url': 'Complete URL to your Facebook page',
            'twitter_url': 'Complete URL to your Twitter profile',
            'instagram_url': 'Complete URL to your Instagram profile',
            'linkedin_url': 'Complete URL to your LinkedIn company page',
            'youtube_url': 'Complete URL to your YouTube channel',
            'layout': 'Overall layout arrangement of header elements',
            'header_background_color': 'Solid background color for the header',
            'header_gradient_colors': 'CSS gradient definition for background',
            'header_border_color': 'Color for borders and accents',
            'header_shadow': 'CSS box-shadow property for depth',
            'header_border_radius': 'Corner rounding in pixels',
            'header_padding': 'Padding around header content',
            'header_margin': 'Margin around the header element',
            'text_shadow': 'CSS text-shadow for text effects',
            'top_bar_background_class': 'Bootstrap class for top bar background',
            'show_top_bar': 'Show contact info bar above main header',
            'hide_on_mobile': 'Hide certain elements on mobile devices',
            'enable_animations': 'Enable CSS animations for header elements',
            'animation_type': 'Type of animation effect',
            'animation_duration': 'Duration of animations in seconds',
            'is_active': 'Set this header configuration as active (only one can be active)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add custom CSS classes to form
        self.attrs = {'class': 'header-info-form'}
        
        # Customize certain fields
        self.fields['font_family'].choices = [
            ('Inter', 'Inter (Modern Sans-Serif)'),
            ('Roboto', 'Roboto (Clean & Professional)'),
            ('Poppins', 'Poppins (Friendly & Rounded)'),
            ('Montserrat', 'Montserrat (Elegant & Stylish)'),
            ('Open Sans', 'Open Sans (Highly Readable)'),
            ('Lato', 'Lato (Corporate & Clean)'),
            ('Playfair Display', 'Playfair Display (Traditional Serif)'),
            ('Merriweather', 'Merriweather (Academic Serif)'),
            ('Source Sans Pro', 'Source Sans Pro (Technical)'),
            ('Nunito', 'Nunito (Friendly Sans-Serif)'),
        ]
        
        self.fields['font_weight'].choices = [
            ('300', 'Light (300)'),
            ('400', 'Normal (400)'),
            ('500', 'Medium (500)'),
            ('600', 'Semi-Bold (600)'),
            ('700', 'Bold (700)'),
            ('800', 'Extra Bold (800)'),
            ('900', 'Black (900)'),
        ]
        
        self.fields['layout'].choices = [
            ('justify-content-center', 'Center Aligned'),
            ('justify-content-start', 'Left Aligned'),
            ('justify-content-end', 'Right Aligned'),
            ('justify-content-between', 'Space Between'),
            ('justify-content-around', 'Space Around'),
        ]
        
        self.fields['animation_type'].choices = [
            ('fadeIn', 'Fade In'),
            ('slideInDown', 'Slide In From Top'),
            ('slideInUp', 'Slide In From Bottom'),
            ('slideInLeft', 'Slide In From Left'),
            ('slideInRight', 'Slide In From Right'),
            ('zoomIn', 'Zoom In'),
            ('bounceIn', 'Bounce In'),
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        is_active = cleaned_data.get('is_active', False)
        
        # Ensure only one HeaderInfo can be active
        if is_active:
            existing_active = HeaderInfo.objects.filter(is_active=True)
            if self.instance.pk:
                existing_active = existing_active.exclude(pk=self.instance.pk)
            
            if existing_active.exists():
                # This validation will be handled by the model's save method,
                # but we can provide a warning here
                self.add_error('is_active', 
                    'Another header configuration is currently active. '
                    'Saving this will deactivate the current one.'
                )
        
        return cleaned_data


class NavbarInfoForm(forms.ModelForm):
    class Meta:
        model = NavbarInfo
        fields = '__all__'
        widgets = {
            'brand_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'College Name'
            }),
            'brand_subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Affiliation or Tagline'
            }),
            'logo': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'class': 'form-control'
            }),
            'search_placeholder': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Search...'
            }),
            'navbar_background_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color'
            }),
            'navbar_text_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color'
            }),
            'navbar_hover_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color'
            }),
            'navbar_border_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color'
            }),
        }


class CollegeInfoForm(forms.ModelForm):
    class Meta:
        model = CollegeInfo
        fields = '__all__'
        widgets = {
            'mission_statement_long': forms.Textarea(attrs={'rows': 4}),
            'founder_message': forms.Textarea(attrs={'rows': 4}),
            'principal_message': forms.Textarea(attrs={'rows': 4}),
            'establishment_year': forms.NumberInput(attrs={'min': 1900, 'max': 2030}),
            'logo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'hero_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = '__all__'
        widgets = {
            'description': CKEditor5Widget(),
            'brochure': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'description': CKEditor5Widget(),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'banner_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(),
            'publish_date': forms.DateInput(attrs={'type': 'date'}),
            'attachment': forms.ClearableFileInput(),
        }


class SocialInitiativeForm(forms.ModelForm):
    class Meta:
        model = SocialInitiative
        fields = '__all__'
        widgets = {
            'description': CKEditor5Widget(),
            'cover_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }


class StudentTestimonialForm(forms.ModelForm):
    class Meta:
        model = StudentTestimonial
        fields = '__all__'
        widgets = {
            'feedback_text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.Select(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]),
            'photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }


class ImportantLinkForm(forms.ModelForm):
    class Meta:
        model = ImportantLink
        fields = '__all__'
        widgets = {
            'ordering': forms.NumberInput(attrs={'min': 0}),
        }


class ContactForm(forms.ModelForm):
    """Front-end contact form"""
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'comments']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number (Optional)'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and '@' not in email:
            raise ValidationError("Please enter a valid email address.")
        return email


# CMS Forms

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        widgets = {
            'ordering': forms.NumberInput(attrs={'min': 0}),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'
        widgets = {
            'ordering': forms.NumberInput(attrs={'min': 0}),
        }

    def clean(self):
        cleaned_data = super().clean()
        path_type = cleaned_data.get('path_type')
        external_url = cleaned_data.get('external_url')
        page = cleaned_data.get('page')

        if path_type == 'external' and not external_url:
            raise ValidationError("External URL is required for external menu items.")
        
        if path_type == 'internal' and not page:
            raise ValidationError("Page is required for internal menu items.")

        return cleaned_data


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'meta_description': forms.Textarea(attrs={'rows': 3}),
            'banner_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }


# Content Block Forms

class BlockRichTextForm(forms.ModelForm):
    class Meta:
        model = BlockRichText
        fields = '__all__'
        widgets = {
            'body': CKEditor5Widget(),
            'ordering': forms.NumberInput(attrs={'min': 0}),
        }


class BlockImageGalleryForm(forms.ModelForm):
    class Meta:
        model = BlockImageGallery
        fields = '__all__'
        widgets = {
            'ordering': forms.NumberInput(attrs={'min': 0}),
        }


class EnhancedGalleryImageForm(forms.ModelForm):
    """Enhanced form for gallery images with better validation and UI"""
    class Meta:
        model = GalleryImage
        fields = ['gallery', 'image', 'caption', 'ordering']
        widgets = {
            'gallery': forms.Select(attrs={
                'class': 'form-select tw-rounded-lg',
                'required': True
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp',
                'data-max-size': '5120',  # 5MB in KB
                'data-allowed-types': 'jpeg,jpg,png,gif,webp'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'Optional image caption or description',
                'maxlength': '200'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'min': '0',
                'max': '999',
                'placeholder': '0'
            }),
        }
        help_texts = {
            'image': 'Upload an image file (JPEG, PNG, GIF, WebP). Maximum size: 5MB. Recommended dimensions: 800x600px or larger.',
            'caption': 'Optional caption that will appear below the image',
            'ordering': 'Display order within the gallery (lower numbers appear first)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter active galleries
        self.fields['gallery'].queryset = BlockImageGallery.objects.filter(is_active=True).select_related('page')
        self.fields['gallery'].empty_label = "Select a gallery..."
        
        # Add CSS classes for better styling
        for field_name, field in self.fields.items():
            if field_name not in ['image']:  # Image field already has custom styling
                field.widget.attrs.update({'class': 'form-control tw-rounded-lg'})
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 5MB)
            if hasattr(image, 'size') and image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'Image file is too large. Maximum size allowed is 5MB. '
                    f'Your file is {image.size / (1024 * 1024):.1f}MB.'
                )
            
            # Check file type
            if hasattr(image, 'content_type'):
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if image.content_type not in allowed_types:
                    raise forms.ValidationError(
                        'Invalid file type. Please upload a JPEG, PNG, GIF, or WebP image.'
                    )
            
            # Check file name extension
            if hasattr(image, 'name'):
                allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
                file_extension = os.path.splitext(image.name)[1].lower()
                if file_extension not in allowed_extensions:
                    raise forms.ValidationError(
                        'Invalid file extension. Allowed extensions: .jpg, .jpeg, .png, .gif, .webp'
                    )
        
        return image
    
    def clean_ordering(self):
        ordering = self.cleaned_data.get('ordering')
        if ordering is not None and ordering < 0:
            raise forms.ValidationError('Ordering must be a non-negative number.')
        return ordering


class GalleryImageForm(EnhancedGalleryImageForm):
    """Backward compatibility alias"""
    pass


class BlockVideoEmbedForm(forms.ModelForm):
    class Meta:
        model = BlockVideoEmbed
        fields = '__all__'
        widgets = {
            'embed_code': forms.Textarea(attrs={'rows': 4}),
            'ordering': forms.NumberInput(attrs={'min': 0}),
        }


class BlockDownloadListForm(forms.ModelForm):
    class Meta:
        model = BlockDownloadList
        fields = '__all__'
        widgets = {
            'ordering': forms.NumberInput(attrs={'min': 0}),
        }


class EnhancedDownloadFileForm(forms.ModelForm):
    """Enhanced form for download files with better validation and UI"""
    class Meta:
        model = DownloadFile
        fields = ['download_list', 'file', 'title', 'description', 'ordering']
        widgets = {
            'download_list': forms.Select(attrs={
                'class': 'form-select tw-rounded-lg',
                'required': True
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'data-max-size': '10240',  # 10MB in KB
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.zip,.rar,.txt,.jpg,.jpeg,.png,.gif'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'Enter descriptive title for the file',
                'maxlength': '200',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'Optional description of the file content',
                'rows': 3,
                'maxlength': '500'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'min': '0',
                'max': '999',
                'placeholder': '0'
            }),
        }
        help_texts = {
            'file': 'Upload a file (PDF, DOC, XLS, PPT, ZIP, images, etc.). Maximum size: 10MB.',
            'title': 'Descriptive title that users will see in the download list',
            'description': 'Optional description explaining what the file contains',
            'ordering': 'Display order within the download list (lower numbers appear first)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter active download lists
        self.fields['download_list'].queryset = BlockDownloadList.objects.filter(is_active=True).select_related('page')
        self.fields['download_list'].empty_label = "Select a download list..."
        
        # Add CSS classes for better styling
        for field_name, field in self.fields.items():
            if field_name not in ['file']:  # File field already has custom styling
                if 'class' not in field.widget.attrs:
                    field.widget.attrs.update({'class': 'form-control tw-rounded-lg'})
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 10MB)
            if hasattr(file, 'size') and file.size > 10 * 1024 * 1024:
                raise forms.ValidationError(
                    'File is too large. Maximum size allowed is 10MB. '
                    f'Your file is {file.size / (1024 * 1024):.1f}MB.'
                )
            
            # Check file name extension
            if hasattr(file, 'name'):
                allowed_extensions = [
                    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                    '.zip', '.rar', '.txt', '.jpg', '.jpeg', '.png', '.gif',
                    '.csv', '.rtf', '.odt', '.ods', '.odp'
                ]
                file_extension = os.path.splitext(file.name)[1].lower()
                if file_extension not in allowed_extensions:
                    raise forms.ValidationError(
                        f'Invalid file extension "{file_extension}". Allowed extensions: {", ".join(allowed_extensions)}'
                    )
        
        return file
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError('Title must be at least 3 characters long.')
        return title
    
    def clean_ordering(self):
        ordering = self.cleaned_data.get('ordering')
        if ordering is not None and ordering < 0:
            raise forms.ValidationError('Ordering must be a non-negative number.')
        return ordering


class DownloadFileForm(EnhancedDownloadFileForm):
    """Backward compatibility alias"""
    pass


class BlockTableHTMLForm(forms.ModelForm):
    class Meta:
        model = BlockTableHTML
        fields = '__all__'
        widgets = {
            'html': forms.Textarea(attrs={'rows': 6}),
            'ordering': forms.NumberInput(attrs={'min': 0}),
        }


class BlockFormForm(forms.ModelForm):
    class Meta:
        model = BlockForm
        fields = '__all__'
        widgets = {
            'ordering': forms.NumberInput(attrs={'min': 0}),
        }


# Search Form

class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search...',
            'autocomplete': 'off'
        }),
        label='Search'
    )
    
    category = forms.ChoiceField(
        choices=[
            ('all', 'All'),
            ('notice', 'Notices'),
            ('event', 'Events'),
            ('program', 'Programs'),
            ('page', 'Pages'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='all'
    )


# Advanced Menu Management Forms

class MenuItemMoveForm(forms.Form):
    """Form for moving menu items between menus and changing hierarchy"""
    
    menu_item = forms.ModelChoiceField(
        queryset=MenuItem.objects.all(),
        label="Menu Item to Move",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Select menu item to move...'
        }),
        help_text="Select the menu item you want to move or reorganize"
    )
    
    target_menu = forms.ModelChoiceField(
        queryset=Menu.objects.filter(is_active=True),
        label="Target Main Menu",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Select target main menu...'
        }),
        help_text="Choose which main menu this item should belong to"
    )
    
    new_parent = forms.ModelChoiceField(
        queryset=MenuItem.objects.none(),  # Will be populated dynamically
        required=False,
        label="New Parent Item (Optional)",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Select parent item or leave empty for top-level...'
        }),
        help_text="Leave empty to make this a top-level menu item, or select a parent to make it a submenu"
    )
    
    new_ordering = forms.IntegerField(
        initial=0,
        label="Display Order",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'placeholder': 'Enter display order (0 = first)'
        }),
        help_text="Lower numbers appear first in the menu"
    )
    
    update_path_type = forms.BooleanField(
        required=False,
        initial=False,
        label="Update Path Type & Link",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Check this if you want to update the link destination while moving"
    )
    
    new_path_type = forms.ChoiceField(
        choices=MenuItem.PATH_TYPE_CHOICES,
        required=False,
        label="New Path Type",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Only used if 'Update Path Type & Link' is checked"
    )
    
    new_external_url = forms.URLField(
        required=False,
        label="New External URL",
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com'
        }),
        help_text="Only used if path type is 'External'"
    )
    
    new_page = forms.ModelChoiceField(
        queryset=Page.objects.filter(is_active=True),
        required=False,
        label="New Page",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Select page...'
        }),
        help_text="Only used if path type is 'Internal'"
    )
    
    preserve_children = forms.BooleanField(
        required=False,
        initial=True,
        label="Move Children Too",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="If checked, all child menu items will also be moved"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter menu items to show hierarchy
        menu_items = MenuItem.objects.select_related('menu', 'parent').filter(is_active=True)
        choices = []
        
        for item in menu_items:
            if item.parent:
                display_name = f"{item.menu.title} → {item.parent.title} → {item.title}"
            else:
                display_name = f"{item.menu.title} → {item.title}"
            choices.append((item.id, display_name))
        
        self.fields['menu_item'].choices = [('', '---------')] + choices
        
        # Update new_parent queryset when target_menu is selected (handled by JavaScript)
        self.fields['new_parent'].queryset = MenuItem.objects.none()
    
    def clean(self):
        cleaned_data = super().clean()
        menu_item = cleaned_data.get('menu_item')
        target_menu = cleaned_data.get('target_menu')
        new_parent = cleaned_data.get('new_parent')
        update_path_type = cleaned_data.get('update_path_type')
        new_path_type = cleaned_data.get('new_path_type')
        new_external_url = cleaned_data.get('new_external_url')
        new_page = cleaned_data.get('new_page')
        
        # Validate that we're not creating circular references
        if menu_item and new_parent:
            # Check if menu_item is an ancestor of new_parent
            current = new_parent
            while current:
                if current == menu_item:
                    raise ValidationError("Cannot move menu item to be a child of itself or its descendants")
                current = current.parent
        
        # Validate parent belongs to target menu
        if new_parent and target_menu and new_parent.menu != target_menu:
            raise ValidationError("Parent menu item must belong to the target menu")
        
        # Validate path type fields if updating
        if update_path_type and new_path_type:
            if new_path_type == 'external' and not new_external_url:
                raise ValidationError("External URL is required when path type is External")
            elif new_path_type == 'internal' and not new_page:
                raise ValidationError("Page selection is required when path type is Internal")
        
        return cleaned_data


class BulkMenuMoveForm(forms.Form):
    """Form for bulk moving multiple menu items"""
    
    menu_items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.all(),
        label="Menu Items to Move",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        help_text="Select multiple menu items to move together"
    )
    
    target_menu = forms.ModelChoiceField(
        queryset=Menu.objects.filter(is_active=True),
        label="Target Main Menu",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Select target main menu...'
        }),
        help_text="All selected items will be moved to this menu"
    )
    
    make_submenu_of = forms.ModelChoiceField(
        queryset=MenuItem.objects.none(),
        required=False,
        label="Make Submenu Of (Optional)",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Select parent item or leave empty...'
        }),
        help_text="Leave empty to make all items top-level, or select a parent"
    )
    
    starting_order = forms.IntegerField(
        initial=0,
        label="Starting Display Order",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        }),
        help_text="Items will be ordered sequentially starting from this number"
    )
    
    preserve_hierarchy = forms.BooleanField(
        required=False,
        initial=True,
        label="Preserve Existing Hierarchy",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="If checked, parent-child relationships between selected items will be maintained"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter menu items to show hierarchy
        menu_items = MenuItem.objects.select_related('menu', 'parent').filter(is_active=True)
        
        self.fields['menu_items'].queryset = MenuItem.objects.filter(is_active=True)
        self.fields['make_submenu_of'].queryset = MenuItem.objects.none()
    
    def clean(self):
        cleaned_data = super().clean()
        menu_items = cleaned_data.get('menu_items')
        target_menu = cleaned_data.get('target_menu')
        make_submenu_of = cleaned_data.get('make_submenu_of')
        
        if menu_items and make_submenu_of:
            # Check that make_submenu_of is not in the list of items to move
            if make_submenu_of in menu_items:
                raise ValidationError("Cannot make items submenu of an item that is also being moved")
            
            # Check that parent belongs to target menu
            if make_submenu_of.menu != target_menu:
                raise ValidationError("Parent menu item must belong to the target menu")
        
        return cleaned_data


class MenuTreeReorganizeForm(forms.Form):
    """Form for tree-based menu reorganization"""
    
    menu = forms.ModelChoiceField(
        queryset=Menu.objects.filter(is_active=True),
        label="Menu to Reorganize",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Select menu to reorganize...'
        }),
        help_text="Choose which menu's structure you want to reorganize"
    )
    
    tree_data = forms.CharField(
        widget=forms.HiddenInput(),
        help_text="JSON data representing the new menu structure"
    )
    
    def clean_tree_data(self):
        tree_data = self.cleaned_data.get('tree_data')
        if tree_data:
            try:
                import json
                data = json.loads(tree_data)
                if not isinstance(data, list):
                    raise ValidationError("Tree data must be a list")
                return data
            except (json.JSONDecodeError, ValueError):
                raise ValidationError("Invalid tree data format")
        return []


class MenuImportForm(forms.Form):
    """Form for importing menu structure"""
    
    import_file = forms.FileField(
        label="Menu Structure File",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.json,.csv,.xlsx'
        }),
        help_text="Upload a JSON, CSV, or Excel file containing menu structure"
    )
    
    target_menu = forms.ModelChoiceField(
        queryset=Menu.objects.filter(is_active=True),
        required=False,
        label="Target Menu (Optional)",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Create new menu or select existing...'
        }),
        help_text="Leave empty to create a new menu, or select existing to append/replace"
    )
    
    new_menu_title = forms.CharField(
        max_length=100,
        required=False,
        label="New Menu Title",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new menu title...'
        }),
        help_text="Required if no target menu selected"
    )
    
    import_mode = forms.ChoiceField(
        choices=[
            ('append', 'Append to existing menu'),
            ('replace', 'Replace existing menu items'),
            ('create_new', 'Create new menu')
        ],
        initial='create_new',
        label="Import Mode",
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        help_text="Choose how to handle the import"
    )
    
    activate_imported = forms.BooleanField(
        required=False,
        initial=True,
        label="Activate Imported Items",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Check to make all imported menu items active"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        target_menu = cleaned_data.get('target_menu')
        new_menu_title = cleaned_data.get('new_menu_title')
        import_mode = cleaned_data.get('import_mode')
        
        if import_mode == 'create_new' and not new_menu_title:
            raise ValidationError("New menu title is required when creating a new menu")
        
        if import_mode in ['append', 'replace'] and not target_menu:
            raise ValidationError("Target menu is required for append/replace modes")
        
        return cleaned_data


class MenuExportForm(forms.Form):
    """Form for exporting menu structure"""
    
    menu = forms.ModelChoiceField(
        queryset=Menu.objects.filter(is_active=True),
        label="Menu to Export",
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Select menu to export...'
        }),
        help_text="Choose which menu structure to export"
    )
    
    export_format = forms.ChoiceField(
        choices=[
            ('json', 'JSON Format'),
            ('csv', 'CSV Format'),
            ('xlsx', 'Excel Format')
        ],
        initial='json',
        label="Export Format",
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        help_text="Choose the export format"
    )
    
    include_inactive = forms.BooleanField(
        required=False,
        initial=False,
        label="Include Inactive Items",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Check to include inactive menu items in export"
    )
    
    include_metadata = forms.BooleanField(
        required=False,
        initial=True,
        label="Include Metadata",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Include creation dates, ordering, and other metadata"
    )


class QuickMenuEditForm(forms.ModelForm):
    """Quick edit form for menu items"""
    
    class Meta:
        model = MenuItem
        fields = ['title', 'menu', 'parent', 'path_type', 'external_url', 'page', 'icon_class', 'is_active', 'ordering']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Menu item title...'
            }),
            'menu': forms.Select(attrs={
                'class': 'form-control select2'
            }),
            'parent': forms.Select(attrs={
                'class': 'form-control select2',
                'data-placeholder': 'Select parent or leave empty for top-level...'
            }),
            'path_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'external_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'page': forms.Select(attrs={
                'class': 'form-control select2'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-home'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter parent choices to exclude self and descendants
        if self.instance and self.instance.pk:
            # Get all descendants of this item
            descendants = []
            
            def get_descendants(item):
                for child in item.children.all():
                    descendants.append(child.pk)
                    get_descendants(child)
            
            get_descendants(self.instance)
            
            # Exclude self and descendants from parent choices
            exclude_ids = [self.instance.pk] + descendants
            
            if self.instance.menu:
                self.fields['parent'].queryset = MenuItem.objects.filter(
                    menu=self.instance.menu,
                    is_active=True
                ).exclude(pk__in=exclude_ids)
            else:
                self.fields['parent'].queryset = MenuItem.objects.none()
        else:
            self.fields['parent'].queryset = MenuItem.objects.filter(is_active=True)
        
        # Filter active pages and menus
        self.fields['page'].queryset = Page.objects.filter(is_active=True)
        self.fields['menu'].queryset = Menu.objects.filter(is_active=True)
    
    def clean(self):
        cleaned_data = super().clean()
        path_type = cleaned_data.get('path_type')
        external_url = cleaned_data.get('external_url')
        page = cleaned_data.get('page')
        parent = cleaned_data.get('parent')
        menu = cleaned_data.get('menu')
        
        # Validate path type requirements
        if path_type == 'external' and not external_url:
            raise ValidationError("External URL is required when path type is External")
        
        if path_type == 'internal' and not page:
            raise ValidationError("Page selection is required when path type is Internal")
        
        # Validate parent belongs to same menu
        if parent and menu and parent.menu != menu:
            raise ValidationError("Parent menu item must belong to the same menu")
        
        return cleaned_data


# IQAC Forms

class IQACFeedbackForm(forms.ModelForm):
    """Comprehensive feedback form for IQAC stakeholders"""
    
    class Meta:
        model = IQACFeedback
        fields = [
            'name', 'email', 'phone', 'feedback_type',
            'teaching_quality', 'infrastructure', 'administration', 'library_resources',
            'overall_satisfaction', 'suggestions', 'strengths', 'areas_for_improvement'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91-XXXXXXXXXX (Optional)'
            }),
            'feedback_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'teaching_quality': forms.Select(attrs={
                'class': 'form-select rating-select',
                'required': True
            }),
            'infrastructure': forms.Select(attrs={
                'class': 'form-select rating-select',
                'required': True
            }),
            'administration': forms.Select(attrs={
                'class': 'form-select rating-select',
                'required': True
            }),
            'library_resources': forms.Select(attrs={
                'class': 'form-select rating-select',
                'required': True
            }),
            'overall_satisfaction': forms.Select(attrs={
                'class': 'form-select rating-select',
                'required': True
            }),
            'suggestions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please provide your suggestions for improvement...',
                'required': True
            }),
            'strengths': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What do you think are the strengths of our institution? (Optional)'
            }),
            'areas_for_improvement': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Which areas do you think need improvement? (Optional)'
            })
        }
        
        help_texts = {
            'name': 'Your full name as you would like it to appear',
            'email': 'Valid email address for any follow-up communication',
            'phone': 'Optional phone number for contact',
            'feedback_type': 'Select the category that best describes you',
            'teaching_quality': 'Rate the overall teaching quality and methods',
            'infrastructure': 'Rate the physical infrastructure and facilities',
            'administration': 'Rate the administrative services and processes',
            'library_resources': 'Rate the library facilities and resources',
            'overall_satisfaction': 'Your overall satisfaction with the institution',
            'suggestions': 'Your valuable suggestions for improvement',
            'strengths': 'What you think the institution does well',
            'areas_for_improvement': 'Areas where you see room for improvement'
        }
        
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'feedback_type': 'I am a',
            'teaching_quality': 'Teaching Quality',
            'infrastructure': 'Infrastructure & Facilities',
            'administration': 'Administrative Services',
            'library_resources': 'Library Resources',
            'overall_satisfaction': 'Overall Satisfaction',
            'suggestions': 'Suggestions for Improvement',
            'strengths': 'Institutional Strengths',
            'areas_for_improvement': 'Areas for Improvement'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes for better styling
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if field_name in ['suggestions', 'strengths', 'areas_for_improvement']:
                    field.widget.attrs['class'] = 'form-control'
                elif 'rating' in field_name or field_name in ['teaching_quality', 'infrastructure', 'administration', 'library_resources', 'overall_satisfaction']:
                    field.widget.attrs['class'] = 'form-select rating-select'
                elif field_name == 'feedback_type':
                    field.widget.attrs['class'] = 'form-select'
                else:
                    field.widget.attrs['class'] = 'form-control'
        
        # Add star rating classes for rating fields
        rating_fields = ['teaching_quality', 'infrastructure', 'administration', 'library_resources', 'overall_satisfaction']
        for field_name in rating_fields:
            self.fields[field_name].widget.attrs['data-rating-field'] = 'true'
        
        # Add character counters for text areas
        self.fields['suggestions'].widget.attrs.update({
            'maxlength': '1000',
            'data-counter': 'true',
            'data-counter-target': 'suggestions-counter'
        })
        
        self.fields['strengths'].widget.attrs.update({
            'maxlength': '500',
            'data-counter': 'true',
            'data-counter-target': 'strengths-counter'
        })
        
        self.fields['areas_for_improvement'].widget.attrs.update({
            'maxlength': '500',
            'data-counter': 'true',
            'data-counter-target': 'improvement-counter'
        })
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 2:
                raise forms.ValidationError('Name must be at least 2 characters long.')
            # Remove extra spaces
            name = ' '.join(name.split())
        return name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            phone = phone.strip()
            # Basic phone validation
            import re
            if not re.match(r'^[\+]?[1-9][\d\s\-\(\)]{8,15}$', phone):
                raise forms.ValidationError(
                    'Please enter a valid phone number. Example: +91-9425540666'
                )
        return phone
    
    def clean_suggestions(self):
        suggestions = self.cleaned_data.get('suggestions')
        if suggestions:
            suggestions = suggestions.strip()
            if len(suggestions) < 10:
                raise forms.ValidationError('Please provide more detailed suggestions (at least 10 characters).')
        return suggestions
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check that at least one rating is provided
        rating_fields = ['teaching_quality', 'infrastructure', 'administration', 'library_resources', 'overall_satisfaction']
        ratings = [cleaned_data.get(field) for field in rating_fields]
        
        if not any(ratings):
            raise forms.ValidationError('Please provide at least one rating.')
        
        # Validate that all required ratings are provided
        missing_ratings = []
        for field in rating_fields:
            if not cleaned_data.get(field):
                missing_ratings.append(self.fields[field].label)
        
        if missing_ratings:
            raise forms.ValidationError(f'Please provide ratings for: {", ".join(missing_ratings)}')
        
        return cleaned_data


class IQACInfoForm(forms.ModelForm):
    """Admin form for IQAC information management"""
    
    class Meta:
        model = IQACInfo
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Internal Quality Assurance Cell'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Excellence in Education through Quality Assurance'
            }),
            'overview': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'vision': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'mission': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'objectives': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'years_of_excellence': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100'
            }),
            'quality_initiatives': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'naac_grade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'A++'
            }),
            'quality_compliance': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '100%'
            }),
            'coordinator_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dr. John Doe'
            }),
            'coordinator_designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IQAC Coordinator'
            }),
            'office_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Administrative Block, Room 101'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91-XXXXXXXXXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'iqac@college.edu'
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '160',
                'placeholder': 'Internal Quality Assurance Cell - Ensuring excellence in education...'
            })
        }


class IQACReportForm(forms.ModelForm):
    """Form for managing IQAC reports"""
    
    class Meta:
        model = IQACReport
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Annual Quality Assurance Report 2023-24'
            }),
            'academic_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '2023-24',
                'pattern': r'\d{4}-\d{2}'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of the report content...'
            }),
            'report_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'cover_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'publish_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }
    
    def clean_academic_year(self):
        academic_year = self.cleaned_data.get('academic_year')
        if academic_year:
            import re
            if not re.match(r'^\d{4}-\d{2}$', academic_year):
                raise forms.ValidationError('Academic year must be in format YYYY-YY (e.g., 2023-24)')
        return academic_year


class SideMenuForm(forms.ModelForm):
    """Form for managing side menus"""
    
    class Meta:
        model = SideMenu
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IQAC Side Menu'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Description of this side menu...'
            }),
            'menu_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IQAC Navigation'
            }),
            'url_pattern': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '/iqac/'
            }),
            'page_slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'iqac-main'
            }),
            'section_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'iqac'
            }),
            'priority': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            })
        }


class SideMenuItemForm(forms.ModelForm):
    """Form for managing side menu items"""
    
    class Meta:
        model = SideMenuItem
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IQAC Overview'
            }),
            'external_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'named_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'college_website:iqac'
            }),
            'anchor_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'overview'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-file-alt'
            }),
            'badge_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'New'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional description...'
            }),
            'custom_css_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'custom-class'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            })
        }
