from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import uuid


class TimeStampedModel(models.Model):
    """Abstract base class with created_at and updated_at fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Student(TimeStampedModel):
    """Student model with comprehensive profile information"""
    
    COURSE_CHOICES = [
        ('btech-cse', 'B.Tech Computer Science'),
        ('btech-it', 'B.Tech Information Technology'),
        ('btech-ece', 'B.Tech Electronics & Communication'),
        ('btech-mech', 'B.Tech Mechanical Engineering'),
        ('btech-civil', 'B.Tech Civil Engineering'),
        ('btech-eee', 'B.Tech Electrical & Electronics'),
        ('mba', 'MBA'),
        ('mca', 'MCA'),
        ('bca', 'BCA'),
        ('bba', 'BBA'),
        ('bcom', 'B.Com'),
        ('bsc', 'B.Sc'),
        ('msc', 'M.Sc'),
        ('other', 'Other'),
    ]
    
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    # Link to Django User model
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile'
    )
    
    # Student specific fields
    student_id = models.CharField(
        max_length=20, 
        unique=True, 
        db_index=True,
        help_text="Unique student ID"
    )
    
    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, blank=True)
    
    # Address Information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='India')
    
    # Academic Information
    course = models.CharField(max_length=20, choices=COURSE_CHOICES)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    batch = models.CharField(max_length=10, help_text="e.g., 2021-2025")
    enrollment_number = models.CharField(max_length=30, blank=True)
    roll_number = models.CharField(max_length=20, blank=True)
    
    # Guardian Information
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    guardian_email = models.EmailField(blank=True)
    
    # Profile Image
    profile_image = models.ImageField(
        upload_to='students/profiles/',
        blank=True,
        null=True,
        help_text="Profile photo"
    )
    
    # Academic Status
    is_active = models.BooleanField(default=True)
    admission_date = models.DateField(null=True, blank=True)
    graduation_date = models.DateField(null=True, blank=True)
    
    # Verification Status
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    
    # Newsletter and Notifications
    newsletter_subscription = models.BooleanField(default=False)
    sms_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['student_id', 'first_name', 'last_name']
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['course', 'year']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.student_id} - {self.get_full_name()}"
    
    @property
    def get_full_name(self):
        """Return the full name of the student"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def get_course_display_full(self):
        """Return full course name with year"""
        course_name = self.get_course_display()
        year_name = self.get_year_display()
        return f"{course_name} - {year_name}"
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    def get_absolute_url(self):
        """Return absolute URL for student profile"""
        return reverse('college_website:student_profile', kwargs={'student_id': self.student_id})
    
    def save(self, *args, **kwargs):
        """Override save to handle student ID generation"""
        if not self.student_id:
            # Generate student ID based on year and course
            year_code = timezone.now().year % 100
            course_code = self.course.upper()[:3] if self.course else 'STU'
            
            # Find next available number
            existing_count = Student.objects.filter(
                student_id__startswith=f"{year_code}{course_code}"
            ).count()
            
            self.student_id = f"{year_code}{course_code}{existing_count + 1:04d}"
        
        super().save(*args, **kwargs)
    
    def send_verification_email(self, request):
        """Send email verification to student"""
        if not self.user.email:
            return False
        
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        # Create verification URL
        verification_url = request.build_absolute_uri(
            reverse('college_website:verify_email', kwargs={'uidb64': uid, 'token': token})
        )
        
        # Render email template
        context = {
            'user': self.user,
            'student': self,
            'verification_url': verification_url,
            'site_name': 'Student Portal',
        }
        
        html_message = render_to_string('college_website/emails/email_verification.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        try:
            send_mail(
                subject='Verify Your Email - Student Portal',
                message=plain_message,
                html_message=html_message,
                from_email=None,  # Will use DEFAULT_FROM_EMAIL
                recipient_list=[self.user.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Error sending verification email: {e}")
            return False


class StudentDocument(TimeStampedModel):
    """Model for storing student documents"""
    
    DOCUMENT_TYPES = [
        ('transcript', 'Academic Transcript'),
        ('certificate', 'Certificate'),
        ('id_proof', 'ID Proof'),
        ('address_proof', 'Address Proof'),
        ('photo', 'Passport Photo'),
        ('signature', 'Signature'),
        ('other', 'Other Document'),
    ]
    
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    file = models.FileField(
        upload_to='students/documents/',
        help_text="Upload document file (PDF, JPG, PNG)"
    )
    
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_documents'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Student Document'
        verbose_name_plural = 'Student Documents'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.student_id} - {self.get_document_type_display()}"


class StudentLoginLog(models.Model):
    """Model to track student login activities"""
    
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='login_logs'
    )
    
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(max_length=50, blank=True)  # mobile, desktop, tablet
    browser = models.CharField(max_length=100, blank=True)
    
    is_successful = models.BooleanField(default=True)
    failure_reason = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Student Login Log'
        verbose_name_plural = 'Student Login Logs'
        ordering = ['-login_time']
        indexes = [
            models.Index(fields=['student', '-login_time']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f"{self.student.student_id} - {self.login_time.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def session_duration(self):
        """Calculate session duration if logged out"""
        if self.logout_time:
            return self.logout_time - self.login_time
        return None


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
    
    # Navbar dimensions and spacing
    navbar_height = models.PositiveIntegerField(default=40, help_text="Navbar height in pixels")
    navbar_padding_top = models.DecimalField(max_digits=4, decimal_places=2, default=0.1, help_text="Top padding in rem")
    navbar_padding_bottom = models.DecimalField(max_digits=4, decimal_places=2, default=0.1, help_text="Bottom padding in rem")
    navbar_padding_horizontal = models.DecimalField(max_digits=4, decimal_places=2, default=0.5, help_text="Horizontal padding in rem")
    
    # Menu item spacing
    menu_item_padding_vertical = models.DecimalField(max_digits=4, decimal_places=2, default=0.15, help_text="Menu item vertical padding in rem")
    menu_item_padding_horizontal = models.DecimalField(max_digits=4, decimal_places=2, default=0.2, help_text="Menu item horizontal padding in rem")
    menu_item_margin = models.DecimalField(max_digits=4, decimal_places=3, default=0.005, help_text="Menu item margin in rem")
    menu_item_gap = models.DecimalField(max_digits=4, decimal_places=3, default=0.005, help_text="Gap between menu items in rem")
    menu_item_border_radius = models.DecimalField(max_digits=3, decimal_places=1, default=2.0, help_text="Menu item border radius in pixels")
    
    # Font settings
    brand_font_size = models.DecimalField(max_digits=4, decimal_places=2, default=0.75, help_text="Brand font size in rem")
    menu_font_size = models.DecimalField(max_digits=4, decimal_places=2, default=0.65, help_text="Menu font size in rem")
    menu_line_height = models.DecimalField(max_digits=3, decimal_places=1, default=1.1, help_text="Menu line height")
    
    # Logo settings
    logo_height = models.PositiveIntegerField(default=28, help_text="Logo height in pixels")
    
    # Responsive breakpoints
    mobile_breakpoint = models.PositiveIntegerField(default=992, help_text="Mobile breakpoint in pixels")
    tablet_breakpoint = models.PositiveIntegerField(default=768, help_text="Tablet breakpoint in pixels")
    
    # Mobile specific settings
    mobile_navbar_height = models.PositiveIntegerField(default=35, help_text="Mobile navbar height in pixels")
    mobile_padding_horizontal = models.DecimalField(max_digits=4, decimal_places=2, default=0.1, help_text="Mobile horizontal padding in rem")
    mobile_menu_font_size = models.DecimalField(max_digits=4, decimal_places=2, default=0.65, help_text="Mobile menu font size in rem")
    mobile_brand_font_size = models.DecimalField(max_digits=4, decimal_places=2, default=0.7, help_text="Mobile brand font size in rem")
    mobile_logo_height = models.PositiveIntegerField(default=20, help_text="Mobile logo height in pixels")
    
    # Dropdown settings
    dropdown_padding = models.DecimalField(max_digits=4, decimal_places=2, default=0.8, help_text="Dropdown padding in rem")
    dropdown_item_padding_vertical = models.DecimalField(max_digits=4, decimal_places=2, default=0.3, help_text="Dropdown item vertical padding in rem")
    dropdown_item_padding_horizontal = models.DecimalField(max_digits=4, decimal_places=2, default=0.8, help_text="Dropdown item horizontal padding in rem")
    dropdown_item_font_size = models.DecimalField(max_digits=4, decimal_places=2, default=0.75, help_text="Dropdown item font size in rem")
    dropdown_item_margin = models.DecimalField(max_digits=4, decimal_places=2, default=0.15, help_text="Dropdown item margin in rem")
    
    # Mega menu settings
    mega_menu_padding = models.DecimalField(max_digits=4, decimal_places=2, default=0.8, help_text="Mega menu padding in rem")
    mega_menu_columns = models.PositiveIntegerField(default=4, help_text="Number of columns in mega menu")
    mega_menu_width = models.CharField(max_length=20, default="auto", help_text="Mega menu width (auto, 100%, or specific value)")
    
    # Animation settings
    transition_duration = models.DecimalField(max_digits=3, decimal_places=1, default=0.3, help_text="Transition duration in seconds")
    hover_scale = models.DecimalField(max_digits=3, decimal_places=2, default=1.05, help_text="Hover scale effect")
    
    # Shadow and border settings
    box_shadow = models.CharField(max_length=100, default="0 1px 3px -1px rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.06)", help_text="Box shadow CSS value")
    border_radius = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text="Navbar border radius in pixels")
    
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
    
    DEGREE_TYPE_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, help_text="Full program name")
    short_name = models.CharField(max_length=50, blank=True, help_text="Abbreviated name (e.g., B.A., B.Sc.)")
    discipline = models.CharField(max_length=20, choices=DISCIPLINE_CHOICES)
    degree_type = models.CharField(max_length=20, choices=DEGREE_TYPE_CHOICES, default='undergraduate')
    description = CKEditor5Field(help_text="Detailed program description")
    
    # Academic Details
    duration = models.CharField(max_length=50, blank=True, help_text="Program duration (e.g., 3 years)")
    total_seats = models.PositiveIntegerField(blank=True, null=True, help_text="Total available seats")
    department = models.CharField(max_length=100, blank=True, help_text="Department offering this program")
    
    # Curriculum and Subjects
    curriculum = CKEditor5Field(blank=True, help_text="Detailed curriculum information")
    core_subjects = models.TextField(blank=True, help_text="List of core subjects (one per line)")
    elective_subjects = models.TextField(blank=True, help_text="List of elective subjects (one per line)")
    
    # Eligibility and Admission
    eligibility = CKEditor5Field(blank=True, help_text="Eligibility criteria and requirements")
    admission_process = CKEditor5Field(blank=True, help_text="Detailed admission process")
    minimum_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Minimum percentage required")
    entrance_exam = models.CharField(max_length=200, blank=True, help_text="Required entrance exam (if any)")
    
    # Career and Opportunities
    career_opportunities = CKEditor5Field(blank=True, help_text="Career prospects and job opportunities")
    average_salary = models.CharField(max_length=100, blank=True, help_text="Expected salary range (e.g., ₹3-5 LPA)")
    top_recruiters = models.TextField(blank=True, help_text="List of top recruiting companies (one per line)")
    
    # Financial Information
    fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Annual fees in INR")
    scholarship_available = models.BooleanField(default=False, help_text="Scholarships available for this program")
    scholarship_details = models.TextField(blank=True, help_text="Details about available scholarships")
    
    # Course Syllabus Information
    first_year_subjects = CKEditor5Field(blank=True, help_text="First year subjects and curriculum")
    second_year_subjects = CKEditor5Field(blank=True, help_text="Second year subjects and curriculum")
    third_year_subjects = CKEditor5Field(blank=True, help_text="Third year subjects and curriculum (if applicable)")
    elective_options = CKEditor5Field(blank=True, help_text="Available elective subjects and options")
    
    # Course Outcomes and Program Outcomes (CO-PO)
    program_outcomes = CKEditor5Field(blank=True, help_text="Program Outcomes (POs) - what students will achieve")
    course_outcomes = CKEditor5Field(blank=True, help_text="Course Outcomes (COs) - specific learning objectives")
    co_po_mapping = CKEditor5Field(blank=True, help_text="CO-PO mapping and alignment details")
    
    # Academic Timetable
    timetable_info = CKEditor5Field(blank=True, help_text="Academic timetable and schedule information")
    class_timings = models.CharField(max_length=200, blank=True, help_text="Class timings (e.g., 9:00 AM - 1:15 PM)")
    weekly_schedule = CKEditor5Field(blank=True, help_text="Weekly class schedule and subject distribution")
    
    # Enhanced Career Prospects
    teaching_careers = CKEditor5Field(blank=True, help_text="Teaching and education career opportunities")
    media_journalism_careers = CKEditor5Field(blank=True, help_text="Media and journalism career paths")
    government_careers = CKEditor5Field(blank=True, help_text="Government services and civil service opportunities")
    private_sector_careers = CKEditor5Field(blank=True, help_text="Private sector career opportunities")
    further_studies = CKEditor5Field(blank=True, help_text="Higher education and further study options")
    entrepreneurship = CKEditor5Field(blank=True, help_text="Entrepreneurship and startup opportunities")
    
    # Course Features and Benefits
    expert_faculty = CKEditor5Field(blank=True, help_text="Information about expert faculty and their qualifications")
    infrastructure = CKEditor5Field(blank=True, help_text="Modern infrastructure and facilities")
    research_opportunities = CKEditor5Field(blank=True, help_text="Research opportunities and projects")
    industry_connect = CKEditor5Field(blank=True, help_text="Industry connections and partnerships")
    additional_benefits = CKEditor5Field(blank=True, help_text="Additional benefits and facilities")
    assessment_methods = CKEditor5Field(blank=True, help_text="Assessment and evaluation methods")
    global_opportunities = CKEditor5Field(blank=True, help_text="International and global opportunities")
    
    # Additional Information
    brochure = models.FileField(upload_to='programs/brochures/', blank=True, help_text="Program brochure PDF")
    program_image = models.ImageField(upload_to='programs/images/', blank=True, help_text="Program representative image")
    is_featured = models.BooleanField(default=False, help_text="Feature this program on homepage")
    
    # SEO and Management
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Meta Information
    accreditation = models.CharField(max_length=200, blank=True, help_text="Accreditation details (e.g., UGC, AICTE)")
    established_year = models.PositiveIntegerField(blank=True, null=True, help_text="Year when program was established")
    last_updated = models.DateTimeField(auto_now=True)
    
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


class AdmissionInquiry(TimeStampedModel):
    """Admission inquiry form submissions from prospective students"""
    INQUIRY_TYPE_CHOICES = [
        ('general', 'General Inquiry'),
        ('eligibility', 'Eligibility Query'),
        ('documents', 'Document Requirements'),
        ('fees', 'Fee Structure'),
        ('application', 'Application Process'),
        ('other', 'Other'),
    ]
    
    PROGRAM_INTEREST_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
        ('not_decided', 'Not Decided Yet'),
    ]
    
    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('both', 'Both'),
    ]
    
    # Personal Information
    full_name = models.CharField(
        max_length=100,
        help_text="Enter your full name"
    )
    email = models.EmailField(
        help_text="Valid email address for communication"
    )
    phone = models.CharField(
        max_length=15,
        help_text="Contact number with country code"
    )
    
    # Academic Information
    current_qualification = models.CharField(
        max_length=100,
        help_text="Your current highest qualification (e.g., 12th Pass, Graduate)"
    )
    percentage_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Percentage in your latest qualification"
    )
    
    # Inquiry Details
    inquiry_type = models.CharField(
        max_length=20,
        choices=INQUIRY_TYPE_CHOICES,
        default='general',
        help_text="Type of inquiry"
    )
    program_interest = models.CharField(
        max_length=20,
        choices=PROGRAM_INTEREST_CHOICES,
        default='not_decided',
        help_text="Program you're interested in"
    )
    specific_course = models.CharField(
        max_length=100,
        blank=True,
        help_text="Specific course name if known (e.g., B.Sc Computer Science)"
    )
    message = models.TextField(
        help_text="Your specific questions or requirements"
    )
    
    # Response Management
    is_responded = models.BooleanField(default=False)
    response_message = models.TextField(blank=True)
    responded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admission_responses'
    )
    responded_at = models.DateTimeField(null=True, blank=True)
    
    # Preferences
    preferred_contact_method = models.CharField(
        max_length=10,
        choices=CONTACT_METHOD_CHOICES,
        default='email'
    )
    newsletter_subscription = models.BooleanField(
        default=False,
        help_text="Subscribe to college newsletter for updates"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Admission Inquiry"
        verbose_name_plural = "Admission Inquiries"
    
    def __str__(self):
        return f"{self.full_name} - {self.get_inquiry_type_display()} ({self.created_at.strftime('%Y-%m-%d')})"
    
    @property
    def status(self):
        """Get inquiry status"""
        return "Responded" if self.is_responded else "Pending"
    
    @property
    def days_since_inquiry(self):
        """Get number of days since inquiry was made"""
        from django.utils import timezone
        return (timezone.now() - self.created_at).days
    
    def mark_as_responded(self, user, response_message):
        """Mark inquiry as responded"""
        from django.utils import timezone
        self.is_responded = True
        self.responded_by = user
        self.responded_at = timezone.now()
        self.response_message = response_message
        self.save()


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


class VisionMissionContent(TimeStampedModel):
    """Model for managing Vision & Mission page content dynamically"""
    name = models.CharField(max_length=100, default="Vision & Mission Content", help_text="Name for this content configuration")
    is_active = models.BooleanField(default=True, help_text="Make this content active")
    
    # Hero Section
    hero_badge_text = models.CharField(max_length=100, default="Our Purpose & Direction", help_text="Badge text in hero section")
    hero_title = models.CharField(max_length=200, default="Vision & Mission", help_text="Main hero title")
    hero_subtitle = CKEditor5Field(default="Guiding principles that shape our commitment to educational excellence and community transformation", help_text="Hero subtitle/description")
    
    # Vision Section
    vision_statement = CKEditor5Field(help_text="Main vision statement text")
    vision_highlight_1 = models.CharField(max_length=100, default="Excellence in Education", help_text="First vision highlight")
    vision_highlight_2 = models.CharField(max_length=100, default="Community Impact", help_text="Second vision highlight")
    vision_highlight_3 = models.CharField(max_length=100, default="Innovation & Research", help_text="Third vision highlight")
    vision_highlight_4 = models.CharField(max_length=100, default="Global Perspective", help_text="Fourth vision highlight")
    
    # Mission Section
    mission_statement = CKEditor5Field(help_text="Main mission statement text")
    mission_objective_1 = models.CharField(max_length=200, default="Deliver quality education accessible to all", help_text="First mission objective")
    mission_objective_2 = models.CharField(max_length=200, default="Foster research and innovation culture", help_text="Second mission objective")
    mission_objective_3 = models.CharField(max_length=200, default="Develop socially responsible citizens", help_text="Third mission objective")
    
    # Call to Action Section
    cta_title = models.CharField(max_length=100, default="Join Our Journey", help_text="Call to action title")
    cta_description = CKEditor5Field(default="Be part of our mission to transform lives through education. Whether you're a prospective student, faculty member, or community partner, we welcome you to join our journey.", help_text="Call to action description")
    
    class Meta:
        verbose_name = "Vision & Mission Content"
        verbose_name_plural = "Vision & Mission Content"
        ordering = ['-is_active', '-created_at']
    
    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"
    
    def clean(self):
        # Ensure only one active content at a time
        if self.is_active:
            active_content = VisionMissionContent.objects.filter(is_active=True).exclude(pk=self.pk)
            if active_content.exists():
                raise ValidationError("Only one Vision & Mission content can be active at a time.")
    
    @classmethod
    def get_active_content(cls):
        """Get the currently active content or create default if none exists"""
        active_content = cls.objects.filter(is_active=True).first()
        if not active_content:
            # Create default content if none exists
            active_content = cls.objects.create(
                name="Default Vision & Mission Content",
                vision_statement="To be a leading institution of higher education that transforms lives through innovative teaching, research, and community engagement, empowering students from rural backgrounds to become global citizens and leaders of tomorrow.",
                mission_statement="To provide accessible, affordable, and quality higher education that nurtures critical thinking, creativity, and character development while fostering research, innovation, and social responsibility among our diverse student community."
            )
        return active_content


class CoreValue(TimeStampedModel):
    """Model for managing core values displayed on Vision & Mission page"""
    vision_mission_content = models.ForeignKey(VisionMissionContent, on_delete=models.CASCADE, related_name='core_values')
    
    title = models.CharField(max_length=50, help_text="Core value title (e.g., Excellence, Integrity)")
    description = models.TextField(help_text="Description of this core value")
    icon_class = models.CharField(max_length=50, default="fas fa-star", help_text="FontAwesome icon class")
    
    # Color customization
    COLOR_CHOICES = [
        ('yellow-orange', 'Yellow to Orange'),
        ('blue-indigo', 'Blue to Indigo'),
        ('purple-pink', 'Purple to Pink'),
        ('green-emerald', 'Green to Emerald'),
        ('teal-cyan', 'Teal to Cyan'),
        ('red-pink', 'Red to Pink'),
    ]
    gradient_color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='blue-indigo', help_text="Gradient color scheme")
    
    ordering = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    is_active = models.BooleanField(default=True, help_text="Show this core value")
    
    class Meta:
        ordering = ['ordering', 'title']
        verbose_name = "Core Value"
        verbose_name_plural = "Core Values"
    
    def __str__(self):
        return f"{self.title} ({self.vision_mission_content.name})"
    
    @property
    def gradient_classes(self):
        """Return Tailwind CSS gradient classes based on color choice"""
        gradient_map = {
            'yellow-orange': 'tw-from-yellow-400 tw-to-orange-500',
            'blue-indigo': 'tw-from-blue-500 tw-to-indigo-600',
            'purple-pink': 'tw-from-purple-500 tw-to-pink-500',
            'green-emerald': 'tw-from-green-500 tw-to-emerald-500',
            'teal-cyan': 'tw-from-teal-500 tw-to-cyan-500',
            'red-pink': 'tw-from-red-500 tw-to-pink-500',
        }
        return gradient_map.get(self.gradient_color, 'tw-from-blue-500 tw-to-indigo-600')


