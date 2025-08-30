from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField


class TimeStampedModel(models.Model):
    """Abstract base class with created_at and updated_at fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class TopUtilityBar(TimeStampedModel):
    """Top utility bar configuration model"""
    name = models.CharField(max_length=100, help_text="Name for this utility bar configuration")
    is_active = models.BooleanField(default=True, help_text="Enable or disable this utility bar")
    
    # Appearance settings
    background_color = ColorField(default="#0d6efd", help_text="Background color (hex code)")
    text_color = ColorField(default="#ffffff", help_text="Text color (hex code)")
    height = models.PositiveIntegerField(default=40, help_text="Height in pixels")
    
    # Position settings
    POSITION_CHOICES = [
        ('top', 'Top of page'),
        ('below_header', 'Below header'),
    ]
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='top')
    
    # Social media settings with individual enable/disable
    show_social_icons = models.BooleanField(default=True, help_text="Display social media icons section")
    
    # Individual social media controls
    enable_facebook = models.BooleanField(default=False, help_text="Enable Facebook link")
    facebook_url = models.URLField(blank=True, help_text="Facebook URL")
    
    enable_twitter = models.BooleanField(default=False, help_text="Enable Twitter link")
    twitter_url = models.URLField(blank=True, help_text="Twitter URL")
    
    enable_instagram = models.BooleanField(default=False, help_text="Enable Instagram link")
    instagram_url = models.URLField(blank=True, help_text="Instagram URL")
    
    enable_youtube = models.BooleanField(default=False, help_text="Enable YouTube link")
    youtube_url = models.URLField(blank=True, help_text="YouTube URL")
    
    enable_linkedin = models.BooleanField(default=False, help_text="Enable LinkedIn link")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn URL")
    
    # Contact information
    show_contact_info = models.BooleanField(default=True, help_text="Display contact information")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    contact_email = models.EmailField(blank=True, help_text="Contact email address")
    
    # Custom links (keeping legacy fields for backward compatibility)
    show_custom_links = models.BooleanField(default=True, help_text="Display custom links section")
    custom_link_1_text = models.CharField(max_length=50, blank=True, help_text="Text for custom link 1")
    custom_link_1_url = models.CharField(max_length=200, blank=True, help_text="URL for custom link 1")
    custom_link_2_text = models.CharField(max_length=50, blank=True, help_text="Text for custom link 2")
    custom_link_2_url = models.CharField(max_length=200, blank=True, help_text="URL for custom link 2")
    custom_link_3_text = models.CharField(max_length=50, blank=True, help_text="Text for custom link 3")
    custom_link_3_url = models.CharField(max_length=200, blank=True, help_text="URL for custom link 3")
    
    # Mobile settings
    show_on_mobile = models.BooleanField(default=True, help_text="Display on mobile devices")
    mobile_collapsed = models.BooleanField(default=True, help_text="Collapse to icon on mobile")
    
    class Meta:
        verbose_name = "Top Utility Bar"
        verbose_name_plural = "Top Utility Bars"
    
    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"
    
    def clean(self):
        # Ensure we don't have multiple active utility bars
        if self.is_active:
            active_bars = TopUtilityBar.objects.filter(is_active=True).exclude(pk=self.pk)
            if active_bars.exists():
                raise ValidationError("Only one utility bar can be active at a time. Please deactivate the other utility bar first.")
    
    @property
    def active_social_links(self):
        """Get list of active social media links"""
        social_links = []
        if self.enable_facebook and self.facebook_url:
            social_links.append({'platform': 'facebook', 'url': self.facebook_url, 'icon': 'fab fa-facebook-f'})
        if self.enable_twitter and self.twitter_url:
            social_links.append({'platform': 'twitter', 'url': self.twitter_url, 'icon': 'fab fa-twitter'})
        if self.enable_instagram and self.instagram_url:
            social_links.append({'platform': 'instagram', 'url': self.instagram_url, 'icon': 'fab fa-instagram'})
        if self.enable_youtube and self.youtube_url:
            social_links.append({'platform': 'youtube', 'url': self.youtube_url, 'icon': 'fab fa-youtube'})
        if self.enable_linkedin and self.linkedin_url:
            social_links.append({'platform': 'linkedin', 'url': self.linkedin_url, 'icon': 'fab fa-linkedin-in'})
        return social_links
    
    @property
    def all_custom_links(self):
        """Get all custom links (legacy fields + dynamic links)"""
        links = []
        
        # Legacy fields
        if self.custom_link_1_text and self.custom_link_1_url:
            links.append({'text': self.custom_link_1_text, 'url': self.custom_link_1_url})
        if self.custom_link_2_text and self.custom_link_2_url:
            links.append({'text': self.custom_link_2_text, 'url': self.custom_link_2_url})
        if self.custom_link_3_text and self.custom_link_3_url:
            links.append({'text': self.custom_link_3_text, 'url': self.custom_link_3_url})
        
        # Dynamic links
        for custom_link in self.custom_links.filter(is_active=True).order_by('ordering'):
            links.append({'text': custom_link.text, 'url': custom_link.url, 'icon': custom_link.icon_class})
        
        return links


class CustomLink(TimeStampedModel):
    """Dynamic custom links for utility bar"""
    utility_bar = models.ForeignKey(
        TopUtilityBar, 
        on_delete=models.CASCADE, 
        related_name='custom_links',
        help_text="The utility bar this link belongs to"
    )
    text = models.CharField(
        max_length=50, 
        help_text="Link text to display"
    )
    url = models.CharField(
        max_length=200, 
        help_text="URL or path for the link"
    )
    icon_class = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Optional FontAwesome icon class (e.g., 'fas fa-graduation-cap')"
    )
    tooltip = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Optional tooltip text on hover"
    )
    open_in_new_tab = models.BooleanField(
        default=False, 
        help_text="Open link in new tab/window"
    )
    ordering = models.PositiveIntegerField(
        default=0, 
        help_text="Display order (lower numbers appear first)"
    )
    is_active = models.BooleanField(
        default=True, 
        help_text="Enable/disable this link"
    )
    
    class Meta:
        ordering = ['ordering', 'text']
        verbose_name = "Custom Link"
        verbose_name_plural = "Custom Links"
    
    def __str__(self):
        return f"{self.utility_bar.name} - {self.text}"
    
    def clean(self):
        # Basic URL validation
        if self.url and not (self.url.startswith(('http://', 'https://', '/')) or self.url.startswith('#')):
            raise ValidationError("URL must start with http://, https://, /, or #")


class ScrollingNotification(TimeStampedModel):
    """Scrolling notification bar model"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    COLOR_CHOICES = [
        ('primary', 'Primary Blue'),
        ('success', 'Success Green'),
        ('warning', 'Warning Yellow'),
        ('danger', 'Danger Red'),
        ('info', 'Info Cyan'),
        ('dark', 'Dark'),
    ]
    
    title = models.CharField(max_length=200, help_text="Brief notification title")
    message = models.TextField(help_text="Detailed notification message")
    link_text = models.CharField(max_length=50, blank=True, help_text="Optional link text (e.g., 'Read More', 'Apply Now')")
    link_url = models.URLField(blank=True, help_text="Optional link URL")
    
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    color_theme = models.CharField(max_length=10, choices=COLOR_CHOICES, default='primary')
    
    # Display settings
    show_icon = models.BooleanField(default=True)
    icon_class = models.CharField(max_length=50, default='fas fa-bullhorn', help_text="FontAwesome icon class")
    
    # Timing settings
    start_date = models.DateTimeField(help_text="When to start showing this notification")
    end_date = models.DateTimeField(blank=True, null=True, help_text="When to stop showing (leave empty for permanent)")
    
    # Animation settings
    scroll_speed = models.IntegerField(default=50, help_text="Scroll speed in seconds for full cycle")
    pause_on_hover = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    
    class Meta:
        ordering = ['display_order', '-priority', '-created_at']
        verbose_name = "Scrolling Notification"
        verbose_name_plural = "Scrolling Notifications"
    
    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"
    
    @property
    def is_currently_active(self):
        from django.utils import timezone
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True
    
    @property
    def combined_text(self):
        """Returns the full text for scrolling"""
        text = f"{self.title}: {self.message}"
        if self.link_text:
            text += f" - {self.link_text}"
        return text


