from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import path, reverse
from django.shortcuts import render
from django import forms
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django_ckeditor_5.widgets import CKEditor5Widget
from .forms import TopUtilityBarForm, CustomLinkForm
from datetime import datetime, timezone, timedelta
from .models import (
    ScrollingNotification, SliderImage, HeaderInfo, NavbarInfo, CollegeInfo, Program, Event, EventImage, Notice, SocialInitiative, 
    StudentTestimonial, ImportantLink, ContactMessage, Menu, MenuItem, 
    Page, BlockRichText, BlockImageGallery, GalleryImage, BlockVideoEmbed,
    BlockDownloadList, BlockTableHTML, BlockForm, DownloadFile,
    Gallery, GalleryPhoto,
    AdmissionInfo, ExamResult, LibraryResource, ELearningCourse,
    PlacementRecord, AlumniProfile, DirectorMessage, PrincipalMessage, TopUtilityBar, CustomLink,
    # IQAC Models
    IQACInfo, IQACReport, NAACInfo, NIRFInfo, QualityInitiative, 
    AccreditationInfo, IQACFeedback, SideMenu, SideMenuItem
)


# CustomLink Inline Admin for TopUtilityBar
class CustomLinkInline(SortableInlineAdminMixin, admin.TabularInline):
    """Enhanced inline admin for CustomLink with better UX"""
    model = CustomLink
    form = CustomLinkForm
    extra = 1
    min_num = 0
    max_num = 10  # Reasonable limit
    fields = ('text', 'url', 'icon_class', 'tooltip', 'open_in_new_tab', 'ordering', 'is_active')
    
    class Media:
        css = {
            'all': ('admin/css/custom_link_inline.css',)
        }
        js = ('admin/js/custom_link_inline.js',)


