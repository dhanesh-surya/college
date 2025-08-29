#!/usr/bin/env python
"""
Script to create sample menu and page data for testing the dynamic navbar
Run this script: python manage.py shell < create_sample_menu_data.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from college_website.models import Menu, MenuItem, Page, BlockRichText

def create_sample_data():
    """Create sample menus, pages, and menu items"""
    
    # Create sample pages first
    about_page, created = Page.objects.get_or_create(
        slug='about-college',
        defaults={
            'title': 'About College',
            'meta_title': 'About Chaitanya Science and Arts College',
            'meta_description': 'Learn about our college history, mission, and vision.',
            'show_banner': True,
            'show_sidebar': True,
            'is_active': True
        }
    )
    
    # Add content to about page
    if created:
        BlockRichText.objects.create(
            page=about_page,
            title='About Our College',
            body='<p>Chaitanya Science and Arts College has been serving the educational needs of rural communities since 2001. Our mission is to provide quality education and empower students with knowledge and skills.</p>',
            ordering=1,
            is_active=True
        )
    
    history_page, created = Page.objects.get_or_create(
        slug='college-history',
        defaults={
            'title': 'College History',
            'meta_title': 'History of Chaitanya Science and Arts College',
            'meta_description': 'Discover the rich history and heritage of our institution.',
            'show_banner': True,
            'show_sidebar': True,
            'is_active': True
        }
    )
    
    if created:
        BlockRichText.objects.create(
            page=history_page,
            title='Our Heritage',
            body='<p>Founded in 2001, our college has a rich history of academic excellence and community service. We have grown from a small institution to a recognized center of learning.</p>',
            ordering=1,
            is_active=True
        )
    
    mission_page, created = Page.objects.get_or_create(
        slug='mission-vision',
        defaults={
            'title': 'Mission & Vision',
            'meta_title': 'Mission and Vision - Chaitanya Science and Arts College',
            'meta_description': 'Our mission and vision for educational excellence.',
            'show_banner': True,
            'show_sidebar': True,
            'is_active': True
        }
    )
    
    if created:
        BlockRichText.objects.create(
            page=mission_page,
            title='Our Mission & Vision',
            body='<p><strong>Mission:</strong> To provide quality education and foster intellectual growth in rural communities.</p><p><strong>Vision:</strong> To be a leading educational institution that empowers students for success in the global economy.</p>',
            ordering=1,
            is_active=True
        )
    
    faculty_page, created = Page.objects.get_or_create(
        slug='faculty-staff',
        defaults={
            'title': 'Faculty & Staff',
            'meta_title': 'Faculty and Staff - Chaitanya Science and Arts College',
            'meta_description': 'Meet our dedicated faculty and staff members.',
            'show_banner': True,
            'show_sidebar': True,
            'is_active': True
        }
    )
    
    if created:
        BlockRichText.objects.create(
            page=faculty_page,
            title='Our Team',
            body='<p>Our college is proud to have a team of dedicated and experienced faculty members who are committed to providing quality education to our students.</p>',
            ordering=1,
            is_active=True
        )
    
    facilities_page, created = Page.objects.get_or_create(
        slug='campus-facilities',
        defaults={
            'title': 'Campus Facilities',
            'meta_title': 'Campus Facilities - Chaitanya Science and Arts College',
            'meta_description': 'Explore our modern campus facilities and infrastructure.',
            'show_banner': True,
            'show_sidebar': True,
            'is_active': True
        }
    )
    
    if created:
        BlockRichText.objects.create(
            page=facilities_page,
            title='Modern Facilities',
            body='<p>Our campus features modern classrooms, well-equipped laboratories, a comprehensive library, sports facilities, and comfortable hostels for students.</p>',
            ordering=1,
            is_active=True
        )
    
    # Create About Menu
    about_menu, created = Menu.objects.get_or_create(
        slug='about',
        defaults={
            'title': 'About',
            'is_active': True,
            'ordering': 1
        }
    )
    
    # Create menu items for About menu
    about_item, created = MenuItem.objects.get_or_create(
        menu=about_menu,
        slug='about-college',
        defaults={
            'title': 'About College',
            'path_type': 'internal',
            'page': about_page,
            'is_active': True,
            'ordering': 1
        }
    )
    
    history_item, created = MenuItem.objects.get_or_create(
        menu=about_menu,
        slug='history',
        defaults={
            'title': 'History',
            'path_type': 'internal',
            'page': history_page,
            'is_active': True,
            'ordering': 2
        }
    )
    
    mission_item, created = MenuItem.objects.get_or_create(
        menu=about_menu,
        slug='mission-vision',
        defaults={
            'title': 'Mission & Vision',
            'path_type': 'internal',
            'page': mission_page,
            'is_active': True,
            'ordering': 3
        }
    )
    
    # Create Academic Menu
    academic_menu, created = Menu.objects.get_or_create(
        slug='academics',
        defaults={
            'title': 'Academics',
            'is_active': True,
            'ordering': 2
        }
    )
    
    # Create parent menu item for Programs
    programs_parent, created = MenuItem.objects.get_or_create(
        menu=academic_menu,
        slug='programs',
        defaults={
            'title': 'Programs',
            'path_type': 'internal',
            'external_url': '',
            'page': None,
            'is_active': True,
            'ordering': 1
        }
    )
    
    # Create child menu items under Programs
    arts_item, created = MenuItem.objects.get_or_create(
        menu=academic_menu,
        parent=programs_parent,
        slug='arts-programs',
        defaults={
            'title': 'Arts Programs',
            'path_type': 'external',
            'external_url': '/programs/?discipline=arts',
            'page': None,
            'is_active': True,
            'ordering': 1
        }
    )
    
    science_item, created = MenuItem.objects.get_or_create(
        menu=academic_menu,
        parent=programs_parent,
        slug='science-programs',
        defaults={
            'title': 'Science Programs',
            'path_type': 'external',
            'external_url': '/programs/?discipline=science',
            'page': None,
            'is_active': True,
            'ordering': 2
        }
    )
    
    commerce_item, created = MenuItem.objects.get_or_create(
        menu=academic_menu,
        parent=programs_parent,
        slug='commerce-programs',
        defaults={
            'title': 'Commerce Programs',
            'path_type': 'external',
            'external_url': '/programs/?discipline=commerce',
            'page': None,
            'is_active': True,
            'ordering': 3
        }
    )
    
    # Add Faculty menu item to Academic menu
    faculty_item, created = MenuItem.objects.get_or_create(
        menu=academic_menu,
        slug='faculty',
        defaults={
            'title': 'Faculty & Staff',
            'path_type': 'internal',
            'page': faculty_page,
            'is_active': True,
            'ordering': 2
        }
    )
    
    # Create Campus Menu
    campus_menu, created = Menu.objects.get_or_create(
        slug='campus',
        defaults={
            'title': 'Campus Life',
            'is_active': True,
            'ordering': 3
        }
    )
    
    # Add facilities to campus menu
    facilities_item, created = MenuItem.objects.get_or_create(
        menu=campus_menu,
        slug='facilities',
        defaults={
            'title': 'Facilities',
            'path_type': 'internal',
            'page': facilities_page,
            'is_active': True,
            'ordering': 1
        }
    )
    
    # Add events link to campus menu
    events_item, created = MenuItem.objects.get_or_create(
        menu=campus_menu,
        slug='events',
        defaults={
            'title': 'Events',
            'path_type': 'external',
            'external_url': '/events/',
            'page': None,
            'is_active': True,
            'ordering': 2
        }
    )
    
    # Add gallery link to campus menu
    gallery_item, created = MenuItem.objects.get_or_create(
        menu=campus_menu,
        slug='gallery',
        defaults={
            'title': 'Gallery',
            'path_type': 'external',
            'external_url': '/gallery/',
            'page': None,
            'is_active': True,
            'ordering': 3
        }
    )
    
    print("✅ Sample menu and page data created successfully!")
    print("\nCreated Menus:")
    print("- About (with About College, History, Mission & Vision)")
    print("- Academics (with Programs submenu: Arts, Science, Commerce + Faculty)")
    print("- Campus Life (with Facilities, Events, Gallery)")
    print("\nCreated Pages:")
    print("- About College (/p/about-college/)")
    print("- College History (/p/college-history/)")
    print("- Mission & Vision (/p/mission-vision/)")
    print("- Faculty & Staff (/p/faculty-staff/)")
    print("- Campus Facilities (/p/campus-facilities/)")

if __name__ == '__main__':
    create_sample_data()