class SliderImage(TimeStampedModel):
    """Image slider/carousel model for homepage and other sections"""
    title = models.CharField(
        max_length=200, 
        help_text="Caption title that appears on the slide"
    )
    caption = models.TextField(
        blank=True, 
        help_text="Optional description text that appears below the title"
    )
    image = models.ImageField(
        upload_to='slider/', 
        help_text="Slider image (recommended size: 1920x800px or 16:9 ratio)"
    )
    button_text = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Optional button text (e.g., 'Learn More', 'Apply Now')"
    )
    button_url = models.URLField(
        blank=True, 
        help_text="Optional button link URL"
    )
    
    # Ordering and visibility
    ordering = models.IntegerField(
        default=0, 
        help_text="Display order (lower numbers appear first)"
    )
    is_active = models.BooleanField(
        default=True, 
        help_text="Uncheck to hide this slide from the slider"
    )
    
    # Optional scheduling
    start_date = models.DateTimeField(
        blank=True, 
        null=True, 
        help_text="Optional: When to start showing this slide (leave empty for immediate)"
    )
    end_date = models.DateTimeField(
        blank=True, 
        null=True, 
        help_text="Optional: When to stop showing this slide (leave empty for permanent)"
    )
    
    # SEO and accessibility
    alt_text = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Alternative text for accessibility (auto-generated from title if empty)"
    )
    
    class Meta:
        ordering = ['ordering', '-created_at']
        verbose_name = "Slider Image"
        verbose_name_plural = "Slider Images"
    
    def save(self, *args, **kwargs):
        # Auto-generate alt text if not provided
        if not self.alt_text:
            self.alt_text = self.title
        super().save(*args, **kwargs)
    
    @property
    def is_currently_active(self):
        """Check if the slide should be shown based on scheduling"""
        if not self.is_active:
            return False
        
        now = timezone.now()
        
        # Check start date
        if self.start_date and self.start_date > now:
            return False
        
        # Check end date
        if self.end_date and self.end_date < now:
            return False
        
        return True
    
    @property
    def has_button(self):
        """Check if slide has a button"""
        return bool(self.button_text and self.button_url)
    
    def __str__(self):
        return f"{self.title} (Order: {self.ordering})"


class HeaderInfo(TimeStampedModel):
    """Enhanced Header/Top bar information model with comprehensive customization"""
    
    # College Information with Typography Controls
    college_name = models.CharField(
        max_length=300, 
        default="Chaitanya Science and Arts College",
        help_text="Full college name"
    )
    college_name_font_size = models.IntegerField(
        default=28, 
        help_text="Font size in pixels (12-48)"
    )
    college_name_font_weight = models.CharField(
        max_length=20,
        choices=[
            ('300', 'Light'),
            ('400', 'Normal'), 
            ('500', 'Medium'),
            ('600', 'Semi-bold'),
            ('700', 'Bold'),
            ('800', 'Extra-bold')
        ],
        default='700'
    )
    college_name_font_family = models.CharField(
        max_length=50,
        choices=[
            ('Arial, sans-serif', 'Arial'),
            ('Georgia, serif', 'Georgia'),
            ('Times New Roman, serif', 'Times New Roman'),
            ('Helvetica, sans-serif', 'Helvetica'),
            ('Verdana, sans-serif', 'Verdana'),
            ('Roboto, sans-serif', 'Roboto'),
            ('Open Sans, sans-serif', 'Open Sans'),
            ('Lato, sans-serif', 'Lato'),
            ('Poppins, sans-serif', 'Poppins'),
            ('Montserrat, sans-serif', 'Montserrat')
        ],
        default='Poppins, sans-serif'
    )
    college_name_color = ColorField(
        max_length=7, 
        default="#1f2937", 
        help_text="Hex color code for college name"
    )
    show_college_name = models.BooleanField(default=True)
    
    # College Address with Typography
    college_address = models.TextField(
        default="Pamgarh, Janjgir Champa, Chhattisgarh, India - 495554",
        help_text="Complete college address"
    )
    address_font_size = models.IntegerField(
        default=14, 
        help_text="Font size in pixels (10-24)"
    )
    address_font_weight = models.CharField(
        max_length=20,
        choices=[
            ('300', 'Light'),
            ('400', 'Normal'),
            ('500', 'Medium'),
            ('600', 'Semi-bold')
        ],
        default='400'
    )
    address_color = ColorField(
        max_length=7, 
        default="#6b7280", 
        help_text="Hex color code for address"
    )
    show_address = models.BooleanField(default=True)
    
    # College Affiliations with Typography
    college_affiliations = models.TextField(
        default="Affiliated to Shaheed Nandkumar Patel Vishwavidyalaya, Raigarh\nRecognized by UGC | NAAC Grade A+ | IIC 3 Star Rating",
        help_text="College affiliations and recognitions (use line breaks for multiple lines)"
    )
    affiliations_font_size = models.IntegerField(
        default=12, 
        help_text="Font size in pixels (10-20)"
    )
    affiliations_font_weight = models.CharField(
        max_length=20,
        choices=[
            ('300', 'Light'),
            ('400', 'Normal'),
            ('500', 'Medium'),
            ('600', 'Semi-bold')
        ],
        default='500'
    )
    affiliations_color = ColorField(
        max_length=7, 
        default="#059669", 
        help_text="Hex color code for affiliations"
    )
    show_affiliations = models.BooleanField(default=True)
    
    # Contact Information with Typography
    email = models.EmailField(default="chaitanyapamgarh@gmail.com")
    phone = models.CharField(max_length=20, default="+91-9425540666")
    website_url = models.URLField(blank=True, help_text="Official website URL")
    
    contact_font_size = models.IntegerField(
        default=13, 
        help_text="Font size for contact info (10-18)"
    )
    contact_color = ColorField(
        max_length=7, 
        default="#374151", 
        help_text="Hex color code for contact info"
    )
    show_contact_info = models.BooleanField(default=True)
    
    # Left Side Logos (up to 3)
    left_logo_1 = models.ImageField(
        upload_to='header/logos/left/', 
        blank=True, 
        help_text="First left logo (recommended: 60x60px)"
    )
    left_logo_1_alt = models.CharField(max_length=100, blank=True, help_text="Alt text for logo 1")
    left_logo_1_link = models.URLField(blank=True, help_text="Optional link for logo 1")
    
    left_logo_2 = models.ImageField(
        upload_to='header/logos/left/', 
        blank=True, 
        help_text="Second left logo (recommended: 60x60px)"
    )
    left_logo_2_alt = models.CharField(max_length=100, blank=True, help_text="Alt text for logo 2")
    left_logo_2_link = models.URLField(blank=True, help_text="Optional link for logo 2")
    
    left_logo_3 = models.ImageField(
        upload_to='header/logos/left/', 
        blank=True, 
        help_text="Third left logo (recommended: 60x60px)"
    )
    left_logo_3_alt = models.CharField(max_length=100, blank=True, help_text="Alt text for logo 3")
    left_logo_3_link = models.URLField(blank=True, help_text="Optional link for logo 3")
    
    # Right Side Logos (up to 3)
    right_logo_1 = models.ImageField(
        upload_to='header/logos/right/', 
        blank=True, 
        help_text="First right logo (recommended: 60x60px)"
    )
    right_logo_1_alt = models.CharField(max_length=100, blank=True, help_text="Alt text for logo 1")
    right_logo_1_link = models.URLField(blank=True, help_text="Optional link for logo 1")
    
    right_logo_2 = models.ImageField(
        upload_to='header/logos/right/', 
        blank=True, 
        help_text="Second right logo (recommended: 60x60px)"
    )
    right_logo_2_alt = models.CharField(max_length=100, blank=True, help_text="Alt text for logo 2")
    right_logo_2_link = models.URLField(blank=True, help_text="Optional link for logo 2")
    
    right_logo_3 = models.ImageField(
        upload_to='header/logos/right/', 
        blank=True, 
        help_text="Third right logo (recommended: 60x60px)"
    )
    right_logo_3_alt = models.CharField(max_length=100, blank=True, help_text="Alt text for logo 3")
    right_logo_3_link = models.URLField(blank=True, help_text="Optional link for logo 3")
    
    # Logo Sizing Options
    logo_size = models.CharField(
        max_length=20,
        choices=[
            ('40', 'Small (40px)'),
            ('50', 'Medium (50px)'),
            ('60', 'Standard (60px)'),
            ('70', 'Large (70px)'),
            ('80', 'Extra Large (80px)')
        ],
        default='60',
        help_text="Size for all logos"
    )
    
    # Social Media Links
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(
        max_length=20, 
        blank=True, 
        help_text="WhatsApp number with country code (e.g., +919425540666)"
    )
    show_social_links = models.BooleanField(default=True)
    
    # Header Layout & Styling
    header_layout = models.CharField(
        max_length=20,
        choices=[
            ('centered', 'Centered'),
            ('left_right', 'Left-Right Split'),
            ('three_column', 'Three Column')
        ],
        default='three_column',
        help_text="Choose header layout style"
    )
    
    header_background_color = ColorField(
        max_length=7, 
        default="#ffffff", 
        help_text="Header background color (hex code)"
    )
    
    header_border_bottom = models.BooleanField(
        default=True, 
        help_text="Show bottom border"
    )
    
    header_border_color = ColorField(
        max_length=7, 
        default="#e5e7eb", 
        help_text="Border color (hex code)"
    )
    
    header_shadow = models.BooleanField(
        default=True, 
        help_text="Add shadow effect to header"
    )
    
    # Responsive Settings
    mobile_stack_layout = models.BooleanField(
        default=True, 
        help_text="Stack elements vertically on mobile"
    )
    
    hide_affiliations_mobile = models.BooleanField(
        default=False, 
        help_text="Hide affiliations on mobile devices"
    )
    
    # Animation Effects
    enable_animations = models.BooleanField(
        default=True, 
        help_text="Enable hover animations and transitions"
    )
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Header Information"
        verbose_name_plural = "Header Information"
    
    def clean(self):
        # Ensure only one active instance
        if self.is_active and HeaderInfo.objects.filter(is_active=True).exclude(pk=self.pk).exists():
            raise ValidationError("Only one header info can be active at a time.")
    
    def __str__(self):
        return f"Header Info - {self.email}"


