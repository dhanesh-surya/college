from django.core.management.base import BaseCommand
from college_website.models import Menu, MenuItem, Page


class Command(BaseCommand):
    help = 'Create test menu items and pages for testing dynamic navbar'
    
    def handle(self, *args, **options):
        # Create test pages first
        home_page, created = Page.objects.get_or_create(
            title="Home",
            slug="home",
            defaults={
                'meta_title': "Home - Chaitanya College",
                'meta_description': "Welcome to Chaitanya Science and Arts College",
                'is_active': True
            }
        )
        
        about_page, created = Page.objects.get_or_create(
            title="About Institution",
            slug="about-institution",
            defaults={
                'meta_title': "About Institution",
                'meta_description': "Learn about our institution",
                'is_active': True
            }
        )
        
        programs_page, created = Page.objects.get_or_create(
            title="Academic Programs",
            slug="academic-programs",
            defaults={
                'meta_title': "Academic Programs",
                'meta_description': "Our academic programs and courses",
                'is_active': True
            }
        )
        
        # Create test menus
        home_menu, created = Menu.objects.get_or_create(
            title="Home",
            slug="home",
            defaults={'ordering': 1, 'is_active': True}
        )
        
        about_menu, created = Menu.objects.get_or_create(
            title="About",
            slug="about",
            defaults={'ordering': 2, 'is_active': True}
        )
        
        academics_menu, created = Menu.objects.get_or_create(
            title="Academics",
            slug="academics",
            defaults={'ordering': 3, 'is_active': True}
        )
        
        # Create menu items
        home_item, created = MenuItem.objects.get_or_create(
            menu=home_menu,
            title="Home",
            slug="home",
            defaults={
                'path_type': 'internal',
                'page': home_page,
                'ordering': 1,
                'is_active': True
            }
        )
        
        about_item, created = MenuItem.objects.get_or_create(
            menu=about_menu,
            title="About Institution",
            slug="about-institution",
            defaults={
                'path_type': 'internal',
                'page': about_page,
                'ordering': 1,
                'is_active': True
            }
        )
        
        # Create submenu items for About
        vision_item, created = MenuItem.objects.get_or_create(
            menu=about_menu,
            parent=about_item,
            title="Vision & Mission",
            slug="vision-mission",
            defaults={
                'path_type': 'external',
                'external_url': '#vision-mission',
                'ordering': 1,
                'is_active': True
            }
        )
        
        history_item, created = MenuItem.objects.get_or_create(
            menu=about_menu,
            parent=about_item,
            title="History",
            slug="history",
            defaults={
                'path_type': 'external',
                'external_url': '#history',
                'ordering': 2,
                'is_active': True
            }
        )
        
        # Create academics menu items
        programs_item, created = MenuItem.objects.get_or_create(
            menu=academics_menu,
            title="Academic Programs",
            slug="programs",
            defaults={
                'path_type': 'internal',
                'page': programs_page,
                'ordering': 1,
                'is_active': True
            }
        )
        
        # Create submenus for academics
        undergraduate_item, created = MenuItem.objects.get_or_create(
            menu=academics_menu,
            parent=programs_item,
            title="Undergraduate",
            slug="undergraduate",
            defaults={
                'path_type': 'external',
                'external_url': '#undergraduate',
                'ordering': 1,
                'is_active': True
            }
        )
        
        postgraduate_item, created = MenuItem.objects.get_or_create(
            menu=academics_menu,
            parent=programs_item,
            title="Postgraduate",
            slug="postgraduate",
            defaults={
                'path_type': 'external',
                'external_url': '#postgraduate',
                'ordering': 2,
                'is_active': True
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created test menus and menu items!')
        )
        
        # Display created items
        self.stdout.write('\nCreated Menus:')
        for menu in Menu.objects.filter(is_active=True):
            self.stdout.write(f'  - {menu.title} (URL: {menu.get_url()})')
            
        self.stdout.write('\nCreated Menu Items:')
        for item in MenuItem.objects.filter(is_active=True):
            indent = '    ' if item.parent else '  '
            self.stdout.write(f'{indent}- {item.title} (URL: {item.get_url()})')