class HistoryContent(TimeStampedModel):
    """Dynamic content management for college history page"""
    name = models.CharField(
        max_length=100, 
        default="College History Content",
        help_text="Name for this history content set"
    )
    
    # Hero Section
    hero_title = models.CharField(
        max_length=200, 
        default="Our History",
        help_text="Main title for the history page"
    )
    hero_subtitle = models.TextField(
        default="A journey through time showcasing our commitment to educational excellence and community development",
        help_text="Subtitle text for the hero section"
    )
    hero_badge_text = models.CharField(
        max_length=50,
        default="Our Heritage",
        help_text="Badge text in hero section"
    )
    
    # Foundation Story Section
    foundation_title = models.CharField(
        max_length=100,
        default="Foundation Story",
        help_text="Title for foundation section"
    )
    foundation_content = CKEditor5Field(
        help_text="Content describing the college's foundation and early history"
    )
    establishment_year = models.PositiveIntegerField(
        default=1985,
        help_text="Year the college was established"
    )
    faculty_count = models.PositiveIntegerField(
        default=50,
        help_text="Current number of faculty members"
    )
    alumni_count = models.PositiveIntegerField(
        default=5000,
        help_text="Total number of alumni"
    )
    accreditations = models.CharField(
        max_length=200,
        default="Multiple Accreditations",
        help_text="Summary of accreditations received"
    )
    
    # Timeline Section
    timeline_title = models.CharField(
        max_length=100,
        default="Historical Timeline",
        help_text="Title for timeline section"
    )
    timeline_description = models.TextField(
        default="Key moments that shaped our institution's growth and development",
        help_text="Description for timeline section"
    )
    
    # Milestones Section
    milestones_title = models.CharField(
        max_length=100,
        default="Major Milestones",
        help_text="Title for milestones section"
    )
    milestones_description = models.TextField(
        default="Celebrating our achievements and recognitions over the years",
        help_text="Description for milestones section"
    )
    
    # Legacy Section
    legacy_title = models.CharField(
        max_length=100,
        default="Our Continuing Legacy",
        help_text="Title for legacy section"
    )
    legacy_content = models.TextField(
        default="As we look towards the future, we remain committed to our founding principles while embracing innovation and change. Our history is not just about the past—it's the foundation for an even brighter future.",
        help_text="Content for legacy section"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Set to active to display this content on the history page"
    )
    
    class Meta:
        verbose_name = "History Content"
        verbose_name_plural = "History Contents"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"


class TimelineEvent(TimeStampedModel):
    """Individual timeline events for college history"""
    GRADIENT_CHOICES = [
        ('emerald-teal', 'Emerald to Teal'),
        ('blue-indigo', 'Blue to Indigo'),
        ('purple-pink', 'Purple to Pink'),
        ('orange-red', 'Orange to Red'),
        ('teal-cyan', 'Teal to Cyan'),
        ('indigo-purple', 'Indigo to Purple'),
        ('yellow-orange', 'Yellow to Orange'),
        ('green-emerald', 'Green to Emerald'),
    ]
    
    history_content = models.ForeignKey(
        HistoryContent,
        on_delete=models.CASCADE,
        related_name='timeline_events',
        help_text="Associated history content"
    )
    year = models.PositiveIntegerField(help_text="Year of the event")
    title = models.CharField(max_length=100, help_text="Event title")
    description = models.TextField(help_text="Event description")
    icon_class = models.CharField(
        max_length=50,
        default="fas fa-calendar",
        help_text="FontAwesome icon class (e.g., fas fa-seedling)"
    )
    gradient_color = models.CharField(
        max_length=20,
        choices=GRADIENT_CHOICES,
        default='emerald-teal',
        help_text="Gradient color scheme for the event card"
    )
    ordering = models.PositiveIntegerField(
        default=0,
        help_text="Order of display (lower numbers appear first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Include this event in the timeline"
    )
    
    class Meta:
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"
        ordering = ['ordering', 'year']
    
    def __str__(self):
        return f"{self.year} - {self.title}"


class Milestone(TimeStampedModel):
    """Achievement milestones for college history"""
    GRADIENT_CHOICES = [
        ('yellow-orange', 'Yellow to Orange'),
        ('blue-indigo', 'Blue to Indigo'),
        ('purple-pink', 'Purple to Pink'),
        ('green-emerald', 'Green to Emerald'),
        ('teal-cyan', 'Teal to Cyan'),
        ('red-pink', 'Red to Pink'),
        ('orange-red', 'Orange to Red'),
        ('indigo-purple', 'Indigo to Purple'),
    ]
    
    history_content = models.ForeignKey(
        HistoryContent,
        on_delete=models.CASCADE,
        related_name='milestones',
        help_text="Associated history content"
    )
    title = models.CharField(max_length=100, help_text="Milestone title")
    description = models.TextField(help_text="Milestone description")
    icon_class = models.CharField(
        max_length=50,
        default="fas fa-trophy",
        help_text="FontAwesome icon class (e.g., fas fa-medal)"
    )
    gradient_color = models.CharField(
        max_length=20,
        choices=GRADIENT_CHOICES,
        default='yellow-orange',
        help_text="Gradient color scheme for the milestone card"
    )
    ordering = models.PositiveIntegerField(
        default=0,
        help_text="Order of display (lower numbers appear first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Include this milestone in the display"
    )
    
    class Meta:
        verbose_name = "Milestone"
        verbose_name_plural = "Milestones"
        ordering = ['ordering', 'title']
    
    def __str__(self):
        return self.title