class NavbarInfo(TimeStampedModel):
    """Navbar configuration and styling model"""
    # Brand/Logo settings
    brand_name = models.CharField(max_length=200, default="Chaitanya Science and Arts College")
    brand_subtitle = models.CharField(max_length=300, default="Shaheed Nandkumar Patel Vishwavidyalaya, Raigarh", blank=True)
    logo = models.ImageField(upload_to='navbar/', blank=True)
    show_logo = models.BooleanField(default=True)
    show_brand_text = models.BooleanField(default=True)
    
    # Navbar styling
    navbar_background_color = ColorField(default="#ffffff", help_text="Hex color code")
    navbar_text_color = ColorField(default="#374151", help_text="Hex color code")
    navbar_hover_color = ColorField(default="#dc2626", help_text="Hex color code")
    navbar_border_color = ColorField(default="#e5e7eb", help_text="Hex color code")
    
    # Search functionality
    enable_search = models.BooleanField(default=True)
    search_placeholder = models.CharField(max_length=100, default="Search...", blank=True)
    
    # Navbar behavior
    is_sticky = models.BooleanField(default=False, help_text="Make navbar stick to top when scrolling")
    show_below_header = models.BooleanField(default=True, help_text="Position navbar below header/top bar")
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Navbar Configuration"
        verbose_name_plural = "Navbar Configuration"
    
    def clean(self):
        # Ensure only one active instance
        if self.is_active and NavbarInfo.objects.filter(is_active=True).exclude(pk=self.pk).exists():
            raise ValidationError("Only one navbar configuration can be active at a time.")
    
    def __str__(self):
        return f"Navbar Config - {self.brand_name}"


class CollegeInfo(TimeStampedModel):
    """Single instance model for college information"""
    name = models.CharField(max_length=200, default="Chaitanya Science and Arts College")
    establishment_year = models.IntegerField(default=2001)
    affiliation = models.CharField(max_length=300, default="Shaheed Nandkumar Patel Vishwavidyalaya, Raigarh")
    address_line = models.TextField(default="Pamgarh, Janjgir Champa, Chhattisgarh, India, 495554")
    email = models.EmailField(default="chaitanyapamgarh@gmail.com")
    phone = models.CharField(max_length=20, default="+91-9425540666")
    
    # Mission and messages
    mission_statement_short = models.CharField(max_length=180)
    mission_statement_long = models.TextField()
    founder_name = models.CharField(max_length=100, default="Mr Veerendra Tiwari")
    founder_message = models.TextField()
    principal_name = models.CharField(max_length=100, default="Dr Vinod Kumar Gupta")
    principal_message = models.TextField()
    
    # Statistics
    courses_count = models.CharField(max_length=10, default="18+")
    students_count = models.CharField(max_length=10, default="8000+")
    faculty_staff_count = models.CharField(max_length=10, default="50+")
    years_of_excellence = models.CharField(max_length=10, default="25+")
    
    # Achievements
    naac_grade = models.CharField(max_length=50, default="NAAC GRADE A AWARD")
    iic_rating = models.CharField(max_length=50, default="3 Star Rating IIC")
    
    # Social links
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Images
    logo = models.ImageField(upload_to='college/', blank=True)
    hero_image = models.ImageField(upload_to='college/', blank=True)
    
    # Meta fields
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "College Information"
        verbose_name_plural = "College Information"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def clean(self):
        # Ensure only one active instance
        if self.is_active and CollegeInfo.objects.filter(is_active=True).exclude(pk=self.pk).exists():
            raise ValidationError("Only one college info can be active at a time.")
    
    def __str__(self):
        return self.name


