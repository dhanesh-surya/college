from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from college_website.models import NSSNCCClub, NSSNCCNotice, NSSNCCGallery, NSSNCCAchievement


class Command(BaseCommand):
    help = 'Create sample data for NSS-NCC Clubs'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample NSS-NCC Clubs data...')
        
        # Create sample clubs
        clubs_data = [
            {
                'name': 'National Service Scheme (NSS)',
                'club_type': 'nss',
                'description': '<p>The National Service Scheme (NSS) is a Central Sector Scheme of Government of India, Ministry of Youth Affairs & Sports. It provides opportunity to the student youth of 11th & 12th Class of schools at +2 Board level and student youth of Technical Institution, Graduate & Post Graduate at colleges and University level of India to take part in various government led community service activities & programmes.</p>',
                'short_description': 'Community service and social responsibility through NSS activities',
                'coordinator_name': 'Dr. Rajesh Kumar',
                'coordinator_email': 'nss@college.edu',
                'coordinator_phone': '+91 9876543210',
                'main_activities': '<p><strong>Main Activities:</strong></p><ul><li>Blood Donation Camps</li><li>Tree Plantation Drives</li><li>Cleanliness Campaigns</li><li>Health Awareness Programs</li><li>Literacy Programs</li><li>Disaster Relief Activities</li></ul>',
                'upcoming_events': '<p><strong>Upcoming Events:</strong></p><ul><li>Annual NSS Camp - December 2024</li><li>Blood Donation Drive - November 2024</li><li>Tree Plantation Campaign - October 2024</li></ul>',
                'is_active': True,
                'is_featured': True,
                'display_order': 1,
            },
            {
                'name': 'National Cadet Corps (NCC)',
                'club_type': 'ncc',
                'description': '<p>The National Cadet Corps (NCC) is the youth wing of the Armed Forces with its headquarters at New Delhi, India. It is open to school and college students on voluntary basis. The NCC provides exposure to the cadets in a wide range of activities, with a distinct emphasis on Social Services, Discipline and Adventure Training.</p>',
                'short_description': 'Military training, discipline, and adventure activities through NCC',
                'coordinator_name': 'Col. Suresh Singh',
                'coordinator_email': 'ncc@college.edu',
                'coordinator_phone': '+91 9876543211',
                'main_activities': '<p><strong>Main Activities:</strong></p><ul><li>Military Training</li><li>Adventure Camps</li><li>Republic Day Parade</li><li>Social Service Activities</li><li>Leadership Development</li><li>Physical Fitness Programs</li></ul>',
                'upcoming_events': '<p><strong>Upcoming Events:</strong></p><ul><li>Annual Training Camp - January 2025</li><li>Republic Day Parade Practice - December 2024</li><li>Adventure Training Camp - November 2024</li></ul>',
                'is_active': True,
                'is_featured': True,
                'display_order': 2,
            },
            {
                'name': 'Technology Club',
                'club_type': 'tech',
                'description': '<p>The Technology Club is dedicated to fostering innovation and technical skills among students. We organize workshops, hackathons, and coding competitions to enhance students\' technical knowledge and prepare them for the digital future.</p>',
                'short_description': 'Innovation, coding, and technology workshops for students',
                'coordinator_name': 'Prof. Priya Sharma',
                'coordinator_email': 'techclub@college.edu',
                'coordinator_phone': '+91 9876543212',
                'main_activities': '<p><strong>Main Activities:</strong></p><ul><li>Programming Workshops</li><li>Hackathons</li><li>Tech Talks</li><li>Project Development</li><li>Industry Visits</li><li>Competition Preparation</li></ul>',
                'upcoming_events': '<p><strong>Upcoming Events:</strong></p><ul><li>Annual Hackathon - March 2025</li><li>AI/ML Workshop - February 2025</li><li>Web Development Bootcamp - January 2025</li></ul>',
                'is_active': True,
                'is_featured': False,
                'display_order': 3,
            },
            {
                'name': 'Cultural Club',
                'club_type': 'cultural',
                'description': '<p>The Cultural Club promotes artistic expression and cultural diversity on campus. We organize various cultural events, performances, and competitions to showcase the rich cultural heritage and talents of our students.</p>',
                'short_description': 'Cultural events, performances, and artistic expression',
                'coordinator_name': 'Dr. Anjali Gupta',
                'coordinator_email': 'cultural@college.edu',
                'coordinator_phone': '+91 9876543213',
                'main_activities': '<p><strong>Main Activities:</strong></p><ul><li>Dance Performances</li><li>Music Concerts</li><li>Drama Productions</li><li>Art Exhibitions</li><li>Cultural Festivals</li><li>Talent Shows</li></ul>',
                'upcoming_events': '<p><strong>Upcoming Events:</strong></p><ul><li>Annual Cultural Fest - April 2025</li><li>Classical Music Concert - March 2025</li><li>Art Exhibition - February 2025</li></ul>',
                'is_active': True,
                'is_featured': False,
                'display_order': 4,
            },
        ]
        
        # Create clubs
        created_clubs = []
        for club_data in clubs_data:
            club, created = NSSNCCClub.objects.get_or_create(
                name=club_data['name'],
                defaults=club_data
            )
            if created:
                self.stdout.write(f'Created club: {club.name}')
            else:
                self.stdout.write(f'Club already exists: {club.name}')
            created_clubs.append(club)
        
        # Create sample notices
        notices_data = [
            {
                'title': 'NSS Annual Camp 2024',
                'content': '<p>Registration for the annual NSS camp is now open. All interested students are requested to submit their applications by the end of this month. The camp will include various community service activities, leadership training, and team building exercises.</p>',
                'category': 'camp',
                'priority': 'high',
                'related_club': created_clubs[0],  # NSS
                'publish_date': timezone.now() - timedelta(days=2),
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'NCC Republic Day Parade Selection',
                'content': '<p>Selection trials for Republic Day parade participation will be conducted next week. NCC cadets are advised to prepare accordingly. This is a great opportunity to represent our college at the national level.</p>',
                'category': 'competition',
                'priority': 'urgent',
                'related_club': created_clubs[1],  # NCC
                'publish_date': timezone.now() - timedelta(days=7),
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'Tech Club Workshop Series',
                'content': '<p>Join our monthly tech workshops covering web development, mobile app development, and AI/ML. Open to all students. No prior experience required. Learn from industry experts and enhance your technical skills.</p>',
                'category': 'event',
                'priority': 'normal',
                'related_club': created_clubs[2],  # Tech Club
                'publish_date': timezone.now() - timedelta(days=14),
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'Cultural Club Auditions',
                'content': '<p>Cultural club is conducting auditions for new members. Students with talents in dance, music, drama, or art are encouraged to participate. Showcase your creativity and join our vibrant cultural community.</p>',
                'category': 'recruitment',
                'priority': 'normal',
                'related_club': created_clubs[3],  # Cultural Club
                'publish_date': timezone.now() - timedelta(days=30),
                'is_active': True,
                'is_featured': False,
            },
        ]
        
        # Create notices
        for notice_data in notices_data:
            notice, created = NSSNCCNotice.objects.get_or_create(
                title=notice_data['title'],
                defaults=notice_data
            )
            if created:
                self.stdout.write(f'Created notice: {notice.title}')
            else:
                self.stdout.write(f'Notice already exists: {notice.title}')
        
        # Create sample achievements
        achievements_data = [
            {
                'title': 'Best NSS Unit Award',
                'description': 'Our NSS unit received the Best NSS Unit Award for outstanding community service activities and social initiatives throughout the year.',
                'achievement_type': 'award',
                'related_club': created_clubs[0],  # NSS
                'achieved_by': 'NSS Unit Team',
                'achievement_date': datetime(2024, 8, 15).date(),
                'organization': 'Ministry of Youth Affairs & Sports',
                'is_active': True,
                'is_featured': True,
                'display_order': 1,
            },
            {
                'title': 'NCC Republic Day Parade Participation',
                'description': 'Our NCC cadets successfully participated in the Republic Day Parade in New Delhi, showcasing discipline and excellence.',
                'achievement_type': 'recognition',
                'related_club': created_clubs[1],  # NCC
                'achieved_by': 'NCC Cadets',
                'achievement_date': datetime(2024, 1, 26).date(),
                'organization': 'Ministry of Defence',
                'is_active': True,
                'is_featured': True,
                'display_order': 2,
            },
            {
                'title': 'National Hackathon Winners',
                'description': 'Our Tech Club team won first place in the National Student Hackathon 2024, developing an innovative solution for environmental monitoring.',
                'achievement_type': 'trophy',
                'related_club': created_clubs[2],  # Tech Club
                'achieved_by': 'Tech Club Team',
                'achievement_date': datetime(2024, 6, 20).date(),
                'organization': 'Ministry of Education',
                'is_active': True,
                'is_featured': True,
                'display_order': 3,
            },
        ]
        
        # Create achievements
        for achievement_data in achievements_data:
            achievement, created = NSSNCCAchievement.objects.get_or_create(
                title=achievement_data['title'],
                defaults=achievement_data
            )
            if created:
                self.stdout.write(f'Created achievement: {achievement.title}')
            else:
                self.stdout.write(f'Achievement already exists: {achievement.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample NSS-NCC Clubs data!')
        )
        self.stdout.write(f'Created {len(created_clubs)} clubs, {len(notices_data)} notices, and {len(achievements_data)} achievements.')
