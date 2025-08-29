#!/usr/bin/env python
"""Setup script to create initial data for the college website"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from college_website.models import CollegeInfo, Menu, MenuItem, ImportantLink

def create_college_info():
    """Create college information"""
    college_info, created = CollegeInfo.objects.get_or_create(
        name="Chaitanya Science and Arts College",
        defaults={
            'establishment_year': 2001,
            'affiliation': 'Shaheed Nandkumar Patel Vishwavidyalaya, Raigarh',
            'address_line': 'Pamgarh, Janjgir Champa, Chhattisgarh, India, 495554',
            'email': 'chaitanyapamgarh@gmail.com',
            'phone': '+91-9425540666',
            'mission_statement_short': 'Empowering rural youth through quality education since 2001',
            'mission_statement_long': 'At Chaitanya Science and Arts College, we are committed to providing quality education that empowers students from rural backgrounds to achieve their dreams and contribute meaningfully to society.',
            'founder_name': 'Mr Veerendra Tiwari',
            'founder_message': 'Education is the foundation of progress. Our mission is to make quality education accessible to all.',
            'principal_name': 'Dr Vinod Kumar Gupta',
            'principal_message': 'We strive to create an environment where knowledge meets innovation and students can flourish.',
            'courses_count': '18+',
            'students_count': '8000+',
            'faculty_staff_count': '50+',
            'years_of_excellence': '25+',
            'naac_grade': 'NAAC GRADE A AWARD',
            'iic_rating': '3 Star Rating IIC',
            'slug': 'chaitanya-science-and-arts-college',
            'is_active': True
        }
    )
    print(f"College info {'created' if created else 'updated'}: {college_info.name}")
    return college_info

def create_quick_links():
    """Create quick links"""
    quick_links_data = [
        {'name': 'Admission', 'url': '/admissions/', 'icon_class': 'fas fa-user-plus'},
        {'name': 'Results', 'url': '/results/', 'icon_class': 'fas fa-chart-bar'},
        {'name': 'Library', 'url': '/library/', 'icon_class': 'fas fa-book'},
        {'name': 'E-Learning', 'url': '/elearning/', 'icon_class': 'fas fa-laptop'},
        {'name': 'Placement', 'url': '/placement/', 'icon_class': 'fas fa-briefcase'},
        {'name': 'Alumni', 'url': '/alumni/', 'icon_class': 'fas fa-users'},
    ]
    
    for i, link_data in enumerate(quick_links_data):
        link, created = ImportantLink.objects.get_or_create(
            name=link_data['name'],
            type='quick',
            defaults={
                'url': link_data['url'],
                'icon_class': link_data['icon_class'],
                'ordering': i,
                'is_active': True
            }
        )
        print(f"Quick link {'created' if created else 'updated'}: {link.name}")

def create_important_links():
    """Create important links"""
    important_links_data = [
        {'name': 'University Website', 'url': 'https://www.snpuniv.ac.in/', 'icon_class': 'fas fa-university'},
        {'name': 'NAAC', 'url': 'https://www.naac.gov.in/', 'icon_class': 'fas fa-certificate'},
        {'name': 'UGC', 'url': 'https://www.ugc.ac.in/', 'icon_class': 'fas fa-graduation-cap'},
        {'name': 'NIRF', 'url': 'https://www.nirfindia.org/', 'icon_class': 'fas fa-trophy'},
    ]
    
    for i, link_data in enumerate(important_links_data):
        link, created = ImportantLink.objects.get_or_create(
            name=link_data['name'],
            type='important',
            defaults={
                'url': link_data['url'],
                'icon_class': link_data['icon_class'],
                'ordering': i,
                'is_active': True
            }
        )
        print(f"Important link {'created' if created else 'updated'}: {link.name}")

if __name__ == '__main__':
    print("Setting up initial data...")
    create_college_info()
    create_quick_links()
    create_important_links()
    print("Initial data setup completed!")