class Program(TimeStampedModel):
    """Academic programs offered by the college"""
    DISCIPLINE_CHOICES = [
        ('arts', 'Arts'),
        ('science', 'Science'),
        ('commerce', 'Commerce'),
        ('management', 'Management'),
    ]
    
    name = models.CharField(max_length=200)
    discipline = models.CharField(max_length=20, choices=DISCIPLINE_CHOICES)
    description = CKEditor5Field()
    duration = models.CharField(max_length=50, blank=True)
    brochure = models.FileField(upload_to='programs/brochures/', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['discipline', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:program_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name


class Event(TimeStampedModel):
    """College events and activities"""
    TYPE_CHOICES = [
        ('workshop', 'Workshop/Seminar'),
        ('celebration', 'Day Celebration'),
        ('foundation', 'Foundation Day'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = CKEditor5Field()
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, default="College Auditorium")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    banner_image = models.ImageField(upload_to='events/', blank=True)
    organizer = models.CharField(max_length=200, blank=True, help_text="Event organizer or department")
    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    registration_required = models.BooleanField(default=False)
    registration_link = models.URLField(blank=True, help_text="External registration form URL")
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:event_detail', kwargs={'slug': self.slug})
    
    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.date >= timezone.now().date()
    
    @property
    def has_images(self):
        return self.images.exists()
    
    def __str__(self):
        return self.title


class EventImage(TimeStampedModel):
    """Multiple images for events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='events/gallery/', 
        help_text="Event image (recommended size: 800x600px or larger)"
    )
    caption = models.CharField(max_length=200, blank=True, help_text="Optional image caption")
    alt_text = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Alternative text for accessibility"
    )
    is_cover = models.BooleanField(
        default=False, 
        help_text="Use as main cover image for this event"
    )
    ordering = models.IntegerField(
        default=0, 
        help_text="Display order (lower numbers appear first)"
    )
    
    class Meta:
        ordering = ['ordering', '-created_at']
        verbose_name = "Event Image"
        verbose_name_plural = "Event Images"
    
    def save(self, *args, **kwargs):
        # Auto-generate alt text if not provided
        if not self.alt_text:
            self.alt_text = f"{self.event.title} - Image {self.ordering + 1}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.event.title} - Image {self.ordering + 1}"


class Notice(TimeStampedModel):
    """Official notices and announcements"""
    CATEGORY_CHOICES = [
        ('exam', 'Exam'),
        ('admission', 'Admission'),
        ('policy', 'Policy'),
        ('general', 'General'),
        ('university', 'University Notices'),
    ]
    
    title = models.CharField(max_length=200)
    content = CKEditor5Field()
    publish_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    attachment = models.FileField(upload_to='notices/', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-publish_date']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:notice_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title


class SocialInitiative(TimeStampedModel):
    """Social initiatives and community programs"""
    name = models.CharField(max_length=200)
    description = CKEditor5Field()
    cover_image = models.ImageField(upload_to='social_initiatives/', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:social_initiative_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name


class StudentTestimonial(TimeStampedModel):
    """Student feedback and testimonials"""
    student_name = models.CharField(max_length=100)
    program_studied = models.CharField(max_length=100)
    feedback_text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    photo = models.ImageField(upload_to='testimonials/', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-rating', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.student_name}-{self.program_studied}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student_name} - {self.program_studied}"


class ImportantLink(TimeStampedModel):
    """Important and quick links"""
    TYPE_CHOICES = [
        ('important', 'Important'),
        ('quick', 'Quick'),
    ]
    
    name = models.CharField(max_length=100)
    url = models.URLField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    icon_class = models.CharField(max_length=50, blank=True, help_text="CSS icon class")
    is_active = models.BooleanField(default=True)
    ordering = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['type', 'ordering', 'name']
    
    def __str__(self):
        return self.name


class ContactMessage(TimeStampedModel):
    """Contact form submissions"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    comments = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    class Meta:
        ordering = ['-submission_date']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.submission_date.strftime('%Y-%m-%d')}"


# CMS Models for Menu System and Page Builder

class Menu(TimeStampedModel):
    """Top-level menu container"""
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    ordering = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordering', 'title']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_url(self):
        """Get URL for the menu - returns the first active menu item's URL if available"""
        first_item = self.items.filter(is_active=True).first()
        if first_item:
            return first_item.get_url()
        return '#'
    
    def __str__(self):
        return self.title


class Page(TimeStampedModel):
    """CMS Pages with flexible content blocks"""
    TEMPLATE_CHOICES = [
        ('default', 'Default'),
        ('wide', 'Wide Layout'),
        ('landing', 'Landing Page'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    banner_image = models.ImageField(upload_to='pages/', blank=True)
    show_banner = models.BooleanField(default=True)
    show_sidebar = models.BooleanField(default=True)
    enable_search_in_navbar = models.BooleanField(default=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    template_variant = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='default')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['title']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:page_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title


class MenuItem(TimeStampedModel):
    """Menu items with hierarchical structure"""
    PATH_TYPE_CHOICES = [
        ('internal', 'Internal Page'),
        ('external', 'External URL'),
        ('named_url', 'Named URL Pattern'),
    ]
    
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    path_type = models.CharField(max_length=20, choices=PATH_TYPE_CHOICES, default='internal')
    external_url = models.URLField(blank=True, help_text="For external links")
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True, help_text="For CMS pages")
    named_url = models.CharField(max_length=100, blank=True, help_text="Django URL name (e.g., 'college_website:academics')")
    icon_class = models.CharField(max_length=50, blank=True, help_text="CSS icon class (e.g., 'fas fa-home')")
    description = models.TextField(blank=True, help_text="Optional description for the menu item")
    is_active = models.BooleanField(default=True)
    ordering = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordering', 'title']
        unique_together = ['menu', 'slug']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_url(self):
        """Get the appropriate URL for this menu item"""
        if self.path_type == 'external' and self.external_url:
            return self.external_url
        elif self.path_type == 'named_url' and self.named_url:
            try:
                return reverse(self.named_url)
            except:
                return '#'
        elif self.path_type == 'internal' and self.page:
            return self.page.get_absolute_url()
        return '#'
    
    def get_full_path(self):
        """Get the full hierarchical path for this menu item"""
        path_parts = []
        current = self
        while current:
            path_parts.insert(0, current.slug)
            current = current.parent
        return '/'.join(path_parts)
    
    def get_breadcrumb(self):
        """Get breadcrumb list for this menu item"""
        breadcrumb = []
        current = self
        while current:
            breadcrumb.insert(0, {
                'title': current.title,
                'url': current.get_url(),
                'slug': current.slug
            })
            current = current.parent
        return breadcrumb
    
    @property
    def has_children(self):
        """Check if this menu item has child items"""
        return self.children.filter(is_active=True).exists()
    
    @property
    def active_children(self):
        """Get active child menu items"""
        return self.children.filter(is_active=True).order_by('ordering', 'title')
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.title} → {self.title}"
        return f"{self.menu.title} - {self.title}"


# Content Block Models

class ContentBlock(TimeStampedModel):
    """Base class for all content blocks"""
    title = models.CharField(max_length=200, blank=True)
    ordering = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['ordering']
        abstract = True


class BlockRichText(ContentBlock):
    """Rich text content block"""
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='rich_text_blocks')
    body = CKEditor5Field()
    
    def __str__(self):
        return f"{self.page.title} - {self.title or 'Rich Text'}"


class BlockImageGallery(ContentBlock):
    """Image gallery content block"""
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='gallery_blocks')
    
    def __str__(self):
        return f"{self.page.title} - {self.title or 'Image Gallery'}"


class GalleryImage(TimeStampedModel):
    """Images for gallery blocks"""
    gallery = models.ForeignKey(BlockImageGallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    ordering = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordering']
    
    def __str__(self):
        return f"{self.gallery.title} - Image {self.ordering}"


class BlockVideoEmbed(ContentBlock):
    """Video embed content block"""
    PROVIDER_CHOICES = [
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
        ('other', 'Other'),
    ]
    
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='video_blocks')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='youtube')
    video_url = models.URLField()
    embed_code = models.TextField(blank=True, help_text="Optional custom embed code")
    
    def __str__(self):
        return f"{self.page.title} - {self.title or 'Video'}"


class BlockDownloadList(ContentBlock):
    """Download list content block"""
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='download_blocks')
    
    def __str__(self):
        return f"{self.page.title} - {self.title or 'Downloads'}"


class DownloadFile(TimeStampedModel):
    """Files for download blocks"""
    download_list = models.ForeignKey(BlockDownloadList, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='downloads/')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    ordering = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordering']
    
    def __str__(self):
        return self.title


class BlockTableHTML(ContentBlock):
    """HTML table content block"""
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='table_blocks')
    html = models.TextField(help_text="HTML table code")
    
    def __str__(self):
        return f"{self.page.title} - {self.title or 'Table'}"


class BlockForm(ContentBlock):
    """Form content block"""
    FORM_TYPE_CHOICES = [
        ('contact', 'Contact Form'),
        ('registration', 'Registration Form'),
        ('feedback', 'Feedback Form'),
    ]
    
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='form_blocks')
    form_type = models.CharField(max_length=20, choices=FORM_TYPE_CHOICES, default='contact')
    
    def __str__(self):
        return f"{self.page.title} - {self.get_form_type_display()}"


