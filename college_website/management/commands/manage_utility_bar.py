"""
Django management command for Top Utility Bar operations
Usage: python manage.py manage_utility_bar <action> [options]
"""

import json
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.core.exceptions import ValidationError
from college_website.models import TopUtilityBar
from college_website.signals import UtilityBarManager
from college_website.validators import TopUtilityBarValidator


class Command(BaseCommand):
    help = 'Manage Top Utility Bar configurations'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            type=str,
            choices=[
                'list', 'activate', 'deactivate', 'validate', 'stats',
                'create', 'delete', 'duplicate', 'export', 'import'
            ],
            help='Action to perform'
        )
        
        parser.add_argument(
            '--id',
            type=int,
            help='Utility bar ID for operations that require it'
        )
        
        parser.add_argument(
            '--name',
            type=str,
            help='Name for new utility bar or filter for listing'
        )
        
        parser.add_argument(
            '--file',
            type=str,
            help='JSON file path for import/export operations'
        )
        
        parser.add_argument(
            '--active-only',
            action='store_true',
            help='Show only active utility bars'
        )
        
        parser.add_argument(
            '--inactive-only',
            action='store_true',
            help='Show only inactive utility bars'
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force operations that might be destructive'
        )

    def handle(self, *args, **options):
        action = options['action']
        
        try:
            if action == 'list':
                self.list_utility_bars(options)
            elif action == 'activate':
                self.activate_utility_bar(options)
            elif action == 'deactivate':
                self.deactivate_utility_bars(options)
            elif action == 'validate':
                self.validate_utility_bars(options)
            elif action == 'stats':
                self.show_stats(options)
            elif action == 'create':
                self.create_utility_bar(options)
            elif action == 'delete':
                self.delete_utility_bar(options)
            elif action == 'duplicate':
                self.duplicate_utility_bar(options)
            elif action == 'export':
                self.export_utility_bars(options)
            elif action == 'import':
                self.import_utility_bars(options)
                
        except CommandError:
            raise
        except Exception as e:
            raise CommandError(f'Error executing {action}: {str(e)}')

    def list_utility_bars(self, options):
        """List all utility bars"""
        queryset = TopUtilityBar.objects.all()
        
        if options.get('active_only'):
            queryset = queryset.filter(is_active=True)
        elif options.get('inactive_only'):
            queryset = queryset.filter(is_active=False)
            
        if options.get('name'):
            queryset = queryset.filter(name__icontains=options['name'])
        
        if not queryset.exists():
            self.stdout.write(
                self.style.WARNING('No utility bars found matching the criteria.')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(f'Found {queryset.count()} utility bar(s):')
        )
        self.stdout.write('')
        
        for bar in queryset.order_by('-is_active', '-updated_at'):
            status = self.style.SUCCESS('ACTIVE') if bar.is_active else self.style.ERROR('INACTIVE')
            
            features = []
            if bar.show_social_icons:
                social_count = sum(1 for url in [
                    bar.facebook_url, bar.twitter_url, bar.instagram_url,
                    bar.youtube_url, bar.linkedin_url
                ] if url)
                if social_count > 0:
                    features.append(f'Social({social_count})')
            
            if bar.show_contact_info:
                contact_count = sum(1 for info in [bar.contact_phone, bar.contact_email] if info)
                if contact_count > 0:
                    features.append(f'Contact({contact_count})')
            
            if bar.show_custom_links:
                link_count = sum(1 for text, url in [
                    (bar.custom_link_1_text, bar.custom_link_1_url),
                    (bar.custom_link_2_text, bar.custom_link_2_url),
                    (bar.custom_link_3_text, bar.custom_link_3_url)
                ] if text and url)
                if link_count > 0:
                    features.append(f'Links({link_count})')
            
            features_str = ' | '.join(features) if features else 'No features'
            
            self.stdout.write(
                f'ID: {bar.pk:3d} | {status} | {bar.name:30s} | {bar.position:12s} | {features_str}'
            )
            self.stdout.write(
                f'           Created: {bar.created_at.strftime("%Y-%m-%d %H:%M")} | '
                f'Updated: {bar.updated_at.strftime("%Y-%m-%d %H:%M")}'
            )
            self.stdout.write('')

    def activate_utility_bar(self, options):
        """Activate a specific utility bar"""
        if not options.get('id'):
            raise CommandError('--id is required for activate action')
        
        success, message = UtilityBarManager.activate_utility_bar(options['id'])
        
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))

    def deactivate_utility_bars(self, options):
        """Deactivate utility bars"""
        if options.get('id'):
            # Deactivate specific utility bar
            try:
                bar = TopUtilityBar.objects.get(pk=options['id'])
                bar.is_active = False
                bar.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Utility bar "{bar.name}" deactivated successfully.')
                )
            except TopUtilityBar.DoesNotExist:
                raise CommandError(f'Utility bar with ID {options["id"]} not found')
        else:
            # Deactivate all utility bars
            success, message = UtilityBarManager.deactivate_all_utility_bars()
            
            if success:
                self.stdout.write(self.style.SUCCESS(message))
            else:
                self.stdout.write(self.style.ERROR(message))

    def validate_utility_bars(self, options):
        """Validate all utility bars"""
        issues = UtilityBarManager.validate_all_utility_bars()
        
        if not issues:
            self.stdout.write(
                self.style.SUCCESS('All utility bars are valid!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Found validation issues in {len(issues)} utility bar(s):')
            )
            self.stdout.write('')
            
            for issue in issues:
                self.stdout.write(
                    self.style.ERROR(f'Utility Bar: {issue["utility_bar"]}')
                )
                
                errors = issue['errors']
                if isinstance(errors, dict):
                    for field, error_list in errors.items():
                        if isinstance(error_list, list):
                            for error in error_list:
                                self.stdout.write(f'  {field}: {error}')
                        else:
                            self.stdout.write(f'  {field}: {error_list}')
                else:
                    for error in errors:
                        self.stdout.write(f'  {error}')
                
                self.stdout.write('')

    def show_stats(self, options):
        """Show utility bar statistics"""
        stats = UtilityBarManager.get_utility_bar_stats()
        
        self.stdout.write(self.style.SUCCESS('Top Utility Bar Statistics:'))
        self.stdout.write('')
        self.stdout.write(f'Total Configurations: {stats["total"]}')
        self.stdout.write(f'Active Configurations: {stats["active"]}')
        self.stdout.write(f'Inactive Configurations: {stats["inactive"]}')
        self.stdout.write(f'Has Active Configuration: {"Yes" if stats["has_active"] else "No"}')
        
        if stats['total'] > 0:
            # Additional stats
            bars = TopUtilityBar.objects.all()
            
            social_enabled = bars.filter(show_social_icons=True).count()
            contact_enabled = bars.filter(show_contact_info=True).count()
            links_enabled = bars.filter(show_custom_links=True).count()
            mobile_enabled = bars.filter(show_on_mobile=True).count()
            
            self.stdout.write('')
            self.stdout.write('Feature Usage:')
            self.stdout.write(f'  Social Icons: {social_enabled}/{stats["total"]} configurations')
            self.stdout.write(f'  Contact Info: {contact_enabled}/{stats["total"]} configurations')
            self.stdout.write(f'  Custom Links: {links_enabled}/{stats["total"]} configurations')
            self.stdout.write(f'  Mobile Display: {mobile_enabled}/{stats["total"]} configurations')

    def create_utility_bar(self, options):
        """Create a new utility bar"""
        if not options.get('name'):
            raise CommandError('--name is required for create action')
        
        # Create with default settings
        utility_bar = TopUtilityBar.objects.create(
            name=options['name'],
            is_active=False,  # Create inactive by default
            background_color='#0d6efd',
            text_color='#ffffff',
            height=40,
            position='top',
            show_social_icons=True,
            show_contact_info=True,
            show_custom_links=True,
            show_on_mobile=True,
            mobile_collapsed=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Utility bar "{utility_bar.name}" created successfully with ID {utility_bar.pk}')
        )
        self.stdout.write(
            self.style.WARNING('Note: The utility bar is created as inactive. Use --id {} activate to enable it.'.format(utility_bar.pk))
        )

    def delete_utility_bar(self, options):
        """Delete a utility bar"""
        if not options.get('id'):
            raise CommandError('--id is required for delete action')
        
        try:
            bar = TopUtilityBar.objects.get(pk=options['id'])
            
            if bar.is_active and not options.get('force'):
                raise CommandError(
                    f'Cannot delete active utility bar "{bar.name}". '
                    'Use --force to delete anyway or deactivate it first.'
                )
            
            bar_name = bar.name
            bar.delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Utility bar "{bar_name}" deleted successfully.')
            )
            
        except TopUtilityBar.DoesNotExist:
            raise CommandError(f'Utility bar with ID {options["id"]} not found')

    def duplicate_utility_bar(self, options):
        """Duplicate a utility bar"""
        if not options.get('id'):
            raise CommandError('--id is required for duplicate action')
        
        new_name = options.get('name')
        success, message = UtilityBarManager.duplicate_utility_bar(options['id'], new_name)
        
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))

    def export_utility_bars(self, options):
        """Export utility bars to JSON file"""
        file_path = options.get('file', f'utility_bars_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json')
        
        queryset = TopUtilityBar.objects.all()
        
        if options.get('active_only'):
            queryset = queryset.filter(is_active=True)
        elif options.get('inactive_only'):
            queryset = queryset.filter(is_active=False)
        
        export_data = []
        for bar in queryset:
            data = {
                'name': bar.name,
                'background_color': bar.background_color,
                'text_color': bar.text_color,
                'height': bar.height,
                'position': bar.position,
                'show_social_icons': bar.show_social_icons,
                'facebook_url': bar.facebook_url,
                'twitter_url': bar.twitter_url,
                'instagram_url': bar.instagram_url,
                'youtube_url': bar.youtube_url,
                'linkedin_url': bar.linkedin_url,
                'show_contact_info': bar.show_contact_info,
                'contact_phone': bar.contact_phone,
                'contact_email': bar.contact_email,
                'show_custom_links': bar.show_custom_links,
                'custom_link_1_text': bar.custom_link_1_text,
                'custom_link_1_url': bar.custom_link_1_url,
                'custom_link_2_text': bar.custom_link_2_text,
                'custom_link_2_url': bar.custom_link_2_url,
                'custom_link_3_text': bar.custom_link_3_text,
                'custom_link_3_url': bar.custom_link_3_url,
                'show_on_mobile': bar.show_on_mobile,
                'mobile_collapsed': bar.mobile_collapsed,
                'is_active': bar.is_active,
                'created_at': bar.created_at.isoformat() if hasattr(bar, 'created_at') else None,
                'updated_at': bar.updated_at.isoformat() if hasattr(bar, 'updated_at') else None,
            }
            export_data.append(data)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.stdout.write(
                self.style.SUCCESS(f'{len(export_data)} utility bar(s) exported to {file_path}')
            )
            
        except Exception as e:
            raise CommandError(f'Error writing to file {file_path}: {str(e)}')

    def import_utility_bars(self, options):
        """Import utility bars from JSON file"""
        file_path = options.get('file')
        if not file_path:
            raise CommandError('--file is required for import action')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
        except FileNotFoundError:
            raise CommandError(f'File {file_path} not found')
        except json.JSONDecodeError as e:
            raise CommandError(f'Invalid JSON in {file_path}: {str(e)}')
        
        if not isinstance(import_data, list):
            raise CommandError('JSON file must contain a list of utility bar configurations')
        
        imported_count = 0
        errors = []
        
        for i, bar_data in enumerate(import_data):
            try:
                # Remove ID-related fields
                bar_data.pop('id', None)
                bar_data.pop('created_at', None)
                bar_data.pop('updated_at', None)
                
                # Ensure name is unique
                original_name = bar_data.get('name', f'Imported Bar {i+1}')
                name = original_name
                counter = 1
                
                while TopUtilityBar.objects.filter(name=name).exists():
                    name = f"{original_name} ({counter})"
                    counter += 1
                
                bar_data['name'] = name
                
                # Create inactive by default
                bar_data['is_active'] = False
                
                # Create the utility bar
                utility_bar = TopUtilityBar(**bar_data)
                utility_bar.full_clean()  # Validate
                utility_bar.save()
                
                imported_count += 1
                
                self.stdout.write(f'✓ Imported: {utility_bar.name}')
                
            except ValidationError as e:
                error_msg = f'Validation error for item {i+1}: {e}'
                errors.append(error_msg)
                self.stdout.write(self.style.ERROR(f'✗ {error_msg}'))
                
            except Exception as e:
                error_msg = f'Error importing item {i+1}: {str(e)}'
                errors.append(error_msg)
                self.stdout.write(self.style.ERROR(f'✗ {error_msg}'))
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(f'{imported_count} utility bar(s) imported successfully.')
        )
        
        if errors:
            self.stdout.write(
                self.style.WARNING(f'{len(errors)} error(s) encountered during import.')
            )

    def activate_utility_bar(self, options):
        """Activate a specific utility bar"""
        if not options.get('id'):
            raise CommandError('--id is required for activate action')
        
        success, message = UtilityBarManager.activate_utility_bar(options['id'])
        
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            raise CommandError(message)

    def deactivate_utility_bars(self, options):
        """Deactivate utility bars"""
        if options.get('id'):
            # Deactivate specific utility bar
            try:
                bar = TopUtilityBar.objects.get(pk=options['id'])
                bar.is_active = False
                bar.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Utility bar "{bar.name}" deactivated successfully.')
                )
            except TopUtilityBar.DoesNotExist:
                raise CommandError(f'Utility bar with ID {options["id"]} not found')
        else:
            # Deactivate all utility bars
            if not options.get('force'):
                self.stdout.write(
                    self.style.WARNING('This will deactivate ALL utility bars. Use --force to confirm.')
                )
                return
            
            success, message = UtilityBarManager.deactivate_all_utility_bars()
            
            if success:
                self.stdout.write(self.style.SUCCESS(message))
            else:
                raise CommandError(message)

    def validate_utility_bars(self, options):
        """Validate all utility bars"""
        self.stdout.write('Validating all utility bars...')
        self.stdout.write('')
        
        issues = UtilityBarManager.validate_all_utility_bars()
        
        if not issues:
            self.stdout.write(
                self.style.SUCCESS('✓ All utility bars passed validation!')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'✗ Found validation issues in {len(issues)} utility bar(s):')
            )
            self.stdout.write('')
            
            for issue in issues:
                self.stdout.write(
                    self.style.WARNING(f'Utility Bar: {issue["utility_bar"]}')
                )
                
                errors = issue['errors']
                if isinstance(errors, dict):
                    for field, error_list in errors.items():
                        if isinstance(error_list, list):
                            for error in error_list:
                                self.stdout.write(f'  {field}: {error}')
                        else:
                            self.stdout.write(f'  {field}: {error_list}')
                else:
                    for error in errors:
                        self.stdout.write(f'  {error}')
                
                self.stdout.write('')

    def show_stats(self, options):
        """Show comprehensive statistics"""
        stats = UtilityBarManager.get_utility_bar_stats()
        
        self.stdout.write(self.style.SUCCESS('=== Top Utility Bar Statistics ==='))
        self.stdout.write('')
        
        # Basic stats
        self.stdout.write(f'Total Configurations: {stats["total"]}')
        self.stdout.write(f'Active: {stats["active"]}')
        self.stdout.write(f'Inactive: {stats["inactive"]}')
        self.stdout.write(f'Has Active: {"Yes" if stats["has_active"] else "No"}')
        
        if stats['total'] > 0:
            # Feature usage stats
            bars = TopUtilityBar.objects.all()
            
            social_enabled = bars.filter(show_social_icons=True).count()
            contact_enabled = bars.filter(show_contact_info=True).count()
            links_enabled = bars.filter(show_custom_links=True).count()
            mobile_enabled = bars.filter(show_on_mobile=True).count()
            
            self.stdout.write('')
            self.stdout.write('Feature Usage:')
            self.stdout.write(f'  Social Icons: {social_enabled}/{stats["total"]} ({social_enabled/stats["total"]*100:.1f}%)')
            self.stdout.write(f'  Contact Info: {contact_enabled}/{stats["total"]} ({contact_enabled/stats["total"]*100:.1f}%)')
            self.stdout.write(f'  Custom Links: {links_enabled}/{stats["total"]} ({links_enabled/stats["total"]*100:.1f}%)')
            self.stdout.write(f'  Mobile Display: {mobile_enabled}/{stats["total"]} ({mobile_enabled/stats["total"]*100:.1f}%)')
            
            # Position distribution
            self.stdout.write('')
            self.stdout.write('Position Distribution:')
            for position, display_name in TopUtilityBar._meta.get_field('position').choices:
                count = bars.filter(position=position).count()
                self.stdout.write(f'  {display_name}: {count}/{stats["total"]} ({count/stats["total"]*100:.1f}%)')
            
            # Recent activity
            recent_bars = bars.order_by('-updated_at')[:3]
            self.stdout.write('')
            self.stdout.write('Recently Updated:')
            for bar in recent_bars:
                status = "ACTIVE" if bar.is_active else "inactive"
                self.stdout.write(f'  {bar.name} ({status}) - {bar.updated_at.strftime("%Y-%m-%d %H:%M")}')

    def duplicate_utility_bar(self, options):
        """Duplicate a utility bar"""
        if not options.get('id'):
            raise CommandError('--id is required for duplicate action')
        
        new_name = options.get('name')
        success, message = UtilityBarManager.duplicate_utility_bar(options['id'], new_name)
        
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            raise CommandError(message)

    def create_utility_bar(self, options):
        """Create a new utility bar with basic configuration"""
        if not options.get('name'):
            raise CommandError('--name is required for create action')
        
        name = options['name']
        
        # Check if name already exists
        if TopUtilityBar.objects.filter(name=name).exists():
            raise CommandError(f'Utility bar with name "{name}" already exists')
        
        try:
            utility_bar = TopUtilityBar.objects.create(
                name=name,
                is_active=False,  # Create as inactive by default
                background_color='#0d6efd',
                text_color='#ffffff',
                height=40,
                position='top',
                show_social_icons=False,
                show_contact_info=False,
                show_custom_links=False,
                show_on_mobile=True,
                mobile_collapsed=True
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Utility bar "{utility_bar.name}" created successfully with ID {utility_bar.pk}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    f'The utility bar is created as inactive with minimal configuration. '
                    f'Use the admin interface or update command to configure features.'
                )
            )
            
        except ValidationError as e:
            raise CommandError(f'Validation error: {e}')
        except Exception as e:
            raise CommandError(f'Error creating utility bar: {str(e)}')
