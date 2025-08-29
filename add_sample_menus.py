#!/usr/bin/env python
"""
Sample script to add CMS menus for testing the hybrid navbar system.
Run this with: python manage.py shell < add_sample_menus.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from college_website.models import Menu, MenuItem, Page

def create_sample_menus():
    """Create sample CMS menus to demonstrate the hybrid navbar system"""
    
    print("Creating sample CMS menus...")
    
    # Create Facilities Menu
    facilities_menu, created = Menu.objects.get_or_create(
        title="Facilities",
        defaults={
            'slug': 'facilities',
            'is_active': True,
            'ordering': 1
        }
    )
    
    if created:
        print(f"✓ Created menu: {facilities_menu.title}")
        
        # Create menu items for Facilities
        facilities_items = [
            {
                'title': 'Library',
                'icon_class': 'fas fa-book',
                'path_type': 'named_url',
                'named_url': 'college_website:library',
                'ordering': 1
            },
            {
                'title': 'Computer Lab',
                'icon_class': 'fas fa-desktop',
                'path_type': 'external',
                'external_url': '/facilities/computer-lab/',
                'ordering': 2
            },
            {
                'title': 'Science Lab',
                'icon_class': 'fas fa-microscope',
                'path_type': 'external',
                'external_url': '/facilities/science-lab/',
                'ordering': 3
            },
            {
                'title': 'Sports Complex',
                'icon_class': 'fas fa-running',
                'path_type': 'external',
                'external_url': '/facilities/sports/',
                'ordering': 4
            },
            {
                'title': 'Hostel',
                'icon_class': 'fas fa-bed',
                'path_type': 'named_url',
                'named_url': 'college_website:hostel',
                'ordering': 5
            }
        ]
        
        for item_data in facilities_items:
            MenuItem.objects.create(
                menu=facilities_menu,
                **item_data
            )
            print(f"  → Added item: {item_data['title']}")
    
    # Create Research Menu
    research_menu, created = Menu.objects.get_or_create(
        title="Research",
        defaults={
            'slug': 'research',
            'is_active': True,
            'ordering': 2
        }
    )
    
    if created:
        print(f"✓ Created menu: {research_menu.title}")
        
        # Create main research item with sub-items
        research_main = MenuItem.objects.create(
            menu=research_menu,
            title='Research Programs',
            icon_class='fas fa-flask',
            path_type='external',
            external_url='/research/',
            ordering=1
        )
        
        # Create sub-items for Research
        research_sub_items = [
            {
                'title': 'Ongoing Projects',
                'icon_class': 'fas fa-project-diagram',
                'path_type': 'external',
                'external_url': '/research/projects/',
                'ordering': 1
            },
            {
                'title': 'Publications',
                'icon_class': 'fas fa-file-alt',
                'path_type': 'named_url',
                'named_url': 'college_website:publications',
                'ordering': 2
            },
            {
                'title': 'Research Collaborations',
                'icon_class': 'fas fa-handshake',
                'path_type': 'external',
                'external_url': '/research/collaborations/',
                'ordering': 3
            }
        ]
        
        for item_data in research_sub_items:
            MenuItem.objects.create(
                menu=research_menu,
                parent=research_main,
                **item_data
            )
            print(f"  → Added sub-item: {item_data['title']}")
    
    # Create Student Services Menu
    services_menu, created = Menu.objects.get_or_create(
        title="Services",
        defaults={
            'slug': 'services',
            'is_active': True,
            'ordering': 3
        }
    )
    
    if created:
        print(f"✓ Created menu: {services_menu.title}")
        
        # Academic Services
        academic_services = MenuItem.objects.create(
            menu=services_menu,
            title='Academic Services',
            icon_class='fas fa-graduation-cap',
            path_type='external',
            external_url='/services/academic/',
            ordering=1
        )
        
        academic_sub_items = [
            {
                'title': 'Online Courses',
                'icon_class': 'fas fa-laptop',
                'path_type': 'named_url',
                'named_url': 'college_website:elearning',
                'ordering': 1
            },
            {
                'title': 'Academic Calendar',
                'icon_class': 'fas fa-calendar',
                'path_type': 'external',
                'external_url': '/academics/calendar/',
                'ordering': 2
            },
            {
                'title': 'Examination Schedule',
                'icon_class': 'fas fa-clock',
                'path_type': 'external',
                'external_url': '/examinations/timetable/',
                'ordering': 3
            }
        ]
        
        for item_data in academic_sub_items:
            MenuItem.objects.create(
                menu=services_menu,
                parent=academic_services,
                **item_data
            )
            print(f"  → Added academic service: {item_data['title']}")
        
        # Student Services
        student_services = MenuItem.objects.create(
            menu=services_menu,
            title='Student Services',
            icon_class='fas fa-users',
            path_type='external',
            external_url='/services/student/',
            ordering=2
        )
        
        student_sub_items = [
            {
                'title': 'Career Counseling',
                'icon_class': 'fas fa-user-tie',
                'path_type': 'external',
                'external_url': '/services/career-counseling/',
                'ordering': 1
            },
            {
                'title': 'Placement Cell',
                'icon_class': 'fas fa-briefcase',
                'path_type': 'named_url',
                'named_url': 'college_website:placement_cell',
                'ordering': 2
            },
            {
                'title': 'Alumni Network',
                'icon_class': 'fas fa-network-wired',
                'path_type': 'named_url',
                'named_url': 'college_website:alumni',
                'ordering': 3
            }
        ]
        
        for item_data in student_sub_items:
            MenuItem.objects.create(
                menu=services_menu,
                parent=student_services,
                **item_data
            )
            print(f"  → Added student service: {item_data['title']}")
    
    # Create Quick Links Menu (simple items)
    quick_menu, created = Menu.objects.get_or_create(
        title="Quick Links",
        defaults={
            'slug': 'quick-links',
            'is_active': True,
            'ordering': 4
        }
    )
    
    if created:
        print(f"✓ Created menu: {quick_menu.title}")
        
        quick_items = [
            {
                'title': 'Downloads',
                'icon_class': 'fas fa-download',
                'path_type': 'external',
                'external_url': '/downloads/',
                'ordering': 1
            },
            {
                'title': 'Fee Payment',
                'icon_class': 'fas fa-credit-card',
                'path_type': 'external',
                'external_url': '/fee-payment/',
                'ordering': 2
            },
            {
                'title': 'Result Portal',
                'icon_class': 'fas fa-poll',
                'path_type': 'external',
                'external_url': '/results/',
                'ordering': 3
            }
        ]
        
        for item_data in quick_items:
            MenuItem.objects.create(
                menu=quick_menu,
                **item_data
            )
            print(f"  → Added quick link: {item_data['title']}")
    
    print("\n🎉 Sample CMS menus created successfully!")
    print("\nYou can now:")
    print("1. Visit the admin panel to manage these menus")
    print("2. View the hybrid navbar with both static and CMS menus")
    print("3. Add/edit/remove menu items as needed")
    print("\nAdmin URL: http://127.0.0.1:8000/admin/college_website/menu/")

if __name__ == "__main__":
    create_sample_menus()
