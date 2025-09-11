import os
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django_ckeditor_5.widgets import CKEditor5Widget
from datetime import datetime
from .models import (
    ScrollingNotification, HeaderInfo, NavbarInfo, CollegeInfo, Program, Event, Notice, SocialInitiative, 
    StudentTestimonial, ImportantLink, ContactMessage, AdmissionInquiry,
    Menu, MenuItem, Page, BlockRichText, BlockImageGallery,
    BlockVideoEmbed, BlockDownloadList, BlockTableHTML, BlockForm,
    GalleryImage, DownloadFile, TopUtilityBar, CustomLink,
    IQACInfo, IQACReport, NAACInfo, NIRFInfo, AccreditationInfo, IQACFeedback, 
<<<<<<< HEAD
    QualityInitiative, SideMenu, SideMenuItem, VisionMissionContent, CoreValue, HeroBanner,
    ExamTimetable, ExamTimetableWeek, ExamTimetableTimeSlot, ExamTimetableExam, QuestionPaper, RevaluationInfo, ExamRulesInfo, ResearchCenterInfo,
    PublicationInfo, Publication, PatentsProjectsInfo, Patent, ResearchProject, IndustryCollaboration,
    ConsultancyInfo, ConsultancyService, ConsultancyExpertise, ConsultancySuccessStory,
    Student, StudentDocument, StudentLoginLog,
    NSSNCCClub, NSSNCCNotice, NSSNCCGallery, NSSNCCAchievement,
    HeroCarouselSlide, HeroCarouselSettings
=======
    QualityInitiative, SideMenu, SideMenuItem,
    InfrastructureInfo, InfrastructureStatistic, AcademicFacility, SportsFacility, TechnologyInfrastructure, StudentAmenity, InfrastructurePhoto,
    AcademicCalendar, AcademicEvent
>>>>>>> a11168e (Fix)
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
            # Brand/Logo settings
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
            
            # Color fields
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
            
            # Navbar dimensions and spacing
            'navbar_height': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '20',
                'max': '100',
                'step': '1'
            }),
            'navbar_padding_top': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '2',
                'step': '0.1'
            }),
            'navbar_padding_bottom': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '2',
                'step': '0.1'
            }),
            'navbar_padding_horizontal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '2',
                'step': '0.1'
            }),
            
            # Menu item spacing
            'menu_item_padding_vertical': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '1',
                'step': '0.05'
            }),
            'menu_item_padding_horizontal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '1',
                'step': '0.05'
            }),
            'menu_item_margin': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '0.1',
                'step': '0.001'
            }),
            'menu_item_gap': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '0.1',
                'step': '0.001'
            }),
            'menu_item_border_radius': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'step': '0.5'
            }),
            
            # Font settings
            'brand_font_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.5',
                'max': '2',
                'step': '0.05'
            }),
            'menu_font_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.5',
                'max': '1.5',
                'step': '0.05'
            }),
            'menu_line_height': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '2',
                'step': '0.1'
            }),
            
            # Logo settings
            'logo_height': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '15',
                'max': '60',
                'step': '1'
            }),
            
            # Responsive breakpoints
            'mobile_breakpoint': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '600',
                'max': '1200',
                'step': '1'
            }),
            'tablet_breakpoint': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '600',
                'max': '1000',
                'step': '1'
            }),
            
            # Mobile specific settings
            'mobile_navbar_height': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '20',
                'max': '80',
                'step': '1'
            }),
            'mobile_padding_horizontal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '1',
                'step': '0.05'
            }),
            'mobile_menu_font_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.5',
                'max': '1',
                'step': '0.05'
            }),
            'mobile_brand_font_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.5',
                'max': '1.5',
                'step': '0.05'
            }),
            'mobile_logo_height': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '15',
                'max': '40',
                'step': '1'
            }),
            
            # Dropdown settings
            'dropdown_padding': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '2',
                'step': '0.1'
            }),
            'dropdown_item_padding_vertical': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '1',
                'step': '0.05'
            }),
            'dropdown_item_padding_horizontal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '2',
                'step': '0.1'
            }),
            'dropdown_item_font_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.5',
                'max': '1.5',
                'step': '0.05'
            }),
            'dropdown_item_margin': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '1',
                'step': '0.05'
            }),
            
            # Mega menu settings
            'mega_menu_padding': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '2',
                'step': '0.1'
            }),
            'mega_menu_columns': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '6',
                'step': '1'
            }),
            'mega_menu_width': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'auto, 100%, 800px, etc.'
            }),
            
            # Animation settings
            'transition_duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.1',
                'max': '2',
                'step': '0.1'
            }),
            'hover_scale': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '1.5',
                'step': '0.01'
            }),
            
            # Shadow and border settings
            'box_shadow': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CSS box-shadow value'
            }),
            'border_radius': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20',
                'step': '0.5'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate responsive breakpoints
        mobile_breakpoint = cleaned_data.get('mobile_breakpoint')
        tablet_breakpoint = cleaned_data.get('tablet_breakpoint')
        
        if mobile_breakpoint and tablet_breakpoint:
            if mobile_breakpoint <= tablet_breakpoint:
                raise forms.ValidationError("Mobile breakpoint must be greater than tablet breakpoint.")
        
        # Validate mega menu columns
        mega_menu_columns = cleaned_data.get('mega_menu_columns')
        if mega_menu_columns and (mega_menu_columns < 1 or mega_menu_columns > 6):
            raise forms.ValidationError("Mega menu columns must be between 1 and 6.")
        
        # Validate navbar height
        navbar_height = cleaned_data.get('navbar_height')
        mobile_navbar_height = cleaned_data.get('mobile_navbar_height')
        
        if navbar_height and (navbar_height < 20 or navbar_height > 100):
            raise forms.ValidationError("Navbar height must be between 20 and 100 pixels.")
        
        if mobile_navbar_height and (mobile_navbar_height < 20 or mobile_navbar_height > 80):
            raise forms.ValidationError("Mobile navbar height must be between 20 and 80 pixels.")
        
        return cleaned_data


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
    """Enhanced form for Program model with comprehensive fields and better organization"""
    
    class Meta:
        model = Program
        fields = '__all__'
        widgets = {
            # Basic Information
            'description': CKEditor5Widget(),
            'curriculum': CKEditor5Widget(),
            'eligibility': CKEditor5Widget(),
            'admission_process': CKEditor5Widget(),
            'career_opportunities': CKEditor5Widget(),
            
            # Course Syllabus
            'first_year_subjects': CKEditor5Widget(),
            'second_year_subjects': CKEditor5Widget(),
            'third_year_subjects': CKEditor5Widget(),
            'elective_options': CKEditor5Widget(),
            
            # CO-PO Information
            'program_outcomes': CKEditor5Widget(),
            'course_outcomes': CKEditor5Widget(),
            'co_po_mapping': CKEditor5Widget(),
            
            # Timetable Information
            'timetable_info': CKEditor5Widget(),
            'weekly_schedule': CKEditor5Widget(),
            
            # Career Prospects
            'teaching_careers': CKEditor5Widget(),
            'media_journalism_careers': CKEditor5Widget(),
            'government_careers': CKEditor5Widget(),
            'private_sector_careers': CKEditor5Widget(),
            'further_studies': CKEditor5Widget(),
            'entrepreneurship': CKEditor5Widget(),
            
            # Course Features
            'expert_faculty': CKEditor5Widget(),
            'infrastructure': CKEditor5Widget(),
            'research_opportunities': CKEditor5Widget(),
            'industry_connect': CKEditor5Widget(),
            'additional_benefits': CKEditor5Widget(),
            'assessment_methods': CKEditor5Widget(),
            'global_opportunities': CKEditor5Widget(),
            
            # File Uploads
            'brochure': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
            'program_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            
            # Number Inputs
            'established_year': forms.NumberInput(attrs={'min': '1900', 'max': '2030'}),
            'minimum_percentage': forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '0.01'}),
            'fees': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
            'total_seats': forms.NumberInput(attrs={'min': '1'}),
            
            # Text Inputs
            'class_timings': forms.TextInput(attrs={'placeholder': 'e.g., 9:00 AM - 1:15 PM'}),
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Bachelor of Arts in English Literature'}),
            'short_name': forms.TextInput(attrs={'placeholder': 'e.g., B.A. English'}),
            'duration': forms.TextInput(attrs={'placeholder': 'e.g., 3 years'}),
            'department': forms.TextInput(attrs={'placeholder': 'e.g., Department of Arts'}),
            'entrance_exam': forms.TextInput(attrs={'placeholder': 'e.g., CUET, College Entrance Test'}),
            'accreditation': forms.TextInput(attrs={'placeholder': 'e.g., UGC, AICTE'}),
            'average_salary': forms.TextInput(attrs={'placeholder': 'e.g., ₹3-5 LPA'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            # Add specific styling for different field types
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs['class'] += ' form-control'
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] += ' form-control'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] += ' form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] += ' form-check-input'
        
        # Add help text and placeholders
        self.fields['name'].help_text = 'Enter the full program name (e.g., Bachelor of Technology in Computer Science)'
        self.fields['short_name'].help_text = 'Enter abbreviated name (e.g., B.Tech CSE)'
        self.fields['duration'].help_text = 'Program duration (e.g., 3 years, 4 years, 2 years)'
        self.fields['minimum_percentage'].help_text = 'Minimum percentage required for admission'
        self.fields['fees'].help_text = 'Annual fees in INR'
        self.fields['average_salary'].help_text = 'Expected salary range (e.g., ₹3-5 LPA)'
    
    def clean_minimum_percentage(self):
        percentage = self.cleaned_data.get('minimum_percentage')
        if percentage is not None and (percentage < 0 or percentage > 100):
            raise forms.ValidationError('Percentage must be between 0 and 100.')
        return percentage
    
    def clean_fees(self):
        fees = self.cleaned_data.get('fees')
        if fees is not None and fees < 0:
            raise forms.ValidationError('Fees cannot be negative.')
        return fees
    
    def clean_total_seats(self):
        seats = self.cleaned_data.get('total_seats')
        if seats is not None and seats < 1:
            raise forms.ValidationError('Total seats must be at least 1.')
        return seats


class ProgramCreateForm(ProgramForm):
    """Form specifically for creating new programs"""
    
    class Meta(ProgramForm.Meta):
        fields = [
            'name', 'short_name', 'discipline', 'degree_type', 'description',
            'duration', 'total_seats', 'department', 'eligibility',
            'minimum_percentage', 'entrance_exam', 'fees', 'program_image',
            'is_featured', 'is_active'
        ]


class ProgramUpdateForm(ProgramForm):
    """Form specifically for updating existing programs"""
    
    class Meta(ProgramForm.Meta):
        fields = '__all__'
        exclude = ['slug']  # Don't allow slug editing


