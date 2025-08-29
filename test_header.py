#!/usr/bin/env python3
"""
Test script to create and verify HeaderInfo configuration
Run this script to test the header redesign functionality
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from college_website.models import HeaderInfo

def create_test_header():
    """Create a test HeaderInfo configuration"""
    
    # Deactivate any existing active headers
    HeaderInfo.objects.filter(is_active=True).update(is_active=False)
    
    # Create a comprehensive test header using the current model structure
    header = HeaderInfo.objects.create(
        college_name="Chaitanya Science and Arts College",
        college_address="Pamgarh, Janjgir Champa, Chhattisgarh, India - 495554",
        college_affiliations="Affiliated to Shaheed Nandkumar Patel Vishwavidyalaya, Raigarh\nRecognized by UGC | NAAC Grade A+",
        email="chaitanyapamgarh@gmail.com",
        phone="+91-9425540666",
        
        # Typography
        college_name_font_family="Poppins, sans-serif",
        college_name_font_size=32,
        college_name_font_weight="700",
        college_name_color="#dc2626",
        
        # Address typography
        address_font_size=14,
        address_font_weight="400",
        address_color="#6b7280",
        
        # Affiliations typography
        affiliations_font_size=12,
        affiliations_font_weight="500",
        affiliations_color="#059669",
        
        # Contact typography
        contact_font_size=13,
        contact_color="#374151",
        
        # Social Media
        facebook_url="https://facebook.com/chaitanyacollege",
        instagram_url="https://instagram.com/chaitanyacollege",
        youtube_url="https://youtube.com/chaitanyacollege",
        linkedin_url="https://linkedin.com/company/chaitanyacollege",
        
        # Header Styling
        header_layout="three_column",
        header_background_color="#ffffff",
        header_border_color="#dc2626",
        header_border_bottom=True,
        header_shadow=True,
        
        # Logo Configuration
        logo_size="70",
        
        # Display options
        show_college_name=True,
        show_address=True,
        show_affiliations=True,
        show_contact_info=True,
        show_social_links=True,
        
        # Responsive
        mobile_stack_layout=True,
        hide_affiliations_mobile=False,
        
        # Features
        enable_animations=True,
        
        # Activation
        is_active=True
    )
    
    print(f"✅ Created test HeaderInfo: {header.college_name}")
    print(f"   ID: {header.id}")
    print(f"   Font: {header.college_name_font_family} {header.college_name_font_size}px")
    print(f"   Layout: {header.header_layout}")
    print(f"   Animations: {'Enabled' if header.enable_animations else 'Disabled'}")
    print(f"   Active: {header.is_active}")
    
    return header

def list_header_info():
    """List all HeaderInfo instances"""
    headers = HeaderInfo.objects.all()
    print(f"\n📋 Total HeaderInfo instances: {headers.count()}")
    
    for header in headers:
        status = "🟢 ACTIVE" if header.is_active else "⭕ INACTIVE"
        print(f"   {status} {header.college_name or 'Unnamed'} (ID: {header.id})")

def verify_context_processor():
    """Verify the context processor is working"""
    from college_website.context_processors import header_info
    from django.http import HttpRequest
    
    request = HttpRequest()
    context = header_info(request)
    
    if 'header_info' in context:
        header = context['header_info']
        if header:
            print(f"\n✅ Context processor working: {header.college_name}")
            left_logos = sum([1 for logo in [header.left_logo_1, header.left_logo_2, header.left_logo_3] if logo])
            right_logos = sum([1 for logo in [header.right_logo_1, header.right_logo_2, header.right_logo_3] if logo])
            print(f"   Left logos: {left_logos}")
            print(f"   Right logos: {right_logos}")
        else:
            print(f"\n⚠️  No active HeaderInfo found")
    else:
        print(f"\n❌ Context processor not working")

if __name__ == "__main__":
    print("🔧 Testing HeaderInfo Configuration")
    print("=" * 50)
    
    # List existing headers
    list_header_info()
    
    # Create test header
    print(f"\n🚀 Creating test HeaderInfo...")
    test_header = create_test_header()
    
    # List headers again
    list_header_info()
    
    # Verify context processor
    verify_context_processor()
    
    print(f"\n✨ Test completed successfully!")
    print(f"   You can now test the header in your browser")
    print(f"   Edit the HeaderInfo in Django admin for customization")