class HistoryGalleryImage(models.Model):
    """Model for managing gallery images in history page"""
    
    CATEGORY_CHOICES = [
        ('campus', 'Campus Life'),
        ('events', 'Events & Celebrations'),
        ('academics', 'Academic Activities'),
        ('sports', 'Sports & Recreation'),
        ('cultural', 'Cultural Programs'),
        ('achievements', 'Achievements & Awards'),
        ('infrastructure', 'Infrastructure & Facilities'),
        ('alumni', 'Alumni Gatherings'),
        ('historical', 'Historical Moments'),
    ]
    
    history_content = models.ForeignKey(
        HistoryContent,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        help_text="History content this image belongs to"
    )
    title = models.CharField(
        max_length=200,
        help_text="Title or caption for the image"
    )
    image = models.ImageField(
        upload_to='history/gallery/',
        help_text="Gallery image (recommended: 800x600px or higher)"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='campus',
        help_text="Category for organizing images"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional detailed description of the image"
    )
    year_taken = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Year when this photo was taken (optional)"
    )
    photographer = models.CharField(
        max_length=100,
        blank=True,
        help_text="Photographer credit (optional)"
    )
    ordering = models.PositiveIntegerField(
        default=0,
        help_text="Order of display (lower numbers appear first)"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Mark as featured image (appears prominently)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Include this image in the gallery"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "History Gallery Image"
        verbose_name_plural = "History Gallery Images"
        ordering = ['category', 'ordering', '-year_taken']
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
    
    def get_thumbnail_url(self):
        """Return thumbnail URL for admin display"""
        if self.image:
            return self.image.url
        return None


class Department(TimeStampedModel):
    """Academic departments in the college"""
    DISCIPLINE_CHOICES = [
        ('science', 'Science'),
        ('arts', 'Arts'),
        ('commerce', 'Commerce'),
        ('management', 'Management'),
        ('other', 'Other'),
    ]
    
    THEME_COLOR_CHOICES = [
        ('blue', 'Blue Theme'),
        ('green', 'Green Theme'),
        ('red', 'Red Theme'),
        ('purple', 'Purple Theme'),
        ('orange', 'Orange Theme'),
        ('teal', 'Teal Theme'),
        ('indigo', 'Indigo Theme'),
        ('pink', 'Pink Theme'),
        ('yellow', 'Yellow Theme'),
        ('gray', 'Gray Theme'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, help_text="Department name (e.g., Department of Physics)")
    short_name = models.CharField(max_length=50, blank=True, help_text="Abbreviated name (e.g., Physics Dept.)")
    slug = models.SlugField(unique=True, help_text="URL-friendly version of name")
    discipline = models.CharField(max_length=20, choices=DISCIPLINE_CHOICES, help_text="Primary discipline")
    tagline = models.CharField(max_length=200, blank=True, help_text="Department tagline or motto")
    
    # Visual Identity
    theme_color = models.CharField(max_length=20, choices=THEME_COLOR_CHOICES, default='blue', 
                                 help_text="Primary color theme for department pages")
    department_logo = models.ImageField(upload_to='departments/logos/', blank=True, null=True, 
                                      help_text="Department logo/emblem")
    department_image = models.ImageField(upload_to='departments/', blank=True, null=True, 
                                       help_text="Main department image")
    banner_image = models.ImageField(upload_to='departments/banners/', blank=True, null=True,
                                   help_text="Hero section banner image")
    
    # Content
    short_description = models.TextField(max_length=500, blank=True, help_text="Brief description for listings")
    description = CKEditor5Field(blank=True, help_text="Detailed department description")
    vision = models.TextField(blank=True, help_text="Department vision statement")
    mission = models.TextField(blank=True, help_text="Department mission statement")
    
    # Leadership
    head_of_department = models.CharField(max_length=200, blank=True, help_text="Name of HOD")
    hod_qualification = models.CharField(max_length=500, blank=True, help_text="HOD's qualifications")
    hod_designation = models.CharField(max_length=100, blank=True, help_text="HOD's designation")
    hod_message = models.TextField(blank=True, help_text="Message from HOD")
    hod_image = models.ImageField(upload_to='departments/hod/', blank=True, null=True)
    
    # Statistics
    established_year = models.PositiveIntegerField(blank=True, null=True, help_text="Year established")
    faculty_count = models.PositiveIntegerField(default=0, help_text="Number of faculty members")
    student_count = models.PositiveIntegerField(default=0, help_text="Current student enrollment")
    alumni_count = models.PositiveIntegerField(default=0, help_text="Total alumni count")
    
    # Academic Information
    programs_offered = models.TextField(blank=True, help_text="List programs, one per line")
    research_areas = models.TextField(blank=True, help_text="Research focus areas, one per line")
    laboratories = models.TextField(blank=True, help_text="Lab facilities, one per line")
    achievements = CKEditor5Field(blank=True, help_text="Department achievements and recognition")
    facilities = models.TextField(blank=True, help_text="Department facilities, one per line")
    
    # Contact Information
    office_location = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website_url = models.URLField(blank=True)
    
    # Documents
    brochure = models.FileField(upload_to='departments/documents/', blank=True, null=True,
                              help_text="Department brochure PDF")
    syllabus = models.FileField(upload_to='departments/documents/', blank=True, null=True,
                              help_text="Syllabus PDF")
    
    # Meta
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show in featured departments")
    ordering = models.PositiveIntegerField(default=0, help_text="Display order")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, help_text="SEO title")
    meta_description = models.TextField(max_length=300, blank=True, help_text="SEO description")
    meta_keywords = models.CharField(max_length=500, blank=True, help_text="SEO keywords, comma-separated")
    
    class Meta:
        ordering = ['ordering', 'name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:department_detail', kwargs={'slug': self.slug})
    
    def get_programs(self):
        """Get related programs for this department"""
        return Program.objects.filter(
            models.Q(name__icontains=self.name) | 
            models.Q(description__icontains=self.name)
        ).filter(is_active=True)[:5]
    
    def get_theme_colors(self):
        """Get CSS classes for department theme"""
        color_map = {
            'blue': {
                'primary': 'tw-bg-blue-600',
                'secondary': 'tw-bg-blue-100',
                'text': 'tw-text-blue-600',
                'border': 'tw-border-blue-500',
                'gradient': 'tw-from-blue-600 tw-to-blue-800'
            },
            'green': {
                'primary': 'tw-bg-green-600',
                'secondary': 'tw-bg-green-100',
                'text': 'tw-text-green-600',
                'border': 'tw-border-green-500',
                'gradient': 'tw-from-green-600 tw-to-green-800'
            },
            'red': {
                'primary': 'tw-bg-red-600',
                'secondary': 'tw-bg-red-100',
                'text': 'tw-text-red-600',
                'border': 'tw-border-red-500',
                'gradient': 'tw-from-red-600 tw-to-red-800'
            },
            'purple': {
                'primary': 'tw-bg-purple-600',
                'secondary': 'tw-bg-purple-100',
                'text': 'tw-text-purple-600',
                'border': 'tw-border-purple-500',
                'gradient': 'tw-from-purple-600 tw-to-purple-800'
            },
            'orange': {
                'primary': 'tw-bg-orange-600',
                'secondary': 'tw-bg-orange-100',
                'text': 'tw-text-orange-600',
                'border': 'tw-border-orange-500',
                'gradient': 'tw-from-orange-600 tw-to-orange-800'
            },
            'teal': {
                'primary': 'tw-bg-teal-600',
                'secondary': 'tw-bg-teal-100',
                'text': 'tw-text-teal-600',
                'border': 'tw-border-teal-500',
                'gradient': 'tw-from-teal-600 tw-to-teal-800'
            },
            'indigo': {
                'primary': 'tw-bg-indigo-600',
                'secondary': 'tw-bg-indigo-100',
                'text': 'tw-text-indigo-600',
                'border': 'tw-border-indigo-500',
                'gradient': 'tw-from-indigo-600 tw-to-indigo-800'
            },
            'pink': {
                'primary': 'tw-bg-pink-600',
                'secondary': 'tw-bg-pink-100',
                'text': 'tw-text-pink-600',
                'border': 'tw-border-pink-500',
                'gradient': 'tw-from-pink-600 tw-to-pink-800'
            },
            'yellow': {
                'primary': 'tw-bg-yellow-600',
                'secondary': 'tw-bg-yellow-100',
                'text': 'tw-text-yellow-600',
                'border': 'tw-border-yellow-500',
                'gradient': 'tw-from-yellow-600 tw-to-yellow-800'
            },
            'gray': {
                'primary': 'tw-bg-gray-600',
                'secondary': 'tw-bg-gray-100',
                'text': 'tw-text-gray-600',
                'border': 'tw-border-gray-500',
                'gradient': 'tw-from-gray-600 tw-to-gray-800'
            }
        }
        return color_map.get(self.theme_color, color_map['blue'])
    
    def get_faculty_members(self):
        """Get active faculty members for this department"""
        return self.faculty_members.filter(is_active=True).order_by('designation_order', 'name')
    
    def get_recent_events(self):
        """Get recent department events"""
        return self.department_events.filter(is_active=True).order_by('-event_date')[:5]


class Faculty(TimeStampedModel):
    """Faculty members in departments"""
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('visiting_faculty', 'Visiting Faculty'),
        ('emeritus', 'Professor Emeritus'),
        ('other', 'Other'),
    ]
    
    QUALIFICATION_CHOICES = [
        ('phd', 'Ph.D'),
        ('mphil', 'M.Phil'),
        ('masters', 'Masters'),
        ('bachelors', 'Bachelors'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, help_text="Full name of faculty member")
    slug = models.SlugField(unique=True, help_text="URL-friendly version of name")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty_members')
    
    # Professional Information
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    designation_order = models.PositiveIntegerField(default=0, help_text="Order for display (lower first)")
    employee_id = models.CharField(max_length=50, blank=True, help_text="Employee ID")
    
    # Qualifications
    highest_qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES, default='masters')
    qualifications = models.TextField(help_text="Detailed qualifications")
    specialization = models.CharField(max_length=200, blank=True, help_text="Area of specialization")
    
    # Experience
    experience_years = models.PositiveIntegerField(default=0, help_text="Years of experience")
    joining_date = models.DateField(blank=True, null=True, help_text="Date of joining institution")
    
    # Contact & Personal
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    office_location = models.CharField(max_length=200, blank=True)
    
    # Social Media & Academic Profiles
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    google_scholar_url = models.URLField(blank=True, help_text="Google Scholar profile URL")
    researchgate_url = models.URLField(blank=True, help_text="ResearchGate profile URL")
    orcid_id = models.CharField(max_length=50, blank=True, help_text="ORCID ID")
    scopus_id = models.CharField(max_length=50, blank=True, help_text="Scopus Author ID")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    facebook_url = models.URLField(blank=True, help_text="Facebook profile URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    website_url = models.URLField(blank=True, help_text="Personal website URL")
    
    # Academic Details
    research_interests = models.TextField(blank=True, help_text="Research interests, one per line")
    publications = CKEditor5Field(blank=True, help_text="Publications and research papers")
    courses_taught = models.TextField(blank=True, help_text="Courses taught, one per line")
    
    # Media
    photo = models.ImageField(upload_to='faculty/', blank=True, null=True, help_text="Faculty photo")
    cv_file = models.FileField(upload_to='faculty/cv/', blank=True, null=True, help_text="CV/Resume PDF")
    
    # Bio & Message
    bio = CKEditor5Field(blank=True, help_text="Faculty biography")
    message = models.TextField(blank=True, help_text="Message to students")
    
    # Meta
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show in featured faculty")
    show_on_website = models.BooleanField(default=True, help_text="Display on public website")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, help_text="SEO title")
    meta_description = models.TextField(max_length=300, blank=True, help_text="SEO description")
    
    class Meta:
        ordering = ['department', 'designation_order', 'name']
        verbose_name = 'Faculty Member'
        verbose_name_plural = 'Faculty Members'
        unique_together = ['department', 'slug']
    
    def __str__(self):
        return f"{self.name} - {self.get_designation_display()}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:faculty_detail', kwargs={
            'dept_slug': self.department.slug,
            'slug': self.slug
        })
    
    def get_research_interests_list(self):
        """Get research interests as a list"""
        if self.research_interests:
            return [interest.strip() for interest in self.research_interests.split('\n') if interest.strip()]
        return []
    
    def get_courses_taught_list(self):
        """Get courses taught as a list"""
        if self.courses_taught:
            return [course.strip() for course in self.courses_taught.split('\n') if course.strip()]
        return []
    
    def get_social_media_links(self):
        """Get all social media and academic profile links"""
        links = {}
        if self.linkedin_url:
            links['linkedin'] = self.linkedin_url
        if self.google_scholar_url:
            links['google_scholar'] = self.google_scholar_url
        if self.researchgate_url:
            links['researchgate'] = self.researchgate_url
        if self.orcid_id:
            links['orcid'] = f"https://orcid.org/{self.orcid_id}"
        if self.scopus_id:
            links['scopus'] = f"https://www.scopus.com/authid/detail.uri?authorId={self.scopus_id}"
        if self.twitter_url:
            links['twitter'] = self.twitter_url
        if self.facebook_url:
            links['facebook'] = self.facebook_url
        if self.instagram_url:
            links['instagram'] = self.instagram_url
        if self.website_url:
            links['website'] = self.website_url
        return links