class ProgramQuickEditForm(forms.ModelForm):
    """Quick edit form for basic program information"""
    
    class Meta:
        model = Program
        fields = [
            'name', 'short_name', 'discipline', 'degree_type', 'duration',
            'total_seats', 'fees', 'is_featured', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'discipline': forms.Select(attrs={'class': 'form-select'}),
            'degree_type': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'fees': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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


class AdmissionInquiryForm(forms.ModelForm):
    """Comprehensive admission inquiry form with Bootstrap 5 and Tailwind CSS styling"""
    
    class Meta:
        model = AdmissionInquiry
        fields = [
            'full_name', 'email', 'phone', 'current_qualification', 'percentage_marks',
            'inquiry_type', 'program_interest', 'specific_course', 'message',
            'preferred_contact_method', 'newsletter_subscription'
        ]
        
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm border-2',
                'placeholder': 'Enter your full name',
                'required': True,
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'Enter your complete name as it appears on your documents'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control rounded-3 shadow-sm border-2',
                'placeholder': 'your.email@example.com',
                'required': True,
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'We will use this email to communicate with you'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm border-2',
                'placeholder': '+91-XXXXXXXXXX',
                'required': True,
                'pattern': r'^[\+]?[1-9][\d\s\-\(\)]{8,15}$',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'Enter your contact number with country code'
            }),
            'current_qualification': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm border-2',
                'placeholder': 'e.g., 12th Pass, B.A., B.Sc., M.A., etc.',
                'required': True,
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'Your highest completed qualification'
            }),
            'percentage_marks': forms.NumberInput(attrs={
                'class': 'form-control rounded-3 shadow-sm border-2',
                'placeholder': 'e.g., 85.5',
                'min': '0',
                'max': '100',
                'step': '0.01',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'Percentage marks in your latest qualification (optional)'
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form-select rounded-3 shadow-sm border-2',
                'required': True,
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'Select the type of inquiry you have'
            }),
            'program_interest': forms.Select(attrs={
                'class': 'form-select rounded-3 shadow-sm border-2',
                'required': True,
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'Which program level are you interested in?'
            }),
            'specific_course': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm border-2',
                'placeholder': 'e.g., B.Sc Computer Science, M.A English, etc.',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'If you know the specific course name, please mention it'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control rounded-3 shadow-sm border-2',
                'rows': 5,
                'placeholder': 'Please share your specific questions, requirements, or any additional information you would like us to know...',
                'required': True,
                'maxlength': '1000',
                'data-counter': 'true',
                'data-counter-target': 'message-counter',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'Please provide detailed information about your inquiry'
            }),
            'preferred_contact_method': forms.RadioSelect(attrs={
                'class': 'form-check-input',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'How would you prefer us to contact you?'
            }),
            'newsletter_subscription': forms.CheckboxInput(attrs={
                'class': 'form-check-input rounded shadow-sm',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'Subscribe to receive updates about courses, events, and announcements'
            })
        }
        
        help_texts = {
            'full_name': 'Please enter your complete name as it appears on your official documents',
            'email': 'We will use this email address for all communication regarding your inquiry',
            'phone': 'Include country code (e.g., +91 for India). We may call you for urgent communications',
            'current_qualification': 'Your highest completed educational qualification',
            'percentage_marks': 'Optional: Your percentage/CGPA in the latest qualification for eligibility assessment',
            'inquiry_type': 'Select the category that best describes your inquiry',
            'program_interest': 'Choose the program level you are interested in',
            'specific_course': 'Optional: If you know the specific course name, please mention it',
            'message': 'Please provide detailed information about your requirements, questions, or concerns',
            'preferred_contact_method': 'How would you like us to contact you with our response?',
            'newsletter_subscription': 'Stay updated with our latest courses, events, and important announcements'
        }
        
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'current_qualification': 'Current Highest Qualification',
            'percentage_marks': 'Percentage/Marks (Optional)',
            'inquiry_type': 'Type of Inquiry',
            'program_interest': 'Program Interest',
            'specific_course': 'Specific Course (Optional)',
            'message': 'Your Message/Questions',
            'preferred_contact_method': 'Preferred Contact Method',
            'newsletter_subscription': 'Subscribe to Newsletter'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add required field indicators
        required_fields = ['full_name', 'email', 'phone', 'current_qualification', 'inquiry_type', 'program_interest', 'message']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                # Add visual indicator for required fields
                if 'class' in self.fields[field_name].widget.attrs:
                    self.fields[field_name].widget.attrs['class'] += ' required'
                else:
                    self.fields[field_name].widget.attrs['class'] = 'form-control required'
        
        # Customize choice fields
        self.fields['inquiry_type'].choices = [
            ('', 'Select Inquiry Type'),
            ('general', 'General Information'),
            ('eligibility', 'Eligibility Requirements'),
            ('documents', 'Required Documents'),
            ('fees', 'Fee Structure & Payment'),
            ('application', 'Application Process'),
            ('other', 'Other (Please specify in message)')
        ]
        
        self.fields['program_interest'].choices = [
            ('', 'Select Program Level'),
            ('undergraduate', 'Undergraduate (Bachelor\'s Degree)'),
            ('postgraduate', 'Postgraduate (Master\'s Degree)'),
            ('diploma', 'Diploma Courses'),
            ('certificate', 'Certificate Courses'),
            ('not_decided', 'Not Decided Yet (Need Guidance)')
        ]
        
        self.fields['preferred_contact_method'].choices = [
            ('email', 'Email (Preferred)'),
            ('phone', 'Phone Call'),
            ('both', 'Both Email & Phone')
        ]
        
        # Add custom styling classes
        self.fields['preferred_contact_method'].widget.attrs.update({
            'class': 'form-check-input me-2'
        })
        
        # Add focus and blur effects
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs.update({
                    'data-field-name': field_name,
                    'onfocus': 'this.classList.add("border-primary", "shadow-lg")',
                    'onblur': 'this.classList.remove("border-primary", "shadow-lg")'
                })
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if full_name:
            full_name = full_name.strip()
            if len(full_name) < 2:
                raise forms.ValidationError('Name must be at least 2 characters long.')
            # Check for numbers in name
            if any(char.isdigit() for char in full_name):
                raise forms.ValidationError('Name should not contain numbers.')
            # Remove extra spaces and capitalize properly
            full_name = ' '.join(word.capitalize() for word in full_name.split())
        return full_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
            # Basic email validation
            if '@' not in email or '.' not in email:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            phone = phone.strip()
            # Remove spaces, hyphens, and parentheses for validation
            phone_digits = ''.join(filter(str.isdigit, phone.replace('+', '')))
            if len(phone_digits) < 10:
                raise forms.ValidationError(
                    'Phone number must have at least 10 digits. '
                    'Example: +91-9425540666 or (555) 123-4567'
                )
            
            # Basic phone validation with country code support
            import re
            if not re.match(r'^[\+]?[1-9][\d\s\-\(\)]{8,15}$', phone):
                raise forms.ValidationError(
                    'Please enter a valid phone number with country code. '
                    'Example: +91-9425540666 or (555) 123-4567'
                )
        return phone
    
    def clean_current_qualification(self):
        qualification = self.cleaned_data.get('current_qualification')
        if qualification:
            qualification = qualification.strip()
            if len(qualification) < 2:
                raise forms.ValidationError('Please provide a valid qualification.')
            # Capitalize each word
            qualification = ' '.join(word.capitalize() for word in qualification.split())
        return qualification
    
    def clean_percentage_marks(self):
        percentage = self.cleaned_data.get('percentage_marks')
        if percentage is not None:
            if percentage < 0 or percentage > 100:
                raise forms.ValidationError('Percentage must be between 0 and 100.')
            if percentage < 35:
                raise forms.ValidationError(
                    'Please double-check your percentage. Marks below 35% are uncommon for higher education.'
                )
        return percentage
    
    def clean_specific_course(self):
        course = self.cleaned_data.get('specific_course')
        if course:
            course = course.strip()
            # Capitalize appropriately
            course = ' '.join(word.capitalize() for word in course.split())
        return course
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            message = message.strip()
            if len(message) < 10:
                raise forms.ValidationError(
                    'Please provide more detailed information (at least 10 characters).'
                )
            if len(message) > 1000:
                raise forms.ValidationError(
                    'Message is too long. Please keep it under 1000 characters.'
                )
        return message
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Cross-field validation
        program_interest = cleaned_data.get('program_interest')
        current_qualification = cleaned_data.get('current_qualification')
        percentage_marks = cleaned_data.get('percentage_marks')
        
        # Validate program interest against current qualification
        if program_interest and current_qualification:
            current_qual_lower = current_qualification.lower()
            
            # Basic eligibility checking
            if program_interest == 'undergraduate':
                if any(word in current_qual_lower for word in ['b.', 'bachelor', 'degree', 'm.', 'master']):
                    self.add_error('program_interest', 
                        'You already have a degree. Consider postgraduate programs instead.'
                    )
            elif program_interest == 'postgraduate':
                if not any(word in current_qual_lower for word in ['b.', 'bachelor', 'degree']) and '12th' in current_qual_lower:
                    self.add_error('program_interest', 
                        'Postgraduate programs typically require a bachelor\'s degree. '
                        'Consider undergraduate programs first.'
                    )
        
        # Validate contact preferences
        phone = cleaned_data.get('phone')
        preferred_contact = cleaned_data.get('preferred_contact_method')
        
        if preferred_contact in ['phone', 'both'] and not phone:
            self.add_error('preferred_contact_method', 
                'Phone number is required if you prefer phone contact.'
            )
        
        return cleaned_data


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


# ============================================================================
# STUDENT PORTAL AUTHENTICATION FORMS
# ============================================================================

class StudentRegistrationForm(UserCreationForm):
    """Enhanced student registration form with comprehensive validation and styling"""
    
    # Personal Information Fields
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'placeholder': 'Enter your first name',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Enter your first name as it appears on your documents'
        })
    )
    
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'placeholder': 'Enter your last name',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Enter your last name as it appears on your documents'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'placeholder': 'your.email@example.com',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'We will use this email for all communications'
        })
    )
    
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'placeholder': '+91-9876543210',
            'pattern': r'^[\+]?[1-9][\d\s\-\(\)]{8,15}$',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Enter your mobile number with country code'
        })
    )
    
    # Academic Information Fields
    student_id = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'placeholder': 'Enter your student ID',
            'style': 'text-transform: uppercase;',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Your official student ID provided by the college'
        })
    )
    
    course = forms.ChoiceField(
        choices=Student.COURSE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Select your enrolled course/program'
        })
    )
    
    year = forms.ChoiceField(
        choices=Student.YEAR_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Select your current academic year'
        })
    )
    
    # Terms and Newsletter
    terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input tw-w-5 tw-h-5 tw-text-blue-600 tw-rounded focus:tw-ring-blue-500',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'You must agree to the terms and conditions to register'
        })
    )
    
    newsletter = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input tw-w-5 tw-h-5 tw-text-blue-600 tw-rounded focus:tw-ring-blue-500',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Subscribe to receive updates about courses, events, and announcements'
        })
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'student_id', 'course', 'year', 'phone', 'password1', 'password2', 'terms', 'newsletter')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'placeholder': 'Create a strong password',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Password must be at least 8 characters with uppercase, lowercase, and numbers'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'placeholder': 'Confirm your password',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Re-enter the same password for confirmation'
        })
        
        # Update labels and help text
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = 'Email Address'
        self.fields['phone'].label = 'Phone Number'
        self.fields['student_id'].label = 'Student ID'
        self.fields['course'].label = 'Course/Program'
        self.fields['year'].label = 'Academic Year'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['terms'].label = 'I agree to the Terms of Service and Privacy Policy'
        self.fields['newsletter'].label = 'Subscribe to newsletter for updates and announcements'
        
        # Add help text
        self.fields['first_name'].help_text = 'Enter your first name as it appears on official documents'
        self.fields['last_name'].help_text = 'Enter your last name as it appears on official documents'
        self.fields['email'].help_text = 'We will use this email for account verification and communications'
        self.fields['phone'].help_text = 'Enter your mobile number with country code (e.g., +91-9876543210)'
        self.fields['student_id'].help_text = 'Your official student ID provided by the college'
        self.fields['course'].help_text = 'Select the course/program you are enrolled in'
        self.fields['year'].help_text = 'Select your current academic year'
        self.fields['password1'].help_text = 'Password must be at least 8 characters long and contain uppercase, lowercase, and numbers'
        self.fields['password2'].help_text = 'Enter the same password as above for verification'
        self.fields['terms'].help_text = 'You must agree to our terms and conditions to create an account'
        self.fields['newsletter'].help_text = 'Stay updated with course information, events, and important announcements'
    
    def clean_first_name(self):
        """Validate first name"""
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            first_name = first_name.strip().title()
            if len(first_name) < 2:
                raise forms.ValidationError('First name must be at least 2 characters long.')
            if not re.match(r'^[a-zA-Z\s\'\-\.]+$', first_name):
                raise forms.ValidationError('First name can only contain letters, spaces, hyphens, apostrophes, and dots.')
        return first_name
    
    def clean_last_name(self):
        """Validate last name"""
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            last_name = last_name.strip().title()
            if len(last_name) < 2:
                raise forms.ValidationError('Last name must be at least 2 characters long.')
            if not re.match(r'^[a-zA-Z\s\'\-\.]+$', last_name):
                raise forms.ValidationError('Last name can only contain letters, spaces, hyphens, apostrophes, and dots.')
        return last_name
    
    def clean_email(self):
        """Validate email and check for uniqueness"""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    'An account with this email already exists. '
                    'Please use a different email or try logging in.'
                )
            
            # Basic email validation (additional to Django's EmailField)
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise forms.ValidationError('Please enter a valid email address.')
        
        return email
    
    def clean_phone(self):
        """Validate phone number"""
        phone = self.cleaned_data.get('phone')
        if phone:
            phone = phone.strip()
            
            # Remove spaces and special characters for validation
            phone_digits = re.sub(r'[^\d+]', '', phone)
            
            # Check if it has minimum digits
            if len(re.sub(r'[^\d]', '', phone_digits)) < 10:
                raise forms.ValidationError(
                    'Phone number must have at least 10 digits. '
                    'Example: +91-9876543210 or (555) 123-4567'
                )
            
            # Basic phone validation with country code support
            if not re.match(r'^[\+]?[1-9][\d\s\-\(\)]{8,15}$', phone):
                raise forms.ValidationError(
                    'Please enter a valid phone number with country code. '
                    'Example: +91-9876543210 or (555) 123-4567'
                )
        
        return phone
    
    def clean_student_id(self):
        """Validate student ID and check for uniqueness"""
        student_id = self.cleaned_data.get('student_id')
        if student_id:
            student_id = student_id.upper().strip()
            
            # Check if student ID already exists
            if Student.objects.filter(student_id=student_id).exists():
                raise forms.ValidationError(
                    'This Student ID is already registered. '
                    'Please check your Student ID or contact administration.'
                )
            
            # Basic format validation
            if len(student_id) < 4:
                raise forms.ValidationError('Student ID must be at least 4 characters long.')
            
            if not re.match(r'^[A-Z0-9\-]+$', student_id):
                raise forms.ValidationError(
                    'Student ID can only contain uppercase letters, numbers, and hyphens.'
                )
        
        return student_id
    
    def clean_password1(self):
        """Enhanced password validation"""
        password1 = self.cleaned_data.get('password1')
        if password1:
            # Check minimum length
            if len(password1) < 8:
                raise forms.ValidationError('Password must be at least 8 characters long.')
            
            # Check for uppercase letter
            if not re.search(r'[A-Z]', password1):
                raise forms.ValidationError('Password must contain at least one uppercase letter.')
            
            # Check for lowercase letter
            if not re.search(r'[a-z]', password1):
                raise forms.ValidationError('Password must contain at least one lowercase letter.')
            
            # Check for digit
            if not re.search(r'\d', password1):
                raise forms.ValidationError('Password must contain at least one number.')
            
            # Check for common passwords
            common_passwords = ['password', '12345678', 'qwerty123', 'admin123']
            if password1.lower() in common_passwords:
                raise forms.ValidationError('This password is too common. Please choose a different one.')
        
        return password1
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        
        # Check password confirmation
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'The two password fields didn\'t match.')
        
        # Validate terms agreement
        terms = cleaned_data.get('terms')
        if not terms:
            self.add_error('terms', 'You must agree to the Terms of Service and Privacy Policy to register.')
        
        return cleaned_data
    
    def save(self, commit=True):
        """Create user and student profile"""
        # Create the user
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['student_id']  # Use student_id as username
        
        if commit:
            user.save()
            
            # Create the student profile
            student = Student.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                phone=self.cleaned_data['phone'],
                course=self.cleaned_data['course'],
                year=self.cleaned_data['year'],
                newsletter_subscription=self.cleaned_data.get('newsletter', False)
            )
        
        return user