# Standalone Gallery Models for Gallery Page

class Gallery(TimeStampedModel):
    """Standalone Gallery for main gallery page"""
    CATEGORY_CHOICES = [
        ('campus', 'Campus'),
        ('events', 'Events'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
        ('academic', 'Academic'),
        ('facilities', 'Facilities'),
        ('achievements', 'Achievements'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='campus')
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True)
    is_featured = models.BooleanField(default=False, help_text='Show on homepage')
    is_active = models.BooleanField(default=True)
    ordering = models.IntegerField(default=0)
    
    # SEO fields
    meta_description = models.TextField(max_length=160, blank=True)
    
    class Meta:
        ordering = ['ordering', '-created_at']
        verbose_name_plural = 'Galleries'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_description:
            self.meta_description = self.description[:160] if self.description else f"View {self.title} gallery"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:gallery_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title


class GalleryPhoto(models.Model):
    """Photos for standalone galleries"""
    CATEGORY_CHOICES = [
        ('events', 'Events'),
        ('activities', 'Activities'),
        ('campus', 'Campus Life'),
        ('academics', 'Academics'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('general', 'General'),
    ]
    
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='gallery/photos/')
    title = models.CharField(max_length=200, blank=True)
    caption = models.TextField(blank=True)
    photographer = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    date_taken = models.DateField(blank=True, null=True)
    ordering = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordering', 'created_at']
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Gallery Photos"

    def __str__(self):
        return f"{self.title or 'Photo'} - {self.gallery.title}" or f'Photo {self.ordering}'


# Academic Section Models

class AdmissionInfo(TimeStampedModel):
    """Admission information and procedures"""
    ADMISSION_TYPE_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    admission_type = models.CharField(max_length=20, choices=ADMISSION_TYPE_CHOICES)
    description = models.TextField()
    eligibility_criteria = CKEditor5Field()
    application_process = CKEditor5Field()
    required_documents = CKEditor5Field()
    fees_structure = CKEditor5Field(blank=True)
    important_dates = CKEditor5Field(blank=True)
    contact_info = models.TextField(blank=True)
    application_form = models.FileField(upload_to='admissions/forms/', blank=True)
    brochure = models.FileField(upload_to='admissions/brochures/', blank=True)
    is_active = models.BooleanField(default=True)
    ordering = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordering', 'title']
        verbose_name = "Admission Information"
        verbose_name_plural = "Admission Information"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:admission_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title


class ExamResult(TimeStampedModel):
    """Exam results and announcements"""
    RESULT_TYPE_CHOICES = [
        ('semester', 'Semester Exam'),
        ('annual', 'Annual Exam'),
        ('entrance', 'Entrance Exam'),
        ('supplementary', 'Supplementary Exam'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE_CHOICES)
    exam_date = models.DateField()
    result_date = models.DateField()
    description = CKEditor5Field(blank=True)
    result_file = models.FileField(upload_to='results/', blank=True)
    result_link = models.URLField(blank=True, help_text="External result portal link")
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-result_date', 'title']
        verbose_name = "Exam Result"
        verbose_name_plural = "Exam Results"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.result_date.year}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:result_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return f"{self.title} - {self.result_date.strftime('%B %Y')}"


class LibraryResource(TimeStampedModel):
    """Library resources and services"""
    RESOURCE_TYPE_CHOICES = [
        ('book', 'Book'),
        ('journal', 'Journal'),
        ('ebook', 'E-Book'),
        ('database', 'Database'),
        ('thesis', 'Thesis'),
        ('magazine', 'Magazine'),
        ('newspaper', 'Newspaper'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    author = models.CharField(max_length=200, blank=True)
    isbn = models.CharField(max_length=20, blank=True, verbose_name="ISBN/ISSN")
    publisher = models.CharField(max_length=200, blank=True)
    publication_year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    subject_category = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True, help_text="Shelf/Section location")
    availability_status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('issued', 'Issued'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
    ], default='available')
    digital_copy = models.FileField(upload_to='library/digital/', blank=True)
    external_link = models.URLField(blank=True)
    cover_image = models.ImageField(upload_to='library/covers/', blank=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['title']
        verbose_name = "Library Resource"
        verbose_name_plural = "Library Resources"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:library_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return f"{self.title} - {self.get_resource_type_display()}"


class ELearningCourse(TimeStampedModel):
    """E-Learning courses and materials"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    course_code = models.CharField(max_length=20, unique=True)
    instructor = models.CharField(max_length=100)
    duration_hours = models.PositiveIntegerField(help_text="Course duration in hours")
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    prerequisites = models.TextField(blank=True)
    learning_outcomes = CKEditor5Field()
    course_content = CKEditor5Field()
    course_materials = models.FileField(upload_to='elearning/materials/', blank=True)
    video_lectures = models.URLField(blank=True, help_text="Link to video lectures")
    assignments = models.FileField(upload_to='elearning/assignments/', blank=True)
    quiz_link = models.URLField(blank=True)
    certificate_available = models.BooleanField(default=False)
    enrollment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    max_enrollment = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['title']
        verbose_name = "E-Learning Course"
        verbose_name_plural = "E-Learning Courses"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:elearning_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return f"{self.course_code} - {self.title}"


class PlacementRecord(TimeStampedModel):
    """Student placement records and company information"""
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, blank=True)
    course = models.CharField(max_length=100)
    graduation_year = models.PositiveIntegerField()
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=100)
    package_offered = models.DecimalField(max_digits=10, decimal_places=2, help_text="Annual package in lakhs")
    placement_date = models.DateField()
    company_location = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=20, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ], default='full_time')
    student_photo = models.ImageField(upload_to='placements/students/', blank=True)
    company_logo = models.ImageField(upload_to='placements/companies/', blank=True)
    testimonial = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-placement_date', 'student_name']
        verbose_name = "Placement Record"
        verbose_name_plural = "Placement Records"
    
    def __str__(self):
        return f"{self.student_name} - {self.company_name} ({self.graduation_year})"


class AlumniProfile(TimeStampedModel):
    """Alumni profiles and achievements"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    graduation_year = models.PositiveIntegerField()
    course = models.CharField(max_length=100)
    current_position = models.CharField(max_length=200)
    current_company = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_profile = models.URLField(blank=True)
    bio = models.TextField()
    achievements = CKEditor5Field(blank=True)
    career_journey = CKEditor5Field(blank=True)
    advice_to_students = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='alumni/photos/', blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    willing_to_mentor = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-graduation_year', 'name']
        verbose_name = "Alumni Profile"
        verbose_name_plural = "Alumni Profiles"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.graduation_year}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:alumni_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return f"{self.name} ({self.graduation_year}) - {self.current_position}"


# Director and Principal Message Models

class DirectorMessage(TimeStampedModel):
    """Director's message and profile information"""
    name = models.CharField(max_length=100, default="Mr. Veerendra Tiwari")
    designation = models.CharField(max_length=100, default="Director")
    qualifications = models.CharField(
        max_length=300, 
        blank=True, 
        help_text="Educational qualifications and certifications"
    )
    experience_years = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        help_text="Years of experience in education sector"
    )
    message_title = models.CharField(
        max_length=200, 
        default="Director's Message",
        help_text="Title for the message section"
    )
    message_content = CKEditor5Field(
        help_text="Director's message to students and visitors"
    )
    vision = models.TextField(
        blank=True,
        help_text="Director's vision for the institution"
    )
    achievements = CKEditor5Field(
        blank=True,
        help_text="Notable achievements and awards"
    )
    profile_photo = models.ImageField(
        upload_to='leadership/director/', 
        blank=True,
        help_text="Director's profile photo (recommended size: 400x500px)"
    )
    email = models.EmailField(blank=True, help_text="Official email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    
    # Social media links
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn Profile")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter Profile")
    facebook_url = models.URLField(blank=True, verbose_name="Facebook Profile")
    
    # Display settings
    show_on_homepage = models.BooleanField(
        default=True, 
        help_text="Display message snippet on homepage"
    )
    show_achievements = models.BooleanField(
        default=True, 
        help_text="Display achievements section"
    )
    show_contact_info = models.BooleanField(
        default=True, 
        help_text="Display contact information"
    )
    is_active = models.BooleanField(
        default=True, 
        help_text="Enable/disable director message section"
    )
    
    # SEO
    meta_description = models.CharField(
        max_length=160, 
        blank=True,
        help_text="SEO meta description for director's message page"
    )
    
    class Meta:
        verbose_name = "Director's Message"
        verbose_name_plural = "Director's Messages"
    
    def clean(self):
        # Ensure only one active instance
        if self.is_active and DirectorMessage.objects.filter(is_active=True).exclude(pk=self.pk).exists():
            raise ValidationError("Only one director message can be active at a time.")
    
    def get_absolute_url(self):
        return reverse('college_website:director_message')
    
    def __str__(self):
        return f"{self.name} - {self.designation}"


