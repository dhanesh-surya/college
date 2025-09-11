from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from college_website.models import AcademicCalendar, AcademicEvent


class Command(BaseCommand):
    help = 'Create sample academic calendar data'

    def handle(self, *args, **options):
        self.stdout.write('Creating academic calendar data...')
        
        # Create Academic Calendar 2024-25
        calendar_2024_25, created = AcademicCalendar.objects.get_or_create(
            academic_year='2024-25',
            defaults={
                'title': 'Academic Calendar 2024-25',
                'description': 'Current academic session with comprehensive schedule of events, examinations, and holidays.',
                'start_date': date(2024, 7, 15),
                'end_date': date(2025, 6, 30),
                'is_active': True,
                'is_published': True,
            }
        )
        
        if created:
            self.stdout.write(f'Created calendar: {calendar_2024_25}')
        else:
            self.stdout.write(f'Calendar already exists: {calendar_2024_25}')
        
        # Create Academic Calendar 2023-24
        calendar_2023_24, created = AcademicCalendar.objects.get_or_create(
            academic_year='2023-24',
            defaults={
                'title': 'Academic Calendar 2023-24',
                'description': 'Previous academic session for reference.',
                'start_date': date(2023, 7, 15),
                'end_date': date(2024, 6, 30),
                'is_active': False,
                'is_published': True,
            }
        )
        
        if created:
            self.stdout.write(f'Created calendar: {calendar_2023_24}')
        else:
            self.stdout.write(f'Calendar already exists: {calendar_2023_24}')
        
        # Sample events for 2024-25
        events_2024_25 = [
            # July 2024
            {'title': 'Academic Session Begins', 'event_type': 'academic', 'semester': 'first', 'start_date': date(2024, 7, 15), 'is_important': True},
            {'title': 'Orientation Program', 'event_type': 'orientation', 'semester': 'first', 'start_date': date(2024, 7, 20), 'end_date': date(2024, 7, 22)},
            {'title': 'Regular Classes Commence', 'event_type': 'academic', 'semester': 'first', 'start_date': date(2024, 7, 25)},
            
            # August 2024
            {'title': 'Independence Day (Holiday)', 'event_type': 'holiday', 'semester': 'both', 'start_date': date(2024, 8, 15)},
            {'title': 'First Internal Assessment', 'event_type': 'exam', 'semester': 'first', 'start_date': date(2024, 8, 20), 'end_date': date(2024, 8, 25)},
            
            # September 2024
            {'title': "Teachers' Day Celebration", 'event_type': 'event', 'semester': 'both', 'start_date': date(2024, 9, 5)},
            {'title': 'Mid-Semester Break', 'event_type': 'break', 'semester': 'first', 'start_date': date(2024, 9, 15), 'end_date': date(2024, 9, 20)},
            
            # October 2024
            {'title': 'Gandhi Jayanti (Holiday)', 'event_type': 'holiday', 'semester': 'both', 'start_date': date(2024, 10, 2)},
            {'title': 'Second Internal Assessment', 'event_type': 'exam', 'semester': 'first', 'start_date': date(2024, 10, 20), 'end_date': date(2024, 10, 25)},
            
            # November 2024
            {'title': 'Diwali Break Begins', 'event_type': 'break', 'semester': 'first', 'start_date': date(2024, 11, 1), 'end_date': date(2024, 11, 10)},
            {'title': 'Classes Resume', 'event_type': 'academic', 'semester': 'first', 'start_date': date(2024, 11, 11)},
            
            # December 2024
            {'title': 'First Semester Examinations Begin', 'event_type': 'exam', 'semester': 'first', 'start_date': date(2024, 12, 15), 'end_date': date(2024, 12, 30), 'is_important': True},
            {'title': 'Winter Break Begins', 'event_type': 'break', 'semester': 'both', 'start_date': date(2024, 12, 31), 'end_date': date(2025, 1, 14)},
            
            # January 2025
            {'title': 'Second Semester Begins', 'event_type': 'academic', 'semester': 'second', 'start_date': date(2025, 1, 15), 'is_important': True},
            {'title': 'Republic Day (Holiday)', 'event_type': 'holiday', 'semester': 'both', 'start_date': date(2025, 1, 26)},
            
            # February 2025
            {'title': "Valentine's Day Celebration", 'event_type': 'event', 'semester': 'both', 'start_date': date(2025, 2, 14)},
            {'title': 'Third Internal Assessment', 'event_type': 'exam', 'semester': 'second', 'start_date': date(2025, 2, 20), 'end_date': date(2025, 2, 25)},
            
            # March 2025
            {'title': "International Women's Day", 'event_type': 'event', 'semester': 'both', 'start_date': date(2025, 3, 8)},
            {'title': 'Holi (Holiday)', 'event_type': 'holiday', 'semester': 'both', 'start_date': date(2025, 3, 15)},
            
            # April 2025
            {'title': 'Ambedkar Jayanti (Holiday)', 'event_type': 'holiday', 'semester': 'both', 'start_date': date(2025, 4, 14)},
            {'title': 'Fourth Internal Assessment', 'event_type': 'exam', 'semester': 'second', 'start_date': date(2025, 4, 20), 'end_date': date(2025, 4, 25)},
            
            # May 2025
            {'title': 'Labour Day (Holiday)', 'event_type': 'holiday', 'semester': 'both', 'start_date': date(2025, 5, 1)},
            {'title': 'Second Semester Examinations Begin', 'event_type': 'exam', 'semester': 'second', 'start_date': date(2025, 5, 15), 'end_date': date(2025, 5, 30), 'is_important': True},
            
            # June 2025
            {'title': 'Academic Year Ends', 'event_type': 'academic', 'semester': 'both', 'start_date': date(2025, 6, 30), 'is_important': True},
        ]
        
        # Create events for 2024-25
        for event_data in events_2024_25:
            event, created = AcademicEvent.objects.get_or_create(
                calendar=calendar_2024_25,
                title=event_data['title'],
                defaults={
                    'event_type': event_data['event_type'],
                    'semester': event_data['semester'],
                    'start_date': event_data['start_date'],
                    'end_date': event_data.get('end_date'),
                    'is_important': event_data.get('is_important', False),
                    'is_published': True,
                }
            )
            if created:
                self.stdout.write(f'Created event: {event.title}')
        
        # Sample events for 2023-24
        events_2023_24 = [
            {'title': 'Academic Session Begins', 'event_type': 'academic', 'semester': 'first', 'start_date': date(2023, 7, 15), 'is_important': True},
            {'title': 'Independence Day (Holiday)', 'event_type': 'holiday', 'semester': 'both', 'start_date': date(2023, 8, 15)},
            {'title': 'First Internal Assessment', 'event_type': 'exam', 'semester': 'first', 'start_date': date(2023, 8, 20), 'end_date': date(2023, 8, 25)},
            {'title': "Teachers' Day Celebration", 'event_type': 'event', 'semester': 'both', 'start_date': date(2023, 9, 5)},
            {'title': 'Gandhi Jayanti (Holiday)', 'event_type': 'holiday', 'semester': 'both', 'start_date': date(2023, 10, 2)},
            {'title': 'Diwali Break', 'event_type': 'break', 'semester': 'first', 'start_date': date(2023, 11, 1), 'end_date': date(2023, 11, 10)},
            {'title': 'First Semester Examinations', 'event_type': 'exam', 'semester': 'first', 'start_date': date(2023, 12, 15), 'end_date': date(2023, 12, 30), 'is_important': True},
            {'title': 'Second Semester Begins', 'event_type': 'academic', 'semester': 'second', 'start_date': date(2024, 1, 15), 'is_important': True},
            {'title': 'Republic Day (Holiday)', 'event_type': 'holiday', 'semester': 'both', 'start_date': date(2024, 1, 26)},
            {'title': 'Holi (Holiday)', 'event_type': 'holiday', 'semester': 'both', 'start_date': date(2024, 3, 15)},
            {'title': 'Second Semester Examinations', 'event_type': 'exam', 'semester': 'second', 'start_date': date(2024, 5, 15), 'end_date': date(2024, 5, 30), 'is_important': True},
            {'title': 'Academic Year Ends', 'event_type': 'academic', 'semester': 'both', 'start_date': date(2024, 6, 30), 'is_important': True},
        ]
        
        # Create events for 2023-24
        for event_data in events_2023_24:
            event, created = AcademicEvent.objects.get_or_create(
                calendar=calendar_2023_24,
                title=event_data['title'],
                defaults={
                    'event_type': event_data['event_type'],
                    'semester': event_data['semester'],
                    'start_date': event_data['start_date'],
                    'end_date': event_data.get('end_date'),
                    'is_important': event_data.get('is_important', False),
                    'is_published': True,
                }
            )
            if created:
                self.stdout.write(f'Created event: {event.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created academic calendar data!')
        )