class StudentLoginForm(AuthenticationForm):
    """Enhanced student login form with modern styling"""
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'placeholder': 'Student ID or Email',
            'autocomplete': 'username',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Enter your Student ID or registered email address'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Enter your password'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input tw-w-4 tw-h-4 tw-text-blue-600 tw-rounded focus:tw-ring-blue-500',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Keep me logged in on this device'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update labels
        self.fields['username'].label = 'Student ID or Email'
        self.fields['password'].label = 'Password'
        self.fields['remember_me'].label = 'Remember me on this device'
        
        # Add help text
        self.fields['username'].help_text = 'Enter your Student ID or registered email address'
        self.fields['password'].help_text = 'Enter your password'
        self.fields['remember_me'].help_text = 'Check this to stay logged in for up to 30 days'
    
    def clean_username(self):
        """Allow login with either student ID or email"""
        username = self.cleaned_data.get('username')
        if username:
            username = username.strip()
            
            # If it looks like an email, find the user by email
            if '@' in username:
                try:
                    user = User.objects.get(email=username.lower())
                    username = user.username
                except User.DoesNotExist:
                    raise forms.ValidationError('No account found with this email address.')
            else:
                # Convert to uppercase for student ID
                username = username.upper()
        
        return username


class StudentPasswordResetForm(PasswordResetForm):
    """Custom password reset form for students"""
    
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg rounded-3 shadow-sm tw-transition-all tw-duration-300 focus:tw-ring-2 focus:tw-ring-blue-500',
            'placeholder': 'Enter your registered email address',
            'autocomplete': 'email',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Enter the email address associated with your student account'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update labels and help text
        self.fields['email'].label = 'Email Address'
        self.fields['email'].help_text = 'Enter the email address you used to register your student account'
    
    def clean_email(self):
        """Validate email exists and is associated with a student"""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
            
            # Check if email exists
            try:
                user = User.objects.get(email=email)
                # Check if user has a student profile
                if not hasattr(user, 'student_profile'):
                    raise forms.ValidationError(
                        'This email is not associated with a student account. '
                        'Please contact administration for assistance.'
                    )
            except User.DoesNotExist:
                raise forms.ValidationError(
                    'No account found with this email address. '
                    'Please check your email or register for a new account.'
                )
        
        return email


class StudentProfileUpdateForm(forms.ModelForm):
    """Form for updating student profile information"""
    
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'middle_name', 'phone', 'alternate_phone',
            'date_of_birth', 'gender', 'address', 'city', 'state', 'pincode',
            'father_name', 'mother_name', 'guardian_phone', 'guardian_email',
            'profile_image', 'newsletter_subscription', 'sms_notifications', 
            'email_notifications'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': 'Last Name'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': 'Middle Name (Optional)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': '+91-9876543210'
            }),
            'alternate_phone': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': 'Alternate Phone (Optional)'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select rounded-3 shadow-sm'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'rows': 3,
                'placeholder': 'Complete Address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': 'State'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': 'PIN Code'
            }),
            'father_name': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': "Father's Name"
            }),
            'mother_name': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': "Mother's Name"
            }),
            'guardian_phone': forms.TextInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': "Guardian's Phone"
            }),
            'guardian_email': forms.EmailInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'placeholder': "Guardian's Email"
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',
                'accept': 'image/*'
            }),
            'newsletter_subscription': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'sms_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


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


<<<<<<< HEAD
class VisionMissionContentForm(forms.ModelForm):
    """Form for managing Vision & Mission page content dynamically"""
    
    class Meta:
        model = VisionMissionContent
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Vision & Mission Content Configuration Name'
            }),
            'hero_badge_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Our Purpose & Direction'
            }),
            'hero_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Vision & Mission'
            }),
            'hero_subtitle': CKEditor5Widget(attrs={
                'class': 'django_ckeditor_5',
            }, config_name='extends'),
            'vision_statement': CKEditor5Widget(attrs={
                'class': 'django_ckeditor_5',
            }, config_name='extends'),
            'vision_highlight_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Excellence in Education'
            }),
            'vision_highlight_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Community Impact'
            }),
            'vision_highlight_3': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Innovation & Research'
            }),
            'vision_highlight_4': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Global Perspective'
            }),
            'mission_statement': CKEditor5Widget(attrs={
                'class': 'django_ckeditor_5',
            }, config_name='extends'),
            'mission_objective_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Deliver quality education accessible to all'
            }),
            'mission_objective_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Foster research and innovation culture'
            }),
            'mission_objective_3': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Develop socially responsible citizens'
            }),
            'cta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Join Our Journey'
            }),
            'cta_description': CKEditor5Widget(attrs={
                'class': 'django_ckeditor_5',
            }, config_name='extends'),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        is_active = cleaned_data.get('is_active')
        
        # Ensure only one active content at a time
        if is_active:
            existing_active = VisionMissionContent.objects.filter(is_active=True)
            if self.instance.pk:
                existing_active = existing_active.exclude(pk=self.instance.pk)
            
            if existing_active.exists():
                raise ValidationError("Only one Vision & Mission content configuration can be active at a time. Please deactivate the current active configuration first.")
        
        return cleaned_data


class CoreValueForm(forms.ModelForm):
    """Form for managing individual core values"""
    
    class Meta:
        model = CoreValue
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Excellence'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe this core value and its importance to the institution...'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-trophy',
                'data-toggle': 'tooltip',
                'title': 'FontAwesome icon class (e.g., fas fa-trophy, fas fa-star)'
            }),
            'gradient_color': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class CoreValueInlineFormSet(forms.BaseInlineFormSet):
    """Custom formset for managing core values inline with vision mission content"""
    
    def clean(self):
        """Ensure at least one active core value exists"""
        super().clean()
        
        if any(self.errors):
            return
        
        active_values = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_active', False):
                    active_values += 1
        
        if active_values == 0:
            raise ValidationError("At least one core value must be active.")
        
        if active_values > 6:
            raise ValidationError("Maximum 6 core values can be active at once for optimal display.")


# Create the inline formset
CoreValueFormSet = forms.inlineformset_factory(
    VisionMissionContent,
    CoreValue,
    form=CoreValueForm,
    formset=CoreValueInlineFormSet,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)


class HeroBannerForm(forms.ModelForm):
    """Form for editing hero banner content and styling"""
    
    class Meta:
        model = HeroBanner
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter hero title...',
                'maxlength': '200'
            }),
            'subtitle': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter hero subtitle...'
            }),
            'primary_button_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Get Started'
            }),
            'primary_button_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'secondary_button_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Learn More'
            }),
            'secondary_button_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'background_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'background-type-select'
            }),
            'gradient_start_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'gradient_end_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'gradient_direction': forms.Select(attrs={
                'class': 'form-select'
            }),
            'solid_background_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'background_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'background_image_opacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'type': 'range'
            }),
            'background_video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.youtube.com/watch?v=...'
            }),
            'title_font_family': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title_font_size': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title_font_weight': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subtitle_font_family': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subtitle_font_size': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'subtitle_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'primary_button_bg_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'primary_button_text_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'secondary_button_bg_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'secondary_button_text_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'secondary_button_border_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'padding_top': forms.Select(attrs={
                'class': 'form-select'
            }),
            'content_alignment': forms.Select(attrs={
                'class': 'form-select'
            }),
            'enable_animations': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'animation_duration': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            # Two-color title support
            'title_highlight_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 18+ Courses',
                'maxlength': '100'
            }),
            'title_highlight_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            # Statistics Cards Customization
            'show_statistics': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'stat_1_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-calendar-alt'
            }),
            'stat_1_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '25+'
            }),
            'stat_1_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years Experience'
            }),
            'stat_1_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'stat_2_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-users'
            }),
            'stat_2_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '8000+'
            }),
            'stat_2_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Students'
            }),
            'stat_2_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'stat_3_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-book-open'
            }),
            'stat_3_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '18+'
            }),
            'stat_3_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Courses'
            }),
            'stat_3_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'stat_4_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-lock'
            }),
            'stat_4_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '95%'
            }),
            'stat_4_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Placement'
            }),
            'stat_4_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            # Accreditations Customization
            'show_accreditations': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'accred_1_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UGC Recognized'
            }),
            'accred_1_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-star'
            }),
            'accred_1_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'accred_2_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NAAC Grade A'
            }),
            'accred_2_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-star'
            }),
            'accred_2_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'accred_3_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3 Star IIC Rating'
            }),
            'accred_3_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-map-marker-alt'
            }),
            'accred_3_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            # Statistics Cards Customization
            'show_statistics': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'stat_1_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-calendar-alt'
            }),
            'stat_1_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '25+'
            }),
            'stat_1_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years Experience'
            }),
            'stat_1_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'stat_2_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-users'
            }),
            'stat_2_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '8000+'
            }),
            'stat_2_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Students'
            }),
            'stat_2_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'stat_3_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-book-open'
            }),
            'stat_3_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '18+'
            }),
            'stat_3_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Courses'
            }),
            'stat_3_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'stat_4_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-briefcase'
            }),
            'stat_4_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '95%'
            }),
            'stat_4_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Placement'
            }),
            'stat_4_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            # Accreditations Customization
            'show_accreditations': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'accred_1_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UGC Recognized'
            }),
            'accred_1_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-shield-alt'
            }),
            'accred_1_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'accred_2_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NAAC Grade A'
            }),
            'accred_2_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-star'
            }),
            'accred_2_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'accred_3_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3 Star IIC Rating'
            }),
            'accred_3_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-map-pin'
            }),
            'accred_3_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom validation and field grouping
        self.fields['title'].required = True
        self.fields['background_type'].required = True
        
        # Add help text for better UX
        self.fields['background_video_url'].help_text = "Enter YouTube or Vimeo video URL"
        self.fields['background_image_opacity'].help_text = "Drag to adjust opacity (0-100%)"
    
    def clean(self):
        cleaned_data = super().clean()
        background_type = cleaned_data.get('background_type')
        
        # Validate background type specific fields
        if background_type == 'gradient':
            if not cleaned_data.get('gradient_start_color') or not cleaned_data.get('gradient_end_color'):
                raise forms.ValidationError("Gradient colors are required when background type is gradient.")
        
        elif background_type == 'solid':
            if not cleaned_data.get('solid_background_color'):
                raise forms.ValidationError("Solid background color is required when background type is solid.")
        
        elif background_type == 'image':
            if not cleaned_data.get('background_image'):
                raise forms.ValidationError("Background image is required when background type is image.")
        
        elif background_type == 'video':
            if not cleaned_data.get('background_video_url'):
                raise forms.ValidationError("Background video URL is required when background type is video.")
        
        # Validate button configurations
        if cleaned_data.get('primary_button_text') and not cleaned_data.get('primary_button_url'):
            raise forms.ValidationError("Primary button URL is required when primary button text is provided.")
        
        if cleaned_data.get('secondary_button_text') and not cleaned_data.get('secondary_button_url'):
            raise forms.ValidationError("Secondary button URL is required when secondary button text is provided.")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set default values for unused background types
        if instance.background_type != 'gradient':
            instance.gradient_start_color = '#1e3a8a'
            instance.gradient_end_color = '#7c3aed'
        
        if instance.background_type != 'solid':
            instance.solid_background_color = '#1e3a8a'
        
        if instance.background_type != 'image':
            instance.background_image = None
            instance.background_image_opacity = 100
        
        if instance.background_type != 'video':
            instance.background_video_url = ''
        
        if commit:
            instance.save()
        return instance


