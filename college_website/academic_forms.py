from django import forms
from django.core.exceptions import ValidationError
from .models import AcademicCalendar, AcademicEvent


class AcademicCalendarForm(forms.ModelForm):
    """Enhanced form for Academic Calendar management with comprehensive validation and user experience improvements"""
    
    class Meta:
        model = AcademicCalendar
        fields = '__all__'
        widgets = {
            'academic_year': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select academic year'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Academic Calendar 2024-25',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of the academic year',
                'rows': 3
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        help_texts = {
            'academic_year': 'Select the academic year for this calendar',
            'title': 'Display title for the academic calendar',
            'description': 'Brief description of the academic year',
            'start_date': 'Academic year start date',
            'end_date': 'Academic year end date',
            'pdf_file': 'Upload PDF version of the academic calendar (optional)',
            'is_active': 'Mark as current active academic year (only one can be active)',
            'is_published': 'Make calendar publicly visible on the website',
        }
        labels = {
            'academic_year': 'Academic Year',
            'title': 'Calendar Title',
            'description': 'Description',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'pdf_file': 'PDF File',
            'is_active': 'Active Calendar',
            'is_published': 'Published',
        }
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError('Title must be at least 3 characters long.')
        return title
    
    def clean_pdf_file(self):
        """Validate PDF file"""
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            # Check file extension
            if not pdf_file.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')
            
            # Check file size (max 10MB)
            if pdf_file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('PDF file size cannot exceed 10MB.')
        
        return pdf_file
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError('End date must be after start date.')
        
        return cleaned_data


class AcademicEventForm(forms.ModelForm):
    """Enhanced form for Academic Event management with comprehensive validation and user experience improvements"""
    
    class Meta:
        model = AcademicEvent
        fields = '__all__'
        widgets = {
            'calendar': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select academic calendar'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Academic Session Begins',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Event description (optional)',
                'rows': 2
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_important': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Display order'
            }),
        }
        help_texts = {
            'calendar': 'Select the academic calendar this event belongs to',
            'title': 'Event title or name',
            'description': 'Optional detailed description of the event',
            'event_type': 'Category of the event',
            'semester': 'Which semester this event applies to',
            'start_date': 'Event start date',
            'end_date': 'Event end date (leave blank for single-day events)',
            'is_important': 'Mark as important event (will be highlighted)',
            'is_published': 'Make event publicly visible',
            'ordering': 'Display order (lower numbers appear first)',
        }
        labels = {
            'calendar': 'Academic Calendar',
            'title': 'Event Title',
            'description': 'Description',
            'event_type': 'Event Type',
            'semester': 'Semester',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'is_important': 'Important Event',
            'is_published': 'Published',
            'ordering': 'Display Order',
        }
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError('Event title must be at least 3 characters long.')
        return title
    
    def clean_ordering(self):
        """Validate ordering"""
        ordering = self.cleaned_data.get('ordering')
        if ordering is not None and ordering < 0:
            raise forms.ValidationError('Display order must be a non-negative number.')
        return ordering
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        calendar = cleaned_data.get('calendar')
        
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError('End date must be after or equal to start date.')
        
        if calendar and start_date:
            # Check if event date is within academic year
            if start_date < calendar.start_date or start_date > calendar.end_date:
                raise forms.ValidationError(f'Event date must be within the academic year ({calendar.start_date} to {calendar.end_date}).')
        
        return cleaned_data


class AcademicEventInlineForm(forms.ModelForm):
    """Inline form for Academic Events with simplified fields"""
    
    class Meta:
        model = AcademicEvent
        fields = ['title', 'event_type', 'semester', 'start_date', 'end_date', 'is_important', 'ordering']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Event title'
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select form-select-sm'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-select form-select-sm'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control form-control-sm',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control form-control-sm',
                'type': 'date'
            }),
            'is_important': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'ordering': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'min': '0'
            }),
        }
