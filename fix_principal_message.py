import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaitanya_site.settings')
django.setup()

from college_website.models import PrincipalMessage

# Create or get principal message
pm, created = PrincipalMessage.objects.get_or_create(
    is_active=True,
    defaults={
        'name': 'Dr. Vinod Kumar Gupta',
        'designation': 'Principal',
        'qualifications': 'Ph.D. in Computer Science, M.Tech, B.Tech',
        'specialization': 'Artificial Intelligence & Machine Learning',
        'experience_years': 25,
        'office_hours': 'Monday to Friday: 10:00 AM - 4:00 PM',
        'message_title': 'Welcome to Our Institution',
        'message_content': '''<p>Dear Students, Faculty, and Staff,</p>
        
<p>It is my great pleasure to welcome you to our esteemed institution. As we embark on another academic year filled with opportunities for growth, learning, and discovery, I am excited to share our vision for excellence in education.</p>

<blockquote>"Education is the most powerful weapon which you can use to change the world." - Nelson Mandela</blockquote>

<p>Our institution stands as a beacon of academic excellence, fostering an environment where students can explore their potential, engage in meaningful research, and develop the skills necessary to become leaders in their chosen fields.</p>

<p>We are committed to providing world-class education with modern teaching methodologies, encouraging research and innovation across all disciplines, and building character while instilling values of integrity and social responsibility.</p>

<p>Wishing you all a successful and fulfilling academic year ahead.</p>

<p>Warm regards,<br>Dr. Vinod Kumar Gupta<br>Principal</p>''',
        'email': 'principal@college.edu',
        'phone': '+91-9876543210',
    }
)

print(f"{'Created' if created else 'Found existing'} Principal Message: {pm.name}")
