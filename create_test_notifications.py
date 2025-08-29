#!/usr/bin/env python
"""
Quick script to create test scrolling notifications
"""

import os
import sys
import django
from datetime import datetime, timezone, timedelta

# Add the project directory to Python path
sys.path.append(r'D:\cooccp')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from college_website.models import ScrollingNotification

def create_test_notifications():
    """Create test scrolling notifications"""
    
    # Clear existing notifications
    ScrollingNotification.objects.all().delete()
    
    # Create test notifications with varying lengths
    notifications = [
        {
            'title': 'Admission Open',
            'message': 'Applications for 2025-26 academic session are now open!',
            'link_text': 'Apply Now',
            'link_url': '/admissions/',
            'priority': 'high',
            'color_theme': 'primary',
            'icon_class': 'fas fa-graduation-cap',
            'scroll_speed': 50,
            'display_order': 1
        },
        {
            'title': 'Notice',
            'message': 'Semester exams will be conducted from February 15th.',
            'link_text': 'View Details',
            'link_url': '/notices/',
            'priority': 'medium',
            'color_theme': 'warning',
            'icon_class': 'fas fa-bell',
            'scroll_speed': 50,
            'display_order': 2
        },
        {
            'title': 'URGENT',
            'message': 'Fee submission deadline: January 31st, 2025',
            'link_text': 'Pay Now',
            'link_url': '/payments/',
            'priority': 'urgent',
            'color_theme': 'danger',
            'icon_class': 'fas fa-exclamation-triangle',
            'scroll_speed': 30,
            'display_order': 3
        },
        {
            'title': 'Workshop',
            'message': 'AI & Machine Learning workshop on Dec 20th - Register now!',
            'link_text': 'Register',
            'link_url': '/events/',
            'priority': 'medium',
            'color_theme': 'info',
            'icon_class': 'fas fa-laptop-code',
            'scroll_speed': 50,
            'display_order': 4
        },
        {
            'title': 'Results',
            'message': 'Semester 1 results declared',
            'link_text': 'Check Results',
            'link_url': '/results/',
            'priority': 'high',
            'color_theme': 'success',
            'icon_class': 'fas fa-trophy',
            'scroll_speed': 50,
            'display_order': 5
        }
    ]
    
    # Create notifications
    created_count = 0
    for notification_data in notifications:
        notification = ScrollingNotification.objects.create(
            title=notification_data['title'],
            message=notification_data['message'],
            link_text=notification_data['link_text'],
            link_url=notification_data['link_url'],
            priority=notification_data['priority'],
            color_theme=notification_data['color_theme'],
            icon_class=notification_data['icon_class'],
            scroll_speed=notification_data['scroll_speed'],
            display_order=notification_data['display_order'],
            start_date=datetime.now(timezone.utc) - timedelta(days=1),  # Started yesterday
            end_date=datetime.now(timezone.utc) + timedelta(days=30),  # Ends in 30 days
            is_active=True,
            pause_on_hover=True,
            show_icon=True
        )
        created_count += 1
        print(f"✅ Created notification: {notification.title}")
    
    print(f"\n🎉 Successfully created {created_count} test notifications!")
    print("💡 You can now see the horizontal scrolling notifications on the website!")
    print("🔧 Visit Django admin to manage notifications: http://127.0.0.1:8000/admin/")

if __name__ == '__main__':
    create_test_notifications()