class PrincipalMessage(TimeStampedModel):
    """Principal's message and profile information"""
    name = models.CharField(max_length=100, default="Dr. Vinod Kumar Gupta")
    designation = models.CharField(max_length=100, default="Principal")
    qualifications = models.CharField(
        max_length=300, 
        blank=True, 
        help_text="Educational qualifications and certifications"
    )
    specialization = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Area of specialization or expertise"
    )
    experience_years = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        help_text="Years of experience in education sector"
    )
    message_title = models.CharField(
        max_length=200, 
        default="Principal's Message",
        help_text="Title for the message section"
    )
    message_content = CKEditor5Field(
        help_text="Principal's message to students and visitors"
    )
    educational_philosophy = models.TextField(
        blank=True,
        help_text="Principal's educational philosophy and approach"
    )
    achievements = CKEditor5Field(
        blank=True,
        help_text="Notable achievements, publications, and awards"
    )
    profile_photo = models.ImageField(
        upload_to='leadership/principal/', 
        blank=True,
        help_text="Principal's profile photo (recommended size: 400x500px)"
    )
    email = models.EmailField(blank=True, help_text="Official email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    office_hours = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Office hours for student meetings"
    )
    
    # Social media links
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn Profile")
    researchgate_url = models.URLField(blank=True, verbose_name="ResearchGate Profile")
    orcid_url = models.URLField(blank=True, verbose_name="ORCID Profile")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter Profile")
    
    # Display settings
    show_on_homepage = models.BooleanField(
        default=True, 
        help_text="Display message snippet on homepage"
    )
    show_achievements = models.BooleanField(
        default=True, 
        help_text="Display achievements section"
    )
    show_contact_info = models.BooleanField(
        default=True, 
        help_text="Display contact information"
    )
    show_office_hours = models.BooleanField(
        default=True, 
        help_text="Display office hours information"
    )
    is_active = models.BooleanField(
        default=True, 
        help_text="Enable/disable principal message section"
    )
    
    # SEO
    meta_description = models.CharField(
        max_length=160, 
        blank=True,
        help_text="SEO meta description for principal's message page"
    )
    
    class Meta:
        verbose_name = "Principal's Message"
        verbose_name_plural = "Principal's Messages"
    
    def clean(self):
        # Ensure only one active instance
        if self.is_active and PrincipalMessage.objects.filter(is_active=True).exclude(pk=self.pk).exists():
            raise ValidationError("Only one principal message can be active at a time.")
    
    def get_absolute_url(self):
        return reverse('college_website:principal_message')
    
    def __str__(self):
        return f"{self.name} - {self.designation}"


# IQAC (Internal Quality Assurance Cell) Models

class IQACInfo(TimeStampedModel):
    """IQAC main information and overview"""
    title = models.CharField(
        max_length=200,
        default="Internal Quality Assurance Cell",
        help_text="IQAC page title"
    )
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        help_text="Subtitle or tagline for IQAC"
    )
    overview = CKEditor5Field(
        help_text="Detailed overview of IQAC objectives and functions"
    )
    vision = models.TextField(
        blank=True,
        help_text="IQAC vision statement"
    )
    mission = models.TextField(
        blank=True,
        help_text="IQAC mission statement"
    )
    objectives = CKEditor5Field(
        blank=True,
        help_text="Key objectives of IQAC"
    )
    
    # Statistics
    years_of_excellence = models.PositiveIntegerField(
        default=10,
        help_text="Years of excellence in quality assurance"
    )
    quality_initiatives = models.PositiveIntegerField(
        default=50,
        help_text="Number of quality initiatives implemented"
    )
    naac_grade = models.CharField(
        max_length=10,
        default="A++",
        help_text="NAAC accreditation grade"
    )
    quality_compliance = models.CharField(
        max_length=10,
        default="100%",
        help_text="Quality compliance percentage"
    )
    
    # Contact Information
    coordinator_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Name of IQAC coordinator"
    )
    coordinator_designation = models.CharField(
        max_length=100,
        blank=True,
        help_text="Designation of IQAC coordinator"
    )
    office_location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Physical location of IQAC office"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="IQAC contact phone number"
    )
    email = models.EmailField(
        blank=True,
        help_text="IQAC official email address"
    )
    
    # Display Settings
    show_statistics = models.BooleanField(
        default=True,
        help_text="Display statistics section"
    )
    show_contact_info = models.BooleanField(
        default=True,
        help_text="Display contact information"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Enable/disable IQAC section"
    )
    
    # SEO
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO meta description for IQAC page"
    )
    
    class Meta:
        verbose_name = "IQAC Information"
        verbose_name_plural = "IQAC Information"
    
    def clean(self):
        # Ensure only one active instance
        if self.is_active and IQACInfo.objects.filter(is_active=True).exclude(pk=self.pk).exists():
            raise ValidationError("Only one IQAC info can be active at a time.")
    
    def __str__(self):
        return self.title


class IQACReport(TimeStampedModel):
    """IQAC reports and documents"""
    REPORT_TYPES = [
        ('annual', 'Annual Report'),
        ('self_study', 'Self Study Report'),
        ('aqar', 'Annual Quality Assurance Report (AQAR)'),
        ('ssr', 'Self Study Report (SSR)'),
        ('naac', 'NAAC Related'),
        ('nirf', 'NIRF Related'),
        ('other', 'Other Report'),
    ]
    
    title = models.CharField(
        max_length=200,
        help_text="Report title"
    )
    slug = models.SlugField(unique=True, blank=True)
    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPES,
        default='annual'
    )
    academic_year = models.CharField(
        max_length=9,
        help_text="Academic year (e.g., 2023-24)"
    )
    description = models.TextField(
        blank=True,
        help_text="Brief description of the report"
    )
    report_file = models.FileField(
        upload_to='iqac/reports/',
        help_text="Upload PDF report file"
    )
    cover_image = models.ImageField(
        upload_to='iqac/covers/',
        blank=True,
        help_text="Optional cover image for the report"
    )
    file_size = models.CharField(
        max_length=20,
        blank=True,
        help_text="File size (auto-calculated)"
    )
    download_count = models.PositiveIntegerField(default=0)
    
    # Publishing
    publish_date = models.DateField(
        default=timezone.now,
        help_text="Report publication date"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this report on main IQAC page"
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Make report publicly available"
    )
    
    class Meta:
        ordering = ['-publish_date', '-created_at']
        verbose_name = "IQAC Report"
        verbose_name_plural = "IQAC Reports"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.academic_year}")
        
        # Calculate file size if file exists
        if self.report_file:
            try:
                size = self.report_file.size
                if size < 1024:
                    self.file_size = f"{size} B"
                elif size < 1024 * 1024:
                    self.file_size = f"{size / 1024:.1f} KB"
                else:
                    self.file_size = f"{size / (1024 * 1024):.1f} MB"
            except:
                self.file_size = "Unknown"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.academic_year})"


