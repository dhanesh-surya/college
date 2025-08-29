from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from college_website.models import (
    CollegeInfo, Program, Event, Notice, SocialInitiative,
    StudentTestimonial, ImportantLink, Menu, MenuItem, Page,
    BlockRichText
)


class Command(BaseCommand):
    help = 'Seed the database with demo data for Chaitanya Science and Arts College'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting demo data creation...'))

        # Create College Info
        college_info, created = CollegeInfo.objects.get_or_create(
            name="Chaitanya Science and Arts College",
            defaults={
                'establishment_year': 2001,
                'affiliation': "Shaheed Nandkumar Patel Vishwavidyalaya, Raigarh",
                'address_line': "Pamgarh, Janjgir Champa, Chhattisgarh, India, 495554",
                'email': "chaitanyapamgarh@gmail.com",
                'phone': "+91-9425540666",
                'mission_statement_short': "Empowering rural youth through quality education and fostering academic excellence in the heart of Chhattisgarh.",
                'mission_statement_long': "Our mission is to provide accessible, affordable, and quality higher education to students from rural backgrounds, enabling them to compete globally while staying rooted in their cultural values.",
                'founder_name': "Mr Veerendra Tiwari",
                'founder_message': "Education is the most powerful weapon which you can use to change the world. Our college stands as a beacon of hope for rural youth, providing them with opportunities to excel and contribute to society.",
                'principal_name': "Dr Vinod Kumar Gupta",
                'principal_message': "At Chaitanya College, we believe in nurturing not just academic excellence but also character development. Our students are prepared to face the challenges of the modern world while maintaining their ethical foundation.",
                'courses_count': "18+",
                'students_count': "8000+",
                'faculty_staff_count': "50+",
                'years_of_excellence': "25+",
                'naac_grade': "NAAC GRADE A AWARD",
                'iic_rating': "3 Star Rating IIC",
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ College Info created'))

        # Create Programs
        programs_data = [
            ('M.Sc. Botany', 'science', 'Advanced study of plant sciences with research opportunities', '2 Years'),
            ('M.Sc. Chemistry', 'science', 'Comprehensive chemistry program with laboratory work', '2 Years'),
            ('M.Sc. Physics', 'science', 'Physics program focusing on theoretical and applied physics', '2 Years'),
            ('M.Sc. Mathematics', 'science', 'Advanced mathematics with computational applications', '2 Years'),
            ('M.A. Sociology', 'arts', 'Study of society, social behavior, and social change', '2 Years'),
            ('M.A. Political Science', 'arts', 'Political theory, governance, and public administration', '2 Years'),
            ('M.A. History', 'arts', 'Historical research and cultural studies', '2 Years'),
            ('M.A. English', 'arts', 'Literature, linguistics, and communication skills', '2 Years'),
            ('M.A. Hindi', 'arts', 'Hindi literature and language studies', '2 Years'),
            ('MSW', 'arts', 'Master of Social Work - community development and social welfare', '2 Years'),
            ('B.Sc. Biology', 'science', 'Undergraduate biology with focus on life sciences', '3 Years'),
            ('B.Sc. Chemistry', 'science', 'Undergraduate chemistry program', '3 Years'),
            ('B.Sc. Physics', 'science', 'Undergraduate physics program', '3 Years'),
            ('B.Sc. Mathematics', 'science', 'Undergraduate mathematics program', '3 Years'),
            ('B.A.', 'arts', 'Bachelor of Arts with multiple specializations', '3 Years'),
            ('B.Com.', 'commerce', 'Bachelor of Commerce - business and accounting', '3 Years'),
            ('DCA', 'management', 'Diploma in Computer Applications', '1 Year'),
            ('PGDCA', 'management', 'Post Graduate Diploma in Computer Applications', '1 Year'),
        ]

        for name, discipline, description, duration in programs_data:
            Program.objects.get_or_create(
                name=name,
                defaults={
                    'discipline': discipline,
                    'description': description,
                    'duration': duration,
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(programs_data)} Programs created'))

        # Create Events
        events_data = [
            ('Chaitanya Scholarship Entrance Exam 2025', 'exam', 'Annual scholarship examination for deserving students', date.today() + timedelta(days=30)),
            ('World Quantum Day Celebration', 'celebration', 'Celebrating quantum physics and its applications', date.today() + timedelta(days=45)),
            ('First Semester UG Practical Dates', 'exam', 'Practical examination schedule for undergraduate students', date.today() + timedelta(days=60)),
            ('Annual Sports Meet 2025', 'other', 'Inter-college sports competition and cultural events', date.today() + timedelta(days=90)),
            ('Science Exhibition', 'workshop', 'Student science projects and innovations showcase', date.today() + timedelta(days=120)),
            ('Foundation Day Celebration', 'foundation', 'Celebrating 25 years of educational excellence', date.today() + timedelta(days=150)),
        ]

        for title, event_type, description, event_date in events_data:
            Event.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'date': event_date,
                    'type': event_type,
                    'location': 'College Auditorium',
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(events_data)} Events created'))

        # Create Notices
        notices_data = [
            ('Practical Exam Time-Table First Semester UG', 'exam', 'Time table for first semester undergraduate practical examinations has been published.'),
            ('Admission Open for Session 2025-26', 'admission', 'Online admission process has started for all undergraduate and postgraduate programs.'),
            ('NEP 2020 Implementation Guidelines', 'policy', 'New Education Policy 2020 implementation guidelines for students and faculty.'),
            ('Library Renovation Notice', 'general', 'Central library will be closed for renovation from next week.'),
            ('University Examination Schedule', 'university', 'Final examination schedule released by the university.'),
            ('Scholarship Application Deadline', 'general', 'Last date for scholarship applications is approaching.'),
            ('Faculty Development Program', 'general', 'Professional development workshop for faculty members.'),
            ('Student Council Elections', 'general', 'Annual student council election nominations are open.'),
        ]

        for title, category, content in notices_data:
            Notice.objects.get_or_create(
                title=title,
                defaults={
                    'content': content,
                    'category': category,
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(notices_data)} Notices created'))

        # Create Social Initiatives
        social_initiatives = [
            ('Beti Bachao Beti Padhao', 'A national initiative to promote girl child education and empowerment. Our college actively participates in awareness campaigns and provides special support for female students.'),
            ('National Service Scheme (NSS)', 'Community service program where students engage in social work, environmental conservation, and rural development activities to build character and social responsibility.'),
        ]

        for name, description in social_initiatives:
            SocialInitiative.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(social_initiatives)} Social Initiatives created'))

        # Create Student Testimonials
        testimonials_data = [
            ('Priya Sharma', 'M.Sc. Botany (2022-24)', 'The faculty at Chaitanya College is exceptional. They provided me with excellent guidance for my research work and helped me secure admission in a PhD program.', 5),
            ('Rahul Verma', 'B.Sc. Physics (2020-23)', 'Great learning environment with modern labs. The college helped me build a strong foundation in physics and I am now working as a research assistant.', 5),
            ('Anita Patel', 'MSW (2021-23)', 'The social work program here is comprehensive and practical. I learned valuable skills that help me in my current job with an NGO.', 4),
            ('Suresh Kumar', 'M.A. Political Science (2019-21)', 'Excellent faculty and good library facilities. The college provided me with opportunities to participate in debates and conferences.', 4),
            ('Kavita Singh', 'B.Com. (2018-21)', 'The commerce department has experienced teachers who made complex topics easy to understand. I am now working in a reputed company.', 5),
        ]

        for name, program, feedback, rating in testimonials_data:
            StudentTestimonial.objects.get_or_create(
                student_name=name,
                program_studied=program,
                defaults={
                    'feedback_text': feedback,
                    'rating': rating,
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(testimonials_data)} Testimonials created'))

        # Create Important Links
        important_links = [
            ('www.snpv.ac.in', 'http://www.snpv.ac.in', 'important'),
            ('www.ugc.gov.in', 'https://www.ugc.gov.in', 'important'),
            ('www.naac-india.org', 'https://www.naac-india.org', 'important'),
            ('Admission Online', '#', 'quick'),
            ('Events', '/events/', 'quick'),
            ('Notices', '/notices/', 'quick'),
            ('NEP 2020', 'https://www.education.gov.in/nep', 'quick'),
            ('University Notices', 'http://www.snpv.ac.in', 'quick'),
        ]

        for name, url, link_type in important_links:
            ImportantLink.objects.get_or_create(
                name=name,
                defaults={
                    'url': url,
                    'type': link_type,
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(important_links)} Important Links created'))

        # Create Sample Pages and Menu
        main_menu, created = Menu.objects.get_or_create(
            title="Main Navigation",
            defaults={'is_active': True, 'ordering': 1}
        )

        # Create sample pages
        about_page, created = Page.objects.get_or_create(
            title="About Us",
            defaults={
                'meta_description': 'Learn about Chaitanya Science and Arts College history, mission, and values.',
                'is_active': True
            }
        )

        if created:
            BlockRichText.objects.create(
                page=about_page,
                title="College History",
                body="<p>Chaitanya Science and Arts College was established in 2001 with a vision to provide quality higher education to rural youth. Over the years, we have grown to become one of the leading colleges in Chhattisgarh.</p>",
                ordering=1,
                is_active=True
            )

        # Create menu items
        MenuItem.objects.get_or_create(
            menu=main_menu,
            title="About Us",
            defaults={
                'path_type': 'internal',
                'page': about_page,
                'is_active': True,
                'ordering': 1
            }
        )

        self.stdout.write(self.style.SUCCESS('✓ Sample pages and menu created'))
        self.stdout.write(self.style.SUCCESS('Demo data creation completed successfully!'))
        self.stdout.write(self.style.WARNING('You can now access the admin panel to manage content.'))