@admin.register(TopUtilityBar)
class TopUtilityBarAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Enhanced admin interface for Top Utility Bar management with comprehensive controls"""
    
    form = TopUtilityBarForm
    list_display = [
        'name', 'is_active', 'get_status_display', 'position', 'get_features_summary', 
        'show_on_mobile', 'get_preview_link', 'created_at'
    ]
    list_filter = [
        'is_active', 'position', 'show_social_icons', 'show_contact_info', 
        'show_custom_links', 'show_on_mobile', 'mobile_collapsed', 'created_at'
    ]
    list_editable = ['is_active']
    search_fields = ['name', 'contact_email', 'contact_phone']
    ordering = ['-is_active', '-created_at']
    actions = [
        'activate_utility_bars', 'deactivate_utility_bars', 'duplicate_utility_bars',
        'test_utility_bar_links', 'export_configuration'
    ]
    
    fieldsets = (
        ('Configuration Name & Status', {
            'fields': ('name', 'is_active'),
            'description': 'Basic configuration settings. Only one utility bar can be active at a time.',
            'classes': ('wide',)
        }),
        ('Visual Appearance', {
            'fields': (
                ('background_color', 'text_color'),
                ('height', 'position')
            ),
            'description': 'Control the visual styling and position of the utility bar',
            'classes': ('wide',)
        }),
        ('Social Media Integration', {
            'fields': (
                'show_social_icons',
                ('facebook_url', 'twitter_url'),
                ('instagram_url', 'youtube_url'),
                'linkedin_url'
            ),
            'description': 'Social media links that will appear as icons in the utility bar',
            'classes': ('collapse', 'wide', 'social-media-fields')
        }),
        ('Contact Information Display', {
            'fields': (
                'show_contact_info',
                ('contact_phone', 'contact_email')
            ),
            'description': 'Contact details to display in the utility bar',
            'classes': ('collapse', 'wide', 'contact-info-fields')
        }),
        ('Custom Quick Links', {
            'fields': (
                'show_custom_links',
                ('custom_link_1_text', 'custom_link_1_url'),
                ('custom_link_2_text', 'custom_link_2_url'),
                ('custom_link_3_text', 'custom_link_3_url')
            ),
            'description': 'Add up to 3 custom quick access links (e.g., Admissions, Results, Library)',
            'classes': ('collapse', 'wide', 'custom-links-fields')
        }),
        ('Mobile & Responsive Settings', {
            'fields': (
                ('show_on_mobile', 'mobile_collapsed')
            ),
            'description': 'Control how the utility bar appears on mobile devices',
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CustomLinkInline]
    
    def get_status_display(self, obj):
        """Display active status with visual indicator"""
        if obj.is_active:
            return format_html(
                '<span style="color: #28a745; font-weight: bold; display: inline-flex; align-items: center;">'
                '<span style="width: 8px; height: 8px; background: #28a745; border-radius: 50%; margin-right: 6px;"></span>'
                'Active</span>'
            )
        else:
            return format_html(
                '<span style="color: #6c757d; display: inline-flex; align-items: center;">'
                '<span style="width: 8px; height: 8px; background: #6c757d; border-radius: 50%; margin-right: 6px;"></span>'
                'Inactive</span>'
            )
    get_status_display.short_description = 'Status'
    get_status_display.admin_order_field = 'is_active'
    
    def get_features_summary(self, obj):
        """Show a summary of enabled features"""
        features = []
        
        if obj.show_social_icons:
            social_count = sum(1 for url in [
                obj.facebook_url, obj.twitter_url, obj.instagram_url, 
                obj.youtube_url, obj.linkedin_url
            ] if url)
            if social_count > 0:
                features.append(f'Social ({social_count})')
        
        if obj.show_contact_info:
            contact_methods = []
            if obj.contact_phone:
                contact_methods.append('Phone')
            if obj.contact_email:
                contact_methods.append('Email')
            if contact_methods:
                features.append(f'Contact ({len(contact_methods)})')
        
        if obj.show_custom_links:
            custom_count = sum(1 for text, url in [
                (obj.custom_link_1_text, obj.custom_link_1_url),
                (obj.custom_link_2_text, obj.custom_link_2_url),
                (obj.custom_link_3_text, obj.custom_link_3_url)
            ] if text and url)
            if custom_count > 0:
                features.append(f'Links ({custom_count})')
        
        if not features:
            return format_html('<span style="color: #ffc107;">No features enabled</span>')
        
        return format_html(
            '<span style="color: #0d6efd; font-size: 12px;">{}</span>',
            ' • '.join(features)
        )
    get_features_summary.short_description = 'Features'
    
    def get_preview_link(self, obj):
        """Show a preview/test link"""
        if obj.is_active:
            return format_html(
                '<a href="#" onclick="previewUtilityBar({}); return false;" '
                'style="color: #0d6efd; text-decoration: none; font-size: 12px;">'
                '<i class="fas fa-eye"></i> Preview</a>',
                obj.pk
            )
        return format_html(
            '<span style="color: #6c757d; font-size: 12px;">'
            '<i class="fas fa-eye-slash"></i> Inactive</span>'
        )
    get_preview_link.short_description = 'Preview'
    
    def save_model(self, request, obj, form, change):
        """Enhanced save method with user feedback"""
        # Store the previous active utility bar for messaging
        previous_active = None
        if obj.is_active:
            previous_active = TopUtilityBar.objects.filter(
                is_active=True
            ).exclude(pk=obj.pk).first()
            
            # Deactivate other utility bars
            TopUtilityBar.objects.exclude(pk=obj.pk).update(is_active=False)
        
        super().save_model(request, obj, form, change)
        
        # Provide informative messages
        if obj.is_active:
            if previous_active:
                messages.success(
                    request,
                    f'Utility bar "{obj.name}" has been activated and is now live on the website. '
                    f'The previous configuration "{previous_active.name}" has been deactivated.'
                )
            else:
                messages.success(
                    request,
                    f'Utility bar "{obj.name}" has been activated and is now live on the website.'
                )
        else:
            messages.info(
                request,
                f'Utility bar "{obj.name}" has been saved but is currently inactive. '
                'To make it live, set it as active.'
            )
    
    # Custom Admin Actions
    def activate_utility_bars(self, request, queryset):
        """Activate selected utility bars (only the last selected will remain active)"""
        if queryset.count() == 0:
            self.message_user(request, "No utility bars selected.", level=messages.WARNING)
            return
        
        # Get the last selected item to activate
        last_selected = queryset.last()
        
        # Deactivate all utility bars first
        TopUtilityBar.objects.all().update(is_active=False)
        
        # Activate only the last selected one
        last_selected.is_active = True
        last_selected.save()
        
        self.message_user(
            request, 
            f'Utility bar "{last_selected.name}" has been activated. '
            f'All other utility bars have been deactivated.',
            level=messages.SUCCESS
        )
    activate_utility_bars.short_description = "Activate selected utility bar (last selected)"
    
    def deactivate_utility_bars(self, request, queryset):
        """Deactivate selected utility bars"""
        updated = queryset.update(is_active=False)
        if updated > 0:
            self.message_user(
                request, 
                f'{updated} utility bar(s) have been deactivated.',
                level=messages.SUCCESS
            )
        else:
            self.message_user(
                request, 
                'No utility bars were deactivated.',
                level=messages.INFO
            )
    deactivate_utility_bars.short_description = "Deactivate selected utility bars"
    
    def duplicate_utility_bars(self, request, queryset):
        """Create copies of selected utility bars"""
        duplicated = 0
        for obj in queryset:
            obj.pk = None
            obj.name = f"{obj.name} (Copy)"
            obj.is_active = False  # Make copies inactive by default
            obj.save()
            duplicated += 1
        
        if duplicated > 0:
            self.message_user(
                request, 
                f'{duplicated} utility bar(s) have been duplicated successfully. '
                'All copies are inactive by default.',
                level=messages.SUCCESS
            )
    duplicate_utility_bars.short_description = "Duplicate selected utility bars"
    
    def test_utility_bar_links(self, request, queryset):
        """Test all links in selected utility bars"""
        import requests
        from urllib.parse import urlparse
        
        tested_count = 0
        broken_links = []
        
        for obj in queryset:
            links_to_test = []
            
            # Collect all URLs to test
            if obj.show_social_icons:
                for url in [obj.facebook_url, obj.twitter_url, obj.instagram_url, obj.youtube_url, obj.linkedin_url]:
                    if url:
                        links_to_test.append(('Social Media', url))
            
            if obj.show_custom_links:
                for i, (text, url) in enumerate([
                    (obj.custom_link_1_text, obj.custom_link_1_url),
                    (obj.custom_link_2_text, obj.custom_link_2_url),
                    (obj.custom_link_3_text, obj.custom_link_3_url)
                ], 1):
                    if text and url:
                        # Only test absolute URLs, not relative paths
                        if url.startswith(('http://', 'https://')):
                            links_to_test.append((f'Custom Link {i} ({text})', url))
            
            # Test each link
            for link_type, url in links_to_test:
                tested_count += 1
                try:
                    response = requests.head(url, timeout=10, allow_redirects=True)
                    if response.status_code >= 400:
                        broken_links.append(f'{obj.name}: {link_type} - {url} (Status: {response.status_code})')
                except Exception as e:
                    broken_links.append(f'{obj.name}: {link_type} - {url} (Error: {str(e)[:50]}...)')
        
        # Report results
        if broken_links:
            self.message_user(
                request, 
                f'Link testing completed. {len(broken_links)} broken links found out of {tested_count} tested:\n'
                + '\n'.join(broken_links),
                level=messages.WARNING
            )
        elif tested_count > 0:
            self.message_user(
                request, 
                f'All {tested_count} links tested successfully!',
                level=messages.SUCCESS
            )
        else:
            self.message_user(
                request, 
                'No external links found to test.',
                level=messages.INFO
            )
    test_utility_bar_links.short_description = "Test all external links"
    
    def export_configuration(self, request, queryset):
        """Export utility bar configurations as JSON"""
        import json
        from django.http import HttpResponse
        
        export_data = []
        for obj in queryset:
            config = {
                'name': obj.name,
                'background_color': obj.background_color,
                'text_color': obj.text_color,
                'height': obj.height,
                'position': obj.position,
                'show_social_icons': obj.show_social_icons,
                'facebook_url': obj.facebook_url,
                'twitter_url': obj.twitter_url,
                'instagram_url': obj.instagram_url,
                'youtube_url': obj.youtube_url,
                'linkedin_url': obj.linkedin_url,
                'show_contact_info': obj.show_contact_info,
                'contact_phone': obj.contact_phone,
                'contact_email': obj.contact_email,
                'show_custom_links': obj.show_custom_links,
                'custom_link_1_text': obj.custom_link_1_text,
                'custom_link_1_url': obj.custom_link_1_url,
                'custom_link_2_text': obj.custom_link_2_text,
                'custom_link_2_url': obj.custom_link_2_url,
                'custom_link_3_text': obj.custom_link_3_text,
                'custom_link_3_url': obj.custom_link_3_url,
                'show_on_mobile': obj.show_on_mobile,
                'mobile_collapsed': obj.mobile_collapsed,
                'created_at': obj.created_at.isoformat() if hasattr(obj, 'created_at') else None,
            }
            export_data.append(config)
        
        response = HttpResponse(
            json.dumps(export_data, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="utility_bar_configurations.json"'
        
        self.message_user(
            request,
            f'{len(export_data)} utility bar configuration(s) exported successfully.',
            level=messages.SUCCESS
        )
        
        return response
    export_configuration.short_description = "Export configurations as JSON"
    
    def get_queryset(self, request):
        """Optimize queryset for list display"""
        return super().get_queryset(request).order_by('-is_active', '-created_at')
    
    def changelist_view(self, request, extra_context=None):
        """Add extra context to the changelist view"""
        extra_context = extra_context or {}
        
        # Add statistics
        total_count = TopUtilityBar.objects.count()
        active_count = TopUtilityBar.objects.filter(is_active=True).count()
        inactive_count = total_count - active_count
        
        extra_context.update({
            'total_utility_bars': total_count,
            'active_utility_bars': active_count,
            'inactive_utility_bars': inactive_count,
            'has_active': active_count > 0,
        })
        
        return super().changelist_view(request, extra_context=extra_context)
    
    class Media:
        css = {
            'all': (
                'admin/css/top_utility_bar_admin.css',
            )
        }
        js = (
            'admin/js/top_utility_bar_admin.js',
        )


@admin.register(CustomLink)
class CustomLinkAdmin(admin.ModelAdmin):
    """Standalone admin interface for CustomLink management"""
    
    form = CustomLinkForm
    list_display = [
        'text', 'url', 'icon_class', 'tooltip', 'open_in_new_tab', 
        'ordering', 'is_active', 'created_at'
    ]
    list_filter = [
        'is_active', 'open_in_new_tab', 'created_at'
    ]
    list_editable = ['ordering', 'is_active']
    search_fields = ['text', 'url', 'tooltip']
    ordering = ['ordering', '-created_at']
    actions = [
        'activate_links', 'deactivate_links', 'duplicate_links',
        'test_links'
    ]
    
    fieldsets = (
        ('Link Information', {
            'fields': ('text', 'url', 'icon_class', 'tooltip'),
            'description': 'Basic link information and appearance'
        }),
        ('Link Behavior', {
            'fields': ('open_in_new_tab',),
            'description': 'How the link should behave when clicked'
        }),
        ('Display Options', {
            'fields': ('ordering', 'is_active'),
            'description': 'Control how and when this link appears'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def activate_links(self, request, queryset):
        """Activate selected custom links"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request, 
            f'{updated} custom link(s) have been activated.',
            level=messages.SUCCESS
        )
    activate_links.short_description = "Activate selected custom links"
    
    def deactivate_links(self, request, queryset):
        """Deactivate selected custom links"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request, 
            f'{updated} custom link(s) have been deactivated.',
            level=messages.SUCCESS
        )
    deactivate_links.short_description = "Deactivate selected custom links"
    
    def duplicate_links(self, request, queryset):
        """Create copies of selected custom links"""
        duplicated = 0
        for link in queryset:
            link.pk = None
            link.text = f"{link.text} (Copy)"
            link.is_active = False  # Make copies inactive by default
            link.save()
            duplicated += 1
        
        if duplicated > 0:
            self.message_user(
                request, 
                f'{duplicated} custom link(s) have been duplicated successfully. '
                'All copies are inactive by default.',
                level=messages.SUCCESS
            )
    duplicate_links.short_description = "Duplicate selected custom links"
    
    def test_links(self, request, queryset):
        """Test URLs of selected custom links"""
        import requests
        from urllib.parse import urlparse
        
        tested_count = 0
        broken_links = []
        
        for link in queryset:
            if link.url and link.url.startswith(('http://', 'https://')):
                tested_count += 1
                try:
                    response = requests.head(link.url, timeout=10, allow_redirects=True)
                    if response.status_code >= 400:
                        broken_links.append(f'{link.text}: {link.url} (Status: {response.status_code})')
                except Exception as e:
                    broken_links.append(f'{link.text}: {link.url} (Error: {str(e)[:50]}...)')
        
        # Report results
        if broken_links:
            self.message_user(
                request, 
                f'Link testing completed. {len(broken_links)} broken links found out of {tested_count} tested:\n'
                + '\n'.join(broken_links),
                level=messages.WARNING
            )
        elif tested_count > 0:
            self.message_user(
                request, 
                f'All {tested_count} external links tested successfully!',
                level=messages.SUCCESS
            )
        else:
            self.message_user(
                request, 
                'No external links found to test.',
                level=messages.INFO
            )
    test_links.short_description = "Test selected link URLs"
    
    def get_queryset(self, request):
        """Optimize queryset for list display"""
        return super().get_queryset(request).order_by('ordering', '-created_at')
    
    class Media:
        css = {
            'all': ('admin/css/custom_link_admin.css',)
        }
        js = ('admin/js/custom_link_admin.js',)


@admin.register(ScrollingNotification)
class ScrollingNotificationAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'priority', 'color_theme', 'is_currently_active_display', 
        'is_active', 'start_date', 'end_date', 'display_order', 'created_at'
    ]
    list_filter = [
        'priority', 'color_theme', 'is_active', 'start_date', 'end_date', 'created_at'
    ]
    list_editable = ['display_order', 'is_active']
    search_fields = ['title', 'message', 'link_text']
    ordering = ['display_order', '-priority', '-start_date']
    
    fieldsets = (
        ('Notification Content', {
            'fields': ('title', 'message', 'link_text', 'link_url'),
            'description': 'Main notification content and optional action link'
        }),
        ('Appearance', {
            'fields': ('priority', 'color_theme', 'show_icon', 'icon_class'),
            'description': 'Visual styling and importance level'
        }),
        ('Timing & Display', {
            'fields': ('start_date', 'end_date', 'display_order'),
            'description': 'When and how to display this notification'
        }),
        ('Animation Settings', {
            'fields': ('scroll_speed', 'pause_on_hover'),
            'classes': ('collapse',),
            'description': 'Animation behavior settings'
        }),
        ('Status', {
            'fields': ('is_active',),
            'description': 'Enable or disable this notification'
        }),
    )
    
    def is_currently_active_display(self, obj):
        if obj.is_currently_active:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">\u2713 Active</span>'
            )
        else:
            return format_html(
                '<span style="color: #dc3545;">\u2717 Inactive</span>'
            )
    is_currently_active_display.short_description = 'Status'
    is_currently_active_display.admin_order_field = 'is_active'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('display_order', '-priority', '-start_date')
    
    actions = ['activate_notifications', 'deactivate_notifications', 'duplicate_notifications']
    
    def activate_notifications(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} notification(s) were activated.')
    activate_notifications.short_description = "Activate selected notifications"
    
    def deactivate_notifications(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} notification(s) were deactivated.')
    deactivate_notifications.short_description = "Deactivate selected notifications"
    
    def duplicate_notifications(self, request, queryset):
        count = 0
        for notification in queryset:
            notification.pk = None
            notification.title = f"{notification.title} (Copy)"
            notification.is_active = False  # Make copies inactive by default
            notification.save()
            count += 1
        self.message_user(request, f'{count} notification(s) were duplicated (inactive by default).')
    duplicate_notifications.short_description = "Duplicate selected notifications"
    
    class Media:
        css = {
            'all': ('admin/css/scrolling_notification_admin.css',)
        }


# Slider Image Admin

class SliderImageForm(forms.ModelForm):
    class Meta:
        model = SliderImage
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter slide title (e.g., Welcome to Chaitanya College)'
            }),
            'caption': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Optional description text for the slide'
            }),
            'button_text': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Optional button text (e.g., Learn More, Apply Now)'
            }),
            'button_url': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Button destination URL'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Alternative text for accessibility (auto-generated if empty)'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].help_text = 'Main title that appears on the slide'
        self.fields['caption'].help_text = 'Description text that appears below the title'
        self.fields['image'].help_text = 'Slider image (recommended size: 1920x800px or 16:9 ratio)'
        self.fields['button_text'].help_text = 'Optional action button text'
        self.fields['button_url'].help_text = 'URL where the button should link to'
        self.fields['ordering'].help_text = 'Display order (lower numbers appear first)'
        self.fields['is_active'].help_text = 'Uncheck to hide this slide from the slider'
        self.fields['start_date'].help_text = 'Optional: When to start showing this slide'
        self.fields['end_date'].help_text = 'Optional: When to stop showing this slide'
        self.fields['alt_text'].help_text = 'Image description for screen readers'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check if it's a new upload
            if hasattr(image, 'content_type'):
                if image.size > 8 * 1024 * 1024:  # 8MB limit
                    raise forms.ValidationError('Image file too large. Maximum size is 8MB.')
                if not image.content_type.startswith('image/'):
                    raise forms.ValidationError('Please upload a valid image file.')
        return image


@admin.register(SliderImage)
class SliderImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = SliderImageForm
    list_display = [
        'image_preview', 'title', 'get_status_display', 'has_button', 
        'ordering', 'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'start_date', 'end_date', 'created_at']
    list_editable = ['ordering', 'is_active']
    search_fields = ['title', 'caption', 'button_text']
    actions = ['activate_slides', 'deactivate_slides', 'duplicate_slides']
    
    fieldsets = (
        ('Slide Content', {
            'fields': ('title', 'caption', 'image', 'alt_text'),
            'description': 'Main slide content and image'
        }),
        ('Action Button (Optional)', {
            'fields': ('button_text', 'button_url'),
            'description': 'Optional call-to-action button'
        }),
        ('Display Settings', {
            'fields': ('ordering', 'is_active'),
            'description': 'Control how and when this slide appears'
        }),
        ('Scheduling (Optional)', {
            'fields': ('start_date', 'end_date'),
            'classes': ('collapse',),
            'description': 'Optional scheduling for automatic show/hide'
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 100px; border-radius: 4px; object-fit: cover; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 100px; height: 60px; background: #f8f9fa; border: 1px dashed #dee2e6; display: flex; align-items: center; justify-content: center; border-radius: 4px; font-size: 12px; color: #6c757d;">No Image</div>'
        )
    image_preview.short_description = 'Preview'
    
    def get_status_display(self, obj):
        if obj.is_currently_active:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">\u2713 Active Now</span>'
            )
        elif not obj.is_active:
            return format_html(
                '<span style="color: #dc3545;">\u2717 Disabled</span>'
            )
        else:
            return format_html(
                '<span style="color: #ffc107;">\u23F8 Scheduled</span>'
            )
    get_status_display.short_description = 'Status'
    get_status_display.admin_order_field = 'is_active'
    
    def has_button(self, obj):
        return obj.has_button
    has_button.boolean = True
    has_button.short_description = 'Button'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('ordering', '-created_at')
    
    # Custom Actions
    def activate_slides(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} slide(s) were activated.')
    activate_slides.short_description = "Activate selected slides"
    
    def deactivate_slides(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} slide(s) were deactivated.')
    deactivate_slides.short_description = "Deactivate selected slides"
    
    def duplicate_slides(self, request, queryset):
        count = 0
        for slide in queryset:
            slide.pk = None
            slide.title = f"{slide.title} (Copy)"
            slide.is_active = False  # Make copies inactive by default
            slide.save()
            count += 1
        self.message_user(request, f'{count} slide(s) were duplicated (inactive by default).')
    duplicate_slides.short_description = "Duplicate selected slides"
    
    class Media:
        css = {
            'all': ('admin/css/slider_admin.css',)
        }
        js = ('admin/js/slider_admin.js',)


@admin.register(HeaderInfo)
class HeaderInfoAdmin(admin.ModelAdmin):
    list_display = [
        'college_name', 'email', 'phone', 'header_layout', 
        'show_college_name', 'show_contact_info', 'show_social_links', 'is_active'
    ]
    list_filter = [
        'is_active', 'header_layout', 'show_college_name', 'show_address', 
        'show_affiliations', 'show_contact_info', 'show_social_links'
    ]
    search_fields = ['college_name', 'email', 'phone', 'college_address']
    
    fieldsets = (
        ('College Name Settings', {
            'fields': (
                'college_name', 'show_college_name', 'college_name_font_family', 
                'college_name_font_size', 'college_name_font_weight', 'college_name_color'
            ),
            'description': 'Configure college name display and typography'
        }),
        ('Address Settings', {
            'fields': (
                'college_address', 'show_address', 'address_font_size', 
                'address_font_weight', 'address_color'
            ),
            'description': 'Configure college address display and typography'
        }),
        ('Affiliations Settings', {
            'fields': (
                'college_affiliations', 'show_affiliations', 'affiliations_font_size', 
                'affiliations_font_weight', 'affiliations_color'
            ),
            'description': 'Configure college affiliations and recognitions'
        }),
        ('Contact Information', {
            'fields': (
                'email', 'phone', 'website_url', 'show_contact_info', 
                'contact_font_size', 'contact_color'
            ),
            'description': 'Contact details and styling'
        }),
        ('Left Side Logos', {
            'fields': (
                ('left_logo_1', 'left_logo_1_alt', 'left_logo_1_link'),
                ('left_logo_2', 'left_logo_2_alt', 'left_logo_2_link'),
                ('left_logo_3', 'left_logo_3_alt', 'left_logo_3_link')
            ),
            'description': 'Upload up to 3 logos for left side (recommended: 60x60px each)',
            'classes': ('collapse',)
        }),
        ('Right Side Logos', {
            'fields': (
                ('right_logo_1', 'right_logo_1_alt', 'right_logo_1_link'),
                ('right_logo_2', 'right_logo_2_alt', 'right_logo_2_link'),
                ('right_logo_3', 'right_logo_3_alt', 'right_logo_3_link')
            ),
            'description': 'Upload up to 3 logos for right side (recommended: 60x60px each)',
            'classes': ('collapse',)
        }),
        ('Logo Settings', {
            'fields': ('logo_size',),
            'description': 'Configure logo sizing for all logos'
        }),
        ('Social Media Links', {
            'fields': (
                'facebook_url', 'youtube_url', 'instagram_url', 'twitter_url', 
                'linkedin_url', 'whatsapp_number', 'show_social_links'
            ),
            'classes': ('collapse',)
        }),
        ('Header Layout & Styling', {
            'fields': (
                'header_layout', 'header_background_color', 'header_border_bottom', 
                'header_border_color', 'header_shadow'
            ),
            'description': 'Configure header appearance and layout'
        }),
        ('Responsive Settings', {
            'fields': (
                'mobile_stack_layout', 'hide_affiliations_mobile'
            ),
            'description': 'Mobile and tablet display options',
            'classes': ('collapse',)
        }),
        ('Animation Effects', {
            'fields': ('enable_animations',),
            'description': 'Enable hover effects and smooth transitions',
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    class Media:
        css = {
            'all': (
                'admin/css/header_admin.css',
                'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700;800&family=Roboto:wght@300;400;500;700&display=swap'
            )
        }
        js = (
            'admin/js/header_admin.js',
            'https://cdn.jsdelivr.net/npm/spectrum-colorpicker2/dist/spectrum.min.js'
        )


@admin.register(NavbarInfo)
class NavbarInfoAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'show_logo', 'show_brand_text', 'is_sticky', 'is_active']
    list_filter = ['is_active', 'show_logo', 'show_brand_text', 'is_sticky']
    
    fieldsets = (
        ('Brand Information', {
            'fields': ('brand_name', 'brand_subtitle', 'logo', 'show_logo', 'show_brand_text')
        }),
        ('Navigation Behavior', {
            'fields': ('is_sticky', 'show_below_header')
        }),
        ('Search Settings', {
            'fields': ('enable_search', 'search_placeholder')
        }),
        ('Styling', {
            'fields': ('navbar_background_color', 'navbar_text_color', 'navbar_hover_color', 'navbar_border_color'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(CollegeInfo)
class CollegeInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'establishment_year', 'is_active', 'created_at']
    list_filter = ['is_active', 'establishment_year']
    search_fields = ['name', 'email', 'phone']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'establishment_year', 'affiliation', 'address_line', 'email', 'phone', 'slug', 'is_active')
        }),
        ('Mission & Messages', {
            'fields': ('mission_statement_short', 'mission_statement_long', 'founder_name', 'founder_message', 'principal_name', 'principal_message')
        }),
        ('Statistics', {
            'fields': ('courses_count', 'students_count', 'faculty_staff_count', 'years_of_excellence')
        }),
        ('Achievements', {
            'fields': ('naac_grade', 'iic_rating')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'youtube_url', 'instagram_url')
        }),
        ('Images', {
            'fields': ('logo', 'hero_image')
        }),
    )


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'discipline', 'duration', 'is_active', 'created_at']
    list_filter = ['discipline', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


# Event Image Forms and Inlines

class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ['image', 'caption', 'alt_text', 'is_cover', 'ordering']
        widgets = {
            'caption': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Optional image caption'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Alternative text for accessibility (auto-generated if empty)'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '0',
                'style': 'width: 80px;'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Upload event image (JPG, PNG, GIF). Recommended size: 800x600px or larger'
        self.fields['caption'].help_text = 'Optional caption that will appear below the image'
        self.fields['alt_text'].help_text = 'Alternative text for screen readers (auto-generated if empty)'
        self.fields['is_cover'].help_text = 'Mark as main cover image for this event'
        self.fields['ordering'].help_text = 'Display order within the event gallery'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validate file size (max 5MB)
            if hasattr(image, 'size') and image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file too large. Maximum size is 5MB.')
            
            # Validate file type
            if hasattr(image, 'content_type') and not image.content_type.startswith('image/'):
                raise forms.ValidationError('Please upload a valid image file.')
        
        return image


class EventImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = EventImage
    form = EventImageForm
    extra = 1
    min_num = 0
    fields = ('image_preview', 'image', 'caption', 'alt_text', 'is_cover', 'ordering')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 80px; border-radius: 4px; object-fit: cover; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 80px; height: 60px; background: #f8f9fa; border: 1px dashed #dee2e6; display: flex; align-items: center; justify-content: center; border-radius: 4px; font-size: 12px; color: #6c757d;">'
            '<i class="fas fa-plus" style="opacity: 0.5;"></i>'
            '</div>'
        )
    image_preview.short_description = "Preview"
    
    class Media:
        css = {
            'all': ('admin/css/event_admin.css',)
        }
        js = ('admin/js/event_admin.js',)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter event title (e.g., Annual Day Celebration 2024)'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Event venue/location'
            }),
            'organizer': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Organizing department or person'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Contact person name'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+91-XXXXXXXXXX'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'contact@example.com'
            }),
            'registration_link': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://registration-form-url.com'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control', 
                'type': 'time'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].help_text = 'Event title that will appear on the website'
        self.fields['description'].help_text = 'Detailed description of the event'
        self.fields['date'].help_text = 'Event date'
        self.fields['time'].help_text = 'Event start time (optional)'
        self.fields['location'].help_text = 'Where the event will take place'
        self.fields['type'].help_text = 'Category of the event'
        self.fields['banner_image'].help_text = 'Main banner image for the event (optional if you add images below)'
        self.fields['organizer'].help_text = 'Department or organization hosting the event'
        self.fields['registration_required'].help_text = 'Check if attendees need to register'
        self.fields['registration_link'].help_text = 'External registration form URL (if required)'
        self.fields['is_featured'].help_text = 'Featured events appear prominently on homepage'
        self.fields['is_active'].help_text = 'Uncheck to hide this event from the website'


@admin.register(Event)
class EventAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = EventForm
    list_display = ['title', 'date', 'time', 'type', 'location', 'get_images_count', 'is_featured', 'is_active']
    list_filter = ['type', 'is_active', 'is_featured', 'date', 'registration_required']
    list_editable = ['is_featured', 'is_active']
    search_fields = ['title', 'description', 'location', 'organizer']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
    inlines = [EventImageInline]
    actions = ['make_featured', 'remove_featured', 'make_active', 'make_inactive']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'slug', 'description', 'type', 'is_featured', 'is_active'),
            'description': 'Basic event information'
        }),
        ('Date & Location', {
            'fields': ('date', 'time', 'location'),
            'description': 'When and where the event will take place'
        }),
        ('Event Banner', {
            'fields': ('banner_image',),
            'description': 'Main banner image (you can also add multiple images below)',
            'classes': ('collapse',)
        }),
        ('Organization Details', {
            'fields': ('organizer', 'contact_person', 'contact_phone', 'contact_email'),
            'description': 'Contact information and organizer details',
            'classes': ('collapse',)
        }),
        ('Registration', {
            'fields': ('registration_required', 'registration_link'),
            'description': 'Registration settings if applicable',
            'classes': ('collapse',)
        }),
    )
    
    def get_images_count(self, obj):
        count = obj.images.count()
        if count == 0:
            return format_html('<span style="color:#dc3545;">No images</span>')
        elif count < 3:
            return format_html('<span style="color:#ffc107;">{} images</span>', count)
        else:
            return format_html('<span style="color:#28a745;">{} images</span>', count)
    get_images_count.short_description = 'Gallery Images'
    get_images_count.admin_order_field = 'images__count'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('images').order_by('-date')
    
    # Custom Actions
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} event(s) marked as featured.')
    make_featured.short_description = "Mark as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} event(s) removed from featured.')
    remove_featured.short_description = "Remove from featured"
    
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} event(s) activated.')
    make_active.short_description = "Activate events"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} event(s) deactivated.')
    make_inactive.short_description = "Deactivate events"
    
    class Media:
        css = {
            'all': ('admin/css/event_admin.css',)
        }
        js = ('admin/js/event_admin.js',)


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    form = EventImageForm
    list_display = ['image_preview', 'event', 'caption', 'is_cover', 'ordering', 'created_at']
    list_filter = ['event', 'is_cover', 'created_at']
    search_fields = ['caption', 'event__title']
    list_per_page = 20
    
    fieldsets = (
        ('Image Information', {
            'fields': ('event', 'image', 'caption', 'alt_text', 'is_cover', 'ordering')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event')
    
    class Media:
        css = {
            'all': ('admin/css/event_admin.css',)
        }


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'publish_date', 'has_attachment', 'is_active', 'convert_to_notification_button']
    list_filter = ['category', 'is_active', 'publish_date']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    
    def has_attachment(self, obj):
        return bool(obj.attachment)
    has_attachment.boolean = True
    has_attachment.short_description = 'Attachment'
    
    def convert_to_notification_button(self, obj):
        """Add button to convert notice to scrolling notification"""
        url = reverse('admin:convert_notice_to_notification', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="background: #417690; color: white; padding: 5px 10px; '
            'border-radius: 4px; text-decoration: none; font-size: 12px; display: inline-block; '
            'text-align: center; min-width: 80px;">'
            '<i class="fas fa-bell"></i> Add to Ticker</a>',
            url
        )
    convert_to_notification_button.short_description = 'Convert to Notification'
    convert_to_notification_button.allow_tags = True
    
    def get_urls(self):
        """Add custom URL for notice conversion"""
        urls = super().get_urls()
        custom_urls = [
            path(
                'convert-notice-to-notification/<int:notice_id>/',
                self.admin_site.admin_view(self.convert_notice_to_notification),
                name='convert_notice_to_notification'
            ),
        ]
        return custom_urls + urls
    
    def convert_notice_to_notification(self, request, notice_id):
        """Convert a notice to scrolling notification"""
        try:
            notice = Notice.objects.get(pk=notice_id)
            
            # Create scrolling notification from notice
            notification = ScrollingNotification.objects.create(
                title=notice.title[:200],  # Limit to 200 chars
                message=notice.content[:500] if len(notice.content) <= 500 else notice.content[:497] + '...',
                link_text='View Details',
                link_url=notice.get_absolute_url(),
                priority='medium',
                color_theme='primary',
                icon_class='fas fa-bullhorn',
                scroll_speed=50,
                start_date=datetime.now(timezone.utc),
                end_date=datetime.now(timezone.utc) + timedelta(days=30),
                is_active=True,
                pause_on_hover=True,
                show_icon=True,
                display_order=0
            )
            
            messages.success(
                request, 
                f'Notice "{notice.title}" has been successfully converted to scrolling notification '
                f'and will appear in the ticker for 30 days. '
                f'<a href="{reverse("admin:college_website_scrollingnotification_change", args=[notification.pk])}">'
                f'Edit notification</a>'
            )
            
        except Notice.DoesNotExist:
            messages.error(request, 'Notice not found.')
        except Exception as e:
            messages.error(request, f'Error converting notice: {str(e)}')
        
        # Redirect back to notice list
        return HttpResponseRedirect(reverse('admin:college_website_notice_changelist'))


@admin.register(SocialInitiative)
class SocialInitiativeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(StudentTestimonial)
class StudentTestimonialAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'program_studied', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['student_name', 'program_studied', 'feedback_text']
    prepopulated_fields = {'slug': ('student_name', 'program_studied')}


@admin.register(ImportantLink)
class ImportantLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'type', 'url', 'is_active', 'ordering']
    list_filter = ['type', 'is_active']
    search_fields = ['name', 'url']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'status', 'submission_date']
    list_filter = ['status', 'submission_date']
    search_fields = ['first_name', 'last_name', 'email', 'comments']
    readonly_fields = ['submission_date']
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-submission_date')


# CMS Admin

# Custom Forms for Menu Management
class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter menu title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Auto-generated from title'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].help_text = 'The display name for this menu'
        self.fields['slug'].help_text = 'URL-friendly version (auto-generated if empty)'
        self.fields['is_active'].help_text = 'Uncheck to hide this menu from the website'
        self.fields['ordering'].help_text = 'Lower numbers appear first'


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['menu', 'parent', 'title', 'slug', 'path_type', 'external_url', 'page', 'is_active', 'ordering']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter menu item title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Auto-generated from title'}),
            'external_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set help text only for fields that exist in the form
        # 'menu' field is not present when used as inline in MenuAdmin
        if 'menu' in self.fields:
            self.fields['menu'].help_text = 'Select the parent menu'
        if 'parent' in self.fields:
            self.fields['parent'].help_text = 'Leave empty for top-level items, or select a parent for sub-items'
        if 'title' in self.fields:
            self.fields['title'].help_text = 'The display name for this menu item'
        if 'path_type' in self.fields:
            self.fields['path_type'].help_text = 'Choose whether this links to an internal page or external URL'
        if 'external_url' in self.fields:
            self.fields['external_url'].help_text = 'Required if path type is External'
        if 'page' in self.fields:
            self.fields['page'].help_text = 'Required if path type is Internal'
        if 'is_active' in self.fields:
            self.fields['is_active'].help_text = 'Uncheck to hide this item from the menu'
        if 'ordering' in self.fields:
            self.fields['ordering'].help_text = 'Lower numbers appear first'

    def clean(self):
        cleaned_data = super().clean()
        path_type = cleaned_data.get('path_type')
        external_url = cleaned_data.get('external_url')
        page = cleaned_data.get('page')

        if path_type == 'external' and not external_url:
            raise forms.ValidationError('External URL is required when path type is External')
        
        if path_type == 'internal' and not page:
            raise forms.ValidationError('Page selection is required when path type is Internal')
        
        return cleaned_data


# Enhanced Inline for MenuItem with better interface
class MenuItemInline(SortableInlineAdminMixin, admin.StackedInline):
    model = MenuItem
    form = MenuItemForm
    extra = 1
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'parent', 'is_active', 'ordering')
        }),
        ('Link Configuration', {
            'fields': ('path_type', 'external_url', 'page'),
            'description': 'Configure where this menu item should link to'
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/menu_admin.css',)
        }
        js = ('admin/js/menu_admin.js',)


# Nested Inline for Sub-menu Items
class SubMenuItemInline(admin.TabularInline):
    model = MenuItem
    fk_name = 'parent'
    extra = 0
    fields = ('title', 'slug', 'path_type', 'external_url', 'page', 'is_active', 'ordering')
    prepopulated_fields = {'slug': ('title',)}
    verbose_name = 'Sub-menu Item'
    verbose_name_plural = 'Sub-menu Items'


@admin.register(Menu)
class MenuAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = MenuForm
    list_display = ['title', 'slug', 'get_items_count', 'is_active', 'ordering']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'ordering']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [MenuItemInline]
    
    fieldsets = (
        ('Menu Information', {
            'fields': ('title', 'slug', 'is_active', 'ordering'),
            'description': 'Basic menu configuration'
        }),
    )
    
    def get_items_count(self, obj):
        count = obj.items.count()
        active_count = obj.items.filter(is_active=True).count()
        return f"{active_count}/{count} active"
    get_items_count.short_description = 'Menu Items'
    get_items_count.admin_order_field = 'items__count'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')
    
    class Media:
        css = {
            'all': ('admin/css/menu_admin.css',)
        }
        js = ('admin/js/menu_admin.js',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemForm
    list_display = ['title', 'menu', 'parent', 'path_type', 'get_url_display', 'is_active', 'ordering']
    list_filter = ['menu', 'path_type', 'is_active', 'parent']
    list_editable = ['is_active', 'ordering']
    search_fields = ['title', 'menu__title']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SubMenuItemInline]
    actions = [
        'move_to_menu_action', 'make_submenu_action', 'make_top_level_action', 
        'duplicate_menu_items', 'activate_items', 'deactivate_items',
        'export_menu_structure'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('menu', 'parent', 'title', 'slug', 'is_active', 'ordering')
        }),
        ('Link Configuration', {
            'fields': ('path_type', 'external_url', 'page'),
            'description': 'Configure where this menu item should link to'
        }),
    )
    
    def get_url_display(self, obj):
        url = obj.get_url()
        if len(url) > 50:
            return f"{url[:47]}..."
        return url
    get_url_display.short_description = 'URL'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('menu', 'parent', 'page')
    
    # Admin Actions for Menu Management
    def move_to_menu_action(self, request, queryset):
        """Move selected menu items to a different menu"""
        if queryset.count() == 0:
            self.message_user(request, "No items selected.", level=messages.WARNING)
            return
        
        # Store selected IDs for the intermediate form
        request.session['selected_menu_items'] = list(queryset.values_list('id', flat=True))
        
        # Redirect to custom view for menu selection
        return HttpResponseRedirect(reverse('admin:menu_move_items'))
    move_to_menu_action.short_description = "Move selected items to another menu"
    
    def make_submenu_action(self, request, queryset):
        """Make selected items submenus of another item"""
        if queryset.count() == 0:
            self.message_user(request, "No items selected.", level=messages.WARNING)
            return
        
        # Store selected IDs for the intermediate form
        request.session['selected_menu_items'] = list(queryset.values_list('id', flat=True))
        
        # Redirect to custom view for parent selection
        return HttpResponseRedirect(reverse('admin:menu_make_submenu'))
    make_submenu_action.short_description = "Make selected items submenus"
    
    def make_top_level_action(self, request, queryset):
        """Make selected items top-level (remove parent)"""
        updated = 0
        for item in queryset:
            if item.parent:
                item.parent = None
                item.save()
                updated += 1
        
        if updated > 0:
            self.message_user(
                request, 
                f'{updated} menu item(s) moved to top level.',
                level=messages.SUCCESS
            )
        else:
            self.message_user(
                request, 
                'No items were changed (they were already top-level).',
                level=messages.INFO
            )
    make_top_level_action.short_description = "Make selected items top-level"
    
    def duplicate_menu_items(self, request, queryset):
        """Duplicate selected menu items"""
        duplicated = 0
        for item in queryset:
            # Store children before duplicating parent
            children = list(item.children.all())
            
            # Duplicate the item
            item.pk = None
            item.title = f"{item.title} (Copy)"
            item.slug = f"{item.slug}-copy"
            item.is_active = False  # Make copies inactive by default
            item.save()
            duplicated += 1
            
            # Duplicate children if any
            for child in children:
                child.pk = None
                child.parent = item
                child.title = f"{child.title} (Copy)"
                child.slug = f"{child.slug}-copy"
                child.is_active = False
                child.save()
                duplicated += 1
        
        self.message_user(
            request, 
            f'{duplicated} menu item(s) duplicated successfully (inactive by default).',
            level=messages.SUCCESS
        )
    duplicate_menu_items.short_description = "Duplicate selected items (with children)"
    
    def activate_items(self, request, queryset):
        """Activate selected menu items"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request, 
            f'{updated} menu item(s) activated.',
            level=messages.SUCCESS
        )
    activate_items.short_description = "Activate selected items"
    
    def deactivate_items(self, request, queryset):
        """Deactivate selected menu items"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request, 
            f'{updated} menu item(s) deactivated.',
            level=messages.SUCCESS
        )
    deactivate_items.short_description = "Deactivate selected items"
    
    def export_menu_structure(self, request, queryset):
        """Export menu structure for selected items"""
        if queryset.count() == 0:
            self.message_user(request, "No items selected.", level=messages.WARNING)
            return
        
        import json
        from django.http import JsonResponse
        
        # Build export data
        export_data = []
        for item in queryset:
            item_data = {
                'title': item.title,
                'slug': item.slug,
                'menu': item.menu.title,
                'parent': item.parent.title if item.parent else None,
                'path_type': item.path_type,
                'external_url': item.external_url,
                'page': item.page.title if item.page else None,
                'icon_class': item.icon_class,
                'description': item.description,
                'ordering': item.ordering,
                'is_active': item.is_active,
                'created_at': item.created_at.isoformat() if hasattr(item, 'created_at') else None,
            }
            export_data.append(item_data)
        
        # Store export data in session for download view
        request.session['menu_export_data'] = export_data
        
        # Redirect to export download view
        return HttpResponseRedirect(reverse('admin:menu_export_download'))
    export_menu_structure.short_description = "Export selected items structure"
    
    def get_urls(self):
        """Add custom URLs for menu management"""
        urls = super().get_urls()
        custom_urls = [
            path(
                'move-items/',
                self.admin_site.admin_view(self.move_items_view),
                name='menu_move_items'
            ),
            path(
                'make-submenu/',
                self.admin_site.admin_view(self.make_submenu_view),
                name='menu_make_submenu'
            ),
            path(
                'export-download/',
                self.admin_site.admin_view(self.export_download_view),
                name='menu_export_download'
            ),
            path(
                'tree-view/',
                self.admin_site.admin_view(self.tree_view),
                name='menu_tree_view'
            ),
        ]
        return custom_urls + urls
    
    def move_items_view(self, request):
        """Custom view for moving menu items"""
        from .forms import BulkMenuMoveForm
        
        selected_ids = request.session.get('selected_menu_items', [])
        if not selected_ids:
            messages.error(request, "No menu items selected.")
            return HttpResponseRedirect(reverse('admin:college_website_menuitem_changelist'))
        
        selected_items = MenuItem.objects.filter(id__in=selected_ids)
        
        if request.method == 'POST':
            form = BulkMenuMoveForm(request.POST)
            if form.is_valid():
                target_menu = form.cleaned_data['target_menu']
                make_submenu_of = form.cleaned_data.get('make_submenu_of')
                starting_order = form.cleaned_data['starting_order']
                preserve_hierarchy = form.cleaned_data['preserve_hierarchy']
                
                # Perform the move operation
                moved_count = 0
                for i, item in enumerate(selected_items):
                    item.menu = target_menu
                    if not preserve_hierarchy or not item.parent or item.parent not in selected_items:
                        item.parent = make_submenu_of
                    item.ordering = starting_order + i
                    item.save()
                    moved_count += 1
                
                # Clear session data
                if 'selected_menu_items' in request.session:
                    del request.session['selected_menu_items']
                
                messages.success(request, f'{moved_count} menu items moved successfully.')
                return HttpResponseRedirect(reverse('admin:college_website_menuitem_changelist'))
        else:
            form = BulkMenuMoveForm()
        
        context = {
            'form': form,
            'selected_items': selected_items,
            'title': 'Move Menu Items',
            'opts': self.model._meta,
        }
        
        return render(request, 'admin/college_website/menuitem/move_items.html', context)
    
    def make_submenu_view(self, request):
        """Custom view for making items submenus"""
        selected_ids = request.session.get('selected_menu_items', [])
        if not selected_ids:
            messages.error(request, "No menu items selected.")
            return HttpResponseRedirect(reverse('admin:college_website_menuitem_changelist'))
        
        selected_items = MenuItem.objects.filter(id__in=selected_ids)
        
        # Get potential parent choices (exclude selected items and their descendants)
        potential_parents = MenuItem.objects.filter(is_active=True).exclude(id__in=selected_ids)
        
        if request.method == 'POST':
            parent_id = request.POST.get('parent')
            if parent_id:
                parent = MenuItem.objects.get(id=parent_id)
                updated_count = 0
                for item in selected_items:
                    # Validate that we're not creating circular references
                    if not self._would_create_circular_reference(item, parent):
                        item.parent = parent
                        item.menu = parent.menu  # Move to same menu as parent
                        item.save()
                        updated_count += 1
                
                # Clear session data
                if 'selected_menu_items' in request.session:
                    del request.session['selected_menu_items']
                
                messages.success(request, f'{updated_count} menu items made submenus successfully.')
            else:
                messages.error(request, "No parent selected.")
            
            return HttpResponseRedirect(reverse('admin:college_website_menuitem_changelist'))
        
        context = {
            'selected_items': selected_items,
            'potential_parents': potential_parents,
            'title': 'Make Submenus',
            'opts': self.model._meta,
        }
        
        return render(request, 'admin/college_website/menuitem/make_submenu.html', context)
    
    def export_download_view(self, request):
        """Download exported menu structure"""
        export_data = request.session.get('menu_export_data')
        if not export_data:
            messages.error(request, "No export data available.")
            return HttpResponseRedirect(reverse('admin:college_website_menuitem_changelist'))
        
        import json
        from django.http import HttpResponse
        
        # Create JSON response
        response = HttpResponse(
            json.dumps(export_data, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="menu_structure.json"'
        
        # Clear session data
        if 'menu_export_data' in request.session:
            del request.session['menu_export_data']
        
        return response
    
    def tree_view(self, request):
        """Tree view for menu structure visualization"""
        menus = Menu.objects.filter(is_active=True).prefetch_related(
            'items__children__children__children'  # Support up to 4 levels deep
        )
        
        context = {
            'menus': menus,
            'title': 'Menu Tree View',
            'opts': self.model._meta,
        }
        
        return render(request, 'admin/college_website/menuitem/tree_view.html', context)
    
    def _would_create_circular_reference(self, item, potential_parent):
        """Check if making item a child of potential_parent would create a circular reference"""
        current = potential_parent
        while current:
            if current == item:
                return True
            current = current.parent
        return False
    
    class Media:
        css = {
            'all': ('admin/css/menu_admin.css',)
        }
        js = ('admin/js/menu_admin.js',)


# Content Block Inlines

# GalleryImageForm definition - must be before EnhancedGalleryImageInline
class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'caption', 'ordering']
        widgets = {
            'caption': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Optional image description'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '0',
                'style': 'width: 80px;'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Upload image (JPG, PNG, GIF). Recommended size: 800x600px or larger'
        self.fields['caption'].help_text = 'Optional caption that will appear below the image'
        self.fields['ordering'].help_text = 'Display order within the gallery'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validate file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file too large. Maximum size is 5MB.')
            
            # Validate file type
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError('Please upload a valid image file.')
        
        return image


class BlockRichTextInline(admin.StackedInline):
    model = BlockRichText
    extra = 0
    fieldsets = (
        ('Content Block', {
            'fields': ('title', 'body', 'ordering', 'is_active'),
            'description': 'Rich text content with CKEditor support'
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/content_blocks.css',)
        }
        js = ('admin/js/content_blocks.js',)


class EnhancedGalleryImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = GalleryImage
    form = GalleryImageForm
    extra = 1
    min_num = 0
    fields = ('image_preview', 'image', 'caption', 'ordering')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<div class="image-upload-preview">'
                '<img src="{}" style="max-height: 80px; max-width: 120px; border-radius: 8px; '
                'object-fit: cover; box-shadow: 0 2px 8px rgba(0,0,0,0.15);" />'
                '</div>',
                obj.image.url
            )
        return format_html(
            '<div class="image-upload-placeholder">'
            '<div style="width: 120px; height: 80px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); '
            'border: 2px dashed #dee2e6; display: flex; align-items: center; justify-content: center; '
            'border-radius: 8px; font-size: 12px; color: #6c757d; flex-direction: column;">'
            '<i class="fas fa-camera mb-1" style="font-size: 16px; opacity: 0.6;"></i>'
            '<span>Upload Image</span>'
            '</div></div>'
        )
    image_preview.short_description = "Preview"
    
    class Media:
        css = {
            'all': ('admin/css/gallery_inline.css',)
        }
        js = ('admin/js/gallery_inline.js',)


class BlockImageGalleryInline(admin.StackedInline):
    model = BlockImageGallery
    extra = 0
    fieldsets = (
        ('Gallery Information', {
            'fields': ('title', 'ordering', 'is_active'),
            'description': 'Gallery block settings - images are managed below after saving'
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/content_blocks.css',)
        }
        js = ('admin/js/content_blocks.js',)


class BlockVideoEmbedInline(admin.StackedInline):
    model = BlockVideoEmbed
    extra = 0
    fieldsets = (
        ('Video Information', {
            'fields': ('title', 'provider', 'video_url', 'embed_code', 'ordering', 'is_active'),
            'description': 'Embed videos from YouTube, Vimeo, or custom HTML'
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/content_blocks.css',)
        }
        js = ('admin/js/content_blocks.js',)


class EnhancedDownloadFileInline(SortableInlineAdminMixin, admin.TabularInline):
    model = DownloadFile
    extra = 1
    min_num = 0
    fields = ('file_preview', 'file', 'title', 'description', 'ordering')
    readonly_fields = ('file_preview',)
    
    def file_preview(self, obj):
        if obj.file:
            file_name = obj.file.name.split('/')[-1]
            file_ext = file_name.split('.')[-1].lower() if '.' in file_name else ''
            
            # File type icons
            icon_map = {
                'pdf': 'fas fa-file-pdf text-danger',
                'doc': 'fas fa-file-word text-primary',
                'docx': 'fas fa-file-word text-primary',
                'xls': 'fas fa-file-excel text-success',
                'xlsx': 'fas fa-file-excel text-success',
                'ppt': 'fas fa-file-powerpoint text-warning',
                'pptx': 'fas fa-file-powerpoint text-warning',
                'zip': 'fas fa-file-archive text-secondary',
                'rar': 'fas fa-file-archive text-secondary',
                'txt': 'fas fa-file-alt text-secondary',
                'jpg': 'fas fa-file-image text-info',
                'jpeg': 'fas fa-file-image text-info',
                'png': 'fas fa-file-image text-info',
                'gif': 'fas fa-file-image text-info',
            }
            
            icon_class = icon_map.get(file_ext, 'fas fa-file text-secondary')
            
            return format_html(
                '<div class="file-upload-preview">'
                '<div style="display: flex; align-items: center; padding: 8px; '
                'background: #f8f9fa; border-radius: 6px; min-width: 120px;">'
                '<i class="{} me-2" style="font-size: 18px;"></i>'
                '<div>'
                '<div style="font-size: 12px; font-weight: 500; color: #495057;">{}</div>'
                '<div style="font-size: 10px; color: #6c757d;">Click to download</div>'
                '</div>'
                '</div>'
                '</div>',
                icon_class, file_name
            )
        return format_html(
            '<div class="file-upload-placeholder">'
            '<div style="width: 120px; height: 50px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); '
            'border: 2px dashed #dee2e6; display: flex; align-items: center; justify-content: center; '
            'border-radius: 6px; font-size: 12px; color: #6c757d; flex-direction: column;">'
            '<i class="fas fa-upload mb-1" style="font-size: 14px; opacity: 0.6;"></i>'
            '<span>Upload File</span>'
            '</div></div>'
        )
    file_preview.short_description = "File"
    
    class Media:
        css = {
            'all': ('admin/css/download_inline.css',)
        }
        js = ('admin/js/download_inline.js',)


class BlockDownloadListInline(admin.StackedInline):
    model = BlockDownloadList
    extra = 0
    fieldsets = (
        ('Download List Information', {
            'fields': ('title', 'ordering', 'is_active'),
            'description': 'Download list block settings - files are managed below after saving'
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/content_blocks.css',)
        }
        js = ('admin/js/content_blocks.js',)


class BlockTableHTMLInline(admin.StackedInline):
    model = BlockTableHTML
    extra = 0
    fieldsets = (
        ('Table Information', {
            'fields': ('title', 'html', 'ordering', 'is_active'),
            'description': 'HTML table content block'
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/content_blocks.css',)
        }
        js = ('admin/js/content_blocks.js',)


class BlockFormInline(admin.StackedInline):
    model = BlockForm
    extra = 0
    fieldsets = (
        ('Form Information', {
            'fields': ('title', 'form_type', 'ordering', 'is_active'),
            'description': 'Embed contact, registration, or feedback forms'
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/content_blocks.css',)
        }
        js = ('admin/js/content_blocks.js',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'template_variant', 'show_banner', 'show_sidebar', 'is_active', 'created_at']
    list_filter = ['template_variant', 'show_banner', 'show_sidebar', 'is_active']
    search_fields = ['title', 'meta_title', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'is_active')
        }),
        ('Layout Options', {
            'fields': ('template_variant', 'show_banner', 'show_sidebar', 'enable_search_in_navbar', 'banner_image')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        BlockRichTextInline,
        BlockImageGalleryInline,
        BlockVideoEmbedInline,
        BlockDownloadListInline,
        BlockTableHTMLInline,
        BlockFormInline,
    ]


# Custom Forms for Gallery Management

class BlockImageGalleryForm(forms.ModelForm):
    class Meta:
        model = BlockImageGallery
        fields = ['page', 'title', 'ordering', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter gallery title (e.g., Campus Photos, Events, etc.)'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '0',
                'placeholder': 'Display order'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['page'].help_text = 'Select the page where this gallery will be displayed'
        self.fields['title'].help_text = 'Gallery title (leave blank for default "Image Gallery")'
        self.fields['ordering'].help_text = 'Lower numbers appear first on the page'
        self.fields['is_active'].help_text = 'Uncheck to hide this gallery from the website'
        
        # Make page field more user-friendly
        self.fields['page'].queryset = Page.objects.filter(is_active=True).order_by('title')
        self.fields['page'].empty_label = "Select a page..."




# Enhanced Gallery Images Inline

class GalleryImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = GalleryImage
    form = GalleryImageForm
    extra = 1
    fields = ('image', 'caption', 'ordering')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'
    
    class Media:
        css = {
            'all': ('admin/css/gallery_admin.css',)
        }
        js = ('admin/js/gallery_admin.js',)


@admin.register(BlockImageGallery)
class BlockImageGalleryAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = BlockImageGalleryForm
    list_display = ['title', 'page', 'get_images_count', 'is_active', 'ordering', 'created_at']
    list_filter = ['page', 'is_active', 'created_at']
    list_editable = ['is_active', 'ordering']
    search_fields = ['title', 'page__title']
    inlines = [GalleryImageInline]
    actions = ['make_active', 'make_inactive', 'duplicate_gallery']
    
    fieldsets = (
        ('Gallery Information', {
            'fields': ('page', 'title', 'is_active', 'ordering'),
            'description': 'Basic gallery configuration'
        }),
    )
    
    def get_images_count(self, obj):
        count = obj.images.count()
        if count == 0:
            return format_html('<span style="color:#dc3545;">No images</span>')
        elif count < 3:
            return format_html('<span style="color:#ffc107;">{} images</span>', count)
        else:
            return format_html('<span style="color:#28a745;">{} images</span>', count)
    get_images_count.short_description = 'Images'
    get_images_count.admin_order_field = 'images__count'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('page').prefetch_related('images')
    
    # Custom Actions
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} gallery(s) were successfully activated.')
    make_active.short_description = "Activate selected galleries"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} gallery(s) were successfully deactivated.')
    make_inactive.short_description = "Deactivate selected galleries"
    
    def duplicate_gallery(self, request, queryset):
        count = 0
        for gallery in queryset:
            # Store original images
            original_images = list(gallery.images.all())
            
            # Duplicate gallery
            gallery.pk = None
            gallery.title = f"{gallery.title} (Copy)" if gallery.title else "Image Gallery (Copy)"
            gallery.save()
            
            # Duplicate images
            for image in original_images:
                image.pk = None
                image.gallery = gallery
                image.save()
            
            count += 1
        
        self.message_user(request, f'{count} gallery(s) with all images were successfully duplicated.')
    duplicate_gallery.short_description = "Duplicate selected galleries with images"
    
    class Media:
        css = {
            'all': ('admin/css/gallery_admin.css',)
        }
        js = ('admin/js/gallery_admin.js',)


# Standalone Gallery Image Admin for direct management

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    form = GalleryImageForm
    list_display = ['image_preview', 'gallery', 'caption', 'ordering', 'created_at']
    list_filter = ['gallery__page', 'gallery', 'created_at']
    search_fields = ['caption', 'gallery__title', 'gallery__page__title']
    list_per_page = 20
    
    fieldsets = (
        ('Image Information', {
            'fields': ('gallery', 'image', 'caption', 'ordering')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('gallery', 'gallery__page')
    
    class Media:
        css = {
            'all': ('admin/css/gallery_admin.css',)
        }
        js = ('admin/js/gallery_admin.js',)


# Download Files Inline

class DownloadFileInline(SortableInlineAdminMixin, admin.TabularInline):
    model = DownloadFile
    extra = 0


@admin.register(BlockDownloadList)
class BlockDownloadListAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'page', 'ordering', 'is_active']
    list_filter = ['page', 'is_active']
    inlines = [DownloadFileInline]


# Individual Block Admins

@admin.register(BlockRichText)
class BlockRichTextAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'ordering', 'is_active']
    list_filter = ['page', 'is_active']


@admin.register(BlockVideoEmbed)
class BlockVideoEmbedAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'provider', 'ordering', 'is_active']
    list_filter = ['page', 'provider', 'is_active']


@admin.register(BlockTableHTML)
class BlockTableHTMLAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'ordering', 'is_active']
    list_filter = ['page', 'is_active']


@admin.register(BlockForm)
class BlockFormAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'form_type', 'ordering', 'is_active']
    list_filter = ['page', 'form_type', 'is_active']


# Standalone Gallery Admin

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter gallery title (e.g., Campus Tour 2024, Annual Day)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Brief description of this gallery'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2,
                'placeholder': 'SEO description (max 160 characters)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].help_text = 'Gallery title that will appear on the gallery page'
        self.fields['description'].help_text = 'Description shown with the gallery'
        self.fields['category'].help_text = 'Category for filtering on gallery page'
        self.fields['cover_image'].help_text = 'Main image representing this gallery (recommended: 800x600px)'
        self.fields['is_featured'].help_text = 'Featured galleries appear prominently on homepage'
        self.fields['is_active'].help_text = 'Uncheck to hide this gallery from the website'
        self.fields['ordering'].help_text = 'Lower numbers appear first'


class GalleryPhotoForm(forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = ['image', 'title', 'caption', 'photographer', 'date_taken', 'ordering', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Photo title (optional)'
            }),
            'caption': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2,
                'placeholder': 'Photo description or caption'
            }),
            'photographer': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Photographer name (optional)'
            }),
            'date_taken': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '0',
                'style': 'width: 80px;'
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check if it's a new upload (has content_type) or existing file
            if hasattr(image, 'content_type'):
                if image.size > 10 * 1024 * 1024:  # 10MB limit
                    raise forms.ValidationError('Image file too large. Maximum size is 10MB.')
                if not image.content_type.startswith('image/'):
                    raise forms.ValidationError('Please upload a valid image file.')
            elif hasattr(image, 'size') and image.size > 10 * 1024 * 1024:
                # For existing files, only check size if accessible
                raise forms.ValidationError('Image file too large. Maximum size is 10MB.')
        return image


class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    form = GalleryPhotoForm
    extra = 0
    min_num = 0
    fields = ('image_preview', 'image', 'title', 'caption', 'photographer', 'category', 'date_taken', 'ordering', 'is_active')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px; max-width: 80px; border-radius: 4px; object-fit: cover;" />', obj.image.url)
        return format_html('<div style="width: 80px; height: 60px; background: #f8f9fa; border: 1px dashed #dee2e6; display: flex; align-items: center; justify-content: center; border-radius: 4px; font-size: 12px; color: #6c757d;">No Image</div>')
    image_preview.short_description = "Preview"


@admin.register(Gallery)
class GalleryAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = GalleryForm
    list_display = ['title', 'category', 'get_photos_count', 'is_featured', 'is_active', 'ordering', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    list_editable = ['is_featured', 'is_active', 'ordering']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryPhotoInline]
    actions = ['make_featured', 'remove_featured', 'make_active', 'make_inactive']
    
    fieldsets = (
        ('Gallery Information', {
            'fields': ('title', 'slug', 'description', 'category', 'cover_image'),
            'description': 'Basic gallery information'
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_active', 'ordering'),
            'description': 'Control how this gallery appears on the website'
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',),
            'description': 'Search engine optimization'
        }),
    )
    
    def get_photos_count(self, obj):
        count = obj.photos.count()
        active_count = obj.photos.filter(is_active=True).count()
        if count == 0:
            return format_html('<span style="color:#dc3545;">No photos</span>')
        elif active_count < count:
            return format_html('<span style="color:#ffc107;">{}/{} active</span>', active_count, count)
        else:
            return format_html('<span style="color:#28a745;">{} photos</span>', count)
    get_photos_count.short_description = 'Photos'
    get_photos_count.admin_order_field = 'photos__count'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('photos')
    
    # Custom Actions
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} gallery(s) marked as featured.')
    make_featured.short_description = "Mark as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} gallery(s) removed from featured.')
    remove_featured.short_description = "Remove from featured"
    
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} gallery(s) activated.')
    make_active.short_description = "Activate galleries"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} gallery(s) deactivated.')
    make_inactive.short_description = "Deactivate galleries"


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    form = GalleryPhotoForm
    list_display = ['image_preview', 'title', 'gallery', 'photographer', 'date_taken', 'is_active', 'created_at']
    list_filter = ['gallery__category', 'gallery', 'is_active', 'date_taken', 'created_at']
    search_fields = ['title', 'caption', 'gallery__title', 'photographer']
    list_per_page = 30
    
    fieldsets = (
        ('Photo Information', {
            'fields': ('gallery', 'image', 'title', 'caption')
        }),
        ('Additional Details', {
            'fields': ('photographer', 'date_taken', 'ordering', 'is_active'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 90px; border-radius: 4px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('gallery')


# Academic Section Admin

@admin.register(AdmissionInfo)
class AdmissionInfoAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'admission_type', 'is_active', 'ordering', 'created_at']
    list_filter = ['admission_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'admission_type', 'description', 'is_active', 'ordering')
        }),
        ('Admission Details', {
            'fields': ('eligibility_criteria', 'application_process', 'required_documents')
        }),
        ('Financial Information', {
            'fields': ('fees_structure',),
            'classes': ('collapse',)
        }),
        ('Important Information', {
            'fields': ('important_dates', 'contact_info')
        }),
        ('Documents', {
            'fields': ('application_form', 'brochure'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['title', 'result_type', 'exam_date', 'result_date', 'is_published', 'is_featured']
    list_filter = ['result_type', 'is_published', 'is_featured', 'result_date']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'result_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'result_type', 'description')
        }),
        ('Dates', {
            'fields': ('exam_date', 'result_date')
        }),
        ('Result Access', {
            'fields': ('result_file', 'result_link', 'instructions')
        }),
        ('Publishing Options', {
            'fields': ('is_published', 'is_featured')
        }),
    )


@admin.register(LibraryResource)
class LibraryResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'author', 'publication_year', 'availability_status', 'is_featured']
    list_filter = ['resource_type', 'availability_status', 'is_featured', 'publication_year']
    search_fields = ['title', 'author', 'isbn', 'subject_category']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'resource_type', 'description', 'subject_category')
        }),
        ('Publication Details', {
            'fields': ('author', 'publisher', 'publication_year', 'isbn')
        }),
        ('Library Management', {
            'fields': ('location', 'availability_status')
        }),
        ('Digital Resources', {
            'fields': ('digital_copy', 'external_link'),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('cover_image', 'is_featured')
        }),
    )


@admin.register(ELearningCourse)
class ELearningCourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'title', 'instructor', 'difficulty_level', 'duration_hours', 'is_active', 'is_featured']
    list_filter = ['difficulty_level', 'is_active', 'is_featured', 'certificate_available']
    search_fields = ['title', 'course_code', 'instructor']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'slug', 'course_code', 'description', 'instructor')
        }),
        ('Course Details', {
            'fields': ('difficulty_level', 'duration_hours', 'prerequisites', 'learning_outcomes', 'course_content')
        }),
        ('Course Materials', {
            'fields': ('course_materials', 'video_lectures', 'assignments', 'quiz_link'),
            'classes': ('collapse',)
        }),
        ('Enrollment', {
            'fields': ('enrollment_fee', 'start_date', 'end_date', 'max_enrollment')
        }),
        ('Options', {
            'fields': ('certificate_available', 'is_active', 'is_featured')
        }),
    )


@admin.register(PlacementRecord)
class PlacementRecordAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'company_name', 'job_title', 'package_offered', 'graduation_year', 'placement_date', 'is_featured']
    list_filter = ['graduation_year', 'job_type', 'is_featured', 'is_published', 'placement_date']
    search_fields = ['student_name', 'company_name', 'job_title', 'course']
    date_hierarchy = 'placement_date'
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'student_id', 'course', 'graduation_year', 'student_photo')
        }),
        ('Placement Details', {
            'fields': ('company_name', 'company_logo', 'job_title', 'job_type', 'package_offered', 'placement_date', 'company_location')
        }),
        ('Additional Information', {
            'fields': ('testimonial',),
            'classes': ('collapse',)
        }),
        ('Publishing Options', {
            'fields': ('is_featured', 'is_published')
        }),
    )


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'graduation_year', 'current_position', 'current_company', 'is_featured', 'willing_to_mentor']
    list_filter = ['graduation_year', 'is_featured', 'is_published', 'willing_to_mentor']
    search_fields = ['name', 'course', 'current_position', 'current_company']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'slug', 'profile_photo', 'graduation_year', 'course')
        }),
        ('Current Status', {
            'fields': ('current_position', 'current_company', 'location')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'linkedin_profile'),
            'classes': ('collapse',)
        }),
        ('Profile Content', {
            'fields': ('bio', 'achievements', 'career_journey', 'advice_to_students')
        }),
        ('Options', {
            'fields': ('is_featured', 'is_published', 'willing_to_mentor')
        }),
    )


# Director and Principal Message Admin

class DirectorMessageForm(forms.ModelForm):
    class Meta:
        model = DirectorMessage
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Director full name'
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Official designation'
            }),
            'qualifications': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Educational qualifications and certifications'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '0',
                'placeholder': 'Years of experience'
            }),
            'message_title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Title for the message section'
            }),
            'vision': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Director\'s vision for the institution'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Official email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+91-XXXXXXXXXX'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://linkedin.com/in/profile'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://twitter.com/username'
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://facebook.com/profile'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].help_text = 'Full name of the director'
        self.fields['designation'].help_text = 'Official title/designation'
        self.fields['qualifications'].help_text = 'Educational background and professional certifications'
        self.fields['experience_years'].help_text = 'Years of experience in education field'
        self.fields['message_content'].help_text = 'Director\'s message to students and visitors'
        self.fields['vision'].help_text = 'Director\'s vision statement for the institution'
        self.fields['achievements'].help_text = 'Notable achievements, awards, and recognitions'
        self.fields['profile_photo'].help_text = 'Director\'s professional photo (recommended size: 400x500px)'
        self.fields['show_on_homepage'].help_text = 'Display message snippet on homepage'
        self.fields['is_active'].help_text = 'Enable/disable director message section'


@admin.register(DirectorMessage)
class DirectorMessageAdmin(admin.ModelAdmin):
    form = DirectorMessageForm
    list_display = ['name', 'designation', 'show_on_homepage', 'is_active', 'updated_at']
    list_filter = ['is_active', 'show_on_homepage', 'show_achievements', 'show_contact_info']
    search_fields = ['name', 'designation', 'message_content']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'designation', 'qualifications', 'experience_years', 'profile_photo'),
            'description': 'Director\'s basic information and profile'
        }),
        ('Message Content', {
            'fields': ('message_title', 'message_content', 'vision', 'achievements'),
            'description': 'Director\'s message and vision content'
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'linkedin_url', 'twitter_url', 'facebook_url'),
            'description': 'Contact details and social media profiles',
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('show_on_homepage', 'show_achievements', 'show_contact_info', 'is_active'),
            'description': 'Control how and where the message appears'
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',),
            'description': 'Search engine optimization'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-updated_at')
    
    class Media:
        css = {
            'all': ('admin/css/leadership_admin.css',)
        }


class PrincipalMessageForm(forms.ModelForm):
    class Meta:
        model = PrincipalMessage
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Principal full name'
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Official designation'
            }),
            'qualifications': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Educational qualifications and certifications'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Area of specialization or expertise'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '0',
                'placeholder': 'Years of experience'
            }),
            'message_title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Title for the message section'
            }),
            'educational_philosophy': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Educational philosophy and teaching approach'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Official email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+91-XXXXXXXXXX'
            }),
            'office_hours': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Mon-Fri 10:00 AM - 4:00 PM'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://linkedin.com/in/profile'
            }),
            'researchgate_url': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://researchgate.net/profile'
            }),
            'orcid_url': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://orcid.org/0000-0000-0000-0000'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://twitter.com/username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].help_text = 'Full name of the principal'
        self.fields['designation'].help_text = 'Official title/designation'
        self.fields['qualifications'].help_text = 'Educational background and professional qualifications'
        self.fields['specialization'].help_text = 'Academic specialization or area of expertise'
        self.fields['experience_years'].help_text = 'Years of experience in education field'
        self.fields['message_content'].help_text = 'Principal\'s message to students and visitors'
        self.fields['educational_philosophy'].help_text = 'Teaching philosophy and educational approach'
        self.fields['achievements'].help_text = 'Academic achievements, publications, and awards'
        self.fields['profile_photo'].help_text = 'Principal\'s professional photo (recommended size: 400x500px)'
        self.fields['office_hours'].help_text = 'Available hours for student meetings'
        self.fields['show_on_homepage'].help_text = 'Display message snippet on homepage'
        self.fields['is_active'].help_text = 'Enable/disable principal message section'


@admin.register(PrincipalMessage)
class PrincipalMessageAdmin(admin.ModelAdmin):
    form = PrincipalMessageForm
    list_display = ['name', 'designation', 'specialization', 'show_on_homepage', 'is_active', 'updated_at']
    list_filter = ['is_active', 'show_on_homepage', 'show_achievements', 'show_contact_info', 'show_office_hours']
    search_fields = ['name', 'designation', 'specialization', 'message_content']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'designation', 'qualifications', 'specialization', 'experience_years', 'profile_photo'),
            'description': 'Principal\'s basic information and profile'
        }),
        ('Message Content', {
            'fields': ('message_title', 'message_content', 'educational_philosophy', 'achievements'),
            'description': 'Principal\'s message and educational philosophy'
        }),
        ('Contact & Office Information', {
            'fields': ('email', 'phone', 'office_hours'),
            'description': 'Contact details and office hours'
        }),
        ('Academic Profiles', {
            'fields': ('linkedin_url', 'researchgate_url', 'orcid_url', 'twitter_url'),
            'description': 'Academic and professional social media profiles',
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('show_on_homepage', 'show_achievements', 'show_contact_info', 'show_office_hours', 'is_active'),
            'description': 'Control how and where the message appears'
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',),
            'description': 'Search engine optimization'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-updated_at')
    
    class Media:
        css = {
            'all': ('admin/css/leadership_admin.css',)
        }


# ================================
# IQAC ADMIN CONFIGURATIONS
# ================================

# IQAC Forms

class IQACInfoForm(forms.ModelForm):
    """Enhanced form for IQAC Info management"""
    class Meta:
        model = IQACInfo
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Internal Quality Assurance Cell - Chaitanya College'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Excellence through Quality Assurance'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of IQAC'
            }),
            'overview': CKEditor5Widget(),
            'vision': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'mission': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'objectives': CKEditor5Widget(),
            'coordinator_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IQAC Coordinator Name'
            }),
            'coordinator_designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Designation'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91-XXXXXXXXXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'iqac@college.edu'
            }),
            'office_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Office location/room number'
            })
        }


class IQACReportForm(forms.ModelForm):
    """Enhanced form for IQAC Report management"""
    class Meta:
        model = IQACReport
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Annual Quality Assurance Report 2023-24'
            }),
            'academic_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '2023-24'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'file_size': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2.5 MB'
            })
        }

    def clean_academic_year(self):
        academic_year = self.cleaned_data.get('academic_year')
        if academic_year:
            # Validate format like "2023-24" or "2023-2024"
            import re
            if not re.match(r'^\d{4}-\d{2,4}$', academic_year):
                raise forms.ValidationError('Please enter academic year in format: YYYY-YY or YYYY-YYYY')
        return academic_year


class NAACInfoForm(forms.ModelForm):
    """Enhanced form for NAAC Info management"""
    class Meta:
        model = NAACInfo
        fields = '__all__'
        widgets = {
            'current_grade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., A++, A+, A, B++'
            }),
            'current_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '4',
                'placeholder': '3.65'
            }),
            'accreditation_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1990',
                'max': '2050'
            }),
            'validity_period': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '2020',
                'max': '2050'
            }),
            'peer_team_visit_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'overview': CKEditor5Widget(),
            'useful_links': CKEditor5Widget(),
            'important_documents': CKEditor5Widget(),
        }


class NIRFInfoForm(forms.ModelForm):
    """Enhanced form for NIRF Info management"""
    class Meta:
        model = NIRFInfo
        fields = '__all__'
        widgets = {
            'current_ranking': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Current ranking position'
            }),
            'ranking_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '2015',
                'max': '2050'
            }),
            'total_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'tlr_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '30'
            }),
            'rp_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '30'
            }),
            'go_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '20'
            }),
            'oi_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '10'
            }),
            'pr_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '10'
            }),
            'overview': CKEditor5Widget()
        }


class QualityInitiativeForm(forms.ModelForm):
    """Enhanced form for Quality Initiative management"""
    class Meta:
        model = QualityInitiative
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quality initiative title'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'progress_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '1'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'objectives': CKEditor5Widget(),
            'methodology': CKEditor5Widget(),
            'outcomes': CKEditor5Widget(),
            'challenges': CKEditor5Widget()
        }


class SideMenuItemInline(SortableInlineAdminMixin, admin.TabularInline):
    """Inline for Side Menu Items"""
    model = SideMenuItem
    extra = 1
    min_num = 0
    fields = ('title', 'url_pattern', 'page_slug', 'external_url', 'icon_class', 'badge_text', 'description', 'ordering', 'is_active')
    

# IQAC Admin Classes

@admin.register(IQACInfo)
class IQACInfoAdmin(admin.ModelAdmin):
    """Admin for IQAC Information"""
    form = IQACInfoForm
    list_display = [
        'title', 'coordinator_name', 'show_statistics', 'show_contact_info', 'is_active', 'updated_at'
    ]
    list_filter = [
        'is_active', 'show_statistics', 'show_contact_info', 'created_at', 'updated_at'
    ]
    search_fields = ['title', 'coordinator_name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'description', 'is_active'),
            'description': 'Basic IQAC information displayed on the main page'
        }),
        ('Content Sections', {
            'fields': ('overview', 'vision', 'mission', 'objectives'),
            'description': 'Detailed content sections for IQAC page'
        }),
        ('Statistics Display', {
            'fields': (
                'show_statistics',
                ('years_of_excellence', 'quality_initiatives'),
                ('naac_grade', 'quality_compliance')
            ),
            'description': 'Statistical information to display on IQAC page'
        }),
        ('Coordinator Information', {
            'fields': (
                'show_contact_info',
                ('coordinator_name', 'coordinator_designation'),
                ('phone', 'email'),
                'office_location'
            ),
            'description': 'IQAC Coordinator contact information'
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',),
            'description': 'Search engine optimization'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['activate_iqac_info', 'deactivate_iqac_info']
    
    def activate_iqac_info(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} IQAC info(s) activated.')
    activate_iqac_info.short_description = "Activate selected IQAC info"
    
    def deactivate_iqac_info(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} IQAC info(s) deactivated.')
    deactivate_iqac_info.short_description = "Deactivate selected IQAC info"
    
    class Media:
        css = {
            'all': ('admin/css/iqac_admin.css',)
        }
        js = ('admin/js/iqac_admin.js',)


@admin.register(IQACReport)
class IQACReportAdmin(admin.ModelAdmin):
    """Admin for IQAC Reports"""
    form = IQACReportForm
    list_display = [
        'title', 'report_type', 'academic_year', 'is_featured', 'download_count', 'is_published', 'created_at'
    ]
    list_filter = [
        'report_type', 'is_featured', 'is_published', 'academic_year', 'created_at'
    ]
    list_editable = ['is_featured', 'is_published']
    search_fields = ['title', 'description', 'academic_year']
    date_hierarchy = 'created_at'
    actions = ['make_featured', 'remove_featured', 'reset_download_count']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('title', 'report_type', 'academic_year', 'description'),
            'description': 'Basic report information'
        }),
        ('Report File', {
            'fields': ('report_file', 'file_size', 'cover_image'),
            'description': 'Report file and optional cover image'
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_active'),
            'description': 'Control how this report appears'
        }),
        ('Statistics', {
            'fields': ('download_count',),
            'description': 'Report statistics (auto-updated)'
        })
    )
    
    readonly_fields = ['download_count']
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} report(s) marked as featured.')
    make_featured.short_description = "Mark as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} report(s) removed from featured.')
    remove_featured.short_description = "Remove from featured"
    
    def reset_download_count(self, request, queryset):
        updated = queryset.update(download_count=0)
        self.message_user(request, f'Download count reset for {updated} report(s).')
    reset_download_count.short_description = "Reset download count"
    
    class Media:
        css = {
            'all': ('admin/css/iqac_admin.css',)
        }
        js = ('admin/js/iqac_admin.js',)


@admin.register(NAACInfo)
class NAACInfoAdmin(admin.ModelAdmin):
    """Admin for NAAC Information"""
    form = NAACInfoForm
    list_display = [
        'current_grade', 'cgpa_score', 'accreditation_year', 'validity_period', 'is_active', 'updated_at'
    ]
    list_filter = [
        'current_grade', 'is_active', 'accreditation_year', 'validity_period'
    ]
    search_fields = ['current_grade', 'overview']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Current Accreditation', {
            'fields': (
                ('current_grade', 'current_score'),
                ('accreditation_year', 'validity_period'),
                'peer_team_visit_date'
            ),
            'description': 'Current NAAC accreditation details'
        }),
        ('Assessment Scores', {
            'fields': (
                ('criteria_1_score', 'criteria_2_score'),
                ('criteria_3_score', 'criteria_4_score'),
                ('criteria_5_score', 'criteria_6_score'),
                'criteria_7_score'
            ),
            'description': 'NAAC seven criteria scores'
        }),
        ('Content', {
            'fields': ('overview', 'useful_links', 'important_documents'),
            'description': 'NAAC page content and resources'
        }),
        ('Coordinator Information', {
            'fields': (
                ('coordinator_name', 'coordinator_designation'),
                ('contact_phone', 'contact_email')
            ),
            'description': 'NAAC Coordinator details',
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    class Media:
        css = {
            'all': ('admin/css/iqac_admin.css',)
        }
        js = ('admin/js/iqac_admin.js',)


@admin.register(NIRFInfo)
class NIRFInfoAdmin(admin.ModelAdmin):
    """Admin for NIRF Information"""
    form = NIRFInfoForm
    list_display = [
        'current_ranking', 'category', 'ranking_year', 'overall_score', 'is_active', 'updated_at'
    ]
    list_filter = [
        'category', 'is_active', 'ranking_year', 'current_ranking'
    ]
    search_fields = ['category', 'overview']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Current Ranking', {
            'fields': (
                ('current_ranking', 'category'),
                ('ranking_year', 'total_score')
            ),
            'description': 'Current NIRF ranking details'
        }),
        ('Parameter Scores', {
            'fields': (
                ('tlr_score', 'rp_score'),
                ('go_score', 'oi_score'),
                'pr_score'
            ),
            'description': 'NIRF five parameter scores'
        }),
        ('Content', {
            'fields': ('overview',),
            'description': 'NIRF page content'
        }),
        ('Coordinator Information', {
            'fields': (
                ('coordinator_name', 'coordinator_designation'),
                ('contact_phone', 'contact_email')
            ),
            'description': 'NIRF Coordinator details',
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    class Media:
        css = {
            'all': ('admin/css/iqac_admin.css',)
        }
        js = ('admin/js/iqac_admin.js',)


@admin.register(QualityInitiative)
class QualityInitiativeAdmin(admin.ModelAdmin):
    """Admin for Quality Initiatives"""
    form = QualityInitiativeForm
    list_display = [
        'title', 'status', 'start_date', 'end_date', 'progress_percentage', 'coordinator', 'is_published'
    ]
    list_filter = [
        'status', 'is_published', 'start_date', 'end_date', 'created_at'
    ]
    list_editable = ['status', 'is_published']
    search_fields = ['title', 'objectives', 'responsible_person']
    date_hierarchy = 'start_date'
    actions = ['mark_completed', 'mark_in_progress', 'mark_planned']
    
    fieldsets = (
        ('Initiative Information', {
            'fields': ('title', 'status', 'responsible_person', 'is_active'),
            'description': 'Basic initiative information'
        }),
        ('Timeline & Progress', {
            'fields': (
                ('start_date', 'end_date'),
                'progress_percentage'
            ),
            'description': 'Initiative timeline and progress tracking'
        }),
        ('Budget', {
            'fields': ('budget',),
            'description': 'Initiative budget information',
            'classes': ('collapse',)
        }),
        ('Content', {
            'fields': ('objectives', 'methodology', 'outcomes', 'challenges'),
            'description': 'Detailed initiative content'
        })
    )
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} initiative(s) marked as completed.')
    mark_completed.short_description = "Mark as completed"
    
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} initiative(s) marked as in progress.')
    mark_in_progress.short_description = "Mark as in progress"
    
    def mark_planned(self, request, queryset):
        updated = queryset.update(status='planned')
        self.message_user(request, f'{updated} initiative(s) marked as planned.')
    mark_planned.short_description = "Mark as planned"
    
    class Media:
        css = {
            'all': ('admin/css/iqac_admin.css',)
        }
        js = ('admin/js/iqac_admin.js',)


@admin.register(AccreditationInfo)
class AccreditationInfoAdmin(admin.ModelAdmin):
    """Admin for Accreditation Information"""
    list_display = [
        'accrediting_body', 'accreditation_type', 'grade_or_rating', 'accreditation_date', 'validity_period', 'is_featured', 'is_active'
    ]
    list_filter = [
        'accrediting_body', 'accreditation_type', 'is_featured', 'is_active', 'accreditation_date'
    ]
    list_editable = ['is_featured']
    search_fields = ['accrediting_body', 'accreditation_type', 'description']
    date_hierarchy = 'accreditation_date'
    actions = ['make_featured', 'remove_featured']
    
    fieldsets = (
        ('Accreditation Details', {
            'fields': (
                ('accrediting_body', 'accreditation_type'),
                ('grade_score', 'accreditation_date'),
                'validity_until'
            ),
            'description': 'Basic accreditation information'
        }),
        ('Content', {
            'fields': ('description', 'certificate_document'),
            'description': 'Accreditation description and certificate'
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_active'),
            'description': 'Control how this accreditation appears'
        })
    )
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} accreditation(s) marked as featured.')
    make_featured.short_description = "Mark as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} accreditation(s) removed from featured.')
    remove_featured.short_description = "Remove from featured"
    
    class Media:
        css = {
            'all': ('admin/css/iqac_admin.css',)
        }


@admin.register(IQACFeedback)
class IQACFeedbackAdmin(admin.ModelAdmin):
    """Admin for IQAC Feedback"""
    list_display = [
        'name', 'feedback_type', 'overall_satisfaction', 'is_reviewed', 'created_at'
    ]
    list_filter = [
        'feedback_type', 'overall_satisfaction', 'teaching_quality', 'infrastructure', 
        'administration', 'library_resources', 'is_reviewed', 'created_at'
    ]
    search_fields = ['name', 'email', 'suggestions', 'strengths', 'areas_for_improvement']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'feedback_type'),
            'description': 'Feedback submitter information'
        }),
        ('Rating Categories', {
            'fields': ('teaching_quality', 'infrastructure', 'administration', 'library_resources', 'overall_satisfaction'),
            'description': 'Rating across different categories'
        }),
        ('Feedback Content', {
            'fields': ('suggestions', 'strengths', 'areas_for_improvement'),
            'description': 'Detailed feedback content'
        }),
        ('Review Status', {
            'fields': ('is_reviewed', 'reviewed_by', 'review_date', 'response'),
            'description': 'Administrative review fields'
        }),
        ('Submission Info', {
            'fields': ('created_at',),
            'description': 'Submission timestamp'
        })
    )
    
    actions = ['export_feedback_csv']
    
    def export_feedback_csv(self, request, queryset):
        """Export feedback data as CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="iqac_feedback.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Email', 'Phone', 'Feedback Type', 'Teaching Quality', 'Infrastructure',
            'Administration', 'Library Resources', 'Overall Satisfaction', 'Suggestions',
            'Strengths', 'Areas for Improvement', 'Reviewed', 'Reviewed By', 'Created At'
        ])
        
        for feedback in queryset:
            writer.writerow([
                feedback.name, feedback.email, feedback.phone, feedback.feedback_type,
                feedback.teaching_quality, feedback.infrastructure, feedback.administration,
                feedback.library_resources, feedback.overall_satisfaction, feedback.suggestions,
                feedback.strengths, feedback.areas_for_improvement, feedback.is_reviewed,
                feedback.reviewed_by, feedback.created_at
            ])
        
        return response
    export_feedback_csv.short_description = "Export selected feedback as CSV"
    
    class Media:
        css = {
            'all': ('admin/css/iqac_admin.css',)
        }


