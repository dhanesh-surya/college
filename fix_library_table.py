#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def create_library_resource_table():
    """Create the LibraryResource table manually"""
    with connection.cursor() as cursor:
        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='college_website_libraryresource';
        """)
        
        if not cursor.fetchone():
            print("Creating college_website_libraryresource table...")
            
            # Create the LibraryResource table
            cursor.execute("""
                CREATE TABLE "college_website_libraryresource" (
                    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "created_at" datetime NOT NULL,
                    "updated_at" datetime NOT NULL,
                    "title" varchar(300) NOT NULL,
                    "slug" varchar(50) NOT NULL UNIQUE,
                    "resource_type" varchar(20) NOT NULL,
                    "author" varchar(200) NOT NULL,
                    "isbn" varchar(20) NOT NULL,
                    "publisher" varchar(200) NOT NULL,
                    "publication_year" integer unsigned NULL,
                    "description" text NOT NULL,
                    "subject_category" varchar(100) NOT NULL,
                    "location" varchar(100) NOT NULL,
                    "availability_status" varchar(20) NOT NULL,
                    "digital_copy" varchar(100) NOT NULL,
                    "external_link" varchar(200) NOT NULL,
                    "cover_image" varchar(100) NOT NULL,
                    "is_featured" bool NOT NULL
                );
            """)
            
            print("Table created successfully!")
            
            # Mark migration as applied
            cursor.execute("""
                INSERT OR IGNORE INTO django_migrations (app, name, applied) 
                VALUES ('college_website', '0006_admissioninfo_alumniprofile_elearningcourse_and_more', datetime('now'));
            """)
            
            print("Migration marked as applied!")
        else:
            print("Table already exists!")

if __name__ == '__main__':
    create_library_resource_table()
