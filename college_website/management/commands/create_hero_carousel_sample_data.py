from django.core.management.base import BaseCommand
from django.utils import timezone
from college_website.models import HeroCarouselSlide, HeroCarouselSettings


class Command(BaseCommand):
    help = 'Create sample hero carousel slides and settings'

    def handle(self, *args, **options):
        self.stdout.write('Creating hero carousel sample data...')
        
        # Create or get settings
        settings, created = HeroCarouselSettings.objects.get_or_create(
            pk=1,
            defaults={
                'is_enabled': True,
                'auto_play': True,
                'default_interval': 5000,
                'show_indicators': True,
                'show_controls': True,
                'pause_on_hover': True,
                'enable_keyboard': True,
                'enable_touch': True,
                'transition_duration': 600,
                'fade_effect': True,
                'mobile_height': '24rem',
                'tablet_height': '28rem',
                'desktop_height': '24rem',
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✓ Created hero carousel settings')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠ Hero carousel settings already exist')
            )
        
        # Create sample slides
        slides_data = [
            {
                'title': 'Transform Your Future with Quality Education',
                'subtitle': 'Discover 18+ courses across Science, Arts, Commerce, and Management programs designed for your success.',
                'slide_type': 'welcome',
                'is_active': True,
                'display_order': 0,
                'badge_text': 'Welcome to Excellence',
                'badge_icon': 'fas fa-star',
                'badge_color': '#FFD700',
                'primary_button_text': 'Explore Programs',
                'primary_button_url': '/programs/',
                'primary_button_icon': 'fas fa-graduation-cap',
                'primary_button_color': '#FFC107',
                'secondary_button_text': 'Learn More',
                'secondary_button_url': '/about/',
                'secondary_button_icon': 'fas fa-info-circle',
                'secondary_button_color': '#FFFFFF',
                'gradient_type': 'blue-purple',
                'show_statistics': True,
                'stat_1_number': '18+',
                'stat_1_label': 'Courses',
                'stat_1_icon': 'fas fa-graduation-cap',
                'stat_1_color': '#3B82F6',
                'stat_2_number': '5000+',
                'stat_2_label': 'Students',
                'stat_2_icon': 'fas fa-users',
                'stat_2_color': '#8B5CF6',
                'stat_3_number': '150+',
                'stat_3_label': 'Faculty',
                'stat_3_icon': 'fas fa-chalkboard-teacher',
                'stat_3_color': '#10B981',
                'stat_4_number': '25+',
                'stat_4_label': 'Years',
                'stat_4_icon': 'fas fa-award',
                'stat_4_color': '#F59E0B',
                'show_content_cards': False,
                'auto_play_interval': 5000,
                'show_indicators': True,
                'show_controls': True,
            },
            {
                'title': 'Start Your Academic Journey Today',
                'subtitle': 'Join thousands of successful graduates. Apply now for the upcoming academic session and secure your future.',
                'slide_type': 'admissions',
                'is_active': True,
                'display_order': 1,
                'badge_text': 'Admissions Open',
                'badge_icon': 'fas fa-door-open',
                'badge_color': '#10B981',
                'primary_button_text': 'Apply Now',
                'primary_button_url': '/admissions/',
                'primary_button_icon': 'fas fa-file-alt',
                'primary_button_color': '#10B981',
                'secondary_button_text': 'Online Application',
                'secondary_button_url': '/online-application/',
                'secondary_button_icon': 'fas fa-laptop',
                'secondary_button_color': '#FFFFFF',
                'gradient_type': 'green-teal',
                'show_statistics': False,
                'show_content_cards': True,
                'content_title': 'Why Choose Us?',
                'content_icon': 'fas fa-university',
                'content_items': '''
                    <ul class="tw-text-white tw-text-left tw-space-y-2">
                        <li class="tw-flex tw-items-center">
                            <i class="fas fa-check-circle tw-text-green-400 tw-mr-3"></i>
                            Accredited Programs
                        </li>
                        <li class="tw-flex tw-items-center">
                            <i class="fas fa-check-circle tw-text-green-400 tw-mr-3"></i>
                            Experienced Faculty
                        </li>
                        <li class="tw-flex tw-items-center">
                            <i class="fas fa-check-circle tw-text-green-400 tw-mr-3"></i>
                            Modern Infrastructure
                        </li>
                        <li class="tw-flex tw-items-center">
                            <i class="fas fa-check-circle tw-text-green-400 tw-mr-3"></i>
                            Placement Support
                        </li>
                    </ul>
                ''',
                'auto_play_interval': 5000,
                'show_indicators': True,
                'show_controls': True,
            },
            {
                'title': 'Innovation Through Research',
                'subtitle': 'Discover cutting-edge research opportunities, publications, and collaborative projects that shape the future.',
                'slide_type': 'research',
                'is_active': True,
                'display_order': 2,
                'badge_text': 'Research Excellence',
                'badge_icon': 'fas fa-microscope',
                'badge_color': '#8B5CF6',
                'primary_button_text': 'Explore Research',
                'primary_button_url': '/research/',
                'primary_button_icon': 'fas fa-flask',
                'primary_button_color': '#3B82F6',
                'secondary_button_text': 'Publications',
                'secondary_button_url': '/publications/',
                'secondary_button_icon': 'fas fa-book-open',
                'secondary_button_color': '#FFFFFF',
                'gradient_type': 'purple-pink',
                'show_statistics': False,
                'show_content_cards': True,
                'content_title': 'Research Areas',
                'content_icon': 'fas fa-lightbulb',
                'content_items': '''
                    <div class="tw-grid tw-grid-cols-2 tw-gap-3">
                        <div class="tw-bg-white tw-bg-opacity-10 tw-backdrop-blur-sm tw-rounded-lg tw-p-3 tw-text-center tw-text-white">
                            <i class="fas fa-lightbulb tw-text-2xl tw-mb-2 tw-text-yellow-400"></i>
                            <div class="tw-text-base tw-font-bold">Innovation</div>
                            <div class="tw-text-xs tw-opacity-80">Labs & Centers</div>
                        </div>
                        <div class="tw-bg-white tw-bg-opacity-10 tw-backdrop-blur-sm tw-rounded-lg tw-p-3 tw-text-center tw-text-white">
                            <i class="fas fa-handshake tw-text-2xl tw-mb-2 tw-text-blue-400"></i>
                            <div class="tw-text-base tw-font-bold">Collaboration</div>
                            <div class="tw-text-xs tw-opacity-80">Industry Partners</div>
                        </div>
                        <div class="tw-bg-white tw-bg-opacity-10 tw-backdrop-blur-sm tw-rounded-lg tw-p-3 tw-text-center tw-text-white">
                            <i class="fas fa-certificate tw-text-2xl tw-mb-2 tw-text-green-400"></i>
                            <div class="tw-text-base tw-font-bold">Patents</div>
                            <div class="tw-text-xs tw-opacity-80">Research Output</div>
                        </div>
                        <div class="tw-bg-white tw-bg-opacity-10 tw-backdrop-blur-sm tw-rounded-lg tw-p-3 tw-text-center tw-text-white">
                            <i class="fas fa-globe tw-text-2xl tw-mb-2 tw-text-purple-400"></i>
                            <div class="tw-text-base tw-font-bold">Global</div>
                            <div class="tw-text-xs tw-opacity-80">Recognition</div>
                        </div>
                    </div>
                ''',
                'auto_play_interval': 5000,
                'show_indicators': True,
                'show_controls': True,
            },
            {
                'title': 'Beyond Academics: Enriching Experiences',
                'subtitle': 'Join clubs, participate in sports, cultural events, and community service. Make memories that last a lifetime.',
                'slide_type': 'student_life',
                'is_active': True,
                'display_order': 3,
                'badge_text': 'Student Life',
                'badge_icon': 'fas fa-heart',
                'badge_color': '#F59E0B',
                'primary_button_text': 'Sports & Culture',
                'primary_button_url': '/sports-cultural/',
                'primary_button_icon': 'fas fa-running',
                'primary_button_color': '#F59E0B',
                'secondary_button_text': 'Clubs & Activities',
                'secondary_button_url': '/nss-ncc-clubs/',
                'secondary_button_icon': 'fas fa-users',
                'secondary_button_color': '#FFFFFF',
                'gradient_type': 'orange-red',
                'show_statistics': False,
                'show_content_cards': True,
                'content_title': 'Student Activities',
                'content_icon': 'fas fa-heart',
                'content_items': '''
                    <div class="tw-grid tw-grid-cols-3 tw-gap-2">
                        <div class="tw-bg-white tw-bg-opacity-10 tw-backdrop-blur-sm tw-rounded-lg tw-p-3 tw-text-center tw-text-white">
                            <i class="fas fa-futbol tw-text-xl tw-mb-1 tw-text-green-400"></i>
                            <div class="tw-text-xs tw-font-bold">Sports</div>
                        </div>
                        <div class="tw-bg-white tw-bg-opacity-10 tw-backdrop-blur-sm tw-rounded-lg tw-p-3 tw-text-center tw-text-white">
                            <i class="fas fa-music tw-text-xl tw-mb-1 tw-text-purple-400"></i>
                            <div class="tw-text-xs tw-font-bold">Music</div>
                        </div>
                        <div class="tw-bg-white tw-bg-opacity-10 tw-backdrop-blur-sm tw-rounded-lg tw-p-3 tw-text-center tw-text-white">
                            <i class="fas fa-palette tw-text-xl tw-mb-1 tw-text-pink-400"></i>
                            <div class="tw-text-xs tw-font-bold">Arts</div>
                        </div>
                        <div class="tw-bg-white tw-bg-opacity-10 tw-backdrop-blur-sm tw-rounded-lg tw-p-3 tw-text-center tw-text-white">
                            <i class="fas fa-users tw-text-xl tw-mb-1 tw-text-blue-400"></i>
                            <div class="tw-text-xs tw-font-bold">NSS</div>
                        </div>
                        <div class="tw-bg-white tw-bg-opacity-10 tw-backdrop-blur-sm tw-rounded-lg tw-p-3 tw-text-center tw-text-white">
                            <i class="fas fa-flag tw-text-xl tw-mb-1 tw-text-red-400"></i>
                            <div class="tw-text-xs tw-font-bold">NCC</div>
                        </div>
                        <div class="tw-bg-white tw-bg-opacity-10 tw-backdrop-blur-sm tw-rounded-lg tw-p-3 tw-text-center tw-text-white">
                            <i class="fas fa-camera tw-text-xl tw-mb-1 tw-text-yellow-400"></i>
                            <div class="tw-text-xs tw-font-bold">Events</div>
                        </div>
                    </div>
                ''',
                'auto_play_interval': 5000,
                'show_indicators': True,
                'show_controls': True,
            }
        ]
        
        created_count = 0
        for slide_data in slides_data:
            slide, created = HeroCarouselSlide.objects.get_or_create(
                title=slide_data['title'],
                defaults=slide_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created slide: {slide.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Slide already exists: {slide.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Successfully created {created_count} new hero carousel slides!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Hero carousel is now ready for use. Visit the admin panel to customize slides.'
            )
        )