@admin.register(SideMenu)
class SideMenuAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Admin for Side Menus"""
    list_display = [
        'name', 'url_pattern', 'page_slug', 'show_title', 'is_active', 'created_at'
    ]
    list_filter = [
        'is_active', 'show_title', 'created_at'
    ]
    search_fields = ['name', 'url_pattern', 'page_slug']
    inlines = [SideMenuItemInline]
    actions = ['activate_menus', 'deactivate_menus', 'duplicate_menus']
    
    fieldsets = (
        ('Menu Information', {
            'fields': ('name', 'show_title', 'is_active'),
            'description': 'Basic menu configuration'
        }),
        ('Display Conditions', {
            'fields': (
                'url_pattern',
                'page_slug'
            ),
            'description': 'Define where this menu should appear'
        }),
        ('Styling', {
            'fields': ('css_classes',),
            'description': 'Additional CSS classes for styling',
            'classes': ('collapse',)
        })
    )
    
    def activate_menus(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} side menu(s) activated.')
    activate_menus.short_description = "Activate selected menus"
    
    def deactivate_menus(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} side menu(s) deactivated.')
    deactivate_menus.short_description = "Deactivate selected menus"
    
    def duplicate_menus(self, request, queryset):
        duplicated = 0
        for menu in queryset:
            # Store original items
            original_items = list(menu.items.all())
            
            # Duplicate menu
            menu.pk = None
            menu.name = f"{menu.name} (Copy)"
            menu.is_active = False
            menu.save()
            
            # Duplicate items
            for item in original_items:
                item.pk = None
                item.side_menu = menu
                item.save()
            
            duplicated += 1
        
        self.message_user(request, f'{duplicated} side menu(s) duplicated with all items.')
    duplicate_menus.short_description = "Duplicate selected menus with items"
    
    class Media:
        css = {
            'all': ('admin/css/iqac_admin.css',)
        }
        js = ('admin/js/iqac_admin.js',)


@admin.register(SideMenuItem)
class SideMenuItemAdmin(admin.ModelAdmin):
    """Admin for Side Menu Items"""
    list_display = [
        'title', 'side_menu', 'get_link_type', 'get_url_preview', 'badge_text', 'ordering', 'is_active'
    ]
    list_filter = [
        'side_menu', 'is_active', 'open_in_new_tab', 'created_at'
    ]
    list_editable = ['ordering', 'is_active']
    search_fields = ['title', 'description', 'url_pattern', 'external_url']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('side_menu', 'title', 'description', 'icon_class', 'badge_text'),
            'description': 'Basic menu item information'
        }),
        ('Link Configuration', {
            'fields': (
                'url_pattern',
                'page_slug',
                'external_url',
                'open_in_new_tab'
            ),
            'description': 'Configure where this item links to'
        }),
        ('Display Options', {
            'fields': ('ordering', 'is_active'),
            'description': 'Control how this item appears'
        })
    )
    
    def get_link_type(self, obj):
        if obj.external_url:
            return format_html('<span style="color: #e74c3c;">External</span>')
        elif obj.url_pattern:
            return format_html('<span style="color: #3498db;">URL Pattern</span>')
        elif obj.page_slug:
            return format_html('<span style="color: #2ecc71;">Page Slug</span>')
        else:
            return format_html('<span style="color: #95a5a6;">None</span>')
    get_link_type.short_description = 'Link Type'
    
    def get_url_preview(self, obj):
        url = obj.get_url()
        if len(url) > 50:
            return f"{url[:47]}..."
        return url
    get_url_preview.short_description = 'URL Preview'
    
    class Media:
        css = {
            'all': ('admin/css/iqac_admin.css',)
        }
        js = ('admin/js/iqac_admin.js',)


# Customize admin site

admin.site.site_header = "Chaitanya College Administration"
admin.site.site_title = "Chaitanya College Admin"
admin.site.index_title = "Welcome to Chaitanya College Administration"
