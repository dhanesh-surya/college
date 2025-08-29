#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from college_website.models import SliderImage

def create_sample_slider_data():
    """Create sample slider images for testing"""
    
    # Clear existing slider images
    print("Clearing existing slider images...")
    SliderImage.objects.all().delete()
    
    # Sample slider data
    slider_data = [
        {
            'title': 'Welcome to Chaitanya College',
            'caption': 'Empowering rural youth through quality education since 2001. Join us in our journey of excellence and innovation.',
            'button_text': 'Learn More',
            'button_url': '/about/',
            'ordering': 1,
            'is_active': True,
            'alt_text': 'Welcome to Chaitanya College - Campus view with students'
        },
        {
            'title': 'Excellence in Science Education',
            'caption': 'State-of-the-art laboratories and experienced faculty providing comprehensive science education with practical learning.',
            'button_text': 'Explore Programs',
            'button_url': '/programs/?discipline=science',
            'ordering': 2,
            'is_active': True,
            'alt_text': 'Science laboratory with modern equipment and students conducting experiments'
        },
        {
            'title': 'Arts & Culture Programs',
            'caption': 'Fostering creativity and cultural understanding through our diverse liberal arts programs and extracurricular activities.',
            'button_text': 'View Arts Programs',
            'button_url': '/programs/?discipline=arts',
            'ordering': 3,
            'is_active': True,
            'alt_text': 'Students participating in cultural activities and arts programs'
        },
        {
            'title': 'NAAC Grade A Accredited',
            'caption': 'Recognized for our commitment to quality education and continuous improvement. Join our legacy of academic excellence.',
            'button_text': 'View Achievements',
            'button_url': '/achievements/',
            'ordering': 4,
            'is_active': True,
            'alt_text': 'NAAC accreditation certificate and college achievements'
        },
        {
            'title': '95% Placement Success',
            'caption': 'Our strong industry connections and career guidance ensure excellent placement opportunities for our graduates.',
            'button_text': 'See Placements',
            'button_url': '/placements/',
            'ordering': 5,
            'is_active': True,
            'alt_text': 'Successful students with job offers and placement statistics'
        }
    ]
    
    print("Creating sample slider images...")
    
    for i, data in enumerate(slider_data, 1):
        try:
            # Create slider image without actual image file for now
            slide = SliderImage.objects.create(**data)
            print(f"✓ Created slide {i}: {slide.title}")
            
        except Exception as e:
            print(f"✗ Error creating slide {i}: {e}")
    
    print(f"\nSample data creation completed!")
    print(f"Created {SliderImage.objects.count()} slider images.")
    print("\nNote: These slides don't have actual images yet.")
    print("To add images:")
    print("1. Go to Django Admin: http://localhost:8000/admin/")
    print("2. Navigate to College Website > Slider Images")
    print("3. Edit each slide and upload an image")
    print("4. Recommended image size: 1920x800px (16:9 ratio)")

if __name__ == '__main__':
    create_sample_slider_data()
