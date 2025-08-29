#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from college_website.models import LibraryResource

def create_missing_table():
    """Create the missing LibraryResource table"""
    try:
        # Try to query the table to see if it exists
        LibraryResource.objects.count()
        print("LibraryResource table already exists!")
        return True
    except Exception as e:
        print(f"Table doesn't exist: {e}")
        
        # Create the table using Django's schema editor
        from django.db import connection
        from django.db.migrations.state import ProjectState
        from django.db.migrations.migration import Migration
        from django.db.migrations.operations import CreateModel
        
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(LibraryResource)
            print("LibraryResource table created successfully!")
            
        # Mark the migration as applied
        from django.db.migrations.recorder import MigrationRecorder
        recorder = MigrationRecorder(connection)
        recorder.record_applied('college_website', '0006_admissioninfo_alumniprofile_elearningcourse_and_more')
        print("Migration marked as applied!")
        
        return True

if __name__ == '__main__':
    create_missing_table()
