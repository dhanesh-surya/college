#!/usr/bin/env python3
"""
Script to create sample history content data for testing
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from college_website.models import HistoryContent, TimelineEvent, Milestone

def create_sample_history_data():
    """Create comprehensive sample history content data"""
    
    # Delete existing data
    HistoryContent.objects.all().delete()
    print("Deleted existing history content data")
    
    # Create main history content
    history_content = HistoryContent.objects.create(
        name="Chaitanya College History - Main",
        is_active=True,
        
        # Hero Section
        hero_title="Our Inspiring Journey",
        hero_subtitle="Four decades of educational excellence, innovation, and community transformation through quality higher education",
        hero_badge_text="Heritage & Excellence",
        
        # Foundation Story
        foundation_title="The Foundation Story",
        foundation_content="""
        <p>Established in 1985 with a noble vision to democratize quality higher education in rural Karnataka, Chaitanya College began as a beacon of hope for aspiring students from farming and working-class families.</p>
        
        <p>Founded by visionary educators Dr. Rajesh Kumar and Prof. Sunita Sharma, our institution started with just 120 students in Arts and Science streams, housed in a modest two-story building surrounded by agricultural fields.</p>
        
        <p>From these humble beginnings, we have grown into a comprehensive educational institution serving over 3,000 students across multiple disciplines, while maintaining our core commitment to accessible, quality education.</p>
        """,
        establishment_year=1985,
        faculty_count=85,
        alumni_count=12000,
        accreditations="NAAC Grade A, UGC Recognition, State University Affiliation",
        
        # Timeline Section
        timeline_title="Journey Through Time",
        timeline_description="Milestones that shaped our growth from a small rural college to a recognized institution of higher learning",
        
        # Milestones Section
        milestones_title="Achievements & Recognition",
        milestones_description="Celebrating our institutional accomplishments and the recognition we've earned for educational excellence",
        
        # Legacy Section
        legacy_title="Building Tomorrow's Leaders",
        legacy_content="""
        <p>As we look towards the future, our commitment to educational excellence and social transformation remains stronger than ever. We continue to evolve our programs, embrace technology, and expand opportunities for students from all backgrounds.</p>
        
        <p>Our legacy lives not just in the infrastructure we've built or the degrees we've awarded, but in the thousands of graduates who are making meaningful contributions as teachers, engineers, doctors, entrepreneurs, and community leaders across India and beyond.</p>
        
        <p>We remain dedicated to our founding mission: providing world-class education that empowers students to achieve their dreams while serving society with integrity and compassion.</p>
        """
    )
    
    print(f"Created main history content: {history_content.name}")
    
    # Create timeline events
    timeline_events = [
        {
            'year': 1985,
            'title': 'Foundation & First Batch',
            'description': 'Established with Arts and Science streams, welcoming our first batch of 120 students with 8 dedicated faculty members.',
            'icon_class': 'fas fa-seedling',
            'gradient_color': 'emerald-teal',
            'ordering': 1
        },
        {
            'year': 1992,
            'title': 'Commerce Stream Launch',
            'description': 'Introduced Bachelor of Commerce program to meet growing demand for business education and entrepreneurship development.',
            'icon_class': 'fas fa-chart-line',
            'gradient_color': 'blue-indigo',
            'ordering': 2
        },
        {
            'year': 1998,
            'title': 'Computer Science Department',
            'description': 'Established Computer Science department with state-of-the-art lab facilities, pioneering IT education in the region.',
            'icon_class': 'fas fa-laptop-code',
            'gradient_color': 'purple-pink',
            'ordering': 3
        },
        {
            'year': 2003,
            'title': 'New Campus Expansion',
            'description': 'Inaugurated modern 5-acre campus with advanced laboratories, library, and sports facilities to accommodate growing student body.',
            'icon_class': 'fas fa-building',
            'gradient_color': 'orange-red',
            'ordering': 4
        },
        {
            'year': 2008,
            'title': 'Research Center Established',
            'description': 'Launched dedicated research center focusing on agricultural innovation and sustainable development projects.',
            'icon_class': 'fas fa-microscope',
            'gradient_color': 'teal-cyan',
            'ordering': 5
        },
        {
            'year': 2015,
            'title': 'Digital Learning Initiative',
            'description': 'Implemented comprehensive digital learning platform with smart classrooms and online resources for enhanced education.',
            'icon_class': 'fas fa-digital-tachograph',
            'gradient_color': 'indigo-purple',
            'ordering': 6
        },
        {
            'year': 2020,
            'title': 'Pandemic Adaptation',
            'description': 'Successfully transitioned to hybrid learning model during COVID-19, ensuring uninterrupted education for all students.',
            'icon_class': 'fas fa-shield-virus',
            'gradient_color': 'yellow-orange',
            'ordering': 7
        },
        {
            'year': 2023,
            'title': 'Excellence Recognition',
            'description': 'Achieved NAAC Grade A accreditation and recognition as "Best Rural College" by State Education Board.',
            'icon_class': 'fas fa-trophy',
            'gradient_color': 'emerald-teal',
            'ordering': 8
        }
    ]
    
    for event_data in timeline_events:
        event = TimelineEvent.objects.create(
            history_content=history_content,
            **event_data,
            is_active=True
        )
        print(f"Created timeline event: {event.year} - {event.title}")
    
    # Create milestones
    milestones = [
        {
            'title': 'NAAC Grade A Accreditation',
            'description': 'Achieved National Assessment and Accreditation Council Grade A certification, recognizing our commitment to quality education and institutional excellence.',
            'icon_class': 'fas fa-award',
            'gradient_color': 'emerald-teal',
            'ordering': 1
        },
        {
            'title': 'State University Affiliation',
            'description': 'Proudly affiliated with Karnataka State University, ensuring our degrees meet the highest academic standards and are recognized nationwide.',
            'icon_class': 'fas fa-university',
            'gradient_color': 'blue-indigo',
            'ordering': 2
        },
        {
            'title': 'Research Excellence Award',
            'description': 'Recognized for outstanding research contributions in agricultural sciences and sustainable development with multiple publications and patents.',
            'icon_class': 'fas fa-microscope',
            'gradient_color': 'purple-pink',
            'ordering': 3
        },
        {
            'title': 'Industry Partnerships',
            'description': 'Established strategic partnerships with leading companies for internships, placements, and collaborative research projects.',
            'icon_class': 'fas fa-handshake',
            'gradient_color': 'orange-red',
            'ordering': 4
        },
        {
            'title': 'Green Campus Initiative',
            'description': 'Achieved carbon-neutral status through solar power, rainwater harvesting, and comprehensive waste management systems.',
            'icon_class': 'fas fa-leaf',
            'gradient_color': 'teal-cyan',
            'ordering': 5
        },
        {
            'title': 'Alumni Success Network',
            'description': 'Over 12,000 successful alumni working in prestigious positions across India and internationally, maintaining strong institutional connections.',
            'icon_class': 'fas fa-users',
            'gradient_color': 'indigo-purple',
            'ordering': 6
        }
    ]
    
    for milestone_data in milestones:
        milestone = Milestone.objects.create(
            history_content=history_content,
            **milestone_data,
            is_active=True
        )
        print(f"Created milestone: {milestone.title}")
    
    # Create sample gallery images
    gallery_images = [
        {
            'title': 'Main Campus Building',
            'category': 'infrastructure',
            'description': 'Our iconic main building that houses administrative offices and lecture halls.',
            'year_taken': 2023,
            'photographer': 'College Photography Club',
            'ordering': 1,
            'is_featured': True
        },
        {
            'title': 'Annual Convocation Ceremony',
            'category': 'events',
            'description': 'Graduates celebrating their achievements at the annual convocation ceremony.',
            'year_taken': 2023,
            'photographer': 'Event Documentation Team',
            'ordering': 1,
            'is_featured': True
        },
        {
            'title': 'Science Laboratory',
            'category': 'academics',
            'description': 'State-of-the-art laboratory facilities for hands-on learning and research.',
            'year_taken': 2022,
            'photographer': 'Academic Affairs',
            'ordering': 1
        },
        {
            'title': 'Inter-College Sports Meet',
            'category': 'sports',
            'description': 'Students participating in the annual inter-college sports competition.',
            'year_taken': 2023,
            'photographer': 'Sports Committee',
            'ordering': 1
        },
        {
            'title': 'Cultural Festival Performance',
            'category': 'cultural',
            'description': 'Traditional dance performance during our annual cultural festival.',
            'year_taken': 2023,
            'photographer': 'Cultural Committee',
            'ordering': 1
        },
        {
            'title': 'NAAC Accreditation Award',
            'category': 'achievements',
            'description': 'Receiving the prestigious NAAC Grade A accreditation certificate.',
            'year_taken': 2023,
            'photographer': 'Administration',
            'ordering': 1,
            'is_featured': True
        },
        {
            'title': 'Library Reading Hall',
            'category': 'infrastructure',
            'description': 'Spacious and well-equipped library providing a conducive learning environment.',
            'year_taken': 2022,
            'photographer': 'Library Staff',
            'ordering': 2
        },
        {
            'title': 'Alumni Reunion 2023',
            'category': 'alumni',
            'description': 'Alumni gathering to celebrate achievements and share experiences.',
            'year_taken': 2023,
            'photographer': 'Alumni Association',
            'ordering': 1
        },
        {
            'title': 'Foundation Day Celebration',
            'category': 'historical',
            'description': 'Commemorating the founding of our institution with special ceremonies.',
            'year_taken': 2023,
            'photographer': 'Documentation Team',
            'ordering': 1
        },
        {
            'title': 'Student Life on Campus',
            'category': 'campus',
            'description': 'Students enjoying recreational activities in the campus courtyard.',
            'year_taken': 2023,
            'photographer': 'Student Council',
            'ordering': 1
        },
        {
            'title': 'Computer Lab Session',
            'category': 'academics',
            'description': 'Students working on programming projects in the computer laboratory.',
            'year_taken': 2022,
            'photographer': 'IT Department',
            'ordering': 2
        },
        {
            'title': 'Green Campus Initiative',
            'category': 'campus',
            'description': 'Tree plantation drive as part of our environmental sustainability program.',
            'year_taken': 2022,
            'photographer': 'Environmental Club',
            'ordering': 2
        }
    ]
    
    # Note: Since we can't upload actual images in this script, we'll create placeholder entries
    # In a real scenario, you would upload actual images through the admin interface
    print(f"📸 Gallery images data prepared (images need to be uploaded through admin):")
    for img_data in gallery_images:
        print(f"   - {img_data['title']} ({img_data['category']})")
        # HistoryGalleryImage.objects.create(
        #     history_content=history_content,
        #     **img_data,
        #     is_active=True
        # )
    
    print(f"\n✅ Successfully created sample history data!")
    print(f"📊 Summary:")
    print(f"   - 1 History Content record")
    print(f"   - {len(timeline_events)} Timeline Events")
    print(f"   - {len(milestones)} Milestones")
    print(f"   - {len(gallery_images)} Gallery Image entries prepared")
    print(f"\n🌐 Visit http://127.0.0.1:8000/about/history/ to see the results!")
    print(f"🔧 Upload images through: http://127.0.0.1:8000/admin/college_website/historygalleryimage/")

if __name__ == '__main__':
    create_sample_history_data()