class NonAcademicStaff(TimeStampedModel):
    """Non-academic staff members"""
    DESIGNATION_CHOICES = [
        ('registrar', 'Registrar'),
        ('deputy_registrar', 'Deputy Registrar'),
        ('assistant_registrar', 'Assistant Registrar'),
        ('accountant', 'Accountant'),
        ('librarian', 'Librarian'),
        ('assistant_librarian', 'Assistant Librarian'),
        ('lab_technician', 'Lab Technician'),
        ('computer_operator', 'Computer Operator'),
        ('clerk', 'Clerk'),
        ('peon', 'Peon'),
        ('security_guard', 'Security Guard'),
        ('cleaner', 'Cleaner'),
        ('driver', 'Driver'),
        ('cook', 'Cook'),
        ('other', 'Other'),
    ]
    
    QUALIFICATION_CHOICES = [
        ('phd', 'Ph.D'),
        ('mphil', 'M.Phil'),
        ('masters', 'Masters'),
        ('bachelors', 'Bachelors'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, help_text="Full name of staff member")
    slug = models.SlugField(unique=True, help_text="URL-friendly version of name")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='non_academic_staff')
    
    # Professional Information
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    designation_order = models.PositiveIntegerField(default=0, help_text="Order for display (lower first)")
    employee_id = models.CharField(max_length=50, blank=True, help_text="Employee ID")
    
    # Qualifications
    highest_qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES, default='bachelors')
    qualifications = models.TextField(help_text="Detailed qualifications")
    specialization = models.CharField(max_length=200, blank=True, help_text="Area of specialization")
    
    # Experience
    experience_years = models.PositiveIntegerField(default=0, help_text="Years of experience")
    joining_date = models.DateField(blank=True, null=True, help_text="Date of joining institution")
    
    # Contact & Personal
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    office_location = models.CharField(max_length=200, blank=True)
    
    # Social Media & Academic Profiles
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    google_scholar_url = models.URLField(blank=True, help_text="Google Scholar profile URL")
    researchgate_url = models.URLField(blank=True, help_text="ResearchGate profile URL")
    orcid_id = models.CharField(max_length=50, blank=True, help_text="ORCID ID")
    scopus_id = models.CharField(max_length=50, blank=True, help_text="Scopus Author ID")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    facebook_url = models.URLField(blank=True, help_text="Facebook profile URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    website_url = models.URLField(blank=True, help_text="Personal website URL")
    
    # Job Details
    job_description = models.TextField(blank=True, help_text="Job responsibilities and duties")
    skills = models.TextField(blank=True, help_text="Skills and competencies, one per line")
    
    # Media
    photo = models.ImageField(upload_to='staff/', blank=True, null=True, help_text="Staff photo")
    cv_file = models.FileField(upload_to='staff/cv/', blank=True, null=True, help_text="CV/Resume PDF")
    
    # Bio & Message
    bio = CKEditor5Field(blank=True, help_text="Staff biography")
    message = models.TextField(blank=True, help_text="Message to students/colleagues")
    
    # Meta
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show in featured staff")
    show_on_website = models.BooleanField(default=True, help_text="Display on public website")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, help_text="SEO title")
    meta_description = models.TextField(max_length=300, blank=True, help_text="SEO description")
    
    class Meta:
        ordering = ['department', 'designation_order', 'name']
        verbose_name = 'Non-Academic Staff Member'
        verbose_name_plural = 'Non-Academic Staff Members'
        unique_together = ['department', 'slug']
    
    def __str__(self):
        return f"{self.name} - {self.get_designation_display()}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:staff_detail', kwargs={
            'dept_slug': self.department.slug,
            'slug': self.slug
        })
    
    def get_skills_list(self):
        """Get skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split('\n') if skill.strip()]
        return []
    
    def get_social_media_links(self):
        """Get all social media and academic profile links"""
        links = {}
        if self.linkedin_url:
            links['linkedin'] = self.linkedin_url
        if self.google_scholar_url:
            links['google_scholar'] = self.google_scholar_url
        if self.researchgate_url:
            links['researchgate'] = self.researchgate_url
        if self.orcid_id:
            links['orcid'] = f"https://orcid.org/{self.orcid_id}"
        if self.scopus_id:
            links['scopus'] = f"https://www.scopus.com/authid/detail.uri?authorId={self.scopus_id}"
        if self.twitter_url:
            links['twitter'] = self.twitter_url
        if self.facebook_url:
            links['facebook'] = self.facebook_url
        if self.instagram_url:
            links['instagram'] = self.instagram_url
        if self.website_url:
            links['website'] = self.website_url
        return links


class DepartmentEvent(TimeStampedModel):
    """Events specific to departments"""
    EVENT_TYPE_CHOICES = [
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('conference', 'Conference'),
        ('guest_lecture', 'Guest Lecture'),
        ('research_presentation', 'Research Presentation'),
        ('cultural', 'Cultural Event'),
        ('sports', 'Sports Event'),
        ('achievement', 'Achievement/Award'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, help_text="Event title")
    slug = models.SlugField(help_text="URL-friendly version of title")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_events')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES, default='seminar')
    
    # Event Details
    description = CKEditor5Field(help_text="Detailed event description")
    short_description = models.TextField(max_length=300, blank=True, help_text="Brief description for listings")
    
    # Date & Time
    event_date = models.DateField(help_text="Event date")
    start_time = models.TimeField(blank=True, null=True, help_text="Event start time")
    end_time = models.TimeField(blank=True, null=True, help_text="Event end time")
    
    # Location
    venue = models.CharField(max_length=200, blank=True, help_text="Event venue")
    location_details = models.TextField(blank=True, help_text="Additional location information")
    
    # People
    organizer = models.CharField(max_length=200, blank=True, help_text="Event organizer")
    speaker = models.CharField(max_length=200, blank=True, help_text="Guest speaker/presenter")
    speaker_bio = models.TextField(blank=True, help_text="Speaker biography")
    
    # Media
    featured_image = models.ImageField(upload_to='events/departments/', blank=True, null=True)
    gallery_images = models.ManyToManyField('GalleryPhoto', blank=True, help_text="Event gallery images")
    
    # Registration
    registration_required = models.BooleanField(default=False)
    registration_link = models.URLField(blank=True, help_text="External registration link")
    max_participants = models.PositiveIntegerField(blank=True, null=True)
    
    # Meta
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show in featured events")
    show_on_homepage = models.BooleanField(default=False, help_text="Display on college homepage")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, help_text="SEO title")
    meta_description = models.TextField(max_length=300, blank=True, help_text="SEO description")
    
    class Meta:
        ordering = ['-event_date', '-created_at']
        verbose_name = 'Department Event'
        verbose_name_plural = 'Department Events'
        unique_together = ['department', 'slug']
    
    def __str__(self):
        return f"{self.title} - {self.department.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('college_website:department_event_detail', kwargs={
            'dept_slug': self.department.slug,
            'slug': self.slug
        })
    
    @property
    def is_upcoming(self):
        """Check if event is upcoming"""
        from django.utils import timezone
        return self.event_date >= timezone.now().date()
    
    @property
    def is_past(self):
        """Check if event is past"""
        return not self.is_upcoming
    
    def get_event_datetime(self):
        """Get combined datetime for the event"""
        if self.start_time:
            from datetime import datetime, time
            return datetime.combine(self.event_date, self.start_time)
        return self.event_date


class HeroBanner(models.Model):
    """Model for managing hero banner content and styling"""
    
    # Content Fields
    title = models.CharField(max_length=200, help_text="Main hero title")
    subtitle = models.TextField(help_text="Hero subtitle/description", blank=True)
    primary_button_text = models.CharField(max_length=50, help_text="Primary button text", blank=True)
    primary_button_url = models.URLField(help_text="Primary button link", blank=True)
    secondary_button_text = models.CharField(max_length=50, help_text="Secondary button text", blank=True)
    secondary_button_url = models.URLField(help_text="Secondary button link", blank=True)
    
    # Background Options
    background_type = models.CharField(
        max_length=20,
        choices=[
            ('gradient', 'Gradient'),
            ('solid', 'Solid Color'),
            ('image', 'Background Image'),
            ('video', 'Background Video'),
        ],
        default='gradient',
        help_text="Choose background type"
    )
    
    # Gradient Background
    gradient_start_color = ColorField(
        default='#1e3a8a',
        help_text="Gradient start color"
    )
    gradient_end_color = ColorField(
        default='#7c3aed',
        help_text="Gradient end color"
    )
    gradient_direction = models.CharField(
        max_length=20,
        choices=[
            ('to right', 'Horizontal'),
            ('to bottom', 'Vertical'),
            ('to bottom right', 'Diagonal'),
            ('135deg', 'Angled'),
        ],
        default='135deg',
        help_text="Gradient direction"
    )
    
    # Solid Background
    solid_background_color = ColorField(
        default='#1e3a8a',
        help_text="Solid background color"
    )
    
    # Background Image
    background_image = models.ImageField(
        upload_to='hero_banner/',
        blank=True,
        null=True,
        help_text="Background image (optional)"
    )
    background_image_opacity = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Background image opacity (0-100)"
    )
    
    # Background Video
    background_video_url = models.URLField(
        blank=True,
        help_text="Background video URL (YouTube/Vimeo)"
    )
    
    # Typography
    title_font_family = models.CharField(
        max_length=50,
        choices=[
            ('Inter', 'Inter'),
            ('Roboto', 'Roboto'),
            ('Open Sans', 'Open Sans'),
            ('Poppins', 'Poppins'),
            ('Montserrat', 'Montserrat'),
            ('Playfair Display', 'Playfair Display'),
        ],
        default='Inter',
        help_text="Title font family"
    )
    title_font_size = models.CharField(
        max_length=20,
        choices=[
            ('text-4xl', 'Small (36px)'),
            ('text-5xl', 'Medium (48px)'),
            ('text-6xl', 'Large (60px)'),
            ('text-7xl', 'Extra Large (72px)'),
            ('text-8xl', 'Huge (96px)'),
        ],
        default='text-6xl',
        help_text="Title font size"
    )
    title_font_weight = models.CharField(
        max_length=20,
        choices=[
            ('font-light', 'Light'),
            ('font-normal', 'Normal'),
            ('font-medium', 'Medium'),
            ('font-semibold', 'Semi Bold'),
            ('font-bold', 'Bold'),
            ('font-extrabold', 'Extra Bold'),
        ],
        default='font-bold',
        help_text="Title font weight"
    )
    
    subtitle_font_family = models.CharField(
        max_length=50,
        choices=[
            ('Inter', 'Inter'),
            ('Roboto', 'Roboto'),
            ('Open Sans', 'Open Sans'),
            ('Poppins', 'Poppins'),
            ('Montserrat', 'Montserrat'),
            ('Playfair Display', 'Playfair Display'),
        ],
        default='Inter',
        help_text="Subtitle font family"
    )
    subtitle_font_size = models.CharField(
        max_length=20,
        choices=[
            ('text-lg', 'Small (18px)'),
            ('text-xl', 'Medium (20px)'),
            ('text-2xl', 'Large (24px)'),
            ('text-3xl', 'Extra Large (30px)'),
        ],
        default='text-xl',
        help_text="Subtitle font size"
    )
    
    # Colors
    title_color = ColorField(default='#ffffff', help_text="Title text color")
    subtitle_color = ColorField(default='#e5e7eb', help_text="Subtitle text color")
    
    # Two-color title support
    title_highlight_text = models.CharField(
        max_length=100,
        blank=True,
        help_text="Text to highlight with different color (e.g., '18+ Courses')"
    )
    title_highlight_color = ColorField(
        default='#fbbf24',
        help_text="Color for highlighted title text (hex code)"
    )
    
    primary_button_bg_color = ColorField(default='#dc2626', help_text="Primary button background color")
    primary_button_text_color = ColorField(default='#ffffff', help_text="Primary button text color")
    secondary_button_bg_color = ColorField(default='transparent', help_text="Secondary button background color")
    secondary_button_text_color = ColorField(default='#ffffff', help_text="Secondary button text color")
    secondary_button_border_color = ColorField(default='#ffffff', help_text="Secondary button border color")
    
    # Layout & Spacing
    padding_top = models.CharField(
        max_length=20,
        choices=[
            ('py-8', 'Small (32px)'),
            ('py-12', 'Medium (48px)'),
            ('py-16', 'Large (64px)'),
            ('py-20', 'Extra Large (80px)'),
            ('py-24', 'Huge (96px)'),
        ],
        default='py-16',
        help_text="Vertical padding"
    )
    
    content_alignment = models.CharField(
        max_length=20,
        choices=[
            ('text-left', 'Left'),
            ('text-center', 'Center'),
            ('text-right', 'Right'),
        ],
        default='text-center',
        help_text="Content alignment"
    )
    
    # Animation
    enable_animations = models.BooleanField(default=True, help_text="Enable entrance animations")
    animation_duration = models.CharField(
        max_length=20,
        choices=[
            ('duration-500', 'Fast (0.5s)'),
            ('duration-700', 'Medium (0.7s)'),
            ('duration-1000', 'Slow (1s)'),
        ],
        default='duration-700',
        help_text="Animation duration"
    )
    
    # Statistics Cards Customization
    show_statistics = models.BooleanField(default=True, help_text="Show statistics cards")
    stat_1_icon = models.CharField(
        max_length=50,
        default='fas fa-calendar-alt',
        help_text="Icon class for first stat (e.g., fas fa-calendar-alt)"
    )
    stat_1_number = models.CharField(
        max_length=20,
        default='25+',
        help_text="First statistic number"
    )
    stat_1_label = models.CharField(
        max_length=50,
        default='Years Experience',
        help_text="First statistic label"
    )
    stat_1_color = ColorField(
        default='#2563eb',
        help_text="First stat card color"
    )
    
    stat_2_icon = models.CharField(
        max_length=50,
        default='fas fa-users',
        help_text="Icon class for second stat (e.g., fas fa-calendar-alt)"
    )
    stat_2_number = models.CharField(
        max_length=20,
        default='8000+',
        help_text="Second statistic number"
    )
    stat_2_label = models.CharField(
        max_length=50,
        default='Students',
        help_text="Second statistic label"
    )
    stat_2_color = ColorField(
        default='#7c3aed',
        help_text="Second stat card color"
    )
    
    stat_3_icon = models.CharField(
        max_length=50,
        default='fas fa-book-open',
        help_text="Icon class for third stat (e.g., fas fa-calendar-alt)"
    )
    stat_3_number = models.CharField(
        max_length=20,
        default='18+',
        help_text="Third statistic number"
    )
    stat_3_label = models.CharField(
        max_length=50,
        default='Courses',
        help_text="Third statistic label"
    )
    stat_3_color = ColorField(
        default='#2563eb',
        help_text="Third stat card color"
    )
    
    stat_4_icon = models.CharField(
        max_length=50,
        default='fas fa-lock',
        help_text="Icon class for fourth stat (e.g., fas fa-calendar-alt)"
    )
    stat_4_number = models.CharField(
        max_length=50,
        default='95%',
        help_text="Fourth statistic number"
    )
    stat_4_label = models.CharField(
        max_length=50,
        default='Placement',
        help_text="Fourth statistic label"
    )
    stat_4_color = ColorField(
        default='#7c3aed',
        help_text="Fourth stat card color"
    )
    
    # Accreditations Customization
    show_accreditations = models.BooleanField(default=True, help_text="Show accreditation badges")
    accred_1_text = models.CharField(
        max_length=100,
        default='UGC Recognized',
        help_text="First accreditation text"
    )
    accred_1_icon = models.CharField(
        max_length=50,
        default='fas fa-star',
        help_text="Icon for first accreditation"
    )
    accred_1_color = ColorField(
        default='#2563eb',
        help_text="First accreditation color"
    )
    
    accred_2_text = models.CharField(
        max_length=100,
        default='NAAC Grade A',
        help_text="Second accreditation text"
    )
    accred_2_icon = models.CharField(
        max_length=50,
        default='fas fa-star',
        help_text="Icon for second accreditation"
    )
    accred_2_color = ColorField(
        default='#7c3aed',
        help_text="Second accreditation color"
    )
    
    accred_3_text = models.CharField(
        max_length=100,
        default='3 Star IIC Rating',
        help_text="Third accreditation text"
    )
    accred_3_icon = models.CharField(
        max_length=50,
        default='fas fa-map-marker-alt',
        help_text="Icon for third accreditation"
    )
    accred_3_color = ColorField(
        default='#2563eb',
        help_text="Third accreditation color"
    )
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Enable this hero banner")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hero Banner"
        verbose_name_plural = "Hero Banners"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"Hero Banner: {self.title}"
    
    def get_background_style(self):
        """Generate CSS background style based on background type"""
        if self.background_type == 'gradient':
            return f"background: linear-gradient({self.gradient_direction}, {self.gradient_start_color}, {self.gradient_end_color})"
        elif self.background_type == 'solid':
            return f"background-color: {self.solid_background_color}"
        elif self.background_type == 'image' and self.background_image:
            opacity = self.background_image_opacity / 100
            return f"background-image: url('{self.background_image.url}'); background-size: cover; background-position: center;"
        return ""
    
    def get_title_classes(self):
        """Generate Tailwind classes for title"""
        return f"{self.title_font_family} {self.title_font_size} {self.title_font_weight}"
    
    def get_subtitle_classes(self):
        """Generate Tailwind classes for subtitle"""
        return f"{self.subtitle_font_family} {self.subtitle_font_size}"
    
    def render_title(self):
        """Render title with highlight support"""
        if self.title_highlight_text and self.title_highlight_text in self.title:
            # Split title around highlight text
            parts = self.title.split(self.title_highlight_text)
            if len(parts) == 2:
                return f'{parts[0]}<span style="color: {self.title_highlight_color};">{self.title_highlight_text}</span>{parts[1]}'
            elif len(parts) > 2:
                # Handle multiple occurrences
                return self.title.replace(
                    self.title_highlight_text, 
                    f'<span style="color: {self.title_highlight_color};">{self.title_highlight_text}</span>'
                )
        return self.title


class ExamTimetable(TimeStampedModel):
    """Exam Timetable configuration model"""
    name = models.CharField(max_length=200, help_text="Name for this timetable (e.g., 'Semester 1 2024')")
    academic_year = models.CharField(max_length=20, help_text="Academic year (e.g., '2024-2025')")
    semester = models.CharField(max_length=20, help_text="Semester (e.g., '1st', '2nd', '3rd', '4th')")
    
    # Header customization
    header_title = models.CharField(max_length=200, default="Exam Timetable", help_text="Main header title")
    header_subtitle = models.CharField(max_length=300, default="View and manage examination schedules efficiently", help_text="Header subtitle")
    header_gradient_start = ColorField(default="#3b82f6", help_text="Header gradient start color")
    header_gradient_end = ColorField(default="#4f46e5", help_text="Header gradient end color")
    
    # Guidelines and timing information
    exam_guidelines = models.TextField(blank=True, help_text="Exam guidelines and rules")
    morning_session_start = models.TimeField(default="09:00", help_text="Morning session start time")
    morning_session_end = models.TimeField(default="12:00", help_text="Morning session end time")
    afternoon_session_start = models.TimeField(default="14:00", help_text="Afternoon session start time")
    afternoon_session_end = models.TimeField(default="17:00", help_text="Afternoon session end time")
    break_duration = models.CharField(max_length=50, default="2 hours", help_text="Break duration description")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Enable this timetable")
    is_featured = models.BooleanField(default=False, help_text="Mark as featured timetable")
    
    class Meta:
        verbose_name = "Exam Timetable"
        verbose_name_plural = "Exam Timetables"
        ordering = ['-academic_year', 'semester', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.academic_year}"
    
    def get_active_weeks(self):
        """Get all active weeks for this timetable"""
        return self.weeks.filter(is_active=True).order_by('week_number')
    
    def get_week_count(self):
        """Get total number of weeks"""
        return self.weeks.filter(is_active=True).count()


class ExamTimetableWeek(TimeStampedModel):
    """Individual week configuration for exam timetable"""
    timetable = models.ForeignKey(ExamTimetable, on_delete=models.CASCADE, related_name='weeks')
    week_number = models.PositiveIntegerField(help_text="Week number (1, 2, 3, 4)")
    week_title = models.CharField(max_length=100, default="", help_text="Custom week title (optional)")
    is_active = models.BooleanField(default=True, help_text="Enable this week")
    
    class Meta:
        verbose_name = "Exam Timetable Week"
        verbose_name_plural = "Exam Timetable Weeks"
        ordering = ['week_number']
        unique_together = ['timetable', 'week_number']
    
    def __str__(self):
        return f"Week {self.week_number} - {self.timetable.name}"
    
    def get_week_display_name(self):
        """Get display name for the week"""
        if self.week_title:
            return self.week_title
        return f"Week {self.week_number}"
    
    def get_active_time_slots(self):
        """Get all active time slots for this week"""
        return self.time_slots.filter(is_active=True).order_by('start_time')


class ExamTimetableTimeSlot(TimeStampedModel):
    """Time slot configuration for exam timetable"""
    week = models.ForeignKey(ExamTimetableWeek, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.TimeField(help_text="Start time for this slot")
    end_time = models.TimeField(help_text="End time for this slot")
    is_active = models.BooleanField(default=True, help_text="Enable this time slot")
    
    class Meta:
        verbose_name = "Exam Timetable Time Slot"
        verbose_name_plural = "Exam Timetable Time Slots"
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.start_time} - {self.end_time} (Week {self.week.week_number})"
    
    def get_time_display(self):
        """Get formatted time display"""
        return f"{self.start_time.strftime('%I:%M %p')}"
    
    def get_active_exams(self):
        """Get all active exams for this time slot"""
        return self.exams.filter(is_active=True).order_by('day_of_week')


class ExamTimetableExam(TimeStampedModel):
    """Individual exam configuration for timetable"""
    time_slot = models.ForeignKey(ExamTimetableTimeSlot, on_delete=models.CASCADE, related_name='exams')
    
    # Day and subject information
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    day_of_week = models.CharField(max_length=20, choices=DAY_CHOICES, help_text="Day of the week")
    
    subject_name = models.CharField(max_length=200, help_text="Subject name")
    room_number = models.CharField(max_length=50, help_text="Room number or lab name")
    duration = models.CharField(max_length=50, help_text="Exam duration (e.g., '2 hours', '3 hours')")
    semester = models.CharField(max_length=20, help_text="Semester (e.g., '1st', '2nd', '3rd', '4th')")
    
    # Priority and status
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('important', 'Important'),
        ('general', 'General'),
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='general', help_text="Exam priority")
    is_featured = models.BooleanField(default=False, help_text="Mark as featured exam")
    
    # Visual customization
    background_color = ColorField(default="#f3f4f6", help_text="Background color for exam slot")
    border_color = ColorField(default="#3b82f6", help_text="Left border color")
    text_color = ColorField(default="#1f2937", help_text="Text color")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Enable this exam")
    
    class Meta:
        verbose_name = "Exam Timetable Exam"
        verbose_name_plural = "Exam Timetable Exams"
        ordering = ['day_of_week', 'time_slot__start_time']
        unique_together = ['time_slot', 'day_of_week']
    
    def __str__(self):
        return f"{self.subject_name} - {self.get_day_of_week_display()} ({self.time_slot.get_time_display()})"
    
    def get_priority_badge_class(self):
        """Get Bootstrap badge class based on priority"""
        priority_classes = {
            'urgent': 'bg-danger',
            'important': 'bg-warning',
            'general': 'bg-info',
        }
        return priority_classes.get(self.priority, 'bg-info')
    
    def get_priority_icon(self):
        """Get Font Awesome icon based on priority"""
        priority_icons = {
            'urgent': 'fas fa-exclamation-triangle',
            'important': 'fas fa-exclamation-circle',
            'general': 'fas fa-info-circle',
        }
        return priority_icons.get(self.priority, 'fas fa-info-circle')


# Menu Management Models
class MenuCategory(TimeStampedModel):
    """Main menu categories (Home, About, Academics, etc.)"""
    name = models.CharField(max_length=100, unique=True, help_text="Menu category name (e.g., 'Home', 'About', 'Academics')")
    slug = models.SlugField(max_length=100, unique=True, help_text="URL-friendly identifier")
    icon_class = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class (e.g., 'fas fa-home')")
    order = models.PositiveIntegerField(default=0, help_text="Display order in navigation")
    is_active = models.BooleanField(default=True, help_text="Show this menu category")
    is_featured = models.BooleanField(default=False, help_text="Mark as featured menu")
    
    # Visual customization
    text_color = ColorField(default="#374151", help_text="Text color for the menu")
    hover_color = ColorField(default="#1f2937", help_text="Hover color for the menu")
    
    class Meta:
        verbose_name = "Menu Category"
        verbose_name_plural = "Menu Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Hidden'})"
    
    def get_active_submenus(self):
        """Get all active submenus for this category"""
        return self.submenus.filter(is_active=True).order_by('order')
    
    def get_submenu_count(self):
        """Get total number of submenus"""
        return self.submenus.count()


class MenuSubmenu(TimeStampedModel):
    """Submenu items within each category"""
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='submenus')
    name = models.CharField(max_length=100, help_text="Submenu item name")
    url = models.CharField(max_length=200, help_text="URL or path (e.g., '/about/', '{% url \"about\" %}')")
    icon_class = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    order = models.PositiveIntegerField(default=0, help_text="Display order within category")
    is_active = models.BooleanField(default=True, help_text="Show this submenu item")
    is_featured = models.BooleanField(default=False, help_text="Mark as featured submenu")
    
    # Grouping and styling
    group_header = models.CharField(max_length=100, blank=True, help_text="Group header text (e.g., 'Institution', 'Leadership')")
    show_divider = models.BooleanField(default=False, help_text="Show divider after this item")
    
    # Visual customization
    text_color = ColorField(default="#6b7280", help_text="Text color for the submenu")
    hover_color = ColorField(default="#374151", help_text="Hover color for the submenu")
    
    class Meta:
        verbose_name = "Menu Submenu"
        verbose_name_plural = "Menu Submenus"
        ordering = ['category__order', 'category__name', 'order', 'name']
        unique_together = ['category', 'name']
    
    def __str__(self):
        return f"{self.category.name} → {self.name} ({'Active' if self.is_active else 'Hidden'})"
    
    def get_full_url(self):
        """Get the full URL, handling both static and dynamic URLs"""
        if self.url.startswith('{%') or self.url.startswith('{{'):
            # This is a Django template tag, return as is
            return self.url
        elif self.url.startswith('/'):
            # This is a relative URL, return as is
            return self.url
        else:
            # This might be a named URL, try to resolve it
            return self.url


class MenuVisibilitySettings(TimeStampedModel):
    """Global menu visibility settings"""
    name = models.CharField(max_length=100, default="Default Menu Settings", help_text="Settings configuration name")
    is_active = models.BooleanField(default=True, help_text="Use these settings")
    
    # Main Menu Controls
    show_research_menu = models.BooleanField(default=True, help_text="Show Research menu")
    show_placement_menu = models.BooleanField(default=True, help_text="Show Placement menu")
    show_alumni_menu = models.BooleanField(default=True, help_text="Show Alumni menu")
    show_events_menu = models.BooleanField(default=True, help_text="Show Events menu")
    show_student_portal = models.BooleanField(default=True, help_text="Show Student Portal")
    
    # Academics Section Controls
    show_academics_programs = models.BooleanField(default=True, help_text="Show Academic Programs")
    show_academics_departments = models.BooleanField(default=True, help_text="Show Academic Departments")
    show_academics_library = models.BooleanField(default=True, help_text="Show Library")
    show_academics_calendar = models.BooleanField(default=True, help_text="Show Academic Calendar")
    
    # Admissions Section Controls
    show_admissions_process = models.BooleanField(default=True, help_text="Show Admission Process")
    show_admissions_guidelines = models.BooleanField(default=True, help_text="Show Admission Guidelines")
    show_admissions_eligibility = models.BooleanField(default=True, help_text="Show Admission Eligibility")
    show_admissions_courses = models.BooleanField(default=True, help_text="Show Courses Offered")
    show_admissions_application = models.BooleanField(default=True, help_text="Show Online Application")
    show_admissions_fees = models.BooleanField(default=True, help_text="Show Fee Structure")
    show_admissions_prospectus = models.BooleanField(default=True, help_text="Show Prospectus")
    show_admissions_scholarships = models.BooleanField(default=True, help_text="Show Scholarships")
    
    # Examination Section Controls
    show_exam_notices = models.BooleanField(default=True, help_text="Show Exam Notices")
    show_exam_timetable = models.BooleanField(default=True, help_text="Show Exam Timetable")
    show_exam_revaluation = models.BooleanField(default=True, help_text="Show Exam Revaluation")
    show_exam_question_papers = models.BooleanField(default=True, help_text="Show Question Papers")
    show_exam_results = models.BooleanField(default=True, help_text="Show Exam Results")
    show_exam_rules = models.BooleanField(default=True, help_text="Show Exam Rules")
    
    # Research Section Controls
    show_research_centers = models.BooleanField(default=True, help_text="Show Research Centers")
    show_research_innovation = models.BooleanField(default=True, help_text="Show Innovation & Incubation")
    show_publications = models.BooleanField(default=True, help_text="Show Publications")
    show_patents_projects = models.BooleanField(default=True, help_text="Show Patents & Projects")
    show_research_collaborations = models.BooleanField(default=True, help_text="Show Collaborations & MOUs")
    show_research_consultancy = models.BooleanField(default=True, help_text="Show Consultancy")
    
    # Student Support Section Controls
    show_student_portal_main = models.BooleanField(default=True, help_text="Show Student Portal Main")
    show_student_library = models.BooleanField(default=True, help_text="Show Student Library")
    show_sports_cultural = models.BooleanField(default=True, help_text="Show Sports & Cultural")
    show_nss_ncc = models.BooleanField(default=True, help_text="Show NSS, NCC & Clubs")
    
    # Events Section Controls
    show_news_announcements = models.BooleanField(default=True, help_text="Show News & Announcements")
    show_academic_events = models.BooleanField(default=True, help_text="Show Academic Events")
    show_extracurricular_events = models.BooleanField(default=True, help_text="Show Extracurricular Events")
    show_gallery = models.BooleanField(default=True, help_text="Show Gallery")
    show_annual_reports = models.BooleanField(default=True, help_text="Show Annual Reports")
    
    # Core Navigation Controls (Always visible but can be controlled)
    show_about_section = models.BooleanField(default=True, help_text="Show About section")
    show_contact_section = models.BooleanField(default=True, help_text="Show Contact section")
    show_notices_section = models.BooleanField(default=True, help_text="Show Notices section")
    
    class Meta:
        verbose_name = "Menu Visibility Settings"
        verbose_name_plural = "Menu Visibility Settings"
    
    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"
    
    def get_active_settings(self):
        """Get the currently active settings"""
        return MenuVisibilitySettings.objects.filter(is_active=True).first()
    
    @classmethod
    def get_current_settings(cls):
        """Get current active settings or create default ones"""
        settings = cls.objects.filter(is_active=True).first()
        if not settings:
            settings = cls.objects.create(
                name="Default Settings",
                is_active=True
            )
        return settings
    
    def get_visible_menu_count(self):
        """Get count of visible menu items"""
        visible_fields = [
            'show_research_menu', 'show_placement_menu', 'show_alumni_menu', 'show_events_menu',
            'show_student_portal', 'show_academics_programs', 'show_academics_departments',
            'show_academics_library', 'show_academics_calendar', 'show_admissions_process',
            'show_admissions_guidelines', 'show_admissions_eligibility', 'show_admissions_courses',
            'show_admissions_application', 'show_admissions_fees', 'show_admissions_prospectus',
            'show_admissions_scholarships', 'show_exam_notices', 'show_exam_timetable',
            'show_exam_revaluation', 'show_exam_question_papers', 'show_exam_results',
            'show_exam_rules', 'show_research_centers', 'show_research_innovation',
            'show_publications', 'show_patents_projects', 'show_research_collaborations',
            'show_research_consultancy', 'show_student_portal_main', 'show_student_library',
            'show_sports_cultural', 'show_nss_ncc', 'show_news_announcements',
            'show_academic_events', 'show_extracurricular_events', 'show_gallery',
            'show_annual_reports', 'show_about_section', 'show_contact_section',
            'show_notices_section'
        ]
        return sum(getattr(self, field) for field in visible_fields)
    
    def get_total_menu_count(self):
        """Get total count of menu items"""
        return 42  # Total number of menu items


class QuestionPaper(TimeStampedModel):
    """Question Papers for different subjects and semesters"""
    
    SEMESTER_CHOICES = [
        ('1', '1st Semester'),
        ('2', '2nd Semester'),
        ('3', '3rd Semester'),
        ('4', '4th Semester'),
        ('5', '5th Semester'),
        ('6', '6th Semester'),
    ]
    
    SUBJECT_CHOICES = [
        ('mathematics', 'Mathematics'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('computer-science', 'Computer Science'),
        ('english', 'English'),
        ('economics', 'Economics'),
        ('business-studies', 'Business Studies'),
        ('accountancy', 'Accountancy'),
        ('statistics', 'Statistics'),
        ('biology', 'Biology'),
        ('history', 'History'),
        ('political-science', 'Political Science'),
        ('sociology', 'Sociology'),
        ('psychology', 'Psychology'),
        ('geography', 'Geography'),
        ('other', 'Other'),
    ]
    
    DEGREE_CHOICES = [
        ('bsc', 'B.Sc'),
        ('bcom', 'B.Com'),
        ('ba', 'B.A'),
        ('bca', 'BCA'),
        ('bba', 'BBA'),
        ('msc', 'M.Sc'),
        ('mcom', 'M.Com'),
        ('ma', 'M.A'),
        ('mca', 'MCA'),
        ('mba', 'MBA'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, help_text="Question paper title (e.g., Mathematics - 1st Semester)")
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, help_text="Subject name")
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, help_text="Semester")
    degree_type = models.CharField(max_length=20, choices=DEGREE_CHOICES, help_text="Degree type")
    academic_year = models.CharField(max_length=20, help_text="Academic year (e.g., 2024-2025)")
    
    # File Information
    question_paper_file = models.FileField(upload_to='question_papers/', help_text="Upload question paper PDF")
    file_size = models.CharField(max_length=20, blank=True, help_text="File size (auto-calculated)")
    
    # Additional Information
    description = models.TextField(blank=True, help_text="Brief description of the question paper")
    exam_date = models.DateField(blank=True, null=True, help_text="Date when the exam was conducted")
    duration = models.CharField(max_length=50, blank=True, help_text="Exam duration (e.g., 3 hours)")
    total_marks = models.PositiveIntegerField(blank=True, null=True, help_text="Total marks for the exam")
    
    # Status and Visibility
    is_active = models.BooleanField(default=True, help_text="Make this question paper visible to students")
    is_featured = models.BooleanField(default=False, help_text="Mark as featured question paper")
    download_count = models.PositiveIntegerField(default=0, help_text="Number of times downloaded")
    
    # SEO and URL
    slug = models.SlugField(unique=True, blank=True, help_text="URL-friendly version of title")
    
    class Meta:
        ordering = ['-academic_year', 'semester', 'subject', 'title']
        verbose_name = "Question Paper"
        verbose_name_plural = "Question Papers"
        unique_together = ['subject', 'semester', 'degree_type', 'academic_year']
    
    def __str__(self):
        return f"{self.title} - {self.academic_year}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.subject}-{self.semester}-{self.degree_type}-{self.academic_year}")
        
        # Auto-calculate file size if file is uploaded
        if self.question_paper_file and not self.file_size:
            try:
                size_bytes = self.question_paper_file.size
                if size_bytes < 1024:
                    self.file_size = f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    self.file_size = f"{size_bytes / 1024:.1f} KB"
                else:
                    self.file_size = f"{size_bytes / (1024 * 1024):.1f} MB"
            except:
                self.file_size = "Unknown"
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Get absolute URL for question paper detail view"""
        return reverse('college_website:question_paper_detail', kwargs={'slug': self.slug})
    
    def increment_download_count(self):
        """Increment download count"""
        self.download_count += 1
        self.save(update_fields=['download_count'])
    
    def get_subject_display_color(self):
        """Get color class for subject display"""
        color_map = {
            'mathematics': 'primary',
            'physics': 'info',
            'chemistry': 'warning',
            'computer-science': 'success',
            'english': 'danger',
            'economics': 'secondary',
            'business-studies': 'dark',
            'accountancy': 'primary',
            'statistics': 'info',
            'biology': 'success',
            'history': 'warning',
            'political-science': 'danger',
            'sociology': 'secondary',
            'psychology': 'dark',
            'geography': 'primary',
            'other': 'light',
        }
        return color_map.get(self.subject, 'primary')
    
    @classmethod
    def get_available_subjects(cls):
        """Get list of subjects that have question papers"""
        return cls.objects.filter(is_active=True).values_list('subject', flat=True).distinct()
    
    @classmethod
    def get_available_semesters(cls):
        """Get list of semesters that have question papers"""
        return cls.objects.filter(is_active=True).values_list('semester', flat=True).distinct()
    
    @classmethod
    def get_available_years(cls):
        """Get list of academic years that have question papers"""
        return cls.objects.filter(is_active=True).values_list('academic_year', flat=True).distinct().order_by('-academic_year')