class NAACInfo(TimeStampedModel):
    """NAAC accreditation information"""
    title = models.CharField(
        max_length=200,
        default="NAAC Accreditation",
        help_text="NAAC section title"
    )
    current_grade = models.CharField(
        max_length=5,
        default="A++",
        help_text="Current NAAC grade"
    )
    accreditation_year = models.PositiveIntegerField(
        help_text="Year of last accreditation"
    )
    validity_period = models.CharField(
        max_length=50,
        help_text="Validity period of accreditation"
    )
    cgpa_score = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="CGPA score obtained"
    )
    overview = CKEditor5Field(
        help_text="Overview of NAAC accreditation process and achievements"
    )
    key_highlights = CKEditor5Field(
        blank=True,
        help_text="Key highlights from NAAC assessment"
    )
    certificate_file = models.FileField(
        upload_to='iqac/naac/',
        blank=True,
        help_text="NAAC accreditation certificate"
    )
    peer_team_report = models.FileField(
        upload_to='iqac/naac/',
        blank=True,
        help_text="Peer team report"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Enable/disable NAAC section"
    )
    
    class Meta:
        verbose_name = "NAAC Information"
        verbose_name_plural = "NAAC Information"
    
    def __str__(self):
        return f"NAAC {self.current_grade} ({self.accreditation_year})"


class NIRFInfo(TimeStampedModel):
    """NIRF ranking information"""
    title = models.CharField(
        max_length=200,
        default="NIRF Rankings",
        help_text="NIRF section title"
    )
    current_ranking = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Current NIRF ranking position"
    )
    ranking_year = models.PositiveIntegerField(
        help_text="Year of ranking"
    )
    category = models.CharField(
        max_length=100,
        default="College",
        help_text="NIRF ranking category"
    )
    overall_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Overall NIRF score"
    )
    overview = CKEditor5Field(
        help_text="Overview of NIRF participation and achievements"
    )
    performance_metrics = CKEditor5Field(
        blank=True,
        help_text="Detailed performance metrics and scores"
    )
    data_template = models.FileField(
        upload_to='iqac/nirf/',
        blank=True,
        help_text="NIRF data template submitted"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Enable/disable NIRF section"
    )
    
    class Meta:
        verbose_name = "NIRF Information"
        verbose_name_plural = "NIRF Information"
        ordering = ['-ranking_year']
    
    def __str__(self):
        if self.current_ranking:
            return f"NIRF Rank {self.current_ranking} ({self.ranking_year})"
        return f"NIRF Participation ({self.ranking_year})"


class AccreditationInfo(TimeStampedModel):
    """General accreditation and certification information"""
    title = models.CharField(
        max_length=200,
        help_text="Accreditation title"
    )
    accrediting_body = models.CharField(
        max_length=200,
        help_text="Name of the accrediting organization"
    )
    accreditation_type = models.CharField(
        max_length=100,
        help_text="Type of accreditation"
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ('accredited', 'Accredited'),
            ('reaccredited', 'Re-accredited'),
            ('in_progress', 'In Progress'),
            ('applied', 'Applied'),
        ],
        default='accredited'
    )
    grade_or_rating = models.CharField(
        max_length=20,
        blank=True,
        help_text="Grade, rating or score received"
    )
    accreditation_date = models.DateField(
        help_text="Date of accreditation"
    )
    validity_period = models.CharField(
        max_length=100,
        help_text="Validity period of accreditation"
    )
    description = CKEditor5Field(
        help_text="Detailed description of the accreditation"
    )
    certificate_file = models.FileField(
        upload_to='iqac/accreditation/',
        blank=True,
        help_text="Accreditation certificate file"
    )
    website_url = models.URLField(
        blank=True,
        help_text="Official website of accrediting body"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature on main accreditation page"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Display this accreditation"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    
    class Meta:
        ordering = ['display_order', '-accreditation_date']
        verbose_name = "Accreditation Information"
        verbose_name_plural = "Accreditation Information"
    
    def __str__(self):
        return f"{self.title} - {self.accrediting_body} ({self.grade_or_rating})"


class IQACFeedback(TimeStampedModel):
    """Feedback system for IQAC"""
    FEEDBACK_TYPES = [
        ('student', 'Student Feedback'),
        ('faculty', 'Faculty Feedback'),
        ('parent', 'Parent Feedback'),
        ('alumni', 'Alumni Feedback'),
        ('employer', 'Employer Feedback'),
        ('other', 'Other Stakeholder'),
    ]
    
    RATING_CHOICES = [
        (5, 'Excellent'),
        (4, 'Very Good'),
        (3, 'Good'),
        (2, 'Fair'),
        (1, 'Poor'),
    ]
    
    name = models.CharField(
        max_length=100,
        help_text="Name of feedback provider"
    )
    email = models.EmailField(
        help_text="Email address"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Phone number (optional)"
    )
    feedback_type = models.CharField(
        max_length=20,
        choices=FEEDBACK_TYPES,
        help_text="Type of stakeholder providing feedback"
    )
    
    # Rating fields
    teaching_quality = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text="Rate teaching quality"
    )
    infrastructure = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text="Rate infrastructure facilities"
    )
    administration = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text="Rate administrative services"
    )
    library_resources = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text="Rate library resources"
    )
    overall_satisfaction = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text="Overall satisfaction rating"
    )
    
    # Feedback content
    suggestions = models.TextField(
        help_text="Suggestions for improvement"
    )
    strengths = models.TextField(
        blank=True,
        help_text="Institutional strengths (optional)"
    )
    areas_for_improvement = models.TextField(
        blank=True,
        help_text="Areas that need improvement (optional)"
    )
    
    # Status
    is_reviewed = models.BooleanField(
        default=False,
        help_text="Mark as reviewed by IQAC team"
    )
    reviewed_by = models.CharField(
        max_length=100,
        blank=True,
        help_text="Name of reviewer"
    )
    review_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date of review"
    )
    response = models.TextField(
        blank=True,
        help_text="IQAC response to feedback"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "IQAC Feedback"
        verbose_name_plural = "IQAC Feedback"
    
    def get_average_rating(self):
        """Calculate average rating across all categories"""
        ratings = [
            self.teaching_quality,
            self.infrastructure,
            self.administration,
            self.library_resources,
            self.overall_satisfaction
        ]
        return sum(ratings) / len(ratings)
    
    def __str__(self):
        return f"{self.name} - {self.get_feedback_type_display()} ({self.created_at.strftime('%Y-%m-%d')})"


class QualityInitiative(TimeStampedModel):
    """Quality enhancement initiatives by IQAC"""
    INITIATIVE_STATUS = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    
    title = models.CharField(
        max_length=200,
        help_text="Initiative title"
    )
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field(
        help_text="Detailed description of the initiative"
    )
    objectives = models.TextField(
        help_text="Key objectives of this initiative"
    )
    target_beneficiaries = models.CharField(
        max_length=200,
        help_text="Who will benefit from this initiative"
    )
    
    # Timeline
    start_date = models.DateField(
        help_text="Initiative start date"
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="Initiative end date (if applicable)"
    )
    status = models.CharField(
        max_length=20,
        choices=INITIATIVE_STATUS,
        default='planned'
    )
    
    # Progress tracking
    progress_percentage = models.PositiveIntegerField(
        default=0,
        help_text="Progress percentage (0-100)"
    )
    budget_allocated = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Budget allocated for this initiative"
    )
    
    # Team and coordination
    coordinator = models.CharField(
        max_length=100,
        help_text="Initiative coordinator name"
    )
    team_members = models.TextField(
        blank=True,
        help_text="Team members involved"
    )
    
    # Documentation
    outcome_report = models.FileField(
        upload_to='iqac/initiatives/',
        blank=True,
        help_text="Outcome or progress report"
    )
    
    # Display settings
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature on main IQAC page"
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Make initiative publicly visible"
    )
    
    class Meta:
        ordering = ['-start_date', 'title']
        verbose_name = "Quality Initiative"
        verbose_name_plural = "Quality Initiatives"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def is_current(self):
        """Check if initiative is currently active"""
        from django.utils import timezone
        now = timezone.now().date()
        return self.start_date <= now and (not self.end_date or self.end_date >= now)
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