class ExamTimetableForm(forms.ModelForm):
    """Form for managing exam timetable configuration"""
    
    class Meta:
        model = ExamTimetable
        fields = [
            'name', 'academic_year', 'semester',
            'header_title', 'header_subtitle',
            'header_gradient_start', 'header_gradient_end',
            'exam_guidelines', 'morning_session_start', 'morning_session_end',
            'afternoon_session_start', 'afternoon_session_end', 'break_duration',
            'is_active', 'is_featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Semester 1 2024'
            }),
            'academic_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2024-2025'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[
                ('1st', '1st Semester'),
                ('2nd', '2nd Semester'),
                ('3rd', '3rd Semester'),
                ('4th', '4th Semester'),
            ]),
            'header_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Main header title'
            }),
            'header_subtitle': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Header subtitle description'
            }),
            'header_gradient_start': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'header_gradient_end': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'exam_guidelines': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter exam guidelines and rules...'
            }),
            'morning_session_start': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'morning_session_end': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'afternoon_session_start': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'afternoon_session_end': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'break_duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2 hours'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ExamTimetableWeekForm(forms.ModelForm):
    """Form for managing exam timetable weeks"""
    
    class Meta:
        model = ExamTimetableWeek
        fields = ['week_number', 'week_title', 'is_active']
        widgets = {
            'week_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 52
            }),
            'week_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Custom week title (optional)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ExamTimetableTimeSlotForm(forms.ModelForm):
    """Form for managing exam timetable time slots"""
    
    class Meta:
        model = ExamTimetableTimeSlot
        fields = ['start_time', 'end_time', 'is_active']
        widgets = {
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ExamTimetableExamForm(forms.ModelForm):
    """Form for managing individual exam entries"""
    
    class Meta:
        model = ExamTimetableExam
        fields = [
            'day_of_week', 'subject_name', 'room_number', 'duration', 'semester',
            'priority', 'is_featured', 'background_color', 'border_color', 'text_color', 'is_active'
        ]
        widgets = {
            'day_of_week': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subject_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mathematics, Physics, Chemistry'
            }),
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Room 101, Lab A'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2 hours, 3 hours'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[
                ('1st', '1st Semester'),
                ('2nd', '2nd Semester'),
                ('3rd', '3rd Semester'),
                ('4th', '4th Semester'),
            ]),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'background_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'border_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'text_color': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ExamTimetableBulkForm(forms.Form):
    """Form for bulk operations on exam timetable"""
    
    ACTION_CHOICES = [
        ('activate', 'Activate Selected'),
        ('deactivate', 'Deactivate Selected'),
        ('delete', 'Delete Selected'),
        ('duplicate', 'Duplicate Selected'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    selected_items = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This will be populated dynamically in the view
        self.fields['selected_items'].choices = []


class QuestionPaperForm(forms.ModelForm):
    """Form for creating and editing question papers"""
    
    class Meta:
        model = QuestionPaper
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mathematics - 1st Semester'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-select'
            }),
            'degree_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'academic_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2024-2025'
            }),
            'question_paper_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of the question paper'
            }),
            'exam_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 3 hours'
            }),
            'total_marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 1000
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_active', 'is_featured']:
                if hasattr(field.widget, 'attrs'):
                    field.widget.attrs.update({'class': 'form-control'})
                elif isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select'})
    
    def clean_question_paper_file(self):
        """Validate uploaded file"""
        file = self.cleaned_data.get('question_paper_file')
        if file:
            # Check file extension
            if not file.name.lower().endswith('.pdf'):
                raise ValidationError('Only PDF files are allowed.')
            
            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise ValidationError('File size cannot exceed 10MB.')
        
        return file
    
    def clean_total_marks(self):
        """Validate total marks"""
        total_marks = self.cleaned_data.get('total_marks')
        if total_marks is not None and total_marks <= 0:
            raise ValidationError('Total marks must be greater than 0.')
        return total_marks


class QuestionPaperCreateForm(QuestionPaperForm):
    """Form for creating new question papers"""
    
    class Meta(QuestionPaperForm.Meta):
        fields = [
            'title', 'subject', 'semester', 'degree_type', 'academic_year',
            'question_paper_file', 'description', 'exam_date', 'duration',
            'total_marks', 'is_active', 'is_featured'
        ]


class QuestionPaperUpdateForm(QuestionPaperForm):
    """Form for updating existing question papers"""
    
    class Meta(QuestionPaperForm.Meta):
        fields = '__all__'
        exclude = ['slug']  # Don't allow direct editing of slug


