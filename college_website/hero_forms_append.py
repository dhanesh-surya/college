class HeroCarouselSlideForm(forms.ModelForm):
    """Comprehensive form for managing hero carousel slides"""
    
    class Meta:
        model = HeroCarouselSlide
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
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
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