# Side Menu System for CMS Pages

class SideMenu(TimeStampedModel):
    """Side menu configuration for any page/section"""
    name = models.CharField(
        max_length=100,
        help_text="Name for this side menu configuration"
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="Unique identifier for this side menu"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of this side menu's purpose"
    )
    
    # Styling options
    menu_title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Title to display above the menu (optional)"
    )
    show_title = models.BooleanField(
        default=True,
        help_text="Display the menu title"
    )
    title_color = ColorField(
        default="#1f2937",
        help_text="Menu title color"
    )
    background_color = ColorField(
        default="#f8fafc",
        help_text="Menu background color"
    )
    border_color = ColorField(
        default="#e2e8f0",
        help_text="Menu border color"
    )
    
    # Menu behavior
    is_collapsible = models.BooleanField(
        default=True,
        help_text="Allow menu to be collapsed on mobile"
    )
    default_collapsed = models.BooleanField(
        default=False,
        help_text="Start collapsed on mobile"
    )
    
    # Assignment to pages/sections
    ASSIGNMENT_TYPE_CHOICES = [
        ('url_pattern', 'URL Pattern'),
        ('page_slug', 'Specific CMS Page'),
        ('section', 'Site Section'),
        ('global', 'Global (All Pages)'),
    ]
    assignment_type = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_TYPE_CHOICES,
        default='url_pattern'
    )
    url_pattern = models.CharField(
        max_length=200,
        blank=True,
        help_text="URL pattern to match (e.g., '/iqac/', '/academics/')"
    )
    page_slug = models.CharField(
        max_length=200,
        blank=True,
        help_text="Specific page slug to attach this menu to"
    )
    section_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Site section name (e.g., 'academics', 'admissions')"
    )
    
    # Priority for multiple menus
    priority = models.PositiveIntegerField(
        default=0,
        help_text="Priority when multiple menus match (higher = higher priority)"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Enable/disable this side menu"
    )
    
    class Meta:
        ordering = ['-priority', 'name']
        verbose_name = "Side Menu"
        verbose_name_plural = "Side Menus"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def active_items(self):
        """Get all active menu items ordered by their position"""
        return self.items.filter(is_active=True).order_by('ordering', 'title')
    
    def matches_request(self, request):
        """Check if this side menu should be displayed for the given request"""
        if not self.is_active:
            return False
        
        if self.assignment_type == 'global':
            return True
        elif self.assignment_type == 'url_pattern' and self.url_pattern:
            return request.path.startswith(self.url_pattern)
        elif self.assignment_type == 'page_slug' and self.page_slug:
            # This would need custom logic based on your page structure
            return request.resolver_match and request.resolver_match.kwargs.get('slug') == self.page_slug
        elif self.assignment_type == 'section' and self.section_name:
            # Check if current URL belongs to the specified section
            return f"/{self.section_name}/" in request.path
        
        return False
    
    def __str__(self):
        return f"{self.name} ({self.get_assignment_type_display()})"


class SideMenuItem(TimeStampedModel):
    """Individual items in a side menu"""
    ITEM_TYPE_CHOICES = [
        ('link', 'Simple Link'),
        ('heading', 'Section Heading'),
        ('separator', 'Separator Line'),
        ('dropdown', 'Dropdown Container'),
    ]
    
    LINK_TYPE_CHOICES = [
        ('internal', 'Internal Page'),
        ('external', 'External URL'),
        ('named_url', 'Named URL Pattern'),
        ('anchor', 'Page Anchor'),
    ]
    
    side_menu = models.ForeignKey(
        SideMenu,
        on_delete=models.CASCADE,
        related_name='items'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text="Parent item for nested menus"
    )
    
    # Basic properties
    title = models.CharField(
        max_length=200,
        help_text="Display text for the menu item"
    )
    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPE_CHOICES,
        default='link'
    )
    
    # Link configuration
    link_type = models.CharField(
        max_length=20,
        choices=LINK_TYPE_CHOICES,
        default='internal',
        blank=True
    )
    external_url = models.URLField(
        blank=True,
        help_text="For external links"
    )
    cms_page = models.ForeignKey(
        'Page',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="For CMS pages"
    )
    named_url = models.CharField(
        max_length=100,
        blank=True,
        help_text="Django URL name (e.g., 'college_website:iqac')"
    )
    anchor_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Page anchor/section ID (e.g., 'overview')"
    )
    
    # Display options
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        help_text="CSS icon class (e.g., 'fas fa-file-alt')"
    )
    badge_text = models.CharField(
        max_length=20,
        blank=True,
        help_text="Optional badge text (e.g., 'New', '5')"
    )
    badge_color = ColorField(
        default="#dc2626",
        blank=True,
        help_text="Badge color"
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Optional description/tooltip"
    )
    
    # Styling
    custom_css_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Custom CSS classes"
    )
    text_color = ColorField(
        default="#374151",
        blank=True,
        help_text="Text color for this item"
    )
    hover_color = ColorField(
        default="#1e40af",
        blank=True,
        help_text="Hover color"
    )
    
    # Behavior
    open_in_new_tab = models.BooleanField(
        default=False,
        help_text="Open link in new tab"
    )
    highlight_current = models.BooleanField(
        default=True,
        help_text="Highlight when current page matches this item"
    )
    
    # Ordering and visibility
    ordering = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Enable/disable this menu item"
    )
    
    # Conditional display
    show_only_authenticated = models.BooleanField(
        default=False,
        help_text="Show only to logged-in users"
    )
    show_only_staff = models.BooleanField(
        default=False,
        help_text="Show only to staff users"
    )
    
    class Meta:
        ordering = ['ordering', 'title']
        verbose_name = "Side Menu Item"
        verbose_name_plural = "Side Menu Items"
    
    def get_url(self):
        """Get the appropriate URL for this menu item"""
        if self.item_type != 'link':
            return '#'
        
        if self.link_type == 'external' and self.external_url:
            return self.external_url
        elif self.link_type == 'named_url' and self.named_url:
            try:
                from django.urls import reverse
                return reverse(self.named_url)
            except:
                return '#'
        elif self.link_type == 'internal' and self.cms_page:
            return self.cms_page.get_absolute_url()
        elif self.link_type == 'anchor' and self.anchor_id:
            return f"#{self.anchor_id}"
        
        return '#'
    
    def is_current(self, request):
        """Check if this menu item represents the current page"""
        if not self.highlight_current:
            return False
        
        current_url = request.path
        item_url = self.get_url()
        
        if item_url == '#':
            return False
        
        # Simple URL matching
        if item_url == current_url:
            return True
        
        # Check if current URL starts with item URL (for section matching)
        if len(item_url) > 1 and current_url.startswith(item_url):
            return True
        
        return False
    
    def should_display(self, request):
        """Check if this menu item should be displayed for the current user"""
        if not self.is_active:
            return False
        
        if self.show_only_authenticated and not request.user.is_authenticated:
            return False
        
        if self.show_only_staff and not (request.user.is_authenticated and request.user.is_staff):
            return False
        
        return True
    
    @property
    def has_children(self):
        """Check if this item has child items"""
        return self.children.filter(is_active=True).exists()
    
    @property
    def active_children(self):
        """Get active child items"""
        return self.children.filter(is_active=True).order_by('ordering', 'title')
    
    def __str__(self):
        if self.parent:
            return f"{self.side_menu.name} → {self.parent.title} → {self.title}"
        return f"{self.side_menu.name} → {self.title}"