class RevaluationInfo(TimeStampedModel):
    """Revaluation information and content management"""
    
    # Basic Information
    title = models.CharField(max_length=200, default="Revaluation", help_text="Page title")
    subtitle = models.CharField(max_length=300, default="Apply for revaluation of your examination papers", help_text="Page subtitle")
    
    # Process Steps
    step1_title = models.CharField(max_length=100, default="Download Form", help_text="Step 1 title")
    step1_description = models.TextField(default="Download the revaluation application form from the college website or collect it from the examination office.", help_text="Step 1 description")
    
    step2_title = models.CharField(max_length=100, default="Fill Application", help_text="Step 2 title")
    step2_description = models.TextField(default="Complete the application form with all required details including subject codes and paper details.", help_text="Step 2 description")
    
    step3_title = models.CharField(max_length=100, default="Pay Fees", help_text="Step 3 title")
    step3_description = models.TextField(default="Pay the prescribed revaluation fees at the college office or through online payment methods.", help_text="Step 3 description")
    
    step4_title = models.CharField(max_length=100, default="Submit Application", help_text="Step 4 title")
    step4_description = models.TextField(default="Submit the completed form along with fee receipt to the examination office within the specified deadline.", help_text="Step 4 description")
    
    # Fee Information
    theory_paper_fee = models.DecimalField(max_digits=8, decimal_places=2, default=500.00, help_text="Fee for theory papers")
    practical_paper_fee = models.DecimalField(max_digits=8, decimal_places=2, default=750.00, help_text="Fee for practical papers")
    project_fee = models.DecimalField(max_digits=8, decimal_places=2, default=1000.00, help_text="Fee for project reports")
    
    # Important Dates
    application_period = models.CharField(max_length=100, default="15 days from result declaration", help_text="Application period")
    processing_time = models.CharField(max_length=100, default="30-45 days", help_text="Processing time")
    result_notification = models.CharField(max_length=100, default="Via SMS/Email", help_text="Result notification method")
    
    # Eligibility Rules
    eligibility_rules = CKEditor5Field(default="<ul><li>Students who have appeared for the examination</li><li>Application must be submitted within 15 days of result declaration</li><li>All dues must be cleared before applying</li><li>Valid student ID and hall ticket required</li></ul>", help_text="Eligibility rules")
    
    # Required Documents
    required_documents = CKEditor5Field(default="<ul><li>Completed revaluation application form</li><li>Fee payment receipt</li><li>Student ID card copy</li><li>Hall ticket copy</li></ul>", help_text="Required documents")
    
    # Contact Information
    controller_name = models.CharField(max_length=100, default="Dr. [Name]", help_text="Examination controller name")
    controller_phone = models.CharField(max_length=20, default="+91-XXX-XXXX-XXX", help_text="Controller phone number")
    controller_email = models.EmailField(default="exam@college.edu", help_text="Controller email")
    controller_office_hours = models.CharField(max_length=100, default="9:00 AM - 5:00 PM", help_text="Controller office hours")
    
    office_location = models.CharField(max_length=200, default="Ground Floor, Main Building", help_text="Examination office location")
    office_phone = models.CharField(max_length=20, default="+91-XXX-XXXX-XXX", help_text="Office phone number")
    office_email = models.EmailField(default="examoffice@college.edu", help_text="Office email")
    office_working_days = models.CharField(max_length=100, default="Monday to Friday", help_text="Office working days")
    
    # Download Forms
    application_form_file = models.FileField(upload_to='revaluation/forms/', blank=True, null=True, help_text="Revaluation application form PDF")
    guidelines_file = models.FileField(upload_to='revaluation/forms/', blank=True, null=True, help_text="Revaluation guidelines PDF")
    fee_structure_file = models.FileField(upload_to='revaluation/forms/', blank=True, null=True, help_text="Fee structure PDF")
    
    # Important Notice
    important_notice = models.TextField(default="Revaluation results are final and binding. Students are advised to carefully consider before applying for revaluation. The college reserves the right to reject applications that do not meet the eligibility criteria or are submitted after the deadline.", help_text="Important notice text")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Make this revaluation information visible")
    
    class Meta:
        verbose_name = "Revaluation Information"
        verbose_name_plural = "Revaluation Information"
    
    def __str__(self):
        return f"Revaluation Information - {self.title}"
    
    def get_active_info(cls):
        """Get the currently active revaluation information"""
        return cls.objects.filter(is_active=True).first()
    
    def get_fee_display(self, fee_type):
        """Get formatted fee display"""
        if fee_type == 'theory':
            return f"₹{self.theory_paper_fee} per paper"
        elif fee_type == 'practical':
            return f"₹{self.practical_paper_fee} per paper"
        elif fee_type == 'project':
            return f"₹{self.project_fee} per project"
        return "₹0"