class QuestionPaperQuickEditForm(forms.ModelForm):
    """Quick edit form for essential question paper fields"""
    
    class Meta:
        model = QuestionPaper
        fields = ['title', 'subject', 'semester', 'academic_year', 'is_active', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mathematics - 1st Semester'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-select'
            }),
            'academic_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2024-2025'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class QuestionPaperSearchForm(forms.Form):
    """Form for searching and filtering question papers"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search question papers...'
        })
    )
    
    subject = forms.ChoiceField(
        required=False,
        choices=[('', 'All Subjects')] + QuestionPaper.SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    semester = forms.ChoiceField(
        required=False,
        choices=[('', 'All Semesters')] + QuestionPaper.SEMESTER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    degree_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Degrees')] + QuestionPaper.DEGREE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    academic_year = forms.ChoiceField(
        required=False,
        choices=[('', 'All Years')],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    is_featured = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate academic year choices dynamically
        years = QuestionPaper.get_available_years()
        self.fields['academic_year'].choices = [('', 'All Years')] + [(year, year) for year in years]


class RevaluationInfoForm(forms.ModelForm):
    """Form for managing revaluation information"""
    
    class Meta:
        model = RevaluationInfo
        fields = '__all__'
        widgets = {
            # Basic Information
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Revaluation'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Apply for revaluation of your examination papers'
            }),
            
            # Process Steps
            'step1_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Download Form'
            }),
            'step1_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Step 1 description'
            }),
            'step2_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Fill Application'
            }),
            'step2_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Step 2 description'
            }),
            'step3_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Pay Fees'
            }),
            'step3_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Step 3 description'
            }),
            'step4_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Submit Application'
            }),
            'step4_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Step 4 description'
            }),
            
            # Fee Information
            'theory_paper_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'practical_paper_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'project_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            
            # Important Dates
            'application_period': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 15 days from result declaration'
            }),
            'processing_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 30-45 days'
            }),
            'result_notification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Via SMS/Email'
            }),
            
            # Rich Text Fields
            'eligibility_rules': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'required_documents': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            
            # Contact Information
            'controller_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Dr. [Name]'
            }),
            'controller_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91-XXX-XXXX-XXX'
            }),
            'controller_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., exam@college.edu'
            }),
            'controller_office_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 9:00 AM - 5:00 PM'
            }),
            'office_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Ground Floor, Main Building'
            }),
            'office_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91-XXX-XXXX-XXX'
            }),
            'office_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., examoffice@college.edu'
            }),
            'office_working_days': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Monday to Friday'
            }),
            
            # File Uploads
            'application_form_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'guidelines_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'fee_structure_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            
            # Important Notice
            'important_notice': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Important notice text'
            }),
            
            # Status
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_active']:
                if hasattr(field.widget, 'attrs'):
                    if 'class' not in field.widget.attrs:
                        field.widget.attrs.update({'class': 'form-control'})
                elif isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select'})
    
    def clean_theory_paper_fee(self):
        """Validate theory paper fee"""
        fee = self.cleaned_data.get('theory_paper_fee')
        if fee is not None and fee < 0:
            raise ValidationError('Fee cannot be negative.')
        return fee
    
    def clean_practical_paper_fee(self):
        """Validate practical paper fee"""
        fee = self.cleaned_data.get('practical_paper_fee')
        if fee is not None and fee < 0:
            raise ValidationError('Fee cannot be negative.')
        return fee
    
    def clean_project_fee(self):
        """Validate project fee"""
        fee = self.cleaned_data.get('project_fee')
        if fee is not None and fee < 0:
            raise ValidationError('Fee cannot be negative.')
        return fee


class RevaluationInfoUpdateForm(RevaluationInfoForm):
    """Form for updating revaluation information"""
    
    class Meta(RevaluationInfoForm.Meta):
        fields = '__all__'
        exclude = ['created_at', 'updated_at']  # Exclude timestamps


class RevaluationInfoQuickEditForm(forms.ModelForm):
    """Quick edit form for essential revaluation information"""
    
    class Meta:
        model = RevaluationInfo
        fields = [
            'title', 'subtitle', 'theory_paper_fee', 'practical_paper_fee', 
            'project_fee', 'application_period', 'processing_time', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Revaluation'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Apply for revaluation of your examination papers'
            }),
            'theory_paper_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'practical_paper_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'project_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'application_period': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 15 days from result declaration'
            }),
            'processing_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 30-45 days'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ExamRulesInfoForm(forms.ModelForm):
    """Form for managing exam rules information"""
    
    class Meta:
        model = ExamRulesInfo
        fields = '__all__'
        widgets = {
            # Basic Information
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Examination Rules & Regulations'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Important guidelines and rules for all examinations'
            }),
            
            # Rich Text Fields
            'timing_rules': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'prohibited_items': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'conduct_rules': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'answer_sheet_details': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'submission_rules': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'violations_penalties': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'appeal_process': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            
            # Special Instructions
            'calculator_rules': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Calculator usage rules'
            }),
            'open_book_rules': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Open book exam rules'
            }),
            'time_extension_rules': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Time extension rules'
            }),
            
            # Contact Information
            'controller_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Dr. [Name]'
            }),
            'controller_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91-XXX-XXXX-XXX'
            }),
            'controller_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., exam@college.edu'
            }),
            'controller_office_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 9:00 AM - 5:00 PM'
            }),
            'office_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Ground Floor, Main Building'
            }),
            'office_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91-XXX-XXXX-XXX'
            }),
            'office_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., examoffice@college.edu'
            }),
            'office_working_days': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Monday to Friday'
            }),
            
            # Important Notice
            'important_notice': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Important notice text'
            }),
            
            # Status
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_active']:
                if hasattr(field.widget, 'attrs'):
                    if 'class' not in field.widget.attrs:
                        field.widget.attrs.update({'class': 'form-control'})
                elif isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select'})


class ExamRulesInfoUpdateForm(ExamRulesInfoForm):
    """Form for updating exam rules information"""
    
    class Meta(ExamRulesInfoForm.Meta):
        fields = '__all__'
        exclude = ['created_at', 'updated_at']  # Exclude timestamps


class ExamRulesInfoQuickEditForm(forms.ModelForm):
    """Quick edit form for essential exam rules information"""
    
    class Meta:
        model = ExamRulesInfo
        fields = [
            'title', 'subtitle', 'controller_name', 'controller_phone', 
            'controller_email', 'office_phone', 'office_email', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Examination Rules & Regulations'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Important guidelines and rules for all examinations'
            }),
            'controller_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Dr. [Name]'
            }),
            'controller_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91-XXX-XXXX-XXX'
            }),
            'controller_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., exam@college.edu'
            }),
            'office_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91-XXX-XXXX-XXX'
            }),
            'office_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., examoffice@college.edu'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ResearchCenterInfoForm(forms.ModelForm):
    """Form for managing research center information"""
    
    class Meta:
        model = ResearchCenterInfo
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Research Centers'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Advancing knowledge through cutting-edge research and innovation'
            }),
            'center1_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Center for Advanced Sciences'
            }),
            'center1_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description of the first research center'
            }),
            'center1_areas': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'center2_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Computer Science Research Lab'
            }),
            'center2_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description of the second research center'
            }),
            'center2_areas': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'center3_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Environmental Research Center'
            }),
            'center3_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description of the third research center'
            }),
            'center3_areas': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'lab_infrastructure': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'research_support': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'physics_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Physics research area description'
            }),
            'biology_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Biology research area description'
            }),
            'mathematics_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Mathematics research area description'
            }),
            'social_sciences_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Social sciences research area description'
            }),
            'publications_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'patents_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'conferences_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'book_chapters_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'grants_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'industry_collaborations': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'international_partnerships': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'national_awards': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'student_opportunities': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'faculty_opportunities': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'director_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Dr. [Research Director Name]'
            }),
            'director_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91-XXX-XXXX-XXX'
            }),
            'director_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., research@college.edu'
            }),
            'director_office_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 9:00 AM - 5:00 PM'
            }),
            'office_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Research Block, 2nd Floor'
            }),
            'office_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91-XXX-XXXX-XXX'
            }),
            'office_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., research.office@college.edu'
            }),
            'office_working_days': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Monday to Friday'
            }),
            'cta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Join Our Research Community'
=======
class MultipleFileInput(forms.FileInput):
    """Custom widget that supports multiple file uploads"""
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is not None:
            self.attrs.update(attrs)
        self.attrs['multiple'] = True

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)


class MultipleInfrastructurePhotoForm(forms.Form):
    """Form for uploading multiple infrastructure photos at once"""
    
    # Multiple file upload field
    images = forms.FileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp',
            'data-max-size': '5120',  # 5MB in KB
            'data-allowed-types': 'jpeg,jpg,png,gif,webp'
        }),
        help_text='Select multiple image files (JPEG, PNG, GIF, WebP). Maximum size: 5MB per file. You can select multiple files at once.',
        label='Photo Files'
    )
    
    # Common settings for all photos
    section_type = forms.ChoiceField(
        choices=InfrastructurePhoto.PHOTO_SECTIONS,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        }),
        help_text='Select the infrastructure section for all photos',
        label='Section Type'
    )
    
    academic_facility = forms.ModelChoiceField(
        queryset=AcademicFacility.objects.filter(is_active=True),
        required=False,
        empty_label="Select Academic Facility (Optional)",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text='Associate all photos with a specific academic facility (optional)',
        label='Academic Facility'
    )
    
    sports_facility = forms.ModelChoiceField(
        queryset=SportsFacility.objects.filter(is_active=True),
        required=False,
        empty_label="Select Sports Facility (Optional)",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text='Associate all photos with a specific sports facility (optional)',
        label='Sports Facility'
    )
    
    technology_infrastructure = forms.ModelChoiceField(
        queryset=TechnologyInfrastructure.objects.filter(is_active=True),
        required=False,
        empty_label="Select Technology Infrastructure (Optional)",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text='Associate all photos with specific technology infrastructure (optional)',
        label='Technology Infrastructure'
    )
    
    student_amenity = forms.ModelChoiceField(
        queryset=StudentAmenity.objects.filter(is_active=True),
        required=False,
        empty_label="Select Student Amenity (Optional)",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text='Associate all photos with a specific student amenity (optional)',
        label='Student Amenity'
    )
    
    # Common display settings
    is_featured = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text='Feature all photos prominently in the gallery',
        label='Featured Photos'
    )
    
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text='Make all photos visible on the website',
        label='Active Photos'
    )
    
    # Auto-generate titles option
    auto_generate_titles = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text='Automatically generate titles from filenames (uncheck to set custom titles)',
        label='Auto-generate Titles'
    )
    
    def clean_images(self):
        """Validate uploaded images"""
        images = self.files.getlist('images')
        
        if not images:
            raise forms.ValidationError('Please select at least one image file.')
        
        if len(images) > 20:
            raise forms.ValidationError('You can upload a maximum of 20 images at once.')
        
        for image in images:
            # Check file size (max 5MB)
            if hasattr(image, 'size') and image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    f'Image "{image.name}" is too large. Maximum size allowed is 5MB. '
                    f'Your file is {image.size / (1024 * 1024):.1f}MB.'
                )
            
            # Check file type
            if hasattr(image, 'content_type'):
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
                if image.content_type not in allowed_types:
                    raise forms.ValidationError(
                        f'Invalid file type for "{image.name}". Please upload a JPEG, PNG, GIF, or WebP image.'
                    )
            
            # Check file name extension
            if hasattr(image, 'name'):
                allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
                file_extension = os.path.splitext(image.name)[1].lower()
                if file_extension not in allowed_extensions:
                    raise forms.ValidationError(
                        f'Invalid file extension for "{image.name}". Allowed extensions: .jpg, .jpeg, .png, .gif, .webp'
                    )
        
        return images
    
    def clean(self):
        """Comprehensive form validation"""
        cleaned_data = super().clean()
        
        # Get facility selections
        academic_facility = cleaned_data.get('academic_facility')
        sports_facility = cleaned_data.get('sports_facility')
        technology_infrastructure = cleaned_data.get('technology_infrastructure')
        student_amenity = cleaned_data.get('student_amenity')
        
        # Validate that only one facility type is selected
        facility_count = sum([
            bool(academic_facility),
            bool(sports_facility),
            bool(technology_infrastructure),
            bool(student_amenity)
        ])
        
        if facility_count > 1:
            raise forms.ValidationError(
                'Please select only one facility type. All photos can only be associated with one specific facility.'
            )
        
        return cleaned_data
    
    def save(self):
        """Save multiple photos with the provided settings"""
        images = self.cleaned_data['images']
        section_type = self.cleaned_data['section_type']
        academic_facility = self.cleaned_data.get('academic_facility')
        sports_facility = self.cleaned_data.get('sports_facility')
        technology_infrastructure = self.cleaned_data.get('technology_infrastructure')
        student_amenity = self.cleaned_data.get('student_amenity')
        is_featured = self.cleaned_data.get('is_featured', False)
        is_active = self.cleaned_data.get('is_active', True)
        auto_generate_titles = self.cleaned_data.get('auto_generate_titles', True)
        
        created_photos = []
        
        for i, image in enumerate(images):
            # Generate title from filename if auto-generate is enabled
            if auto_generate_titles:
                title = os.path.splitext(image.name)[0].replace('_', ' ').replace('-', ' ').title()
            else:
                title = f"Photo {i + 1}"
            
            # Create InfrastructurePhoto instance
            photo = InfrastructurePhoto(
                title=title,
                image=image,
                section_type=section_type,
                academic_facility=academic_facility,
                sports_facility=sports_facility,
                technology_infrastructure=technology_infrastructure,
                student_amenity=student_amenity,
                is_featured=is_featured,
                is_active=is_active,
                display_order=i  # Set display order based on upload order
            )
            
            # Validate the photo instance
            photo.full_clean()
            photo.save()
            created_photos.append(photo)
        
        return created_photos


class InfrastructurePhotoForm(forms.ModelForm):
    """Enhanced form for managing individual infrastructure photos with better validation and UI"""
    
    class Meta:
        model = InfrastructurePhoto
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'placeholder': 'Enter photo title/caption',
                'maxlength': '200',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control tw-rounded-lg',
                'rows': 3,
                'placeholder': 'Enter photo description (optional)',
                'maxlength': '1000'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp',
                'data-max-size': '5120',  # 5MB in KB
                'data-allowed-types': 'jpeg,jpg,png,gif,webp'
            }),
            'section_type': forms.Select(attrs={
                'class': 'form-select tw-rounded-lg',
                'required': True
            }),
            'academic_facility': forms.Select(attrs={
                'class': 'form-select tw-rounded-lg'
            }),
            'sports_facility': forms.Select(attrs={
                'class': 'form-select tw-rounded-lg'
            }),
            'technology_infrastructure': forms.Select(attrs={
                'class': 'form-select tw-rounded-lg'
            }),
            'student_amenity': forms.Select(attrs={
                'class': 'form-select tw-rounded-lg'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control tw-rounded-lg',
                'min': '0',
                'max': '999',
                'placeholder': '0'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        help_texts = {
            'title': 'A descriptive title for the photo (required)',
            'description': 'Optional detailed description of the photo content',
            'image': 'Upload an image file (JPEG, PNG, GIF, WebP). Maximum size: 5MB. Recommended dimensions: 800x600px or larger.',
            'section_type': 'Select the infrastructure section this photo belongs to',
            'academic_facility': 'Associate this photo with a specific academic facility (optional)',
            'sports_facility': 'Associate this photo with a specific sports facility (optional)',
            'technology_infrastructure': 'Associate this photo with specific technology infrastructure (optional)',
            'student_amenity': 'Associate this photo with a specific student amenity (optional)',
            'display_order': 'Display order within the section (lower numbers appear first)',
            'is_featured': 'Feature this photo prominently in the gallery',
            'is_active': 'Make this photo visible on the website'
        }
        
        labels = {
            'title': 'Photo Title',
            'description': 'Description',
            'image': 'Photo File',
            'section_type': 'Section Type',
            'academic_facility': 'Academic Facility',
            'sports_facility': 'Sports Facility',
            'technology_infrastructure': 'Technology Infrastructure',
            'student_amenity': 'Student Amenity',
            'display_order': 'Display Order',
            'is_featured': 'Featured Photo',
            'is_active': 'Active'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add empty option for foreign key fields
        self.fields['academic_facility'].empty_label = "Select Academic Facility (Optional)"
        self.fields['sports_facility'].empty_label = "Select Sports Facility (Optional)"
        self.fields['technology_infrastructure'].empty_label = "Select Technology Infrastructure (Optional)"
        self.fields['student_amenity'].empty_label = "Select Student Amenity (Optional)"
        
        # Filter to only show active facilities
        self.fields['academic_facility'].queryset = AcademicFacility.objects.filter(is_active=True)
        self.fields['sports_facility'].queryset = SportsFacility.objects.filter(is_active=True)
        self.fields['technology_infrastructure'].queryset = TechnologyInfrastructure.objects.filter(is_active=True)
        self.fields['student_amenity'].queryset = StudentAmenity.objects.filter(is_active=True)
        
        # Add CSS classes for better styling
        for field_name, field in self.fields.items():
            if field_name not in ['image']:  # Image field already has custom styling
                if 'class' not in field.widget.attrs:
                    field.widget.attrs.update({'class': 'form-control tw-rounded-lg'})
    
    def clean_image(self):
        """Validate uploaded image"""
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
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError('Title must be at least 3 characters long.')
        return title
    
    def clean_display_order(self):
        """Validate display order"""
        display_order = self.cleaned_data.get('display_order')
        if display_order is not None and display_order < 0:
            raise forms.ValidationError('Display order must be a non-negative number.')
        return display_order
    
    def clean(self):
        """Comprehensive form validation"""
        cleaned_data = super().clean()
        
        # Get facility selections
        academic_facility = cleaned_data.get('academic_facility')
        sports_facility = cleaned_data.get('sports_facility')
        technology_infrastructure = cleaned_data.get('technology_infrastructure')
        student_amenity = cleaned_data.get('student_amenity')
        
        # Validate that only one facility type is selected
        facility_count = sum([
            bool(academic_facility),
            bool(sports_facility),
            bool(technology_infrastructure),
            bool(student_amenity)
        ])
        
        if facility_count > 1:
            raise forms.ValidationError(
                'Please select only one facility type. A photo can only be associated with one specific facility.'
            )
        
        # Note: It's okay to have no facility selected - photos can be general infrastructure
        
        return cleaned_data


class InfrastructurePhotoInlineForm(forms.ModelForm):
    """Simplified form for inline usage in admin"""
    
    class Meta:
        model = InfrastructurePhoto
        fields = ['title', 'image', 'is_featured', 'is_active', 'display_order']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter photo title/caption',
                'maxlength': '200',
                'required': True
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '999',
                'placeholder': '0'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# Enhanced Infrastructure Model Forms

class InfrastructureInfoForm(forms.ModelForm):
    """Enhanced form for Infrastructure Information management with rich text editing"""
    
    class Meta:
        model = InfrastructureInfo
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Infrastructure & Facilities',
                'maxlength': '200'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of infrastructure',
                'maxlength': '300'
            }),
            'hero_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hero section title',
                'maxlength': '200'
            }),
            'hero_subtitle': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Hero section subtitle/description',
                'maxlength': '500'
            }),
            'hero_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp'
            }),
            'hero_badge_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Modern Facilities',
                'maxlength': '100'
            }),
            'overview_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Overview section title',
                'maxlength': '200'
            }),
            'overview_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed overview of infrastructure'
            }),
            'cta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Call to action title',
                'maxlength': '200'
>>>>>>> a11168e (Fix)
            }),
            'cta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Call to action description'
            }),
<<<<<<< HEAD
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_active']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
    
    def clean_grants_amount(self):
        """Validate grants amount"""
        grants_amount = self.cleaned_data.get('grants_amount')
        if grants_amount is not None and grants_amount < 0:
            raise ValidationError("Grants amount cannot be negative.")
        return grants_amount
    
    def clean_publications_count(self):
        """Validate publications count"""
        count = self.cleaned_data.get('publications_count')
        if count is not None and count < 0:
            raise ValidationError("Publications count cannot be negative.")
        return count
    
    def clean_patents_count(self):
        """Validate patents count"""
        count = self.cleaned_data.get('patents_count')
        if count is not None and count < 0:
            raise ValidationError("Patents count cannot be negative.")
        return count


class ResearchCenterInfoUpdateForm(ResearchCenterInfoForm):
    """Update form for research center information (excludes timestamps)"""
    
    class Meta(ResearchCenterInfoForm.Meta):
        exclude = ['created_at', 'updated_at']


class ResearchCenterInfoQuickEditForm(forms.ModelForm):
    """Quick edit form for essential research center information"""
    
    class Meta:
        model = ResearchCenterInfo
        fields = [
            'title', 'subtitle', 'director_name', 'director_phone', 
            'director_email', 'office_phone', 'office_email', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Research Centers'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Advancing knowledge through cutting-edge research and innovation'
            }),
            'director_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Dr. [Research Director Name]'
            }),
            'director_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91-XXX-XXXX-XXX'
            }),
            'director_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., research@college.edu'
            }),
            'office_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91-XXX-XXXX-XXX'
            }),
            'office_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., research.office@college.edu'
=======
            'cta_button_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Schedule a Visit',
                'maxlength': '100'
            }),
            'cta_button_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., /contact/ or https://example.com'
>>>>>>> a11168e (Fix)
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
<<<<<<< HEAD


class PublicationInfoForm(forms.ModelForm):
    """Form for managing publication information"""
    
    class Meta:
        model = PublicationInfo
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Research Publications'
            }),
            'subtitle': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Page subtitle description'
            }),
            'total_publications': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'book_chapters': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'total_citations': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'awards_received': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'international_journals_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'international_citations': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'national_journals_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'national_citations': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'conference_papers_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'conference_citations': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'best_paper_awards': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'average_impact_factor': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'international_collaborations': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'research_students': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'cta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Interested in Collaborating?'
            }),
            'cta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Call to action description'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., research@college.edu'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_active']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
    
    def clean_average_impact_factor(self):
        """Validate impact factor"""
        impact_factor = self.cleaned_data.get('average_impact_factor')
        if impact_factor is not None and impact_factor < 0:
            raise ValidationError("Impact factor cannot be negative.")
        return impact_factor


class PublicationInfoUpdateForm(PublicationInfoForm):
    """Update form for publication information (excludes timestamps)"""
    
    class Meta(PublicationInfoForm.Meta):
        exclude = ['created_at', 'updated_at']


class PublicationInfoQuickEditForm(forms.ModelForm):
    """Quick edit form for essential publication information"""
    
    class Meta:
        model = PublicationInfo
        fields = [
            'title', 'subtitle', 'total_publications', 'total_citations', 
            'contact_email', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Research Publications'
            }),
            'subtitle': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Page subtitle description'
            }),
            'total_publications': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'total_citations': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., research@college.edu'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class PublicationForm(forms.ModelForm):
    """Form for creating and editing publications"""
    
    class Meta:
        model = Publication
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Publication title'
            }),
            'authors': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Author names (comma separated)'
            }),
            'abstract': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Publication abstract'
            }),
            'journal_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Journal or conference name'
            }),
            'journal_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1900,
                'max': 2030
            }),
            'citations': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'impact_factor': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'doi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digital Object Identifier'
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Publication URL'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_featured', 'is_active']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
    
    def clean_publication_year(self):
        """Validate publication year"""
        year = self.cleaned_data.get('publication_year')
        current_year = datetime.now().year
        if year and (year < 1900 or year > current_year + 1):
            raise ValidationError(f"Publication year must be between 1900 and {current_year + 1}.")
        return year
    
    def clean_citations(self):
        """Validate citations count"""
        citations = self.cleaned_data.get('citations')
        if citations is not None and citations < 0:
            raise ValidationError("Citations count cannot be negative.")
        return citations
    
    def clean_impact_factor(self):
        """Validate impact factor"""
        impact_factor = self.cleaned_data.get('impact_factor')
        if impact_factor is not None and impact_factor < 0:
            raise ValidationError("Impact factor cannot be negative.")
        return impact_factor


class PublicationUpdateForm(PublicationForm):
    """Update form for publications (excludes timestamps)"""
    
    class Meta(PublicationForm.Meta):
        exclude = ['created_at', 'updated_at']


class PublicationQuickEditForm(forms.ModelForm):
    """Quick edit form for essential publication fields"""
    
    class Meta:
        model = Publication
        fields = [
            'title', 'authors', 'journal_name', 'department', 
            'publication_year', 'citations', 'is_featured', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Publication title'
            }),
            'authors': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Author names (comma separated)'
            }),
            'journal_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Journal or conference name'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1900,
                'max': 2030
            }),
            'citations': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class PublicationSearchForm(forms.Form):
    """Search form for publications"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, author, or keywords...'
        })
    )
    
    department = forms.ChoiceField(
        required=False,
        choices=[('', 'All Departments')] + Publication.DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    journal_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + Publication.JOURNAL_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Year',
            'min': 1900,
            'max': 2030
        })
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('-publication_year', 'Date (Newest)'),
            ('publication_year', 'Date (Oldest)'),
            ('-citations', 'Citations (High)'),
            ('citations', 'Citations (Low)'),
            ('title', 'Title (A-Z)'),
            ('-title', 'Title (Z-A)'),
        ],
        initial='-publication_year',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


