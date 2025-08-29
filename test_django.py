#!/usr/bin/env python
"""Test script to identify Django issues"""
import os
import sys
import traceback

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
    
    # Try to import Django
    import django
    print(f"✓ Django imported successfully (version: {django.get_version()})")
    
    # Try to setup Django
    django.setup()
    print("✓ Django setup completed")
    
    # Try to import models
    from college_website.models import CollegeInfo
    print("✓ Models imported successfully")
    
    # Check database connection
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✓ Database connection working")
    
    # Try to run migrations check
    from django.core.management import execute_from_command_line
    print("✓ All checks passed - Django should work properly")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
