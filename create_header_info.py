#!/usr/bin/env python
"""
Create a default HeaderInfo record for the college website
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from college_website.models import HeaderInfo

def create_default_header_info():
    """Create a default HeaderInfo record if none exists"""
    
    # Check if any HeaderInfo exists
    if HeaderInfo.objects.exists():
        print("HeaderInfo records already exist:")
        for header in HeaderInfo.objects.all():
            print(f"  - {header.college_name} (Active: {header.is_active})")
        return
    
    # Create default HeaderInfo
    header_info = HeaderInfo.objects.create(
        college_name="Chaitanya Science and Arts College",
        college_name_font_size=28,
        college_name_font_weight='700',
        college_name_font_family='Poppins, sans-serif',
        college_name_color="#1f2937",
        show_college_name=True,
        
        college_address="Pamgarh, Chhattisgarh, India",
        address_font_size=14,
        address_color="#6b7280",
        show_address=True,
        
        affiliation_text="Affiliated to Pt. Ravishankar Shukla University",
        affiliation_font_size=16,
        affiliation_color="#374151",
        show_affiliation=True,
        
        phone="+91-9876543210",
        email="info@chaitanyacollege.edu.in",
        contact_info="info@chaitanyacollege.edu.in | +91-9876543210",
        show_contact_info=True,
        
        header_layout='three_column',
        header_background_color="#ffffff",
        header_text_color="#1f2937",
        header_shadow=True,
        header_border_bottom=True,
        
        show_top_bar=True,
        top_bar_background_class='bg-dark',
        
        is_active=True
    )
    
    print(f"✅ Created default HeaderInfo: {header_info.college_name}")
    print(f"   Layout: {header_info.header_layout}")
    print(f"   Active: {header_info.is_active}")

if __name__ == "__main__":
    create_default_header_info()