# Patents & Projects Forms
class PatentsProjectsInfoForm(forms.ModelForm):
    """Form for managing patents & projects information"""
    
    class Meta:
        model = PatentsProjectsInfo
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Patents & Projects'
            }),
            'subtitle': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Page subtitle description'
            }),
            'total_patents': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'total_projects': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'industry_collaborations': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'research_funding': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'innovation_awards': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'international_recognition': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'active_partnerships': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'students_involved': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'cta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Interested in Collaborating?'
            }),
            'cta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Call to action description'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., research@college.edu'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_active']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'


class PatentsProjectsInfoUpdateForm(PatentsProjectsInfoForm):
    """Update form for patents & projects information (excludes timestamps)"""
    
    class Meta(PatentsProjectsInfoForm.Meta):
        exclude = ['created_at', 'updated_at']


class PatentsProjectsInfoQuickEditForm(forms.ModelForm):
    """Quick edit form for essential patents & projects information"""
    
    class Meta:
        model = PatentsProjectsInfo
        fields = [
            'title', 'subtitle', 'total_patents', 'total_projects', 
            'contact_email', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Patents & Projects'
            }),
            'subtitle': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Page subtitle description'
            }),
            'total_patents': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'total_projects': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., research@college.edu'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class PatentForm(forms.ModelForm):
    """Form for creating and editing patents"""
    
    class Meta:
        model = Patent
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Patent title'
            }),
            'inventors': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Inventor names (comma separated)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Patent description'
            }),
            'patent_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Patent number'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'filing_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1900,
                'max': 2030
            }),
            'application_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Application number'
            }),
            'publication_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'grant_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'patent_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Patent URL'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_featured', 'is_active']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
    
    def clean_filing_year(self):
        """Validate filing year"""
        year = self.cleaned_data.get('filing_year')
        current_year = datetime.now().year
        if year and (year < 1900 or year > current_year + 1):
            raise ValidationError(f"Filing year must be between 1900 and {current_year + 1}.")
        return year


class PatentUpdateForm(PatentForm):
    """Update form for patents (excludes timestamps)"""
    
    class Meta(PatentForm.Meta):
        exclude = ['created_at', 'updated_at']


class PatentQuickEditForm(forms.ModelForm):
    """Quick edit form for essential patent fields"""
    
    class Meta:
        model = Patent
        fields = [
            'title', 'inventors', 'patent_number', 'department', 
            'filing_year', 'status', 'is_featured', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Patent title'
            }),
            'inventors': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Inventor names (comma separated)'
            }),
            'patent_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Patent number'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'filing_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1900,
                'max': 2030
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ResearchProjectForm(forms.ModelForm):
    """Form for creating and editing research projects"""
    
    class Meta:
        model = ResearchProject
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project title'
            }),
            'principal_investigator': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Principal investigator name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Project description'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1900,
                'max': 2030
            }),
            'end_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1900,
                'max': 2030
            }),
            'funding_agency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Funding agency'
            }),
            'funding_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'project_duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project duration'
            }),
            'team_members': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Team members'
            }),
            'project_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project URL'
            }),
            'report_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_featured', 'is_active']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
    
    def clean_start_year(self):
        """Validate start year"""
        year = self.cleaned_data.get('start_year')
        current_year = datetime.now().year
        if year and (year < 1900 or year > current_year + 1):
            raise ValidationError(f"Start year must be between 1900 and {current_year + 1}.")
        return year
    
    def clean_end_year(self):
        """Validate end year"""
        end_year = self.cleaned_data.get('end_year')
        start_year = self.cleaned_data.get('start_year')
        current_year = datetime.now().year
        
        if end_year and (end_year < 1900 or end_year > current_year + 1):
            raise ValidationError(f"End year must be between 1900 and {current_year + 1}.")
        
        if end_year and start_year and end_year < start_year:
            raise ValidationError("End year cannot be before start year.")
        
        return end_year


class ResearchProjectUpdateForm(ResearchProjectForm):
    """Update form for research projects (excludes timestamps)"""
    
    class Meta(ResearchProjectForm.Meta):
        exclude = ['created_at', 'updated_at']


class ResearchProjectQuickEditForm(forms.ModelForm):
    """Quick edit form for essential research project fields"""
    
    class Meta:
        model = ResearchProject
        fields = [
            'title', 'principal_investigator', 'department', 'status',
            'start_year', 'funding_agency', 'funding_amount', 'is_featured', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project title'
            }),
            'principal_investigator': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Principal investigator name'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1900,
                'max': 2030
            }),
            'funding_agency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Funding agency'
            }),
            'funding_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class IndustryCollaborationForm(forms.ModelForm):
    """Form for creating and editing industry collaborations"""
    
    class Meta:
        model = IndustryCollaboration
        fields = '__all__'
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Collaboration description'
            }),
            'collaboration_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type of collaboration'
            }),
            'duration_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'funding_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person'
            }),
            'company_website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company website'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['is_featured', 'is_active']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'


