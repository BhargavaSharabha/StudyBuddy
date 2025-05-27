#!/usr/bin/env python
"""
Data migration script for StudyBuddy application.
This script helps migrate data from SQLite to PostgreSQL.

Usage:
1. Export data from SQLite: python scripts/migrate_data.py export
2. Import data to PostgreSQL: python scripts/migrate_data.py import
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjStudyBuddy.settings.development')
django.setup()

from django.core.management import call_command
from django.conf import settings

def export_data():
    """Export data from current database to fixtures."""
    print("Exporting data from SQLite database...")
    
    # Create fixtures directory if it doesn't exist
    fixtures_dir = project_root / 'fixtures'
    fixtures_dir.mkdir(exist_ok=True)
    
    # Export all data except contenttypes and auth.permission
    fixture_file = fixtures_dir / 'data_export.json'
    
    try:
        call_command(
            'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '--exclude=contenttypes',
            '--exclude=auth.permission',
            '--exclude=sessions.session',
            '--output=str(fixture_file)',
            verbosity=2
        )
        print(f"Data exported successfully to {fixture_file}")
        return True
    except Exception as e:
        print(f"Error exporting data: {e}")
        return False

def import_data():
    """Import data from fixtures to current database."""
    print("Importing data to PostgreSQL database...")
    
    fixtures_dir = project_root / 'fixtures'
    fixture_file = fixtures_dir / 'data_export.json'
    
    if not fixture_file.exists():
        print(f"Fixture file not found: {fixture_file}")
        print("Please run 'python scripts/migrate_data.py export' first.")
        return False
    
    try:
        # Run migrations first
        print("Running migrations...")
        call_command('migrate', verbosity=2)
        
        # Load the data
        print("Loading data...")
        call_command('loaddata', str(fixture_file), verbosity=2)
        
        print("Data imported successfully!")
        return True
    except Exception as e:
        print(f"Error importing data: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/migrate_data.py [export|import]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'export':
        success = export_data()
    elif command == 'import':
        success = import_data()
    else:
        print("Invalid command. Use 'export' or 'import'.")
        sys.exit(1)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main() 