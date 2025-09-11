#!/usr/bin/env python
"""
Script to create sample Principal Message data for the college website.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from college_website.models import PrincipalMessage

def create_principal_message():
    """Create sample principal message data"""
    
    # Check if principal message already exists
    if PrincipalMessage.objects.filter(is_active=True).exists():
        print("Active Principal Message already exists!")
        return
    
    # Create principal message
    principal_message = PrincipalMessage.objects.create(
        name="Dr. Vinod Kumar Gupta",
        designation="Principal",
        qualifications="Ph.D. in Computer Science, M.Tech, B.Tech",
        specialization="Artificial Intelligence & Machine Learning",
        experience_years=25,
        office_hours="Monday to Friday: 10:00 AM - 4:00 PM",
        message_title="Welcome to Our Institution",
        message_content="""
        <p>Dear Students, Faculty, and Staff,</p>
        
        <p>It is my great pleasure to welcome you to our esteemed institution. As we embark on another academic year filled with opportunities for growth, learning, and discovery, I am excited to share our vision for excellence in education.</p>
        
        <blockquote>
        "Education is the most powerful weapon which you can use to change the world." - Nelson Mandela
        </blockquote>
        
        <p>Our institution stands as a beacon of academic excellence, fostering an environment where students can explore their potential, engage in meaningful research, and develop the skills necessary to become leaders in their chosen fields.</p>
        
        <p>We are committed to:</p>
        <ul>
            <li>Providing world-class education with modern teaching methodologies</li>
            <li>Encouraging research and innovation across all disciplines</li>
            <li>Building character and instilling values of integrity and social responsibility</li>
            <li>Creating a supportive and inclusive learning environment</li>
            <li>Preparing students for successful careers and meaningful contributions to society</li>
        </ul>
        
        <p>Our dedicated faculty members bring years of experience and expertise to the classroom, ensuring that every student receives personalized attention and guidance. We believe in the holistic development of our students, combining academic rigor with extracurricular activities, sports, and community service.</p>
        
        <p>As we move forward, we remain committed to adapting to the changing needs of education and industry, incorporating new technologies and innovative approaches to learning. Our goal is to prepare graduates who are not only knowledgeable in their fields but also equipped with critical thinking skills, creativity, and a global perspective.</p>
        
        <p>I encourage all students to make the most of the opportunities available here, to engage actively in their learning journey, and to contribute positively to our academic community. Together, we will continue to uphold the values and traditions that make our institution a place of pride and excellence.</p>
        
        <p>Wishing you all a successful and fulfilling academic year ahead.</p>
        
        <p>Warm regards,<br>
        Dr. Vinod Kumar Gupta<br>
        Principal</p>
        """,
        photo="header/logos/principal-photo.jpg",  # Placeholder path
        email="principal@college.edu",
        phone="+91-9876543210",
        linkedin_url="https://linkedin.com/in/drvinodgupta",
        twitter_url="https://twitter.com/drvinodgupta",
        is_active=True
    )
    
    print(f"✅ Created Principal Message: {principal_message.name}")
    print(f"   Designation: {principal_message.designation}")
    print(f"   Status: {'Active' if principal_message.is_active else 'Inactive'}")
    
if __name__ == "__main__":
    create_principal_message()
    print("\n🎉 Principal Message data created successfully!")