class IndustryCollaborationUpdateForm(IndustryCollaborationForm):
    """Update form for industry collaborations (excludes timestamps)"""
    
    class Meta(IndustryCollaborationForm.Meta):
        exclude = ['created_at', 'updated_at']


class IndustryCollaborationQuickEditForm(forms.ModelForm):
    """Quick edit form for essential industry collaboration fields"""
    
    class Meta:
        model = IndustryCollaboration
        fields = [
            'company_name', 'collaboration_type', 'duration_years', 
            'funding_amount', 'is_featured', 'is_active'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
            'collaboration_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type of collaboration'
            }),
            'duration_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'funding_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# Consultancy Forms
class ConsultancyInfoForm(forms.ModelForm):
    """Form for managing consultancy information"""
    
    class Meta:
        model = ConsultancyInfo
=======
        
        help_texts = {
            'title': 'Main title displayed on the infrastructure page',
            'subtitle': 'Brief subtitle or tagline for the page',
            'hero_title': 'Title for the hero/banner section',
            'hero_subtitle': 'Description text for the hero section',
            'hero_image': 'Background image for the hero section (recommended: 1920x600px)',
            'hero_badge_text': 'Small badge text displayed on the hero section',
            'overview_title': 'Title for the overview section',
            'overview_description': 'Detailed description of your infrastructure',
            'cta_title': 'Title for the call-to-action section',
            'cta_description': 'Description for the call-to-action section',
            'cta_button_text': 'Text for the call-to-action button',
            'cta_button_url': 'URL where the call-to-action button should link',
            'is_active': 'Make this infrastructure information visible on the website'
        }
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError('Title must be at least 3 characters long.')
        return title
    
    def clean_cta_button_url(self):
        """Validate CTA button URL"""
        url = self.cleaned_data.get('cta_button_url')
        if url and not url.startswith(('/', 'http://', 'https://')):
            raise forms.ValidationError('URL must start with /, http://, or https://')
        return url


class InfrastructureStatisticForm(forms.ModelForm):
    """Enhanced form for Infrastructure Statistics with icon and color selection"""
    
    class Meta:
        model = InfrastructureStatistic
>>>>>>> a11168e (Fix)
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
<<<<<<< HEAD
                'placeholder': 'Page title'
            }),
            'subtitle': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Page subtitle'
            }),
            'total_projects': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'industry_partners': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'revenue_generated': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'client_satisfaction': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100
            }),
            'cta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Call to action title'
            }),
            'cta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Call to action description'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact email'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_client_satisfaction(self):
        """Validate client satisfaction percentage"""
        satisfaction = self.cleaned_data.get('client_satisfaction')
        if satisfaction and (satisfaction < 0 or satisfaction > 100):
            raise ValidationError("Client satisfaction must be between 0 and 100.")
        return satisfaction


class ConsultancyInfoUpdateForm(ConsultancyInfoForm):
    """Update form for consultancy information (excludes timestamps)"""
    
    class Meta(ConsultancyInfoForm.Meta):
        exclude = ['created_at', 'updated_at']


class ConsultancyInfoQuickEditForm(forms.ModelForm):
    """Quick edit form for essential consultancy information fields"""
    
    class Meta:
        model = ConsultancyInfo
        fields = [
            'title', 'total_projects', 'industry_partners', 
            'revenue_generated', 'client_satisfaction', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Page title'
            }),
            'total_projects': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'industry_partners': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'revenue_generated': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'client_satisfaction': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ConsultancyServiceForm(forms.ModelForm):
    """Form for managing consultancy services"""
    
    class Meta:
        model = ConsultancyService
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Service title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Service description'
            }),
            'service_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Service features (one per line)'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'FontAwesome icon class (e.g., fas fa-laptop-code)'
=======
                'placeholder': 'e.g., Classrooms, Laboratories, WiFi Coverage',
                'maxlength': '100'
            }),
            'value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 25+, 100%, 5000+',
                'maxlength': '50'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional description of the statistic',
                'maxlength': '200'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-building, fas fa-wifi, fas fa-book',
                'maxlength': '100'
            }),
            'statistic_type': forms.Select(attrs={
                'class': 'form-select'
>>>>>>> a11168e (Fix)
            }),
            'color_class': forms.Select(attrs={
                'class': 'form-select'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
<<<<<<< HEAD
                'min': 0
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
=======
                'min': '0',
                'max': '999',
                'placeholder': '0'
>>>>>>> a11168e (Fix)
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
<<<<<<< HEAD
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add color choices
        self.fields['color_class'].widget.choices = [
            ('primary', 'Primary (Blue)'),
            ('success', 'Success (Green)'),
            ('info', 'Info (Light Blue)'),
            ('warning', 'Warning (Orange)'),
            ('danger', 'Danger (Red)'),
            ('secondary', 'Secondary (Gray)'),
        ]


class ConsultancyServiceUpdateForm(ConsultancyServiceForm):
    """Update form for consultancy services (excludes timestamps)"""
    
    class Meta(ConsultancyServiceForm.Meta):
        exclude = ['created_at', 'updated_at']


class ConsultancyServiceQuickEditForm(forms.ModelForm):
    """Quick edit form for essential consultancy service fields"""
    
    class Meta:
        model = ConsultancyService
        fields = [
            'title', 'service_type', 'display_order', 
            'is_featured', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Service title'
            }),
            'service_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ConsultancyExpertiseForm(forms.ModelForm):
    """Form for managing consultancy expertise areas"""
    
    class Meta:
        model = ConsultancyExpertise
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Expertise area title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Expertise description'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'FontAwesome icon class (e.g., fas fa-microchip)'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ConsultancyExpertiseUpdateForm(ConsultancyExpertiseForm):
    """Update form for consultancy expertise (excludes timestamps)"""
    
    class Meta(ConsultancyExpertiseForm.Meta):
        exclude = ['created_at', 'updated_at']


class ConsultancyExpertiseQuickEditForm(forms.ModelForm):
    """Quick edit form for essential consultancy expertise fields"""
    
    class Meta:
        model = ConsultancyExpertise
        fields = [
            'title', 'display_order', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Expertise area title'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ConsultancySuccessStoryForm(forms.ModelForm):
    """Form for managing consultancy success stories"""
    
    class Meta:
        model = ConsultancySuccessStory
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Success story title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Success story description'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'metric1_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First metric label'
            }),
            'metric1_value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First metric value'
            }),
            'metric2_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Second metric label'
            }),
            'metric2_value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Second metric value'
            }),
            'metric3_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Third metric label'
            }),
            'metric3_value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Third metric value'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ConsultancySuccessStoryUpdateForm(ConsultancySuccessStoryForm):
    """Update form for consultancy success stories (excludes timestamps)"""
    
    class Meta(ConsultancySuccessStoryForm.Meta):
        exclude = ['created_at', 'updated_at']


class ConsultancySuccessStoryQuickEditForm(forms.ModelForm):
    """Quick edit form for essential consultancy success story fields"""
    
    class Meta:
        model = ConsultancySuccessStory
        fields = [
            'title', 'category', 'display_order', 
            'is_featured', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Success story title'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


# NSS-NCC Clubs Forms
class NSSNCCClubForm(forms.ModelForm):
    """Form for managing NSS-NCC Clubs"""
    
    class Meta:
        model = NSSNCCClub
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter club name'
            }),
            'club_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': CKEditor5Widget(config_name='default'),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description for cards'
            }),
            'coordinator_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Coordinator name'
            }),
            'coordinator_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'coordinator@example.com'
            }),
            'coordinator_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 9876543210'
            }),
            'main_activities': CKEditor5Widget(config_name='default'),
            'upcoming_events': CKEditor5Widget(config_name='default'),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/yourpage'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/yourpage'
            }),
            'website_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourwebsite.com'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_coordinator_phone(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('coordinator_phone')
        if phone:
            # Remove all non-digit characters
            phone_digits = re.sub(r'\D', '', phone)
            if len(phone_digits) < 10:
                raise ValidationError("Phone number must be at least 10 digits long.")
        return phone


class NSSNCCClubQuickEditForm(forms.ModelForm):
    """Quick edit form for essential club fields"""
    
    class Meta:
        model = NSSNCCClub
        fields = [
            'name', 'club_type', 'coordinator_name', 'coordinator_email',
            'display_order', 'is_featured', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'club_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'coordinator_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'coordinator_email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class NSSNCCNoticeForm(forms.ModelForm):
    """Form for managing NSS-NCC Notices"""
    
    class Meta:
        model = NSSNCCNotice
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Notice title'
            }),
            'content': CKEditor5Widget(config_name='default'),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'related_club': forms.Select(attrs={
                'class': 'form-select'
            }),
            'publish_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'expiry_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active clubs in the dropdown
        self.fields['related_club'].queryset = NSSNCCClub.objects.filter(is_active=True)
    
    def clean(self):
        cleaned_data = super().clean()
        publish_date = cleaned_data.get('publish_date')
        expiry_date = cleaned_data.get('expiry_date')
        
        if expiry_date and publish_date and expiry_date <= publish_date:
            raise ValidationError("Expiry date must be after publish date.")
        
        return cleaned_data


class NSSNCCNoticeQuickEditForm(forms.ModelForm):
    """Quick edit form for essential notice fields"""
    
    class Meta:
        model = NSSNCCNotice
        fields = [
            'title', 'category', 'priority', 'related_club',
            'is_featured', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'related_club': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_club'].queryset = NSSNCCClub.objects.filter(is_active=True)


class NSSNCCGalleryForm(forms.ModelForm):
    """Form for managing NSS-NCC Gallery Images"""
    
    class Meta:
        model = NSSNCCGallery
=======
        
        help_texts = {
            'title': 'Name of the statistic (e.g., "Classrooms", "Laboratories")',
            'value': 'The statistic value (e.g., "25+", "100%", "5000+")',
            'description': 'Optional additional description for the statistic',
            'icon_class': 'Font Awesome icon class (e.g., fas fa-building, fas fa-wifi)',
            'statistic_type': 'Category of the statistic for better organization',
            'color_class': 'Color theme for the statistic display (blue, emerald, purple, orange)',
            'display_order': 'Order in which statistics appear (lower numbers first)',
            'is_active': 'Make this statistic visible on the website'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add custom choices for color_class
        self.fields['color_class'].widget = forms.Select(choices=[
            ('blue', 'Blue'),
            ('emerald', 'Emerald'),
            ('purple', 'Purple'),
            ('orange', 'Orange'),
            ('red', 'Red'),
            ('green', 'Green'),
            ('indigo', 'Indigo'),
            ('pink', 'Pink'),
        ])
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 2:
                raise forms.ValidationError('Title must be at least 2 characters long.')
        return title
    
    def clean_value(self):
        """Validate value"""
        value = self.cleaned_data.get('value')
        if value:
            value = value.strip()
            if len(value) < 1:
                raise forms.ValidationError('Value cannot be empty.')
        return value


class AcademicFacilityForm(forms.ModelForm):
    """Enhanced form for Academic Facilities with features management"""
    
    class Meta:
        model = AcademicFacility
>>>>>>> a11168e (Fix)
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
<<<<<<< HEAD
                'placeholder': 'Image title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Image description'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'related_club': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_club'].queryset = NSSNCCClub.objects.filter(is_active=True)


class NSSNCCAchievementForm(forms.ModelForm):
    """Form for managing NSS-NCC Achievements"""
    
    class Meta:
        model = NSSNCCAchievement
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Achievement title'
=======
                'placeholder': 'e.g., Smart Classrooms, Modern Laboratories',
                'maxlength': '200'
>>>>>>> a11168e (Fix)
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
<<<<<<< HEAD
                'placeholder': 'Achievement description'
            }),
            'achievement_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'related_club': forms.Select(attrs={
                'class': 'form-select'
            }),
            'achieved_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Individual or team name'
            }),
            'achievement_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization name'
            }),
            'certificate_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_club'].queryset = NSSNCCClub.objects.filter(is_active=True)
    
    def clean_achievement_date(self):
        """Validate achievement date"""
        achievement_date = self.cleaned_data.get('achievement_date')
        if achievement_date and achievement_date > datetime.now().date():
            raise ValidationError("Achievement date cannot be in the future.")
        return achievement_date