class ExamRulesInfo(TimeStampedModel):
    """Exam Rules and Regulations information management"""
    
    # Basic Information
    title = models.CharField(max_length=200, default="Examination Rules & Regulations", help_text="Page title")
    subtitle = models.CharField(max_length=300, default="Important guidelines and rules for all examinations", help_text="Page subtitle")
    
    # General Rules - Timing & Attendance
    timing_rules = CKEditor5Field(default="<ul><li>Students must arrive 15 minutes before exam time</li><li>Late entry is not permitted after 30 minutes</li><li>Hall ticket and ID card are mandatory</li><li>No student can leave within first 30 minutes</li></ul>", help_text="Timing and attendance rules")
    
    # Prohibited Items
    prohibited_items = CKEditor5Field(default="<ul><li>Mobile phones and electronic devices</li><li>Calculators (unless specified)</li><li>Study materials and notes</li><li>Food and beverages</li></ul>", help_text="List of prohibited items")
    
    # Examination Conduct Rules
    conduct_rules = CKEditor5Field(default="<ul><li>Complete silence must be maintained throughout the examination</li><li>No talking or communication with other students</li><li>Any form of cheating will result in immediate disqualification</li><li>For any queries, students must raise their hand</li></ul>", help_text="Examination conduct rules")
    
    # Answer Sheet Guidelines
    answer_sheet_details = CKEditor5Field(default="<ul><li>Write roll number clearly on answer sheet</li><li>Use only blue or black ink pen</li><li>Do not write in margins or outside boxes</li><li>Number answers correctly</li></ul>", help_text="Answer sheet guidelines")
    
    submission_rules = CKEditor5Field(default="<ul><li>Submit answer sheet 5 minutes before time</li><li>Raise hand when ready to submit</li><li>No additional sheets after submission</li><li>Leave immediately after submission</li></ul>", help_text="Submission rules")
    
    # Disciplinary Actions
    violations_penalties = CKEditor5Field(default="<ul><li><strong>Cheating:</strong> Immediate disqualification</li><li><strong>Mobile Phone:</strong> Confiscation and penalty</li><li><strong>Late Entry:</strong> No entry after 30 minutes</li><li><strong>Misbehavior:</strong> Disciplinary action</li></ul>", help_text="Violations and penalties")
    
    appeal_process = CKEditor5Field(default="<ul><li>Submit written appeal within 7 days</li><li>Contact examination controller</li><li>Appeal hearing within 15 days</li><li>Final decision by principal</li></ul>", help_text="Appeal process")
    
    # Special Instructions
    calculator_rules = models.TextField(default="Only non-programmable calculators are allowed for specific subjects. Check with invigilator before use.", help_text="Calculator usage rules")
    open_book_rules = models.TextField(default="For open book examinations, only specified materials are allowed. No additional notes or materials.", help_text="Open book exam rules")
    time_extension_rules = models.TextField(default="No time extensions are granted except in case of technical issues or emergencies with proper documentation.", help_text="Time extension rules")
    
    # Contact Information (can be shared with revaluation)
    controller_name = models.CharField(max_length=100, default="Dr. [Name]", help_text="Examination controller name")
    controller_phone = models.CharField(max_length=20, default="+91-XXX-XXXX-XXX", help_text="Controller phone number")
    controller_email = models.EmailField(default="exam@college.edu", help_text="Controller email")
    controller_office_hours = models.CharField(max_length=100, default="9:00 AM - 5:00 PM", help_text="Controller office hours")
    
    office_location = models.CharField(max_length=200, default="Ground Floor, Main Building", help_text="Examination office location")
    office_phone = models.CharField(max_length=20, default="+91-XXX-XXXX-XXX", help_text="Office phone number")
    office_email = models.EmailField(default="examoffice@college.edu", help_text="Office email")
    office_working_days = models.CharField(max_length=100, default="Monday to Friday", help_text="Office working days")
    
    # Important Notice
    important_notice = models.TextField(default="All students are required to strictly follow these examination rules and regulations. Violation of any rule will result in appropriate disciplinary action as per college policy. For any clarifications, contact the examination office well in advance.", help_text="Important notice text")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Make this exam rules information visible")
    
    class Meta:
        verbose_name = "Exam Rules Information"
        verbose_name_plural = "Exam Rules Information"
    
    def __str__(self):
        return f"Exam Rules Information - {self.title}"
    
    @classmethod
    def get_active_info(cls):
        """Get the currently active exam rules information"""
        return cls.objects.filter(is_active=True).first()


class ResearchCenterInfo(TimeStampedModel):
    """Research Centers information and content management"""
    
    # Basic Information
    title = models.CharField(max_length=200, default="Research Centers", help_text="Page title")
    subtitle = models.CharField(max_length=300, default="Advancing knowledge through cutting-edge research and innovation", help_text="Page subtitle")
    
    # Research Centers
    center1_name = models.CharField(max_length=200, default="Center for Advanced Sciences", help_text="First research center name")
    center1_description = models.TextField(default="Dedicated to fundamental research in physics, chemistry, and mathematics with state-of-the-art laboratories and equipment.", help_text="First center description")
    center1_areas = CKEditor5Field(default="<ul><li>Quantum Physics Research</li><li>Materials Science</li><li>Computational Chemistry</li></ul>", help_text="First center research areas")
    
    center2_name = models.CharField(max_length=200, default="Computer Science Research Lab", help_text="Second research center name")
    center2_description = models.TextField(default="Focusing on artificial intelligence, machine learning, and software engineering with cutting-edge computing resources.", help_text="Second center description")
    center2_areas = CKEditor5Field(default="<ul><li>AI & Machine Learning</li><li>Data Science</li><li>Cybersecurity</li></ul>", help_text="Second center research areas")
    
    center3_name = models.CharField(max_length=200, default="Environmental Research Center", help_text="Third research center name")
    center3_description = models.TextField(default="Committed to environmental sustainability and climate change research with modern analytical facilities.", help_text="Third center description")
    center3_areas = CKEditor5Field(default="<ul><li>Climate Change Studies</li><li>Biodiversity Research</li><li>Renewable Energy</li></ul>", help_text="Third center research areas")
    
    # Research Facilities
    lab_infrastructure = CKEditor5Field(default="<ul><li>Advanced Analytical Instruments</li><li>High-Performance Computing Cluster</li><li>Clean Room Facilities</li><li>Specialized Research Equipment</li></ul>", help_text="Laboratory infrastructure details")
    research_support = CKEditor5Field(default="<ul><li>Expert Faculty Mentorship</li><li>Research Grant Assistance</li><li>Publication Support</li><li>Conference Presentation Funding</li></ul>", help_text="Research support services")
    
    # Research Areas
    physics_description = models.TextField(default="Quantum mechanics, solid state physics, and theoretical physics research.", help_text="Physics research area description")
    biology_description = models.TextField(default="Molecular biology, genetics, and biotechnology research.", help_text="Biology research area description")
    mathematics_description = models.TextField(default="Applied mathematics, statistics, and mathematical modeling.", help_text="Mathematics research area description")
    social_sciences_description = models.TextField(default="Sociology, psychology, and interdisciplinary social research.", help_text="Social sciences research area description")
    
    # Research Achievements
    publications_count = models.PositiveIntegerField(default=150, help_text="Number of research papers published")
    patents_count = models.PositiveIntegerField(default=25, help_text="Number of patents filed")
    conferences_count = models.PositiveIntegerField(default=50, help_text="Number of conference presentations")
    book_chapters_count = models.PositiveIntegerField(default=10, help_text="Number of book chapters")
    
    grants_amount = models.DecimalField(max_digits=10, decimal_places=2, default=25000000.00, help_text="Total research grants in INR")
    industry_collaborations = models.PositiveIntegerField(default=15, help_text="Number of industry collaborations")
    international_partnerships = models.PositiveIntegerField(default=8, help_text="Number of international partnerships")
    national_awards = models.PositiveIntegerField(default=5, help_text="Number of national awards")
    
    # Research Opportunities
    student_opportunities = CKEditor5Field(default="<ul><li>Undergraduate Research Projects</li><li>Summer Research Internships</li><li>Thesis Research Support</li><li>Research Publication Opportunities</li></ul>", help_text="Research opportunities for students")
    faculty_opportunities = CKEditor5Field(default="<ul><li>Research Grant Applications</li><li>Collaborative Research Projects</li><li>International Exchange Programs</li><li>Research Equipment Access</li></ul>", help_text="Research opportunities for faculty")
    
    # Contact Information
    director_name = models.CharField(max_length=100, default="Dr. [Research Director Name]", help_text="Research director name")
    director_phone = models.CharField(max_length=20, default="+91-XXX-XXXX-XXX", help_text="Director phone number")
    director_email = models.EmailField(default="research@college.edu", help_text="Director email")
    director_office_hours = models.CharField(max_length=100, default="9:00 AM - 5:00 PM", help_text="Director office hours")
    
    office_location = models.CharField(max_length=200, default="Research Block, 2nd Floor", help_text="Research office location")
    office_phone = models.CharField(max_length=20, default="+91-XXX-XXXX-XXX", help_text="Office phone number")
    office_email = models.EmailField(default="research.office@college.edu", help_text="Office email")
    office_working_days = models.CharField(max_length=100, default="Monday to Friday", help_text="Office working days")
    
    # Call to Action
    cta_title = models.CharField(max_length=200, default="Join Our Research Community", help_text="Call to action title")
    cta_description = models.TextField(default="Interested in contributing to cutting-edge research? Contact our research office to learn about available opportunities for students and faculty members. Together, we can advance knowledge and make meaningful contributions to society.", help_text="Call to action description")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Make this research center information visible")
    
    class Meta:
        verbose_name = "Research Center Information"
        verbose_name_plural = "Research Center Information"
    
    def __str__(self):
        return f"Research Center Information - {self.title}"
    
    @classmethod
    def get_active_info(cls):
        """Get the currently active research center information"""
        return cls.objects.filter(is_active=True).first()
    
    def get_grants_display(self):
        """Get formatted grants amount display"""
        if self.grants_amount >= 10000000:  # 1 crore
            return f"₹{self.grants_amount / 10000000:.1f} Crore"
        elif self.grants_amount >= 100000:  # 1 lakh
            return f"₹{self.grants_amount / 100000:.1f} Lakh"
        else:
            return f"₹{self.grants_amount:,.0f}"


class PublicationInfo(TimeStampedModel):
    """Publications information and content management"""
    
    # Basic Information
    title = models.CharField(max_length=200, default="Research Publications", help_text="Page title")
    subtitle = models.CharField(max_length=300, default="Explore our extensive collection of research publications, academic papers, and scholarly works that contribute to the advancement of knowledge across various disciplines.", help_text="Page subtitle")
    
    # Statistics
    total_publications = models.PositiveIntegerField(default=150, help_text="Total number of research papers")
    book_chapters = models.PositiveIntegerField(default=25, help_text="Number of book chapters")
    total_citations = models.PositiveIntegerField(default=500, help_text="Total number of citations")
    awards_received = models.PositiveIntegerField(default=15, help_text="Number of awards received")
    
    # Journal Categories
    international_journals_count = models.PositiveIntegerField(default=85, help_text="Number of international journal papers")
    international_citations = models.PositiveIntegerField(default=350, help_text="International journal citations")
    national_journals_count = models.PositiveIntegerField(default=45, help_text="Number of national journal papers")
    national_citations = models.PositiveIntegerField(default=120, help_text="National journal citations")
    conference_papers_count = models.PositiveIntegerField(default=20, help_text="Number of conference papers")
    conference_citations = models.PositiveIntegerField(default=30, help_text="Conference paper citations")
    
    # Research Impact
    best_paper_awards = models.PositiveIntegerField(default=15, help_text="Number of best paper awards")
    average_impact_factor = models.DecimalField(max_digits=4, decimal_places=2, default=3.20, help_text="Average impact factor")
    international_collaborations = models.PositiveIntegerField(default=25, help_text="Number of international collaborations")
    research_students = models.PositiveIntegerField(default=50, help_text="Number of research students")
    
    # Call to Action
    cta_title = models.CharField(max_length=200, default="Interested in Collaborating?", help_text="Call to action title")
    cta_description = models.TextField(default="Join our research community and contribute to cutting-edge research. We welcome collaborations with researchers, institutions, and industry partners worldwide.", help_text="Call to action description")
    contact_email = models.EmailField(default="research@college.edu", help_text="Research contact email")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Make this publication information visible")
    
    class Meta:
        verbose_name = "Publication Information"
        verbose_name_plural = "Publication Information"
    
    def __str__(self):
        return f"Publication Information - {self.title}"
    
    @classmethod
    def get_active_info(cls):
        """Get the currently active publication information"""
        return cls.objects.filter(is_active=True).first()
    
    def get_impact_factor_display(self):
        """Get formatted impact factor display"""
        return f"{self.average_impact_factor:.2f}"


