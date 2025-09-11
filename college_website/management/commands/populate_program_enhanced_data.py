from django.core.management.base import BaseCommand
from college_website.models import Program


class Command(BaseCommand):
    help = 'Populate enhanced program data for BA program'

    def handle(self, *args, **options):
        try:
            # Get or create BA program
            ba_program, created = Program.objects.get_or_create(
                name="Bachelor of Arts",
                defaults={
                    'short_name': 'B.A.',
                    'discipline': 'arts',
                    'degree_type': 'undergraduate',
                    'description': 'A comprehensive undergraduate program in Arts and Humanities',
                    'duration': '3 years',
                    'department': 'Department of Arts',
                    'is_active': True,
                    'is_featured': True,
                }
            )

            # Populate Course Syllabus
            ba_program.first_year_subjects = """
            <h6 class="text-primary mb-3">Core Subjects</h6>
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>English Literature</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>History of India</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Political Science</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Economics</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Sociology</li>
            </ul>
            <h6 class="text-primary mb-3">Elective Subjects</h6>
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-star text-warning me-2"></i>Psychology</li>
                <li class="mb-2"><i class="fas fa-star text-warning me-2"></i>Geography</li>
                <li class="mb-2"><i class="fas fa-star text-warning me-2"></i>Philosophy</li>
            </ul>
            """

            ba_program.second_year_subjects = """
            <h6 class="text-primary mb-3">Advanced Core Subjects</h6>
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Advanced English Literature</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Modern Indian History</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>International Relations</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Development Economics</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Social Psychology</li>
            </ul>
            <h6 class="text-primary mb-3">Specialization</h6>
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-star text-warning me-2"></i>Research Methodology</li>
                <li class="mb-2"><i class="fas fa-star text-warning me-2"></i>Project Work</li>
            </ul>
            """

            ba_program.elective_options = """
            <h6 class="text-primary mb-3">Available Elective Options</h6>
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-star text-warning me-2"></i>Psychology</li>
                <li class="mb-2"><i class="fas fa-star text-warning me-2"></i>Geography</li>
                <li class="mb-2"><i class="fas fa-star text-warning me-2"></i>Philosophy</li>
                <li class="mb-2"><i class="fas fa-star text-warning me-2"></i>Public Administration</li>
                <li class="mb-2"><i class="fas fa-star text-warning me-2"></i>Environmental Studies</li>
            </ul>
            """

            # Populate CO-PO Information
            ba_program.program_outcomes = """
            <div class="mb-3">
                <h6 class="text-primary">PO1: Knowledge Application</h6>
                <p class="small text-muted">Apply knowledge of humanities and social sciences to solve complex problems.</p>
            </div>
            <div class="mb-3">
                <h6 class="text-primary">PO2: Critical Thinking</h6>
                <p class="small text-muted">Develop critical thinking and analytical skills for decision making.</p>
            </div>
            <div class="mb-3">
                <h6 class="text-primary">PO3: Communication</h6>
                <p class="small text-muted">Communicate effectively in written and oral forms.</p>
            </div>
            <div class="mb-3">
                <h6 class="text-primary">PO4: Research Skills</h6>
                <p class="small text-muted">Conduct research and analyze data using appropriate methodologies.</p>
            </div>
            """

            ba_program.course_outcomes = """
            <div class="mb-3">
                <h6 class="text-primary">CO1: Subject Knowledge</h6>
                <p class="small text-muted">Demonstrate comprehensive understanding of core subjects.</p>
            </div>
            <div class="mb-3">
                <h6 class="text-primary">CO2: Analytical Skills</h6>
                <p class="small text-muted">Analyze historical, political, and social phenomena critically.</p>
            </div>
            <div class="mb-3">
                <h6 class="text-primary">CO3: Writing Skills</h6>
                <p class="small text-muted">Write clear, coherent, and well-structured essays and reports.</p>
            </div>
            <div class="mb-3">
                <h6 class="text-primary">CO4: Presentation Skills</h6>
                <p class="small text-muted">Present ideas and arguments effectively in various formats.</p>
            </div>
            """

            # Populate Timetable Information
            ba_program.class_timings = "9:00 AM - 1:15 PM"
            ba_program.weekly_schedule = """
            <div class="table-responsive">
                <table class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Time</th>
                            <th>Monday</th>
                            <th>Tuesday</th>
                            <th>Wednesday</th>
                            <th>Thursday</th>
                            <th>Friday</th>
                            <th>Saturday</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="fw-bold">9:00 - 10:00</td>
                            <td><span class="badge bg-primary">English Literature</span></td>
                            <td><span class="badge bg-success">History</span></td>
                            <td><span class="badge bg-info">Political Science</span></td>
                            <td><span class="badge bg-warning text-dark">Economics</span></td>
                            <td><span class="badge bg-danger">Sociology</span></td>
                            <td><span class="badge bg-secondary">Library</span></td>
                        </tr>
                        <tr>
                            <td class="fw-bold">10:00 - 11:00</td>
                            <td><span class="badge bg-success">History</span></td>
                            <td><span class="badge bg-info">Political Science</span></td>
                            <td><span class="badge bg-warning text-dark">Economics</span></td>
                            <td><span class="badge bg-danger">Sociology</span></td>
                            <td><span class="badge bg-primary">English Literature</span></td>
                            <td><span class="badge bg-dark">Tutorial</span></td>
                        </tr>
                        <tr>
                            <td class="fw-bold">11:00 - 11:15</td>
                            <td colspan="6" class="text-center bg-light"><strong>Break</strong></td>
                        </tr>
                        <tr>
                            <td class="fw-bold">11:15 - 12:15</td>
                            <td><span class="badge bg-info">Political Science</span></td>
                            <td><span class="badge bg-warning text-dark">Economics</span></td>
                            <td><span class="badge bg-danger">Sociology</span></td>
                            <td><span class="badge bg-primary">English Literature</span></td>
                            <td><span class="badge bg-success">History</span></td>
                            <td><span class="badge bg-secondary">Lab Work</span></td>
                        </tr>
                        <tr>
                            <td class="fw-bold">12:15 - 1:15</td>
                            <td><span class="badge bg-warning text-dark">Economics</span></td>
                            <td><span class="badge bg-danger">Sociology</span></td>
                            <td><span class="badge bg-primary">English Literature</span></td>
                            <td><span class="badge bg-success">History</span></td>
                            <td><span class="badge bg-info">Political Science</span></td>
                            <td><span class="badge bg-dark">Project Work</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """

            # Populate Career Prospects
            ba_program.teaching_careers = """
            <p class="card-text text-muted">Become a teacher, lecturer, or educational administrator in schools and colleges.</p>
            <ul class="list-unstyled text-start">
                <li><i class="fas fa-check text-success me-2"></i>School Teacher</li>
                <li><i class="fas fa-check text-success me-2"></i>College Lecturer</li>
                <li><i class="fas fa-check text-success me-2"></i>Educational Consultant</li>
                <li><i class="fas fa-check text-success me-2"></i>Curriculum Developer</li>
            </ul>
            """

            ba_program.media_journalism_careers = """
            <p class="card-text text-muted">Work in print, electronic, and digital media as journalists, editors, or content creators.</p>
            <ul class="list-unstyled text-start">
                <li><i class="fas fa-check text-success me-2"></i>Journalist</li>
                <li><i class="fas fa-check text-success me-2"></i>Content Writer</li>
                <li><i class="fas fa-check text-success me-2"></i>Editor</li>
                <li><i class="fas fa-check text-success me-2"></i>Social Media Manager</li>
            </ul>
            """

            ba_program.government_careers = """
            <p class="card-text text-muted">Join civil services, administrative services, or work in government departments.</p>
            <ul class="list-unstyled text-start">
                <li><i class="fas fa-check text-success me-2"></i>Civil Services</li>
                <li><i class="fas fa-check text-success me-2"></i>Administrative Officer</li>
                <li><i class="fas fa-check text-success me-2"></i>Policy Analyst</li>
                <li><i class="fas fa-check text-success me-2"></i>Public Relations Officer</li>
            </ul>
            """

            ba_program.further_studies = """
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-arrow-right text-primary me-2"></i>Master of Arts (MA) in various subjects</li>
                <li class="mb-2"><i class="fas fa-arrow-right text-primary me-2"></i>Master of Business Administration (MBA)</li>
                <li class="mb-2"><i class="fas fa-arrow-right text-primary me-2"></i>Master of Social Work (MSW)</li>
                <li class="mb-2"><i class="fas fa-arrow-right text-primary me-2"></i>Master of Journalism and Mass Communication</li>
                <li class="mb-2"><i class="fas fa-arrow-right text-primary me-2"></i>Law (LLB) for legal career</li>
            </ul>
            """

            ba_program.private_sector_careers = """
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-arrow-right text-primary me-2"></i>Human Resources Manager</li>
                <li class="mb-2"><i class="fas fa-arrow-right text-primary me-2"></i>Public Relations Officer</li>
                <li class="mb-2"><i class="fas fa-arrow-right text-primary me-2"></i>Research Analyst</li>
                <li class="mb-2"><i class="fas fa-arrow-right text-primary me-2"></i>Social Media Manager</li>
                <li class="mb-2"><i class="fas fa-arrow-right text-primary me-2"></i>Event Manager</li>
            </ul>
            """

            # Populate Course Features
            ba_program.expert_faculty = """
            <p class="card-text small text-muted">Learn from experienced professors with PhD qualifications and industry experience.</p>
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>PhD qualified faculty</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Industry experience</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Research publications</li>
            </ul>
            """

            ba_program.infrastructure = """
            <p class="card-text small text-muted">State-of-the-art classrooms, library, and computer labs with latest technology.</p>
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Modern classrooms</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Digital library</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Computer labs</li>
            </ul>
            """

            ba_program.research_opportunities = """
            <p class="card-text small text-muted">Engage in research projects and publish papers in reputed journals.</p>
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Research projects</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Journal publications</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Conference presentations</li>
            </ul>
            """

            ba_program.industry_connect = """
            <p class="card-text small text-muted">Regular workshops, seminars, and industry visits for practical exposure.</p>
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Industry workshops</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Guest lectures</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Field visits</li>
            </ul>
            """

            ba_program.additional_benefits = """
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Scholarship opportunities</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Placement assistance</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Alumni network</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Cultural activities</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Sports facilities</li>
            </ul>
            """

            ba_program.assessment_methods = """
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Continuous assessment (40%)</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Semester examinations (60%)</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Project work evaluation</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Presentation assessment</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Practical examinations</li>
            </ul>
            """

            ba_program.global_opportunities = """
            <ul class="list-unstyled">
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>International exchange programs</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Study abroad opportunities</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Global internship programs</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>International conferences</li>
                <li class="mb-2"><i class="fas fa-check-circle text-success me-2"></i>Research collaborations</li>
            </ul>
            """

            # Save the program
            ba_program.save()

            self.stdout.write(
                self.style.SUCCESS(f'Successfully populated enhanced data for {ba_program.name}')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error populating program data: {str(e)}')
            )