class NSSNCCAchievementQuickEditForm(forms.ModelForm):
    """Quick edit form for essential achievement fields"""
    
    class Meta:
        model = NSSNCCAchievement
        fields = [
            'title', 'achievement_type', 'related_club',
            'achievement_date', 'is_featured', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'achievement_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'related_club': forms.Select(attrs={
                'class': 'form-select'
            }),
            'achievement_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
=======
                'placeholder': 'Detailed description of the facility'
            }),
            'facility_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-chalkboard-teacher, fas fa-flask',
                'maxlength': '100'
            }),
            'color_class': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp'
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'List features one per line:\n• Feature 1\n• Feature 2\n• Feature 3'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '999',
                'placeholder': '0'
>>>>>>> a11168e (Fix)
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
<<<<<<< HEAD
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_club'].queryset = NSSNCCClub.objects.filter(is_active=True)

class HeroCarouselSlideForm(forms.ModelForm):
    """Comprehensive form for managing hero carousel slides"""
    
    class Meta:
        model = HeroCarouselSlide
=======
        
        help_texts = {
            'title': 'Name of the academic facility',
            'description': 'Detailed description of the facility and its capabilities',
            'facility_type': 'Category of the academic facility',
            'icon_class': 'Font Awesome icon class for the facility',
            'color_class': 'Color theme for the facility display',
            'image': 'Representative image of the facility (recommended: 800x600px)',
            'features': 'List key features of the facility (one per line, use • for bullet points)',
            'display_order': 'Order in which facilities appear (lower numbers first)',
            'is_featured': 'Feature this facility prominently on the website',
            'is_active': 'Make this facility visible on the website'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add custom choices for color_class
        self.fields['color_class'].widget = forms.Select(choices=[
            ('blue', 'Blue'),
            ('emerald', 'Emerald'),
            ('purple', 'Purple'),
            ('orange', 'Orange'),
            ('red', 'Red'),
            ('green', 'Green'),
            ('indigo', 'Indigo'),
            ('pink', 'Pink'),
        ])
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError('Title must be at least 3 characters long.')
        return title
    
    def clean_features(self):
        """Clean and format features"""
        features = self.cleaned_data.get('features')
        if features:
            # Clean up the features text
            features = features.strip()
            # Remove empty lines and clean up formatting
            feature_lines = [line.strip() for line in features.split('\n') if line.strip()]
            features = '\n'.join(feature_lines)
        return features


class SportsFacilityForm(forms.ModelForm):
    """Enhanced form for Sports Facilities"""
    
    class Meta:
        model = SportsFacility
>>>>>>> a11168e (Fix)
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
<<<<<<< HEAD
                'placeholder': 'Enter slide title...'
            }),
            'subtitle': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter slide subtitle/description...'
            }),
            'slide_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'badge_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Welcome to Excellence'
            }),
            'badge_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-star'
            }),
            'primary_button_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Explore Programs'
            }),
            'primary_button_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'primary_button_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-arrow-right'
            }),
            'secondary_button_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Learn More'
            }),
            'secondary_button_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'secondary_button_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-info-circle'
            }),
            'gradient_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'show_statistics': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'stat_1_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 18+'
            }),
            'stat_1_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Courses'
            }),
            'stat_1_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-graduation-cap'
            }),
            'stat_2_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 5000+'
            }),
            'stat_2_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Students'
            }),
            'stat_2_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-users'
            }),
            'stat_3_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 150+'
            }),
            'stat_3_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Faculty'
            }),
            'stat_3_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-chalkboard-teacher'
            }),
            'stat_4_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 25+'
            }),
            'stat_4_label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Years'
            }),
            'stat_4_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-award'
            }),
            'show_content_cards': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'content_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Why Choose Us?'
            }),
            'content_icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-university'
            }),
            'content_items': CKEditor5Widget(attrs={
                'class': 'form-control'
            }),
            'auto_play_interval': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1000',
                'step': '500'
            }),
            'show_indicators': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'show_controls': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
=======
                'placeholder': 'e.g., Basketball Court, Swimming Pool',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed description of the sports facility'
            }),
            'sports_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-basketball-ball, fas fa-swimmer',
                'maxlength': '100'
            }),
            'color_class': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp'
            }),
            'display_order': forms.NumberInput(attrs={
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
            'title': 'Name of the sports facility',
            'description': 'Detailed description of the sports facility and its features',
            'sports_type': 'Category of the sports facility',
            'icon_class': 'Font Awesome icon class for the facility',
            'color_class': 'Color theme for the facility display',
            'image': 'Representative image of the sports facility (recommended: 800x600px)',
            'display_order': 'Order in which facilities appear (lower numbers first)',
            'is_active': 'Make this sports facility visible on the website'
>>>>>>> a11168e (Fix)
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
<<<<<<< HEAD
        # Add help text for better user experience
        self.fields['title'].help_text = "Main heading that appears prominently on the slide"
        self.fields['subtitle'].help_text = "Descriptive text that appears below the title"
        self.fields['slide_type'].help_text = "Choose the type of slide to apply appropriate styling"
        self.fields['display_order'].help_text = "Lower numbers appear first (0 = first slide)"
        self.fields['badge_text'].help_text = "Optional badge text that appears above the title"
        self.fields['badge_icon'].help_text = "FontAwesome icon class (e.g., fas fa-star, fas fa-heart)"
        self.fields['primary_button_text'].help_text = "Text for the main call-to-action button"
        self.fields['primary_button_url'].help_text = "URL where the primary button should link"
        self.fields['secondary_button_text'].help_text = "Text for the secondary button (optional)"
        self.fields['secondary_button_url'].help_text = "URL where the secondary button should link"
        self.fields['gradient_type'].help_text = "Choose a predefined gradient or create custom"
        self.fields['show_statistics'].help_text = "Display statistics cards on the right side"
        self.fields['auto_play_interval'].help_text = "Time in milliseconds between automatic slide changes"
        self.fields['content_items'].help_text = "HTML content for custom slides (use CKEditor for rich formatting)"


class HeroCarouselSlideQuickEditForm(forms.ModelForm):
    """Quick edit form for essential hero carousel slide fields"""
    
    class Meta:
        model = HeroCarouselSlide
        fields = [
            'title', 'subtitle', 'slide_type', 'is_active', 'display_order',
            'badge_text', 'primary_button_text', 'primary_button_url',
            'secondary_button_text', 'secondary_button_url', 'gradient_type'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-sm'
            }),
            'subtitle': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 2
            }),
            'slide_type': forms.Select(attrs={
                'class': 'form-select form-select-sm'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'min': '0'
            }),
            'badge_text': forms.TextInput(attrs={
                'class': 'form-control form-control-sm'
            }),
            'primary_button_text': forms.TextInput(attrs={
                'class': 'form-control form-control-sm'
            }),
            'primary_button_url': forms.URLInput(attrs={
                'class': 'form-control form-control-sm'
            }),
            'secondary_button_text': forms.TextInput(attrs={
                'class': 'form-control form-control-sm'
            }),
            'secondary_button_url': forms.URLInput(attrs={
                'class': 'form-control form-control-sm'
            }),
            'gradient_type': forms.Select(attrs={
                'class': 'form-select form-select-sm'
            }),
        }


class HeroCarouselSettingsForm(forms.ModelForm):
    """Form for managing global hero carousel settings"""
    
    class Meta:
        model = HeroCarouselSettings
        fields = '__all__'
        widgets = {
            'is_enabled': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'auto_play': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'default_interval': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1000',
                'step': '500'
            }),
            'show_indicators': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'show_controls': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'pause_on_hover': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'enable_keyboard': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'enable_touch': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'transition_duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '100',
                'step': '50'
            }),
            'fade_effect': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'mobile_height': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 24rem, 70vh'
            }),
            'tablet_height': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 28rem, 80vh'
            }),
            'desktop_height': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 24rem, 100vh'
            }),
=======
        
        # Add custom choices for color_class
        self.fields['color_class'].widget = forms.Select(choices=[
            ('green', 'Green'),
            ('blue', 'Blue'),
            ('orange', 'Orange'),
            ('red', 'Red'),
            ('purple', 'Purple'),
            ('emerald', 'Emerald'),
            ('indigo', 'Indigo'),
            ('pink', 'Pink'),
        ])
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError('Title must be at least 3 characters long.')
        return title


class TechnologyInfrastructureForm(forms.ModelForm):
    """Enhanced form for Technology Infrastructure"""
    
    class Meta:
        model = TechnologyInfrastructure
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., High-Speed WiFi, Video Conferencing',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed description of the technology infrastructure'
            }),
            'tech_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-wifi, fas fa-video, fas fa-shield-alt',
                'maxlength': '100'
            }),
            'color_class': forms.Select(attrs={
                'class': 'form-select'
            }),
            'display_order': forms.NumberInput(attrs={
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
            'title': 'Name of the technology infrastructure',
            'description': 'Detailed description of the technology and its capabilities',
            'tech_type': 'Category of the technology infrastructure',
            'icon_class': 'Font Awesome icon class for the technology',
            'color_class': 'Color theme for the technology display',
            'display_order': 'Order in which technologies appear (lower numbers first)',
            'is_active': 'Make this technology infrastructure visible on the website'
>>>>>>> a11168e (Fix)
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
<<<<<<< HEAD
        # Add help text for better user experience
        self.fields['is_enabled'].help_text = "Enable or disable the entire hero carousel"
        self.fields['auto_play'].help_text = "Automatically advance slides"
        self.fields['default_interval'].help_text = "Default time between slide changes (milliseconds)"
        self.fields['show_indicators'].help_text = "Show dots at the bottom for slide navigation"
        self.fields['show_controls'].help_text = "Show left/right arrow navigation buttons"
        self.fields['pause_on_hover'].help_text = "Pause auto-play when user hovers over carousel"
        self.fields['enable_keyboard'].help_text = "Allow keyboard navigation (arrow keys)"
        self.fields['enable_touch'].help_text = "Allow touch/swipe navigation on mobile devices"
        self.fields['transition_duration'].help_text = "Duration of slide transition animation (milliseconds)"
        self.fields['fade_effect'].help_text = "Use fade transition instead of slide transition"
        self.fields['mobile_height'].help_text = "Carousel height on mobile devices (CSS units)"
        self.fields['tablet_height'].help_text = "Carousel height on tablet devices (CSS units)"
        self.fields['desktop_height'].help_text = "Carousel height on desktop devices (CSS units)"
=======
        
        # Add custom choices for color_class
        self.fields['color_class'].widget = forms.Select(choices=[
            ('indigo', 'Indigo'),
            ('blue', 'Blue'),
            ('purple', 'Purple'),
            ('emerald', 'Emerald'),
            ('orange', 'Orange'),
            ('red', 'Red'),
            ('green', 'Green'),
            ('pink', 'Pink'),
        ])
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError('Title must be at least 3 characters long.')
        return title


class StudentAmenityForm(forms.ModelForm):
    """Enhanced form for Student Amenities"""
    
    class Meta:
        model = StudentAmenity
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Cafeteria, Medical Center, Parking',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed description of the student amenity'
            }),
            'amenity_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fas fa-utensils, fas fa-ambulance, fas fa-car',
                'maxlength': '100'
            }),
            'color_class': forms.Select(attrs={
                'class': 'form-select'
            }),
            'display_order': forms.NumberInput(attrs={
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
            'title': 'Name of the student amenity',
            'description': 'Detailed description of the amenity and its services',
            'amenity_type': 'Category of the student amenity',
            'icon_class': 'Font Awesome icon class for the amenity',
            'color_class': 'Color theme for the amenity display',
            'display_order': 'Order in which amenities appear (lower numbers first)',
            'is_active': 'Make this student amenity visible on the website'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add custom choices for color_class
        self.fields['color_class'].widget = forms.Select(choices=[
            ('pink', 'Pink'),
            ('blue', 'Blue'),
            ('green', 'Green'),
            ('orange', 'Orange'),
            ('purple', 'Purple'),
            ('emerald', 'Emerald'),
            ('indigo', 'Indigo'),
            ('red', 'Red'),
        ])
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError('Title must be at least 3 characters long.')
        return title
    
    def clean_image(self):
        """Validate uploaded image"""
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
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError('Title must be at least 3 characters long.')
        return title
    
    def clean_display_order(self):
        """Validate display order"""
        display_order = self.cleaned_data.get('display_order')
        if display_order is not None and display_order < 0:
            raise forms.ValidationError('Display order must be a non-negative number.')
        return display_order
>>>>>>> a11168e (Fix)
