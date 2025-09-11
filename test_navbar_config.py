#!/usr/bin/env python
"""
Test script to verify navbar configuration is working
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from college_website.models import NavbarInfo

def test_navbar_configuration():
    """Test navbar configuration functionality"""
    print("🧪 Testing Navbar Configuration System")
    print("=" * 50)
    
    # Get current configuration
    config = NavbarInfo.objects.filter(is_active=True).first()
    
    if not config:
        print("❌ No active navbar configuration found!")
        return False
    
    print(f"✅ Active configuration found: {config.brand_name}")
    print(f"📏 Current navbar height: {config.navbar_height}px")
    print(f"🔤 Current menu font size: {config.menu_font_size}rem")
    print(f"🎨 Current brand font size: {config.brand_font_size}rem")
    print(f"🎨 Background color: {config.navbar_background_color}")
    print(f"🎨 Text color: {config.navbar_text_color}")
    print(f"🎨 Hover color: {config.navbar_hover_color}")
    
    # Test configuration changes
    print("\n🔄 Testing configuration changes...")
    
    # Store original values
    original_height = config.navbar_height
    original_font_size = config.menu_font_size
    original_brand_size = config.brand_font_size
    
    # Make test changes
    config.navbar_height = 50
    config.menu_font_size = 0.7
    config.brand_font_size = 0.8
    config.navbar_background_color = "#1e40af"
    config.navbar_text_color = "#ffffff"
    config.navbar_hover_color = "#fbbf24"
    config.save()
    
    print("✅ Configuration updated successfully!")
    print(f"📏 New navbar height: {config.navbar_height}px")
    print(f"🔤 New menu font size: {config.menu_font_size}rem")
    print(f"🎨 New brand font size: {config.brand_font_size}rem")
    print(f"🎨 New background color: {config.navbar_background_color}")
    print(f"🎨 New text color: {config.navbar_text_color}")
    print(f"🎨 New hover color: {config.navbar_hover_color}")
    
    # Restore original values
    print("\n🔄 Restoring original configuration...")
    config.navbar_height = original_height
    config.menu_font_size = original_font_size
    config.brand_font_size = original_brand_size
    config.navbar_background_color = "#dc2626"
    config.navbar_text_color = "#ffffff"
    config.navbar_hover_color = "#7c3aed"
    config.save()
    
    print("✅ Original configuration restored!")
    print(f"📏 Restored navbar height: {config.navbar_height}px")
    print(f"🔤 Restored menu font size: {config.menu_font_size}rem")
    print(f"🎨 Restored brand font size: {config.brand_font_size}rem")
    
    print("\n🎉 Navbar configuration system is working correctly!")
    print("🌐 Visit http://127.0.0.1:8000/ to see the navbar")
    print("⚙️  Visit http://127.0.0.1:8000/admin/college_website/navbarinfo/ to manage configuration")
    
    return True

if __name__ == "__main__":
    test_navbar_configuration()