class Publication(TimeStampedModel):
    """Individual publication records"""
    
    DEPARTMENT_CHOICES = [
        ('computer-science', 'Computer Science'),
        ('mathematics', 'Mathematics'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('biology', 'Biology'),
        ('commerce', 'Commerce'),
        ('management', 'Management'),
    ]
    
    JOURNAL_TYPE_CHOICES = [
        ('international', 'International Journal'),
        ('national', 'National Journal'),
        ('conference', 'Conference Proceedings'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=500, help_text="Publication title")
    authors = models.CharField(max_length=1000, help_text="Author names (comma separated)")
    abstract = models.TextField(help_text="Publication abstract")
    
    # Publication Details
    journal_name = models.CharField(max_length=300, help_text="Journal or conference name")
    journal_type = models.CharField(max_length=20, choices=JOURNAL_TYPE_CHOICES, default='international', help_text="Type of publication")
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, help_text="Department")
    publication_year = models.PositiveIntegerField(help_text="Year of publication")
    
    # Metrics
    citations = models.PositiveIntegerField(default=0, help_text="Number of citations")
    impact_factor = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Journal impact factor")
    
    # Links and Files
    doi = models.CharField(max_length=200, blank=True, help_text="Digital Object Identifier")
    url = models.URLField(blank=True, help_text="Publication URL")
    pdf_file = models.FileField(upload_to='publications/', blank=True, help_text="PDF file")
    
    # Status
    is_featured = models.BooleanField(default=False, help_text="Feature this publication")
    is_active = models.BooleanField(default=True, help_text="Make this publication visible")
    
    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ['-publication_year', '-citations']
    
    def __str__(self):
        return f"{self.title[:50]}... ({self.publication_year})"
    
    def get_authors_list(self):
        """Get list of authors"""
        return [author.strip() for author in self.authors.split(',')]
    
    def get_department_display_color(self):
        """Get color class for department badge"""
        colors = {
            'computer-science': 'primary',
            'mathematics': 'success',
            'physics': 'info',
            'chemistry': 'warning',
            'biology': 'danger',
            'commerce': 'secondary',
            'management': 'dark',
        }
        return colors.get(self.department, 'secondary')


class PatentsProjectsInfo(TimeStampedModel):
    """Patents & Projects information and content management"""
    
    # Basic Information
    title = models.CharField(max_length=200, default="Patents & Projects", help_text="Page title")
    subtitle = models.CharField(max_length=300, default="Explore our innovative research projects and intellectual property achievements that drive technological advancement and contribute to society.", help_text="Page subtitle")
    
    # Statistics
    total_patents = models.PositiveIntegerField(default=25, help_text="Total number of patents")
    total_projects = models.PositiveIntegerField(default=50, help_text="Total number of research projects")
    industry_collaborations = models.PositiveIntegerField(default=15, help_text="Number of industry collaborations")
    research_funding = models.DecimalField(max_digits=10, decimal_places=2, default=25000000.00, help_text="Total research funding in INR")
    
    # Research Impact
    innovation_awards = models.PositiveIntegerField(default=15, help_text="Number of innovation awards")
    international_recognition = models.PositiveIntegerField(default=25, help_text="Number of countries with recognition")
    active_partnerships = models.PositiveIntegerField(default=15, help_text="Number of active partnerships")
    students_involved = models.PositiveIntegerField(default=100, help_text="Number of students involved")
    
    # Call to Action
    cta_title = models.CharField(max_length=200, default="Interested in Collaborating?", help_text="Call to action title")
    cta_description = models.TextField(default="Join our innovation ecosystem and contribute to cutting-edge research. We welcome collaborations with researchers, institutions, and industry partners worldwide.", help_text="Call to action description")
    contact_email = models.EmailField(default="research@college.edu", help_text="Research contact email")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Make this patents & projects information visible")
    
    class Meta:
        verbose_name = "Patents & Projects Information"
        verbose_name_plural = "Patents & Projects Information"
    
    def __str__(self):
        return f"Patents & Projects Information - {self.title}"
    
    @classmethod
    def get_active_info(cls):
        """Get the currently active patents & projects information"""
        return cls.objects.filter(is_active=True).first()
    
    def get_funding_display(self):
        """Get formatted funding amount display"""
        if self.research_funding >= 10000000:  # 1 crore
            return f"₹{self.research_funding / 10000000:.1f}Cr"
        elif self.research_funding >= 100000:  # 1 lakh
            return f"₹{self.research_funding / 100000:.1f}L"
        else:
            return f"₹{self.research_funding:,.0f}"


class Patent(TimeStampedModel):
    """Individual patent records"""
    
    STATUS_CHOICES = [
        ('granted', 'Granted'),
        ('pending', 'Pending'),
        ('filed', 'Filed'),
        ('published', 'Published'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('computer-science', 'Computer Science'),
        ('mathematics', 'Mathematics'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('biology', 'Biology'),
        ('commerce', 'Commerce'),
        ('management', 'Management'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=500, help_text="Patent title")
    inventors = models.CharField(max_length=1000, help_text="Inventor names (comma separated)")
    description = models.TextField(help_text="Patent description")
    
    # Patent Details
    patent_number = models.CharField(max_length=100, help_text="Patent number")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', help_text="Patent status")
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, help_text="Department")
    filing_year = models.PositiveIntegerField(help_text="Year of filing")
    
    # Additional Information
    application_number = models.CharField(max_length=100, blank=True, help_text="Application number")
    publication_date = models.DateField(null=True, blank=True, help_text="Publication date")
    grant_date = models.DateField(null=True, blank=True, help_text="Grant date")
    
    # Links and Files
    patent_url = models.URLField(blank=True, help_text="Patent URL")
    pdf_file = models.FileField(upload_to='patents/', blank=True, help_text="Patent PDF file")
    
    # Status
    is_featured = models.BooleanField(default=False, help_text="Feature this patent")
    is_active = models.BooleanField(default=True, help_text="Make this patent visible")
    
    class Meta:
        verbose_name = "Patent"
        verbose_name_plural = "Patents"
        ordering = ['-filing_year', '-created_at']
    
    def __str__(self):
        return f"{self.title[:50]}... ({self.filing_year})"
    
    def get_inventors_list(self):
        """Get list of inventors"""
        return [inventor.strip() for inventor in self.inventors.split(',')]
    
    def get_department_display_color(self):
        """Get color class for department badge"""
        colors = {
            'computer-science': 'primary',
            'mathematics': 'success',
            'physics': 'info',
            'chemistry': 'warning',
            'biology': 'danger',
            'commerce': 'secondary',
            'management': 'dark',
        }
        return colors.get(self.department, 'secondary')


class ResearchProject(TimeStampedModel):
    """Individual research project records"""
    
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('planned', 'Planned'),
        ('suspended', 'Suspended'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('computer-science', 'Computer Science'),
        ('mathematics', 'Mathematics'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('biology', 'Biology'),
        ('commerce', 'Commerce'),
        ('management', 'Management'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=500, help_text="Project title")
    principal_investigator = models.CharField(max_length=200, help_text="Principal investigator name")
    description = models.TextField(help_text="Project description")
    
    # Project Details
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, help_text="Department")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing', help_text="Project status")
    start_year = models.PositiveIntegerField(help_text="Start year")
    end_year = models.PositiveIntegerField(null=True, blank=True, help_text="End year")
    
    # Funding Information
    funding_agency = models.CharField(max_length=200, help_text="Funding agency")
    funding_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Funding amount in INR")
    
    # Additional Information
    project_duration = models.CharField(max_length=100, blank=True, help_text="Project duration")
    team_members = models.TextField(blank=True, help_text="Team members")
    
    # Links and Files
    project_url = models.URLField(blank=True, help_text="Project URL")
    report_file = models.FileField(upload_to='projects/', blank=True, help_text="Project report file")
    
    # Status
    is_featured = models.BooleanField(default=False, help_text="Feature this project")
    is_active = models.BooleanField(default=True, help_text="Make this project visible")
    
    class Meta:
        verbose_name = "Research Project"
        verbose_name_plural = "Research Projects"
        ordering = ['-start_year', '-created_at']
    
    def __str__(self):
        return f"{self.title[:50]}... ({self.start_year})"
    
    def get_department_display_color(self):
        """Get color class for department badge"""
        colors = {
            'computer-science': 'primary',
            'mathematics': 'success',
            'physics': 'info',
            'chemistry': 'warning',
            'biology': 'danger',
            'commerce': 'secondary',
            'management': 'dark',
        }
        return colors.get(self.department, 'secondary')
    
    def get_funding_display(self):
        """Get formatted funding amount display"""
        if self.funding_amount >= 10000000:  # 1 crore
            return f"₹{self.funding_amount / 10000000:.1f}Cr"
        elif self.funding_amount >= 100000:  # 1 lakh
            return f"₹{self.funding_amount / 100000:.1f}L"
        else:
            return f"₹{self.funding_amount:,.0f}"


class IndustryCollaboration(TimeStampedModel):
    """Industry collaboration records"""
    
    # Basic Information
    company_name = models.CharField(max_length=200, help_text="Company name")
    description = models.TextField(help_text="Collaboration description")
    
    # Collaboration Details
    collaboration_type = models.CharField(max_length=100, help_text="Type of collaboration")
    duration_years = models.PositiveIntegerField(help_text="Duration in years")
    funding_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Funding amount in INR")
    
    # Additional Information
    contact_person = models.CharField(max_length=200, blank=True, help_text="Contact person")
    company_website = models.URLField(blank=True, help_text="Company website")
    
    # Status
    is_featured = models.BooleanField(default=False, help_text="Feature this collaboration")
    is_active = models.BooleanField(default=True, help_text="Make this collaboration visible")
    
    class Meta:
        verbose_name = "Industry Collaboration"
        verbose_name_plural = "Industry Collaborations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.collaboration_type}"
    
    def get_funding_display(self):
        """Get formatted funding amount display"""
        if self.funding_amount >= 10000000:  # 1 crore
            return f"₹{self.funding_amount / 10000000:.1f}Cr"
        elif self.funding_amount >= 100000:  # 1 lakh
            return f"₹{self.funding_amount / 100000:.1f}L"
        else:
            return f"₹{self.funding_amount:,.0f}"


class ConsultancyInfo(TimeStampedModel):
    """Consultancy information and content management"""
    
    # Basic Information
    title = models.CharField(max_length=200, default="Consultancy Services", help_text="Page title")
    subtitle = models.CharField(max_length=300, default="Leveraging our academic expertise and research capabilities to provide innovative solutions for industry challenges. Our consultancy services bridge the gap between academia and industry.", help_text="Page subtitle")
    
    # Statistics
    total_projects = models.PositiveIntegerField(default=150, help_text="Total number of projects completed")
    industry_partners = models.PositiveIntegerField(default=50, help_text="Number of industry partners")
    revenue_generated = models.DecimalField(max_digits=10, decimal_places=2, default=25000000.00, help_text="Total revenue generated in INR")
    client_satisfaction = models.PositiveIntegerField(default=95, help_text="Client satisfaction percentage")
    
    # Call to Action
    cta_title = models.CharField(max_length=200, default="Ready to Transform Your Business?", help_text="Call to action title")
    cta_description = models.TextField(default="Partner with us to leverage cutting-edge research and academic expertise for your business challenges. Let's work together to achieve your goals.", help_text="Call to action description")
    contact_email = models.EmailField(default="consultancy@college.edu", help_text="Consultancy contact email")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Make this consultancy information visible")
    
    class Meta:
        verbose_name = "Consultancy Information"
        verbose_name_plural = "Consultancy Information"
    
    def __str__(self):
        return f"Consultancy Information - {self.title}"
    
    @classmethod
    def get_active_info(cls):
        """Get the currently active consultancy information"""
        return cls.objects.filter(is_active=True).first()
    
    def get_revenue_display(self):
        """Get formatted revenue amount display"""
        if self.revenue_generated >= 10000000:  # 1 crore
            return f"₹{self.revenue_generated / 10000000:.1f}Cr"
        elif self.revenue_generated >= 100000:  # 1 lakh
            return f"₹{self.revenue_generated / 100000:.1f}L"
        else:
            return f"₹{self.revenue_generated:,.0f}"


class ConsultancyService(TimeStampedModel):
    """Individual consultancy service records"""
    
    SERVICE_TYPE_CHOICES = [
        ('technology', 'Technology Consulting'),
        ('business', 'Business Analytics'),
        ('research', 'Research & Development'),
        ('training', 'Training & Development'),
        ('environmental', 'Environmental Consulting'),
        ('quality', 'Quality Assurance'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, help_text="Service title")
    description = models.TextField(help_text="Service description")
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, help_text="Type of service")
    
    # Service Details
    features = models.TextField(help_text="Service features (one per line)")
    icon_class = models.CharField(max_length=50, default="fas fa-cog", help_text="FontAwesome icon class")
    color_class = models.CharField(max_length=20, default="primary", help_text="Bootstrap color class")
    
    # Status
    is_featured = models.BooleanField(default=False, help_text="Feature this service")
    is_active = models.BooleanField(default=True, help_text="Make this service visible")
    display_order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    
    class Meta:
        verbose_name = "Consultancy Service"
        verbose_name_plural = "Consultancy Services"
        ordering = ['display_order', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"
    
    def get_features_list(self):
        """Get list of features"""
        return [feature.strip() for feature in self.features.split('\n') if feature.strip()]


class ConsultancyExpertise(TimeStampedModel):
    """Consultancy expertise areas"""
    
    # Basic Information
    title = models.CharField(max_length=100, help_text="Expertise area title")
    description = models.TextField(help_text="Expertise description")
    icon_class = models.CharField(max_length=50, default="fas fa-cog", help_text="FontAwesome icon class")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Make this expertise visible")
    display_order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    
    class Meta:
        verbose_name = "Consultancy Expertise"
        verbose_name_plural = "Consultancy Expertise Areas"
        ordering = ['display_order', 'title']
    
    def __str__(self):
        return self.title


class ConsultancySuccessStory(TimeStampedModel):
    """Consultancy success stories"""
    
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('research', 'Research'),
        ('training', 'Training'),
        ('business', 'Business'),
        ('environmental', 'Environmental'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, help_text="Success story title")
    description = models.TextField(help_text="Success story description")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, help_text="Story category")
    
    # Metrics
    metric1_label = models.CharField(max_length=50, help_text="First metric label")
    metric1_value = models.CharField(max_length=20, help_text="First metric value")
    metric2_label = models.CharField(max_length=50, help_text="Second metric label")
    metric2_value = models.CharField(max_length=20, help_text="Second metric value")
    metric3_label = models.CharField(max_length=50, help_text="Third metric label")
    metric3_value = models.CharField(max_length=20, help_text="Third metric value")
    
    # Status
    is_featured = models.BooleanField(default=False, help_text="Feature this success story")
    is_active = models.BooleanField(default=True, help_text="Make this success story visible")
    display_order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    
    class Meta:
        verbose_name = "Consultancy Success Story"
        verbose_name_plural = "Consultancy Success Stories"
        ordering = ['display_order', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"
    
    def get_category_color(self):
        """Get color class for category badge"""
        colors = {
            'technology': 'success',
            'research': 'info',
            'training': 'warning',
            'business': 'primary',
            'environmental': 'success',
        }
        return colors.get(self.category, 'secondary')


# NSS-NCC Clubs Models
class NSSNCCClub(TimeStampedModel):
    """NSS-NCC Clubs main content model"""
    
    CLUB_TYPE_CHOICES = [
        ('nss', 'NSS (National Service Scheme)'),
        ('ncc', 'NCC (National Cadet Corps)'),
        ('sports', 'Sports Club'),
        ('cultural', 'Cultural Club'),
        ('tech', 'Technology Club'),
        ('literary', 'Literary Club'),
        ('environmental', 'Environmental Club'),
        ('music', 'Music Club'),
        ('dance', 'Dance Club'),
        ('drama', 'Drama Club'),
        ('photography', 'Photography Club'),
        ('debate', 'Debate Club'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, help_text="Club/Organization name")
    club_type = models.CharField(max_length=20, choices=CLUB_TYPE_CHOICES, help_text="Type of club/organization")
    description = CKEditor5Field(config_name='default', help_text="Detailed description of the club")
    short_description = models.TextField(max_length=500, help_text="Brief description for cards")
    
    # Contact Information
    coordinator_name = models.CharField(max_length=100, help_text="Club coordinator name")
    coordinator_email = models.EmailField(help_text="Coordinator email")
    coordinator_phone = models.CharField(max_length=15, blank=True, help_text="Coordinator phone")
    
    # Activities and Events
    main_activities = CKEditor5Field(config_name='default', help_text="Main activities and programs")
    upcoming_events = CKEditor5Field(config_name='default', blank=True, help_text="Upcoming events and activities")
    
    # Media
    logo = models.ImageField(upload_to='nss_ncc_clubs/logos/', blank=True, null=True, help_text="Club logo")
    cover_image = models.ImageField(upload_to='nss_ncc_clubs/covers/', blank=True, null=True, help_text="Cover image")
    
    # Status and Display
    is_active = models.BooleanField(default=True, help_text="Make this club visible")
    is_featured = models.BooleanField(default=False, help_text="Feature this club prominently")
    display_order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    
    # Social Media
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram page URL")
    website_url = models.URLField(blank=True, help_text="Official website URL")
    
    class Meta:
        verbose_name = "NSS-NCC Club"
        verbose_name_plural = "NSS-NCC Clubs"
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_club_type_display()})"
    
    def get_club_type_color(self):
        """Get Bootstrap color class for club type"""
        colors = {
            'nss': 'success',
            'ncc': 'primary',
            'sports': 'warning',
            'cultural': 'info',
            'tech': 'secondary',
            'literary': 'dark',
            'environmental': 'success',
            'music': 'danger',
            'dance': 'info',
            'drama': 'warning',
            'photography': 'secondary',
            'debate': 'primary',
            'other': 'light',
        }
        return colors.get(self.club_type, 'secondary')


class NSSNCCNotice(TimeStampedModel):
    """Notices and announcements for NSS-NCC Clubs"""
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('event', 'Event'),
        ('recruitment', 'Recruitment'),
        ('achievement', 'Achievement'),
        ('meeting', 'Meeting'),
        ('camp', 'Camp'),
        ('competition', 'Competition'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, help_text="Notice title")
    content = CKEditor5Field(config_name='default', help_text="Notice content")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general', help_text="Notice category")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal', help_text="Notice priority")
    
    # Related Club
    related_club = models.ForeignKey(NSSNCCClub, on_delete=models.CASCADE, related_name='notices', help_text="Related club")
    
    # Dates
    publish_date = models.DateTimeField(default=timezone.now, help_text="When to publish this notice")
    expiry_date = models.DateTimeField(blank=True, null=True, help_text="When this notice expires (optional)")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Make this notice visible")
    is_featured = models.BooleanField(default=False, help_text="Feature this notice prominently")
    
    # Media
    attachment = models.FileField(upload_to='nss_ncc_clubs/notices/', blank=True, null=True, help_text="Notice attachment")
    
    class Meta:
        verbose_name = "NSS-NCC Notice"
        verbose_name_plural = "NSS-NCC Notices"
        ordering = ['-publish_date', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.related_club.name}"
    
    def get_priority_color(self):
        """Get Bootstrap color class for priority"""
        colors = {
            'low': 'secondary',
            'normal': 'primary',
            'high': 'warning',
            'urgent': 'danger',
        }
        return colors.get(self.priority, 'primary')
    
    def get_category_color(self):
        """Get Bootstrap color class for category"""
        colors = {
            'general': 'primary',
            'event': 'success',
            'recruitment': 'info',
            'achievement': 'warning',
            'meeting': 'secondary',
            'camp': 'dark',
            'competition': 'danger',
            'other': 'light',
        }
        return colors.get(self.category, 'primary')
    
    def is_expired(self):
        """Check if notice has expired"""
        if self.expiry_date:
            return timezone.now() > self.expiry_date
        return False


class NSSNCCGallery(TimeStampedModel):
    """Photo gallery for NSS-NCC Clubs"""
    
    CATEGORY_CHOICES = [
        ('events', 'Events'),
        ('activities', 'Activities'),
        ('camps', 'Camps'),
        ('competitions', 'Competitions'),
        ('meetings', 'Meetings'),
        ('achievements', 'Achievements'),
        ('general', 'General'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, help_text="Image title")
    description = models.TextField(blank=True, help_text="Image description")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general', help_text="Image category")
    
    # Related Club
    related_club = models.ForeignKey(NSSNCCClub, on_delete=models.CASCADE, related_name='gallery_images', help_text="Related club")
    
    # Image
    image = models.ImageField(upload_to='nss_ncc_clubs/gallery/', help_text="Gallery image")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Make this image visible")
    is_featured = models.BooleanField(default=False, help_text="Feature this image prominently")
    display_order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    
    class Meta:
        verbose_name = "NSS-NCC Gallery Image"
        verbose_name_plural = "NSS-NCC Gallery Images"
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.related_club.name}"
    
    def get_category_color(self):
        """Get Bootstrap color class for category"""
        colors = {
            'events': 'primary',
            'activities': 'success',
            'camps': 'info',
            'competitions': 'warning',
            'meetings': 'secondary',
            'achievements': 'danger',
            'general': 'light',
        }
        return colors.get(self.category, 'light')


class NSSNCCAchievement(TimeStampedModel):
    """Achievements and awards for NSS-NCC Clubs"""
    
    ACHIEVEMENT_TYPE_CHOICES = [
        ('award', 'Award'),
        ('recognition', 'Recognition'),
        ('certificate', 'Certificate'),
        ('trophy', 'Trophy'),
        ('medal', 'Medal'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, help_text="Achievement title")
    description = models.TextField(help_text="Achievement description")
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPE_CHOICES, default='award', help_text="Type of achievement")
    
    # Related Club
    related_club = models.ForeignKey(NSSNCCClub, on_delete=models.CASCADE, related_name='achievements', help_text="Related club")
    
    # Achievement Details
    achieved_by = models.CharField(max_length=200, help_text="Who achieved this (individual/team)")
    achievement_date = models.DateField(help_text="Date of achievement")
    organization = models.CharField(max_length=200, help_text="Organization that gave the achievement")
    
    # Media
    certificate_image = models.ImageField(upload_to='nss_ncc_clubs/achievements/', blank=True, null=True, help_text="Certificate or award image")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Make this achievement visible")
    is_featured = models.BooleanField(default=False, help_text="Feature this achievement prominently")
    display_order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    
    class Meta:
        verbose_name = "NSS-NCC Achievement"
        verbose_name_plural = "NSS-NCC Achievements"
        ordering = ['-achievement_date', 'display_order']
    
    def __str__(self):
        return f"{self.title} - {self.related_club.name}"
    
    def get_achievement_type_color(self):
        """Get Bootstrap color class for achievement type"""
        colors = {
            'award': 'warning',
            'recognition': 'info',
            'certificate': 'success',
            'trophy': 'primary',
            'medal': 'danger',
            'other': 'secondary',
        }
        return colors.get(self.achievement_type, 'secondary')


class HeroCarouselSlide(TimeStampedModel):
    """Model for managing hero carousel slides with dynamic content"""
    
    SLIDE_TYPES = [
        ('welcome', 'Welcome & Programs'),
        ('admissions', 'Admissions'),
        ('research', 'Research & Innovation'),
        ('student_life', 'Student Life'),
        ('custom', 'Custom'),
    ]
    
    GRADIENT_CHOICES = [
        ('blue-purple', 'Blue to Purple'),
        ('green-teal', 'Green to Teal'),
        ('purple-pink', 'Purple to Pink'),
        ('orange-red', 'Orange to Red'),
        ('custom', 'Custom Gradient'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, help_text="Main heading of the slide")
    subtitle = models.TextField(help_text="Subtitle/description text")
    slide_type = models.CharField(max_length=20, choices=SLIDE_TYPES, default='welcome')
    is_active = models.BooleanField(default=True, help_text="Whether this slide is active")
    display_order = models.PositiveIntegerField(default=0, help_text="Order of display (0 = first)")
    
    # Badge Information
    badge_text = models.CharField(max_length=100, blank=True, help_text="Badge text (e.g., 'Welcome to Excellence')")
    badge_icon = models.CharField(max_length=50, default='fas fa-star', help_text="FontAwesome icon class for badge")
    badge_color = ColorField(default='#FFD700', help_text="Badge background color")
    
    # Button Configuration
    primary_button_text = models.CharField(max_length=100, blank=True, help_text="Primary button text")
    primary_button_url = models.URLField(blank=True, help_text="Primary button URL")
    primary_button_color = ColorField(default='#FFC107', help_text="Primary button color")
    primary_button_icon = models.CharField(max_length=50, default='fas fa-arrow-right', help_text="Primary button icon")
    
    secondary_button_text = models.CharField(max_length=100, blank=True, help_text="Secondary button text")
    secondary_button_url = models.URLField(blank=True, help_text="Secondary button URL")
    secondary_button_color = ColorField(default='#FFFFFF', help_text="Secondary button color")
    secondary_button_icon = models.CharField(max_length=50, default='fas fa-info-circle', help_text="Secondary button icon")
    
    # Background Configuration
    gradient_type = models.CharField(max_length=20, choices=GRADIENT_CHOICES, default='blue-purple')
    custom_gradient_from = ColorField(default='#1e3a8a', help_text="Custom gradient start color")
    custom_gradient_to = ColorField(default='#7c3aed', help_text="Custom gradient end color")
    custom_gradient_via = ColorField(default='#6b21a8', blank=True, help_text="Custom gradient middle color (optional)")
    
    # Statistics Configuration
    show_statistics = models.BooleanField(default=True, help_text="Show statistics cards")
    stat_1_number = models.CharField(max_length=20, default='18+', help_text="First statistic number")
    stat_1_label = models.CharField(max_length=50, default='Courses', help_text="First statistic label")
    stat_1_icon = models.CharField(max_length=50, default='fas fa-graduation-cap', help_text="First statistic icon")
    stat_1_color = ColorField(default='#3B82F6', help_text="First statistic card color")
    
    stat_2_number = models.CharField(max_length=20, default='5000+', help_text="Second statistic number")
    stat_2_label = models.CharField(max_length=50, default='Students', help_text="Second statistic label")
    stat_2_icon = models.CharField(max_length=50, default='fas fa-users', help_text="Second statistic icon")
    stat_2_color = ColorField(default='#8B5CF6', help_text="Second statistic card color")
    
    stat_3_number = models.CharField(max_length=20, default='150+', help_text="Third statistic number")
    stat_3_label = models.CharField(max_length=50, default='Faculty', help_text="Third statistic label")
    stat_3_icon = models.CharField(max_length=50, default='fas fa-chalkboard-teacher', help_text="Third statistic icon")
    stat_3_color = ColorField(default='#10B981', help_text="Third statistic card color")
    
    stat_4_number = models.CharField(max_length=20, default='25+', help_text="Fourth statistic number")
    stat_4_label = models.CharField(max_length=50, default='Years', help_text="Fourth statistic label")
    stat_4_icon = models.CharField(max_length=50, default='fas fa-award', help_text="Fourth statistic icon")
    stat_4_color = ColorField(default='#F59E0B', help_text="Fourth statistic card color")
    
    # Content Configuration
    show_content_cards = models.BooleanField(default=False, help_text="Show content cards (for admissions, research, etc.)")
    content_title = models.CharField(max_length=200, blank=True, help_text="Content section title")
    content_icon = models.CharField(max_length=50, default='fas fa-university', help_text="Content section icon")
    content_items = CKEditor5Field(blank=True, help_text="Content items (HTML format)")
    
    # Advanced Configuration
    auto_play_interval = models.PositiveIntegerField(default=5000, help_text="Auto-play interval in milliseconds")
    show_indicators = models.BooleanField(default=True, help_text="Show carousel indicators")
    show_controls = models.BooleanField(default=True, help_text="Show navigation controls")
    
    class Meta:
        verbose_name = "Hero Carousel Slide"
        verbose_name_plural = "Hero Carousel Slides"
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_slide_type_display()})"
    
    def get_gradient_style(self):
        """Get CSS gradient style based on gradient type"""
        if self.gradient_type == 'custom':
            if self.custom_gradient_via:
                return f"linear-gradient(to bottom right, {self.custom_gradient_from}, {self.custom_gradient_via}, {self.custom_gradient_to})"
            else:
                return f"linear-gradient(to bottom right, {self.custom_gradient_from}, {self.custom_gradient_to})"
        
        gradients = {
            'blue-purple': 'linear-gradient(to bottom right, #1e3a8a, #6b21a8, #7c3aed)',
            'green-teal': 'linear-gradient(to bottom right, #064e3b, #0f766e, #059669)',
            'purple-pink': 'linear-gradient(to bottom right, #581c87, #be185d, #ec4899)',
            'orange-red': 'linear-gradient(to bottom right, #9a3412, #dc2626, #ec4899)',
        }
        return gradients.get(self.gradient_type, gradients['blue-purple'])
    
    def get_badge_style(self):
        """Get badge styling"""
        return f"background: linear-gradient(to right, {self.badge_color}, {self.badge_color}CC);"
    
    def get_primary_button_style(self):
        """Get primary button styling"""
        return f"background-color: {self.primary_button_color}; border-color: {self.primary_button_color};"
    
    def get_secondary_button_style(self):
        """Get secondary button styling"""
        return f"color: {self.secondary_button_color}; border-color: {self.secondary_button_color};"
    
    def get_stat_card_style(self, stat_number):
        """Get statistic card styling"""
        colors = {
            1: self.stat_1_color,
            2: self.stat_2_color,
            3: self.stat_3_color,
            4: self.stat_4_color,
        }
        color = colors.get(stat_number, self.stat_1_color)
        return f"background: linear-gradient(to bottom right, {color}, {color}CC);"


class HeroCarouselSettings(TimeStampedModel):
    """Model for global hero carousel settings"""
    
    is_enabled = models.BooleanField(default=True, help_text="Enable hero carousel")
    auto_play = models.BooleanField(default=True, help_text="Enable auto-play")
    default_interval = models.PositiveIntegerField(default=5000, help_text="Default auto-play interval (ms)")
    show_indicators = models.BooleanField(default=True, help_text="Show carousel indicators")
    show_controls = models.BooleanField(default=True, help_text="Show navigation controls")
    pause_on_hover = models.BooleanField(default=True, help_text="Pause carousel on hover")
    enable_keyboard = models.BooleanField(default=True, help_text="Enable keyboard navigation")
    enable_touch = models.BooleanField(default=True, help_text="Enable touch/swipe navigation")
    
    # Animation Settings
    transition_duration = models.PositiveIntegerField(default=600, help_text="Transition duration (ms)")
    fade_effect = models.BooleanField(default=True, help_text="Enable fade transition effect")
    
    # Responsive Settings
    mobile_height = models.CharField(max_length=20, default='24rem', help_text="Mobile carousel height")
    tablet_height = models.CharField(max_length=20, default='28rem', help_text="Tablet carousel height")
    desktop_height = models.CharField(max_length=20, default='24rem', help_text="Desktop carousel height")
    
    class Meta:
        verbose_name = "Hero Carousel Settings"
        verbose_name_plural = "Hero Carousel Settings"
    
    def __str__(self):
        return "Hero Carousel Settings"
    
    @classmethod
    def get_settings(cls):
        """Get or create default settings"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
