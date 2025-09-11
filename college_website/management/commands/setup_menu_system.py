from django.core.management.base import BaseCommand
from django.db import transaction
from college_website.models import MenuCategory, MenuSubmenu, MenuVisibilitySettings


class Command(BaseCommand):
    help = 'Setup the menu management system with existing navigation structure'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Setting up menu management system...')
        )
        
        with transaction.atomic():
            # Create default menu visibility settings
            self.create_default_settings()
            
            # Create menu categories and submenus
            self.create_menu_structure()
            
        self.stdout.write(
            self.style.SUCCESS('Menu management system setup completed successfully!')
        )

    def create_default_settings(self):
        """Create default menu visibility settings"""
        settings, created = MenuVisibilitySettings.objects.get_or_create(
            name="Default Menu Settings",
            defaults={
                'is_active': True,
                'show_research_menu': True,
                'show_placement_menu': True,
                'show_alumni_menu': True,
                'show_events_menu': True,
                'show_exam_timetable': True,
                'show_exam_revaluation': True,
                'show_exam_question_papers': True,
                'show_exam_rules': True,
                'show_student_portal': True,
                'show_sports_cultural': True,
                'show_nss_ncc': True,
                'show_research_centers': True,
                'show_publications': True,
                'show_patents_projects': True,
            }
        )
        
        if created:
            self.stdout.write('✓ Created default menu visibility settings')
        else:
            self.stdout.write('✓ Default menu visibility settings already exist')

    def create_menu_structure(self):
        """Create the complete menu structure based on your existing navbar"""
        
        # Home Menu
        home_category, created = MenuCategory.objects.get_or_create(
            slug='home',
            defaults={
                'name': 'Home',
                'icon_class': 'fas fa-home',
                'order': 1,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            self.create_submenus(home_category, [
                {'name': 'Homepage', 'url': '{% url "college_website:home" %}', 'icon_class': 'fas fa-home', 'group_header': 'Institution'},
                {'name': 'About Institution', 'url': '{% url "college_website:about" %}', 'icon_class': 'fas fa-university', 'group_header': 'Institution'},
                {'name': 'History', 'url': '/about/history/', 'icon_class': 'fas fa-history', 'group_header': 'Institution'},
                {'name': 'Principal\'s Message', 'url': '{% url "college_website:principal_message" %}', 'icon_class': 'fas fa-user-tie', 'group_header': 'Leadership'},
                {'name': 'Governing Body', 'url': '/about/governing-body/', 'icon_class': 'fas fa-users-cog', 'group_header': 'Leadership'},
            ])
            self.stdout.write('✓ Created Home menu category with submenus')

        # About Menu
        about_category, created = MenuCategory.objects.get_or_create(
            slug='about',
            defaults={
                'name': 'About',
                'icon_class': 'fas fa-info-circle',
                'order': 2,
                'is_active': True,
            }
        )
        
        if created:
            self.create_submenus(about_category, [
                {'name': 'Overview', 'url': '{% url "college_website:about" %}', 'icon_class': 'fas fa-university', 'group_header': 'Institution'},
                {'name': 'History', 'url': '/about/history/', 'icon_class': 'fas fa-history', 'group_header': 'Institution'},
                {'name': 'Vision & Mission', 'url': '/about/vision-mission/', 'icon_class': 'fas fa-bullseye', 'group_header': 'Institution'},
                {'name': 'Principal\'s Message', 'url': '{% url "college_website:principal_message" %}', 'icon_class': 'fas fa-user-tie', 'group_header': 'Leadership'},
                {'name': 'Director\'s Message', 'url': '{% url "college_website:director_message" %}', 'icon_class': 'fas fa-user-graduate', 'group_header': 'Leadership'},
            ])
            self.stdout.write('✓ Created About menu category with submenus')

        # Academics Menu
        academics_category, created = MenuCategory.objects.get_or_create(
            slug='academics',
            defaults={
                'name': 'Academics',
                'icon_class': 'fas fa-graduation-cap',
                'order': 3,
                'is_active': True,
            }
        )
        
        if created:
            self.create_submenus(academics_category, [
                {'name': 'All Programs', 'url': '{% url "college_website:programs_list" %}', 'icon_class': 'fas fa-list', 'group_header': 'Programs'},
                {'name': 'Science', 'url': '{% url "college_website:programs_list" %}?discipline=science', 'icon_class': 'fas fa-flask', 'group_header': 'Programs'},
                {'name': 'Arts', 'url': '{% url "college_website:programs_list" %}?discipline=arts', 'icon_class': 'fas fa-palette', 'group_header': 'Programs'},
                {'name': 'Commerce', 'url': '{% url "college_website:programs_list" %}?discipline=commerce', 'icon_class': 'fas fa-chart-line', 'group_header': 'Programs'},
                {'name': 'All Departments', 'url': '{% url "college_website:departments_list" %}', 'icon_class': 'fas fa-building', 'group_header': 'Departments'},
                {'name': 'Scholarships', 'url': '{% url "college_website:scholarships" %}', 'icon_class': 'fas fa-hand-holding-heart', 'group_header': 'Departments'},
            ])
            self.stdout.write('✓ Created Academics menu category with submenus')

        # Examinations Menu
        examinations_category, created = MenuCategory.objects.get_or_create(
            slug='examinations',
            defaults={
                'name': 'Examinations',
                'icon_class': 'fas fa-file-alt',
                'order': 4,
                'is_active': True,
            }
        )
        
        if created:
            self.create_submenus(examinations_category, [
                {'name': 'Notices', 'url': '/examinations/notices/', 'icon_class': 'fas fa-bell', 'group_header': 'Exam Information'},
                {'name': 'Timetable', 'url': '/examinations/timetable/', 'icon_class': 'fas fa-calendar-alt', 'group_header': 'Exam Information'},
                {'name': 'Question Papers', 'url': '/examinations/question-papers/', 'icon_class': 'fas fa-file-lines', 'group_header': 'Exam Information'},
                {'name': 'Results', 'url': '/examinations/results/', 'icon_class': 'fas fa-chart-bar', 'group_header': 'Exam Information'},
                {'name': 'Revaluation', 'url': '/examinations/revaluation/', 'icon_class': 'fas fa-sync-alt', 'group_header': 'Exam Information'},
                {'name': 'Rules', 'url': '/examinations/rules/', 'icon_class': 'fas fa-gavel', 'group_header': 'Exam Information'},
            ])
            self.stdout.write('✓ Created Examinations menu category with submenus')

        # Research Menu
        research_category, created = MenuCategory.objects.get_or_create(
            slug='research',
            defaults={
                'name': 'Research',
                'icon_class': 'fas fa-microscope',
                'order': 5,
                'is_active': True,
            }
        )
        
        if created:
            self.create_submenus(research_category, [
                {'name': 'Research Centers', 'url': '/research/centers/', 'icon_class': 'fas fa-building', 'group_header': 'Research Infrastructure'},
                {'name': 'Innovation & Incubation', 'url': '/research/innovation-incubation/', 'icon_class': 'fas fa-lightbulb', 'group_header': 'Research Infrastructure'},
                {'name': 'Publications', 'url': '/research/publications/', 'icon_class': 'fas fa-book-open', 'group_header': 'Research Output'},
                {'name': 'Patents & Projects', 'url': '/research/patents-projects/', 'icon_class': 'fas fa-certificate', 'group_header': 'Research Output'},
                {'name': 'Collaborations & MOUs', 'url': '/research/collaborations-mous/', 'icon_class': 'fas fa-handshake', 'group_header': 'Partnerships'},
                {'name': 'Consultancy', 'url': '/research/consultancy/', 'icon_class': 'fas fa-user-cog', 'group_header': 'Partnerships'},
            ])
            self.stdout.write('✓ Created Research menu category with submenus')

        # Student Support Menu
        student_support_category, created = MenuCategory.objects.get_or_create(
            slug='student-support',
            defaults={
                'name': 'Student Support',
                'icon_class': 'fas fa-users-cog',
                'order': 6,
                'is_active': True,
            }
        )
        
        if created:
            self.create_submenus(student_support_category, [
                {'name': 'Student Portal', 'url': '{% url "college_website:student_portal" %}', 'icon_class': 'fas fa-user-graduate', 'group_header': 'Student Services'},
                {'name': 'Library', 'url': '{% url "college_website:library" %}', 'icon_class': 'fas fa-book-reader', 'group_header': 'Student Services'},
                {'name': 'Sports & Cultural', 'url': '{% url "college_website:sports_cultural" %}', 'icon_class': 'fas fa-running', 'group_header': 'Student Services'},
                {'name': 'NSS, NCC & Clubs', 'url': '{% url "college_website:nss_ncc_clubs" %}', 'icon_class': 'fas fa-users', 'group_header': 'Student Services'},
                {'name': 'Placement Cell', 'url': '{% url "college_website:placement_cell" %}', 'icon_class': 'fas fa-briefcase', 'group_header': 'Student Services'},
                {'name': 'Alumni', 'url': '{% url "college_website:alumni" %}', 'icon_class': 'fas fa-user-tie', 'group_header': 'Student Services'},
            ])
            self.stdout.write('✓ Created Student Support menu category with submenus')

        # Events Menu
        events_category, created = MenuCategory.objects.get_or_create(
            slug='events',
            defaults={
                'name': 'Events',
                'icon_class': 'fas fa-calendar',
                'order': 7,
                'is_active': True,
            }
        )
        
        if created:
            self.create_submenus(events_category, [
                {'name': 'All Events', 'url': '{% url "college_website:events" %}', 'icon_class': 'fas fa-calendar-alt', 'group_header': 'Event Types'},
                {'name': 'Academic Events', 'url': '{% url "college_website:events" %}?type=academic', 'icon_class': 'fas fa-graduation-cap', 'group_header': 'Event Types'},
                {'name': 'Cultural Events', 'url': '{% url "college_website:events" %}?type=cultural', 'icon_class': 'fas fa-music', 'group_header': 'Event Types'},
                {'name': 'Sports Events', 'url': '{% url "college_website:events" %}?type=sports', 'icon_class': 'fas fa-trophy', 'group_header': 'Event Types'},
            ])
            self.stdout.write('✓ Created Events menu category with submenus')

        # Contact Menu
        contact_category, created = MenuCategory.objects.get_or_create(
            slug='contact',
            defaults={
                'name': 'Contact',
                'icon_class': 'fas fa-envelope',
                'order': 8,
                'is_active': True,
            }
        )
        
        if created:
            self.create_submenus(contact_category, [
                {'name': 'Contact Us', 'url': '{% url "college_website:contact" %}', 'icon_class': 'fas fa-envelope', 'group_header': 'Contact Information'},
                {'name': 'Location', 'url': '{% url "college_website:contact" %}#location', 'icon_class': 'fas fa-map-marker-alt', 'group_header': 'Contact Information'},
                {'name': 'Phone & Email', 'url': '{% url "college_website:contact" %}#contact', 'icon_class': 'fas fa-phone', 'group_header': 'Contact Information'},
            ])
            self.stdout.write('✓ Created Contact menu category with submenus')

    def create_submenus(self, category, submenu_data):
        """Create submenu items for a category"""
        for i, submenu_info in enumerate(submenu_data):
            MenuSubmenu.objects.get_or_create(
                category=category,
                name=submenu_info['name'],
                defaults={
                    'url': submenu_info['url'],
                    'icon_class': submenu_info['icon_class'],
                    'order': i + 1,
                    'is_active': True,
                    'group_header': submenu_info.get('group_header', ''),
                    'show_divider': False,
                }
            )
