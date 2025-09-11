
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import (
    CollegeInfo, Program, Event, Notice, SocialInitiative,
    StudentTestimonial, ImportantLink, ContactMessage, Page,
    Menu, MenuItem, BlockRichText, BlockImageGallery, BlockVideoEmbed,
    BlockDownloadList, BlockTableHTML, BlockForm, Gallery, GalleryPhoto,
    AdmissionInfo, ExamResult, LibraryResource, ELearningCourse, QuestionPaper,
    PlacementRecord, AlumniProfile, DirectorMessage, PrincipalMessage,
    IQACInfo, IQACReport, NAACInfo, NIRFInfo, AccreditationInfo, 
    IQACFeedback, QualityInitiative, SideMenu, SideMenuItem, Department,
    HeroBanner, ExamTimetable, ExamTimetableWeek, ExamTimetableExam, RevaluationInfo, ExamRulesInfo, ResearchCenterInfo,
    PublicationInfo, Publication, PatentsProjectsInfo, Patent, ResearchProject, IndustryCollaboration,
    ConsultancyInfo, ConsultancyService, ConsultancyExpertise, ConsultancySuccessStory,
    HeroCarouselSlide, HeroCarouselSettings
)
from .forms import ContactForm, SearchForm, ExamTimetableBulkForm, ExamTimetableWeekForm, ExamTimetableExamForm, ProgramForm, ProgramCreateForm, ProgramUpdateForm, ProgramQuickEditForm, ExamTimetableForm


def get_college_info():
    """Helper function to get active college info"""
    return CollegeInfo.objects.filter(is_active=True).first()


def get_side_menus_for_request(request):
    """Helper function to get active side menus for the current request"""
    side_menus = []
    all_menus = SideMenu.objects.filter(is_active=True).order_by('-priority')
    
    for menu in all_menus:
        if menu.matches_request(request):
            side_menus.append(menu)
    
    return side_menus


def home_view(request):
    """Homepage view"""
    from .models import SliderImage
    
    college_info = get_college_info()
    recent_notices = Notice.objects.filter(is_active=True)[:5]
    recent_events = Event.objects.filter(is_active=True)[:5]
    testimonials = StudentTestimonial.objects.filter(is_active=True)[:6]
    quick_links = ImportantLink.objects.filter(is_active=True, type='quick')[:6]

    # Get director's and principal's messages for homepage display
    director_message = DirectorMessage.objects.filter(is_active=True, show_on_homepage=True).first()
    principal_message = PrincipalMessage.objects.filter(is_active=True, show_on_homepage=True).first()

    # Get active hero banner
    active_hero_banner = HeroBanner.objects.filter(is_active=True).first()
    
    # Get slider images
    slider_images = SliderImage.objects.filter(is_active=True).order_by('ordering')

    # Get hero carousel data
    hero_carousel_settings = HeroCarouselSettings.get_settings()
    hero_carousel_slides = HeroCarouselSlide.objects.filter(
        is_active=True
    ).order_by('display_order', 'created_at')

    # News & Announcements - Only "general" announcements
    recent_announcements = Notice.objects.filter(
        is_active=True, category="general"
    ).order_by("-publish_date")[:5]

    context = {
        'college_info': college_info,
        'recent_notices': recent_notices,
        'recent_events': recent_events,
        'testimonials': testimonials,
        'quick_links': quick_links,
        'director_message': director_message,
        'principal_message': principal_message,
        'recent_announcements': recent_announcements,
        'active_hero_banner': active_hero_banner,
        'slider_images': slider_images,
        'hero_carousel_settings': hero_carousel_settings,
        'hero_carousel_slides': hero_carousel_slides,
    }
    return render(request, 'college_website/home.html', context)


def menu_test_view(request):
    """Menu visibility test view for debugging"""
    college_info = get_college_info()
    context = {
        'college_info': college_info,
    }
    return render(request, 'college_website/menu_test.html', context)


def about_view(request):
    """About page view"""
    college_info = get_college_info()
    context = {
        'college_info': college_info,
    }
    return render(request, 'college_website/about.html', context)


def vision_mission_view(request):
    """Vision & Mission page view"""
    from .models import VisionMissionContent
    
    college_info = get_college_info()
    
    # Get active vision mission content
    vision_mission_content = VisionMissionContent.objects.filter(is_active=True).first()
    
    # Get active core values if content exists
    core_values = []
    if vision_mission_content:
        core_values = vision_mission_content.core_values.filter(is_active=True).order_by('ordering')
    
    context = {
        'college_info': college_info,
        'vision_mission_content': vision_mission_content,
        'core_values': core_values,
    }
    return render(request, 'college_website/vision_mission.html', context)


class ProgramsListView(ListView):
    """Programs listing view"""
    model = Program
    template_name = 'college_website/programs_list.html'
    context_object_name = 'programs'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Program.objects.filter(is_active=True)
        
        # Filter by discipline (stream)
        discipline = self.request.GET.get('discipline')
        if discipline:
            queryset = queryset.filter(discipline=discipline)
        
        # Filter by degree type
        degree_type = self.request.GET.get('degree_type')
        if degree_type:
            queryset = queryset.filter(degree_type=degree_type)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(department__icontains=search_query) |
                Q(short_name__icontains=search_query)
            )
        
        return queryset.order_by('discipline', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disciplines'] = Program.DISCIPLINE_CHOICES
        context['selected_discipline'] = self.request.GET.get('discipline', '')
        context['degree_types'] = Program.DEGREE_TYPE_CHOICES
        context['selected_degree_type'] = self.request.GET.get('degree_type', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class ProgramDetailView(DetailView):
    """Program detail view"""
    model = Program
    template_name = 'college_website/program_detail.html'
    context_object_name = 'program'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Program.objects.filter(is_active=True)


class EventsListView(ListView):
    """Events listing view"""
    model = Event
    template_name = 'college_website/events_list.html'
    context_object_name = 'events'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Event.objects.filter(is_active=True)
        event_type = self.request.GET.get('type')
        if event_type:
            queryset = queryset.filter(type=event_type)
        return queryset.order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = Event.TYPE_CHOICES
        context['selected_type'] = self.request.GET.get('type', '')
        return context


class EventDetailView(DetailView):
    """Event detail view"""
    model = Event
    template_name = 'college_website/event_detail.html'
    context_object_name = 'event'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Event.objects.filter(is_active=True)


class NoticesListView(ListView):
    """Notices listing view"""
    model = Notice
    template_name = 'college_website/notices_list.html'
    context_object_name = 'notices'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Notice.objects.filter(is_active=True)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Notice.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class NoticeDetailView(DetailView):
    """Notice detail view"""
    model = Notice
    template_name = 'college_website/notice_detail.html'
    context_object_name = 'notice'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Notice.objects.filter(is_active=True)


class SocialImpactView(ListView):
    """Social initiatives view"""
    model = SocialInitiative
    template_name = 'college_website/social_impact.html'
    context_object_name = 'initiatives'
    
    def get_queryset(self):
        return SocialInitiative.objects.filter(is_active=True).order_by('name')


class SocialInitiativeDetailView(DetailView):
    """Social initiative detail view"""
    model = SocialInitiative
    template_name = 'college_website/social_initiative_detail.html'
    context_object_name = 'initiative'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return SocialInitiative.objects.filter(is_active=True)


def student_corner_view(request):
    """Student corner view"""
    testimonials = StudentTestimonial.objects.filter(is_active=True).order_by('-rating', '-created_at')
    important_links = ImportantLink.objects.filter(is_active=True, type='important')
    
    context = {
        'testimonials': testimonials,
        'important_links': important_links,
    }
    return render(request, 'college_website/student_corner.html', context)


# ============================================================================
# NEW HIERARCHICAL MENU VIEWS
# ============================================================================

# Home Section Views
def about_institution_view(request):
    """About Institution view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/about_institution.html', context)

def history_view(request):
    """College History view"""
    from .models import HistoryContent
    
    college_info = get_college_info()
    history_content = HistoryContent.objects.filter(is_active=True).first()
    
    timeline_events = []
    milestones = []
    gallery_images = []
    gallery_categories = []
    
    if history_content:
        timeline_events = history_content.timeline_events.filter(is_active=True).order_by('ordering', 'year')
        milestones = history_content.milestones.filter(is_active=True).order_by('ordering', 'title')
        gallery_images = history_content.gallery_images.filter(is_active=True).order_by('category', 'ordering', '-year_taken')
        
        # Get unique categories for filtering
        gallery_categories = gallery_images.values_list('category', flat=True).distinct()
    
    context = {
        'college_info': college_info,
        'history_content': history_content,
        'timeline_events': timeline_events,
        'milestones': milestones,
        'gallery_images': gallery_images,
        'gallery_categories': gallery_categories,
    }
    return render(request, 'college_website/history.html', context)

def governing_body_view(request):
    """Governing Body view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/governing_body.html', context)

# About Section Views
def about_overview_view(request):
    """About Overview view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/about_overview.html', context)

def administration_view(request):
    """Administration view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/administration.html', context)

def organizational_structure_view(request):
    """Organizational Structure view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/organizational_structure.html', context)

def statutory_approvals_view(request):
    """Statutory Approvals view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/statutory_approvals.html', context)

def policies_view(request):
    """Policies main view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/policies.html', context)

def anti_ragging_policy_view(request):
    """Anti Ragging Policy view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/anti_ragging_policy.html', context)

def grievance_redressal_policy_view(request):
    """Grievance Redressal Policy view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/grievance_redressal_policy.html', context)

def code_of_conduct_policy_view(request):
    """Code of Conduct Policy view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/code_of_conduct_policy.html', context)

# Academics Section Views
def academics_view(request):
    """Academics main view with comprehensive data"""
    college_info = get_college_info()
    
    # Get all active programs grouped by discipline
    programs = Program.objects.filter(is_active=True).order_by('discipline', 'name')
    programs_by_discipline = {}
    for program in programs:
        discipline = program.get_discipline_display()
        if discipline not in programs_by_discipline:
            programs_by_discipline[discipline] = []
        programs_by_discipline[discipline].append(program)
    
    # Get all active departments
    departments = Department.objects.filter(is_active=True).order_by('discipline', 'name')
    departments_by_discipline = {}
    for dept in departments:
        discipline = dept.get_discipline_display()
        if discipline not in departments_by_discipline:
            departments_by_discipline[discipline] = []
        departments_by_discipline[discipline].append(dept)
    
    # Get featured programs
    featured_programs = Program.objects.filter(is_active=True, is_featured=True)[:6]
    
    # Get statistics
    total_programs = programs.count()
    total_departments = departments.count()
    total_students = 5000  # This could be dynamic from a model
    
    context = {
        'college_info': college_info,
        'programs': programs,
        'programs_by_discipline': programs_by_discipline,
        'departments': departments,
        'departments_by_discipline': departments_by_discipline,
        'featured_programs': featured_programs,
        'total_programs': total_programs,
        'total_departments': total_departments,
        'total_students': total_students,
        'disciplines': Program.DISCIPLINE_CHOICES,
    }
    return render(request, 'college_website/academics.html', context)

def faculties_view(request):
    """Faculties view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/faculties.html', context)

def academic_faculties_view(request):
    """Academic Faculties view"""
    from .models import Faculty, Department
    
    college_info = get_college_info()
    
    # Get all active faculty members grouped by department
    faculty_by_department = {}
    departments = Department.objects.filter(is_active=True).prefetch_related('faculty_members')
    
    for dept in departments:
        faculty_members = dept.faculty_members.filter(
            is_active=True, 
            show_on_website=True
        ).order_by('designation_order', 'name')
        
        if faculty_members.exists():
            faculty_by_department[dept] = faculty_members
    
    context = {
        'college_info': college_info,
        'faculty_by_department': faculty_by_department,
    }
    return render(request, 'college_website/academic_faculties.html', context)

def non_academic_faculties_view(request):
    """Non-Academic Faculties view"""
    from .models import NonAcademicStaff, Department
    
    college_info = get_college_info()
    
    # Get all active non-academic staff grouped by department
    staff_by_department = {}
    departments = Department.objects.filter(is_active=True).prefetch_related('non_academic_staff')
    
    for dept in departments:
        staff_members = dept.non_academic_staff.filter(
            is_active=True, 
            show_on_website=True
        ).order_by('designation_order', 'name')
        
        if staff_members.exists():
            staff_by_department[dept] = staff_members
    
    context = {
        'college_info': college_info,
        'staff_by_department': staff_by_department,
    }
    return render(request, 'college_website/non_academic_faculties.html', context)

def faculty_detail_view(request, dept_slug, slug):
    """Individual faculty member detail view"""
    from .models import Faculty, Department
    from django.shortcuts import get_object_or_404
    
    college_info = get_college_info()
    
    # Get the faculty member
    faculty = get_object_or_404(
        Faculty.objects.select_related('department'),
        slug=slug,
        department__slug=dept_slug,
        is_active=True,
        show_on_website=True
    )
    
    # Get other faculty members from the same department
    related_faculty = Faculty.objects.filter(
        department=faculty.department,
        is_active=True,
        show_on_website=True
    ).exclude(id=faculty.id).order_by('designation_order', 'name')[:3]
    
    context = {
        'college_info': college_info,
        'faculty': faculty,
        'related_faculty': related_faculty,
    }
    return render(request, 'college_website/faculty_detail.html', context)

def staff_detail_view(request, dept_slug, slug):
    """Individual non-academic staff member detail view"""
    from .models import NonAcademicStaff, Department
    from django.shortcuts import get_object_or_404
    
    college_info = get_college_info()
    
    # Get the staff member
    staff = get_object_or_404(
        NonAcademicStaff.objects.select_related('department'),
        slug=slug,
        department__slug=dept_slug,
        is_active=True,
        show_on_website=True
    )
    
    # Get other staff members from the same department
    related_staff = NonAcademicStaff.objects.filter(
        department=staff.department,
        is_active=True,
        show_on_website=True
    ).exclude(id=staff.id).order_by('designation_order', 'name')[:3]
    
    context = {
        'college_info': college_info,
        'staff': staff,
        'related_staff': related_staff,
    }
    return render(request, 'college_website/staff_detail.html', context)

def departments_view(request):
    """Departments main view"""
    college_info = get_college_info()
    programs = Program.objects.filter(is_active=True)
    context = {
        'college_info': college_info,
        'programs': programs,
    }
    return render(request, 'college_website/departments.html', context)

def arts_department_view(request):
    """Arts Department view"""
    college_info = get_college_info()
    arts_programs = Program.objects.filter(is_active=True, discipline='arts')
    context = {
        'college_info': college_info,
        'programs': arts_programs,
        'department': 'Arts',
    }
    return render(request, 'college_website/department_detail.html', context)

def science_department_view(request):
    """Science Department view"""
    college_info = get_college_info()
    science_programs = Program.objects.filter(is_active=True, discipline='science')
    context = {
        'college_info': college_info,
        'programs': science_programs,
        'department': 'Science',
    }
    return render(request, 'college_website/department_detail.html', context)

def commerce_department_view(request):
    """Commerce Department view"""
    college_info = get_college_info()
    commerce_programs = Program.objects.filter(is_active=True, discipline='commerce')
    context = {
        'college_info': college_info,
        'programs': commerce_programs,
        'department': 'Commerce',
    }
    return render(request, 'college_website/department_detail.html', context)

def management_department_view(request):
    """Management Department view"""
    college_info = get_college_info()
    management_programs = Program.objects.filter(is_active=True, discipline='management')
    context = {
        'college_info': college_info,
        'programs': management_programs,
        'department': 'Management',
    }
    return render(request, 'college_website/department_detail.html', context)

def programs_view(request):
    """Programs main view with enhanced filtering"""
    college_info = get_college_info()
    programs = Program.objects.filter(is_active=True)
    
    # Filter by discipline (stream)
    discipline = request.GET.get('discipline')
    if discipline:
        programs = programs.filter(discipline=discipline)
    
    # Filter by degree type
    degree_type = request.GET.get('degree_type')
    if degree_type:
        programs = programs.filter(degree_type=degree_type)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        programs = programs.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(short_name__icontains=search_query)
        )
    
    # Order programs
    programs = programs.order_by('discipline', 'name')
    
    # Pagination
    paginator = Paginator(programs, 12)  # Show 12 programs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'college_info': college_info,
        'programs': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'disciplines': Program.DISCIPLINE_CHOICES,
        'selected_discipline': request.GET.get('discipline', ''),
        'degree_types': Program.DEGREE_TYPE_CHOICES,
        'selected_degree_type': request.GET.get('degree_type', ''),
        'search_query': request.GET.get('search', ''),
    }
    return render(request, 'college_website/programs_list.html', context)

def ug_programs_view(request):
    """Undergraduate Programs view"""
    college_info = get_college_info()
    # Filter programs that are typically undergraduate
    ug_programs = Program.objects.filter(is_active=True)
    context = {
        'college_info': college_info,
        'programs': ug_programs,
        'program_level': 'Undergraduate',
    }
    return render(request, 'college_website/program_level.html', context)

def pg_programs_view(request):
    """Postgraduate Programs view"""
    college_info = get_college_info()
    # This would need to be filtered based on actual program levels in your data
    pg_programs = Program.objects.filter(is_active=True)
    context = {
        'college_info': college_info,
        'programs': pg_programs,
        'program_level': 'Postgraduate',
    }
    return render(request, 'college_website/program_level.html', context)

def diploma_certificate_view(request):
    """Diploma & Certificate Programs view"""
    college_info = get_college_info()
    diploma_programs = Program.objects.filter(is_active=True)
    context = {
        'college_info': college_info,
        'programs': diploma_programs,
        'program_level': 'Diploma & Certificate',
    }
    return render(request, 'college_website/program_level.html', context)

def phd_research_view(request):
    """PhD & Research view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/phd_research.html', context)

def academic_calendar_view(request):
    """Academic Calendar view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/academic_calendar.html', context)

def syllabus_curriculum_view(request):
    """Syllabus & Curriculum view"""
    college_info = get_college_info()
    programs = Program.objects.filter(is_active=True)
    context = {
        'college_info': college_info,
        'programs': programs,
    }
    return render(request, 'college_website/syllabus_curriculum.html', context)

def teaching_learning_resources_view(request):
    """Teaching Learning Resources view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/teaching_learning_resources.html', context)

# Admissions Section Views
def admissions_view(request):
    """Admissions main view"""
    college_info = get_college_info()
    admission_info = AdmissionInfo.objects.filter(is_active=True)
    context = {
        'college_info': college_info,
        'admission_info': admission_info,
    }
    return render(request, 'college_website/admissions.html', context)

def admission_guidelines_view(request):
    """Admission Guidelines view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/admission_guidelines.html', context)

def admission_eligibility_view(request):
    """Admission Eligibility view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/admission_eligibility.html', context)

def courses_offered_view(request):
    """Courses Offered view with dynamic program data"""
    college_info = get_college_info()
    
    # Get all active programs
    programs = Program.objects.filter(is_active=True).order_by('discipline', 'degree_type', 'name')
    
    # Separate undergraduate and postgraduate programs
    ug_programs = programs.filter(degree_type='undergraduate')
    pg_programs = programs.filter(degree_type='postgraduate')
    
    # Get unique departments
    departments = programs.values_list('department', flat=True).distinct().exclude(department__isnull=True).exclude(department='')
    
    context = {
        'college_info': college_info,
        'programs': programs,
        'ug_programs': ug_programs,
        'pg_programs': pg_programs,
        'total_programs': programs.count(),
        'total_departments': len(departments),
        'departments': departments,
    }
    return render(request, 'college_website/courses_offered.html', context)

def fee_structure_view(request):
    """Fee Structure view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/fee_structure.html', context)

def online_application_view(request):
    """Online Application view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/online_application.html', context)

def prospectus_view(request):
    """Prospectus view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/prospectus.html', context)

def scholarships_view(request):
    """Scholarships view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/scholarships.html', context)

# Examinations Section Views
def examinations_view(request):
    """Examinations main view"""
    college_info = get_college_info()
    recent_results = ExamResult.objects.filter(is_published=True)[:5]
    context = {
        'college_info': college_info,
        'recent_results': recent_results,
    }
    return render(request, 'college_website/examinations.html', context)

def exam_notices_view(request):
    """Exam Notices view"""
    college_info = get_college_info()
    exam_notices = Notice.objects.filter(is_active=True, category='exam')
    context = {
        'college_info': college_info,
        'notices': exam_notices,
    }
    return render(request, 'college_website/exam_notices.html', context)

def exam_timetable_view(request):
    """Exam Timetable view"""
    college_info = get_college_info()
    
    # Get active timetable (featured first, then most recent)
    active_timetable = ExamTimetable.objects.filter(is_active=True).order_by('-is_featured', '-created_at').first()
    
    if active_timetable:
        weeks = active_timetable.get_active_weeks()
        context = {
            'college_info': college_info,
            'timetable': active_timetable,
            'weeks': weeks,
        }
    else:
        context = {
            'college_info': college_info,
            'timetable': None,
            'weeks': [],
        }
    
    return render(request, 'college_website/exam_timetable.html', context)

def question_papers_view(request):
    """Question Papers view with dynamic data"""
    college_info = get_college_info()
    
    # Get all active question papers
    question_papers = QuestionPaper.objects.filter(is_active=True).order_by('-academic_year', 'semester', 'subject')
    
    # Get filter parameters
    subject_filter = request.GET.get('subject', '')
    semester_filter = request.GET.get('semester', '')
    year_filter = request.GET.get('year', '')
    search_query = request.GET.get('search', '')
    
    # Apply filters
    if subject_filter:
        question_papers = question_papers.filter(subject=subject_filter)
    if semester_filter:
        question_papers = question_papers.filter(semester=semester_filter)
    if year_filter:
        question_papers = question_papers.filter(academic_year__icontains=year_filter)
    if search_query:
        question_papers = question_papers.filter(
            Q(title__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Get available filter options
    available_subjects = QuestionPaper.get_available_subjects()
    available_semesters = QuestionPaper.get_available_semesters()
    available_years = QuestionPaper.get_available_years()
    
    # Separate featured and regular question papers
    featured_papers = question_papers.filter(is_featured=True)
    regular_papers = question_papers.filter(is_featured=False)
    
    context = {
        'college_info': college_info,
        'question_papers': question_papers,
        'featured_papers': featured_papers,
        'regular_papers': regular_papers,
        'available_subjects': available_subjects,
        'available_semesters': available_semesters,
        'available_years': available_years,
        'total_papers': question_papers.count(),
        'subject_filter': subject_filter,
        'semester_filter': semester_filter,
        'year_filter': year_filter,
        'search_query': search_query,
    }
    return render(request, 'college_website/question_papers.html', context)

def exam_results_view(request):
    """Exam Results view"""
    college_info = get_college_info()
    results = ExamResult.objects.filter(is_published=True)
    context = {
        'college_info': college_info,
        'results': results,
    }
    return render(request, 'college_website/exam_results.html', context)

def revaluation_view(request):
    """Revaluation view with dynamic content"""
    college_info = get_college_info()
    
    # Get active revaluation information
    revaluation_info = RevaluationInfo.objects.filter(is_active=True).first()
    
    # If no active revaluation info exists, create default one
    if not revaluation_info:
        revaluation_info = RevaluationInfo.objects.create(
            title="Revaluation",
            subtitle="Apply for revaluation of your examination papers",
            is_active=True
        )
    
    context = {
        'college_info': college_info,
        'revaluation_info': revaluation_info,
    }
    return render(request, 'college_website/revaluation.html', context)

def exam_rules_view(request):
    """Exam Rules view with dynamic content"""
    college_info = get_college_info()
    
    # Get active exam rules information
    exam_rules_info = ExamRulesInfo.objects.filter(is_active=True).first()
    
    # If no active exam rules info exists, create default one
    if not exam_rules_info:
        exam_rules_info = ExamRulesInfo.objects.create(
            title="Examination Rules & Regulations",
            subtitle="Important guidelines and rules for all examinations",
            is_active=True
        )
    
    context = {
        'college_info': college_info,
        'exam_rules_info': exam_rules_info,
    }
    return render(request, 'college_website/exam_rules.html', context)

# Research Section Views
def research_view(request):
    """Research main view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/research.html', context)

def research_centers_view(request):
    """Research Centers view with dynamic content"""
    college_info = get_college_info()
    
    # Get active research center information
    research_center_info = ResearchCenterInfo.objects.filter(is_active=True).first()
    
    # If no active research center info exists, create default one
    if not research_center_info:
        research_center_info = ResearchCenterInfo.objects.create(
            title="Research Centers",
            subtitle="Advancing knowledge through cutting-edge research and innovation",
            is_active=True
        )
    
    context = {
        'college_info': college_info,
        'research_center_info': research_center_info,
    }
    return render(request, 'college_website/research_centers.html', context)

def publications_view(request):
    """Publications view with dynamic content"""
    college_info = get_college_info()
    
    # Get active publication information
    publication_info = PublicationInfo.objects.filter(is_active=True).first()
    
    # If no active publication info exists, create default one
    if not publication_info:
        publication_info = PublicationInfo.objects.create(
            title="Research Publications",
            subtitle="Explore our extensive collection of research publications, academic papers, and scholarly works that contribute to the advancement of knowledge across various disciplines.",
            is_active=True
        )
    
    # Get publications with search and filter functionality
    publications = Publication.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        publications = publications.filter(
            Q(title__icontains=search_query) |
            Q(authors__icontains=search_query) |
            Q(abstract__icontains=search_query) |
            Q(journal_name__icontains=search_query)
        )
    
    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        publications = publications.filter(department=department_filter)
    
    # Filter by journal type
    journal_type_filter = request.GET.get('journal_type', '')
    if journal_type_filter:
        publications = publications.filter(journal_type=journal_type_filter)
    
    # Filter by year
    year_filter = request.GET.get('year', '')
    if year_filter:
        publications = publications.filter(publication_year=year_filter)
    
    # Sort publications
    sort_by = request.GET.get('sort_by', '-publication_year')
    publications = publications.order_by(sort_by)
    
    # Get featured publications
    featured_publications = publications.filter(is_featured=True)[:3]
    
    # Get recent publications (excluding featured)
    recent_publications = publications.exclude(is_featured=True)[:6]
    
    # Get available filter options
    available_departments = Publication.DEPARTMENT_CHOICES
    available_journal_types = Publication.JOURNAL_TYPE_CHOICES
    available_years = sorted(Publication.objects.filter(is_active=True).values_list('publication_year', flat=True).distinct(), reverse=True)
    
    context = {
        'college_info': college_info,
        'publication_info': publication_info,
        'publications': publications,
        'featured_publications': featured_publications,
        'recent_publications': recent_publications,
        'available_departments': available_departments,
        'available_journal_types': available_journal_types,
        'available_years': available_years,
        'search_query': search_query,
        'department_filter': department_filter,
        'journal_type_filter': journal_type_filter,
        'year_filter': year_filter,
        'sort_by': sort_by,
    }
    return render(request, 'college_website/publications.html', context)

def patents_projects_view(request):
    """Patents & Projects view with dynamic content"""
    college_info = get_college_info()
    
    # Get active patents & projects information
    patents_projects_info = PatentsProjectsInfo.objects.filter(is_active=True).first()
    
    # If no active info exists, create default one
    if not patents_projects_info:
        patents_projects_info = PatentsProjectsInfo.objects.create(
            title="Patents & Projects",
            subtitle="Explore our innovative research projects and intellectual property achievements that drive technological advancement and contribute to society.",
            is_active=True
        )
    
    # Get patents with search and filter functionality
    patents = Patent.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        patents = patents.filter(
            Q(title__icontains=search_query) |
            Q(inventors__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(patent_number__icontains=search_query)
        )
    
    # Filter by category (patent/project)
    category_filter = request.GET.get('category', '')
    if category_filter == 'patent':
        patents = patents
    elif category_filter == 'project':
        patents = Patent.objects.none()  # Will be handled by projects
    
    # Filter by year
    year_filter = request.GET.get('year', '')
    if year_filter:
        patents = patents.filter(filing_year=year_filter)
    
    # Sort patents
    sort_by = request.GET.get('sort_by', 'date-desc')
    if sort_by == 'date-desc':
        patents = patents.order_by('-filing_year')
    elif sort_by == 'date-asc':
        patents = patents.order_by('filing_year')
    elif sort_by == 'title':
        patents = patents.order_by('title')
    elif sort_by == 'title-desc':
        patents = patents.order_by('-title')
    
    # Get research projects
    projects = ResearchProject.objects.filter(is_active=True)
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(principal_investigator__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(funding_agency__icontains=search_query)
        )
    
    if year_filter:
        projects = projects.filter(start_year=year_filter)
    
    # Get industry collaborations
    collaborations = IndustryCollaboration.objects.filter(is_active=True)
    
    # Get featured items
    featured_patents = patents.filter(is_featured=True)[:2]
    featured_projects = projects.filter(is_featured=True)[:2]
    featured_collaborations = collaborations.filter(is_featured=True)[:3]
    
    # Get recent items (excluding featured)
    recent_patents = patents.exclude(is_featured=True)[:2]
    recent_projects = projects.exclude(is_featured=True)[:2]
    
    # Get available filter options
    available_years = sorted(
        list(set(
            list(Patent.objects.filter(is_active=True).values_list('filing_year', flat=True)) +
            list(ResearchProject.objects.filter(is_active=True).values_list('start_year', flat=True))
        )), reverse=True
    )
    
    context = {
        'college_info': college_info,
        'patents_projects_info': patents_projects_info,
        'patents': patents,
        'projects': projects,
        'collaborations': collaborations,
        'featured_patents': featured_patents,
        'featured_projects': featured_projects,
        'featured_collaborations': featured_collaborations,
        'recent_patents': recent_patents,
        'recent_projects': recent_projects,
        'available_years': available_years,
        'search_query': search_query,
        'category_filter': category_filter,
        'year_filter': year_filter,
        'sort_by': sort_by,
    }
    return render(request, 'college_website/patents_projects.html', context)

def collaborations_mous_view(request):
    """Collaborations & MOUs view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/collaborations_mous.html', context)

def innovation_incubation_view(request):
    """Innovation & Incubation view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/innovation_incubation.html', context)

def consultancy_view(request):
    """Consultancy view with dynamic content"""
    college_info = get_college_info()
    
    # Get active consultancy information
    consultancy_info = ConsultancyInfo.objects.filter(is_active=True).first()
    
    # If no active info exists, create default one
    if not consultancy_info:
        consultancy_info = ConsultancyInfo.objects.create(
            title="Consultancy Services",
            subtitle="Leveraging our academic expertise and research capabilities to provide innovative solutions for industry challenges. Our consultancy services bridge the gap between academia and industry.",
            is_active=True
        )
    
    # Get consultancy services
    services = ConsultancyService.objects.filter(is_active=True).order_by('display_order', 'title')
    
    # Get consultancy expertise areas
    expertise_areas = ConsultancyExpertise.objects.filter(is_active=True).order_by('display_order', 'title')
    
    # Get success stories
    success_stories = ConsultancySuccessStory.objects.filter(is_active=True).order_by('display_order', 'title')
    
    context = {
        'college_info': college_info,
        'consultancy_info': consultancy_info,
        'services': services,
        'expertise_areas': expertise_areas,
        'success_stories': success_stories,
    }
    return render(request, 'college_website/consultancy.html', context)

# Student Support Section Views
def student_support_view(request):
    """Student Support main view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/student_support.html', context)

def student_portal_view(request):
    """Student Portal view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/student_portal.html', context)

def student_register_view(request):
    """Student registration view"""
    college_info = get_college_info()
    
    if request.method == 'POST':
        # Handle form submission
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        student_id = request.POST.get('student_id')
        course = request.POST.get('course')
        year = request.POST.get('year')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        terms = request.POST.get('terms')
        newsletter = request.POST.get('newsletter')
        
        # Basic validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
        elif not terms:
            messages.error(request, 'Please accept the Terms of Service and Privacy Policy.')
        else:
            # Here you would typically create a user account
            # For now, we'll just show a success message
            messages.success(request, f'Account created successfully for {first_name} {last_name}! Please check your email for verification.')
            return redirect('college_website:student_portal')
    
    context = {'college_info': college_info}
    return render(request, 'college_website/student_register.html', context)

def student_login_view(request):
    """Student login view"""
    college_info = get_college_info()
    
    if request.method == 'POST':
        # Handle form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        # Basic validation
        if not username or not password:
            messages.error(request, 'Please fill in all required fields.')
        else:
            # Here you would typically authenticate the user
            # For now, we'll just show a success message
            messages.success(request, f'Welcome back, {username}!')
            return redirect('college_website:student_portal')
    
    context = {'college_info': college_info}
    return render(request, 'college_website/student_login.html', context)

def library_view(request):
    """Library view"""
    college_info = get_college_info()
    library_resources = LibraryResource.objects.filter(is_featured=True)[:10]
    context = {
        'college_info': college_info,
        'library_resources': library_resources,
    }
    return render(request, 'college_website/library.html', context)


# Exam Timetable Management Views
@login_required
def exam_timetable_manage(request):
    """Staff view for managing exam timetables"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Staff privileges required.")
        return redirect('college_website:exam_timetable')
    
    college_info = get_college_info()
    timetables = ExamTimetable.objects.all().order_by('-academic_year', 'semester')
    
    if request.method == 'POST':
        bulk_form = ExamTimetableBulkForm(request.POST)
        if bulk_form.is_valid():
            action = bulk_form.cleaned_data['action']
            selected_items = bulk_form.cleaned_data['selected_items']
            
            if action == 'activate':
                ExamTimetable.objects.filter(id__in=selected_items).update(is_active=True)
                messages.success(request, f"{len(selected_items)} timetable(s) activated.")
            elif action == 'deactivate':
                ExamTimetable.objects.filter(id__in=selected_items).update(is_active=False)
                messages.success(request, f"{len(selected_items)} timetable(s) deactivated.")
            elif action == 'delete':
                ExamTimetable.objects.filter(id__in=selected_items).delete()
                messages.success(request, f"{len(selected_items)} timetable(s) deleted.")
            
            return redirect('college_website:exam_timetable_manage')
    else:
        bulk_form = ExamTimetableBulkForm()
        # Populate choices for bulk form
        bulk_form.fields['selected_items'].choices = [(t.id, t.name) for t in timetables]
    
    context = {
        'college_info': college_info,
        'timetables': timetables,
        'bulk_form': bulk_form,
    }
    return render(request, 'college_website/exam_timetable_manage.html', context)


@login_required
def exam_timetable_create(request):
    """Staff view for creating new exam timetables"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Staff privileges required.")
        return redirect('college_website:exam_timetable')
    
    college_info = get_college_info()
    
    if request.method == 'POST':
        form = ExamTimetableForm(request.POST)
        if form.is_valid():
            timetable = form.save()
            messages.success(request, f"Timetable '{timetable.name}' created successfully!")
            return redirect('college_website:exam_timetable_edit', timetable_id=timetable.id)
    else:
        form = ExamTimetableForm()
    
    context = {
        'college_info': college_info,
        'form': form,
        'action': 'Create',
    }
    return render(request, 'college_website/exam_timetable_form.html', context)


@login_required
def exam_timetable_edit(request, timetable_id):
    """Staff view for editing exam timetables"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Staff privileges required.")
        return redirect('college_website:exam_timetable')
    
    college_info = get_college_info()
    timetable = get_object_or_404(ExamTimetable, id=timetable_id)
    
    if request.method == 'POST':
        form = ExamTimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            messages.success(request, f"Timetable '{timetable.name}' updated successfully!")
            return redirect('college_website:exam_timetable_edit', timetable_id=timetable.id)
    else:
        form = ExamTimetableForm(instance=timetable)
    
    context = {
        'college_info': college_info,
        'form': form,
        'timetable': timetable,
        'action': 'Edit',
    }
    return render(request, 'college_website/exam_timetable_form.html', context)


@login_required
def exam_timetable_week_manage(request, timetable_id):
    """Staff view for managing weeks in a timetable"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Staff privileges required.")
        return redirect('college_website:exam_timetable')
    
    college_info = get_college_info()
    timetable = get_object_or_404(ExamTimetable, id=timetable_id)
    weeks = timetable.weeks.all().order_by('week_number')
    
    if request.method == 'POST':
        week_form = ExamTimetableWeekForm(request.POST)
        if week_form.is_valid():
            week = week_form.save(commit=False)
            week.timetable = timetable
            week.save()
            messages.success(request, f"Week {week.week_number} added successfully!")
            return redirect('college_website:exam_timetable_week_manage', timetable_id=timetable_id)
    else:
        week_form = ExamTimetableWeekForm()
    
    context = {
        'college_info': college_info,
        'timetable': timetable,
        'weeks': weeks,
        'week_form': week_form,
    }
    return render(request, 'college_website/exam_timetable_week_manage.html', context)


@login_required
def exam_timetable_exam_manage(request, week_id):
    """Staff view for managing exams in a week"""
    if not request.user.is_staff:
        messages.error(request, "Access denied. Staff privileges required.")
        return redirect('college_website:exam_timetable')
    
    college_info = get_college_info()
    week = get_object_or_404(ExamTimetableWeek, id=week_id)
    time_slots = week.time_slots.all().order_by('start_time')
    
    if request.method == 'POST':
        exam_form = ExamTimetableExamForm(request.POST)
        if exam_form.is_valid():
            exam = exam_form.save(commit=False)
            exam.time_slot = exam_form.cleaned_data['time_slot']
            exam.save()
            messages.success(request, f"Exam '{exam.subject_name}' added successfully!")
            return redirect('college_website:exam_timetable_exam_manage', week_id=week_id)
    else:
        exam_form = ExamTimetableExamForm()
    
    context = {
        'college_info': college_info,
        'week': week,
        'time_slots': time_slots,
        'exam_form': exam_form,
    }
    return render(request, 'college_website/exam_timetable_exam_manage.html', context)

def hostel_view(request):
    """Hostel view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/hostel.html', context)

def sports_cultural_view(request):
    """Sports & Cultural view"""
    college_info = get_college_info()
    cultural_events = Event.objects.filter(is_active=True, type='celebration')
    context = {
        'college_info': college_info,
        'events': cultural_events,
    }
    return render(request, 'college_website/sports_cultural.html', context)

def nss_ncc_clubs_view(request):
    """NSS, NCC & Clubs view with dynamic content"""
    from .models import NSSNCCClub, NSSNCCNotice, NSSNCCGallery, NSSNCCAchievement
    from django.utils import timezone
    
    college_info = get_college_info()
    
    # Get active clubs
    clubs = NSSNCCClub.objects.filter(is_active=True).order_by('display_order', 'name')
    
    # Get featured clubs (before slicing)
    featured_clubs = clubs.filter(is_featured=True)[:3]
    
    # Get recent notices (not expired) - get featured notices before slicing
    notices_base = NSSNCCNotice.objects.filter(
        is_active=True,
        publish_date__lte=timezone.now()
    ).exclude(
        expiry_date__lt=timezone.now()
    ).order_by('-publish_date', '-created_at')
    
    # Get featured notices (before slicing)
    featured_notices = notices_base.filter(is_featured=True)[:5]
    
    # Get recent notices (after getting featured)
    notices = notices_base[:10]
    
    # Get gallery images
    gallery_images = NSSNCCGallery.objects.filter(is_active=True).order_by('display_order', '-created_at')[:12]
    
    # Get recent achievements
    achievements = NSSNCCAchievement.objects.filter(is_active=True).order_by('-achievement_date', 'display_order')[:6]
    
    context = {
        'college_info': college_info,
        'clubs': clubs,
        'notices': notices,
        'gallery_images': gallery_images,
        'achievements': achievements,
        'featured_clubs': featured_clubs,
        'featured_notices': featured_notices,
    }
    return render(request, 'college_website/nss_ncc_clubs.html', context)


def nss_ncc_notices_view(request):
    """View all NSS-NCC notices"""
    from .models import NSSNCCNotice, NSSNCCClub
    from django.utils import timezone
    from django.core.paginator import Paginator
    
    college_info = get_college_info()
    
    # Get all active notices (not expired)
    notices = NSSNCCNotice.objects.filter(
        is_active=True,
        publish_date__lte=timezone.now()
    ).exclude(
        expiry_date__lt=timezone.now()
    ).order_by('-publish_date', '-created_at')
    
    # Get all active clubs for filtering
    clubs = NSSNCCClub.objects.filter(is_active=True).order_by('name')
    
    # Filter by club if specified
    club_filter = request.GET.get('club')
    if club_filter:
        notices = notices.filter(related_club_id=club_filter)
    
    # Filter by category if specified
    category_filter = request.GET.get('category')
    if category_filter:
        notices = notices.filter(category=category_filter)
    
    # Paginate results
    paginator = Paginator(notices, 10)  # Show 10 notices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'college_info': college_info,
        'notices': page_obj,
        'clubs': clubs,
        'club_filter': club_filter,
        'category_filter': category_filter,
        'notice_categories': NSSNCCNotice.CATEGORY_CHOICES,
    }
    return render(request, 'college_website/nss_ncc_notices.html', context)

def placement_cell_view(request):
    """Placement Cell view"""
    college_info = get_college_info()
    recent_placements = PlacementRecord.objects.filter(is_published=True)[:10]
    context = {
        'college_info': college_info,
        'placements': recent_placements,
    }
    return render(request, 'college_website/placement_cell.html', context)

def alumni_view(request):
    """Enhanced Alumni view with search and filtering"""
    from django.db.models import Q
    
    college_info = get_college_info()
    
    # Get all published alumni
    alumni_list = AlumniProfile.objects.filter(is_published=True)
    
    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        alumni_list = alumni_list.filter(
            Q(name__icontains=search_query) |
            Q(current_company__icontains=search_query) |
            Q(current_position__icontains=search_query) |
            Q(course__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # Filter functionality
    filter_type = request.GET.get('filter', '')
    if filter_type == 'featured':
        alumni_list = alumni_list.filter(is_featured=True)
    elif filter_type == 'mentors':
        alumni_list = alumni_list.filter(willing_to_mentor=True)
    
    # Year-based filtering
    year_filter = request.GET.get('year', '')
    if year_filter:
        if year_filter == '2020-2024':
            alumni_list = alumni_list.filter(graduation_year__gte=2020, graduation_year__lte=2024)
        elif year_filter == '2015-2019':
            alumni_list = alumni_list.filter(graduation_year__gte=2015, graduation_year__lte=2019)
        elif year_filter == '2010-2014':
            alumni_list = alumni_list.filter(graduation_year__gte=2010, graduation_year__lte=2014)
        elif year_filter == '2005-2009':
            alumni_list = alumni_list.filter(graduation_year__gte=2005, graduation_year__lte=2009)
    
    # Order alumni
    alumni_list = alumni_list.order_by('-is_featured', '-graduation_year', 'name')
    
    # Generate graduation years for form
    from datetime import datetime
    current_year = datetime.now().year
    graduation_years = [str(year) for year in range(current_year, current_year - 50, -1)]
    
    # Statistics
    total_alumni = AlumniProfile.objects.filter(is_published=True).count()
    countries = 35  # You can calculate this from location data
    mentors = AlumniProfile.objects.filter(is_published=True, willing_to_mentor=True).count()
    industries = 60  # You can calculate this from company/position data
    
    context = {
        'college_info': college_info,
        'alumni': alumni_list,
        'graduation_years': graduation_years,
        'total_alumni': total_alumni,
        'countries': countries,
        'mentors': mentors,
        'industries': industries,
        'search_query': search_query,
        'filter_type': filter_type,
        'year_filter': year_filter,
    }
    return render(request, 'college_website/alumni.html', context)

# IQAC Section Views
def iqac_view(request):
    """IQAC main view with comprehensive information"""
    college_info = get_college_info()
    side_menus = get_side_menus_for_request(request)
    
    # Get IQAC information
    iqac_info = IQACInfo.objects.filter(is_active=True).first()
    
    # Get featured reports
    featured_reports = IQACReport.objects.filter(
        is_published=True, 
        is_featured=True
    ).order_by('-publish_date')[:6]
    
    # Get recent quality initiatives
    recent_initiatives = QualityInitiative.objects.filter(
        is_published=True,
        is_featured=True
    ).order_by('-start_date')[:4]
    
    # Get NAAC and NIRF info for overview cards
    naac_info = NAACInfo.objects.filter(is_active=True).first()
    nirf_info = NIRFInfo.objects.filter(is_active=True).first()
    
    # Get featured accreditations
    featured_accreditations = AccreditationInfo.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('display_order')[:3]
    
    context = {
        'college_info': college_info,
        'side_menus': side_menus,
        'iqac_info': iqac_info,
        'featured_reports': featured_reports,
        'recent_initiatives': recent_initiatives,
        'naac_info': naac_info,
        'nirf_info': nirf_info,
        'featured_accreditations': featured_accreditations,
        'page_title': 'Internal Quality Assurance Cell (IQAC)',
        'breadcrumbs': breadcrumb_context(request, 'IQAC'),
    }
    return render(request, 'college_website/iqac.html', context)

def iqac_reports_view(request):
    """IQAC Reports view with filtering and pagination"""
    college_info = get_college_info()
    side_menus = get_side_menus_for_request(request)
    
    # Get all published reports
    reports_queryset = IQACReport.objects.filter(is_published=True)
    
    # Filter by report type
    report_type = request.GET.get('type', 'all')
    if report_type != 'all':
        reports_queryset = reports_queryset.filter(report_type=report_type)
    
    # Filter by academic year
    year = request.GET.get('year')
    if year:
        reports_queryset = reports_queryset.filter(academic_year=year)
    
    # Search by title
    search_query = request.GET.get('q')
    if search_query:
        reports_queryset = reports_queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Order by publish date
    reports_queryset = reports_queryset.order_by('-publish_date', '-created_at')
    
    # Pagination
    paginator = Paginator(reports_queryset, 12)
    page_number = request.GET.get('page')
    reports = paginator.get_page(page_number)
    
    # Get available years and types for filters
    available_years = IQACReport.objects.filter(is_published=True).values_list(
        'academic_year', flat=True
    ).distinct().order_by('-academic_year')
    
    context = {
        'college_info': college_info,
        'side_menus': side_menus,
        'reports': reports,
        'report_types': IQACReport.REPORT_TYPES,
        'available_years': available_years,
        'selected_type': report_type,
        'selected_year': year,
        'search_query': search_query,
        'page_title': 'IQAC Reports',
        'breadcrumbs': breadcrumb_context(request, 'Reports'),
    }
    return render(request, 'college_website/iqac_reports.html', context)

def naac_view(request):
    """NAAC accreditation view with detailed information"""
    college_info = get_college_info()
    side_menus = get_side_menus_for_request(request)
    
    # Get NAAC information
    naac_info = NAACInfo.objects.filter(is_active=True).first()
    
    # Get NAAC related reports
    naac_reports = IQACReport.objects.filter(
        is_published=True,
        report_type='naac'
    ).order_by('-publish_date')[:5]
    
    context = {
        'college_info': college_info,
        'side_menus': side_menus,
        'naac_info': naac_info,
        'naac_reports': naac_reports,
        'page_title': 'NAAC Accreditation',
        'breadcrumbs': breadcrumb_context(request, 'NAAC'),
    }
    return render(request, 'college_website/naac.html', context)

def nirf_view(request):
    """NIRF rankings view with comprehensive data"""
    college_info = get_college_info()
    side_menus = get_side_menus_for_request(request)
    
    # Get all NIRF information ordered by year
    nirf_data = NIRFInfo.objects.filter(is_active=True).order_by('-ranking_year')
    
    # Get latest NIRF info
    latest_nirf = nirf_data.first()
    
    # Get NIRF related reports
    nirf_reports = IQACReport.objects.filter(
        is_published=True,
        report_type='nirf'
    ).order_by('-publish_date')[:5]
    
    context = {
        'college_info': college_info,
        'side_menus': side_menus,
        'nirf_data': nirf_data,
        'latest_nirf': latest_nirf,
        'nirf_reports': nirf_reports,
        'page_title': 'NIRF Rankings',
        'breadcrumbs': breadcrumb_context(request, 'NIRF'),
    }
    return render(request, 'college_website/nirf.html', context)

def accreditation_view(request):
    """Accreditation view with all institutional accreditations"""
    college_info = get_college_info()
    side_menus = get_side_menus_for_request(request)
    
    # Get all active accreditations
    accreditations = AccreditationInfo.objects.filter(
        is_active=True
    ).order_by('display_order', '-accreditation_date')
    
    # Separate featured and regular accreditations
    featured_accreditations = accreditations.filter(is_featured=True)
    other_accreditations = accreditations.filter(is_featured=False)
    
    context = {
        'college_info': college_info,
        'side_menus': side_menus,
        'featured_accreditations': featured_accreditations,
        'other_accreditations': other_accreditations,
        'all_accreditations': accreditations,
        'page_title': 'Accreditations & Certifications',
        'breadcrumbs': breadcrumb_context(request, 'Accreditation'),
    }
    return render(request, 'college_website/accreditation.html', context)

def iqac_feedback_view(request):
    """IQAC Feedback view with form handling"""
    college_info = get_college_info()
    side_menus = get_side_menus_for_request(request)
    
    if request.method == 'POST':
        # Handle feedback form submission
        from .forms import IQACFeedbackForm
        form = IQACFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            messages.success(
                request, 
                'Thank you for your feedback! Your input is valuable for our continuous improvement.'
            )
            return redirect('college_website:iqac_feedback')
    else:
        from .forms import IQACFeedbackForm
        form = IQACFeedbackForm()
    
    # Get recent feedback statistics (anonymized)
    total_feedback = IQACFeedback.objects.count()
    avg_ratings = {}
    
    if total_feedback > 0:
        from django.db.models import Avg
        ratings_avg = IQACFeedback.objects.aggregate(
            teaching_quality=Avg('teaching_quality'),
            infrastructure=Avg('infrastructure'),
            administration=Avg('administration'),
            library_resources=Avg('library_resources'),
            overall_satisfaction=Avg('overall_satisfaction'),
        )
        avg_ratings = {
            k: round(v, 1) if v else 0 for k, v in ratings_avg.items()
        }
    
    context = {
        'college_info': college_info,
        'side_menus': side_menus,
        'form': form,
        'total_feedback': total_feedback,
        'avg_ratings': avg_ratings,
        'feedback_types': IQACFeedback.FEEDBACK_TYPES,
        'rating_choices': IQACFeedback.RATING_CHOICES,
        'page_title': 'IQAC Feedback',
        'breadcrumbs': breadcrumb_context(request, 'Feedback'),
    }
    return render(request, 'college_website/iqac_feedback.html', context)

# Events Section Views
def events_view(request):
    """Events main view"""
    college_info = get_college_info()
    events = Event.objects.filter(is_active=True)
    context = {
        'college_info': college_info,
        'events': events,
    }
    return render(request, 'college_website/events.html', context)

def news_announcements_view(request):
    """News & Announcements view"""
    college_info = get_college_info()
    notices = Notice.objects.filter(is_active=True, category='general')
    context = {
        'college_info': college_info,
        'notices': notices,
    }
    return render(request, 'college_website/news_announcements.html', context)

def academic_events_view(request):
    """Academic Events view"""
    college_info = get_college_info()
    academic_events = Event.objects.filter(is_active=True, type='workshop')
    context = {
        'college_info': college_info,
        'events': academic_events,
    }
    return render(request, 'college_website/academic_events.html', context)

def extracurricular_events_view(request):
    """Extracurricular Events view"""
    college_info = get_college_info()
    extracurricular_events = Event.objects.filter(is_active=True).exclude(type='workshop')
    context = {
        'college_info': college_info,
        'events': extracurricular_events,
    }
    return render(request, 'college_website/extracurricular_events.html', context)

def events_gallery_view(request):
    """Events Gallery view"""
    college_info = get_college_info()
    event_galleries = Gallery.objects.filter(is_active=True, category='events')
    context = {
        'college_info': college_info,
        'galleries': event_galleries,
    }
    return render(request, 'college_website/events_gallery.html', context)

def annual_reports_view(request):
    """Annual Reports view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/annual_reports.html', context)

# Mandatory Disclosure Section Views
def mandatory_disclosure_view(request):
    """Mandatory Disclosure main view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/mandatory_disclosure.html', context)

def rti_view(request):
    """RTI view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/rti.html', context)

def institutional_policies_view(request):
    """Institutional Policies view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/institutional_policies.html', context)

def audit_reports_view(request):
    """Audit Reports view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/audit_reports.html', context)

def statutory_committees_view(request):
    """Statutory Committees view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/statutory_committees.html', context)

def grievance_cell_view(request):
    """Grievance Cell view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/grievance_cell.html', context)

def anti_ragging_committee_view(request):
    """Anti Ragging Committee view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/anti_ragging_committee.html', context)

def icc_view(request):
    """ICC (Internal Complaints Committee) view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/icc.html', context)

# Contact Section Views
def contact_info_view(request):
    """Contact Info view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/contact_info.html', context)

def campus_map_view(request):
    """Campus Map view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/campus_map.html', context)

def enquiry_form_view(request):
    """Enquiry Form view"""
    college_info = get_college_info()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your enquiry has been submitted successfully!')
            return redirect('college_website:enquiry_form')
    else:
        form = ContactForm()
    
    context = {
        'college_info': college_info,
        'form': form,
    }
    return render(request, 'college_website/enquiry_form.html', context)

def social_media_view(request):
    """Social Media view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/social_media.html', context)

# ============================================================================
# EXISTING VIEWS (LEGACY COMPATIBILITY)
# ============================================================================

def contact_view(request):
    """Contact page view"""
    college_info = get_college_info()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email notification (optional)
            try:
                send_mail(
                    subject=f'New Contact Form Submission from {contact_message.first_name} {contact_message.last_name}',
                    message=f'Name: {contact_message.first_name} {contact_message.last_name}\n'
                           f'Email: {contact_message.email}\n'
                           f'Phone: {contact_message.phone}\n'
                           f'Message: {contact_message.comments}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[college_info.email if college_info else 'admin@example.com'],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('college_website:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'college_info': college_info,
    }
    return render(request, 'college_website/contact.html', context)


def gallery_view(request):
    """Gallery page view with dynamic content"""
    from .models import Gallery
    
    # Get filter category from URL parameter
    category_filter = request.GET.get('category', 'all')
    
    # Get all active galleries
    galleries = Gallery.objects.filter(is_active=True).prefetch_related('photos')
    
    # Filter by category if specified
    if category_filter != 'all':
        galleries = galleries.filter(category=category_filter)
    
    # Get all available categories for filter tabs
    all_categories = Gallery.CATEGORY_CHOICES
    
    # Get category counts for display
    category_counts = {}
    for category_code, category_name in all_categories:
        count = Gallery.objects.filter(is_active=True, category=category_code).count()
        category_counts[category_code] = count
    
    # Total count for "All" tab
    total_count = Gallery.objects.filter(is_active=True).count()
    
    context = {
        'galleries': galleries,
        'categories': all_categories,
        'category_counts': category_counts,
        'total_count': total_count,
        'current_category': category_filter,
    }
    
    return render(request, 'college_website/gallery.html', context)


class GalleryDetailView(DetailView):
    """Individual gallery detail view with photos"""
    model = Gallery
    template_name = 'college_website/gallery_detail.html'
    context_object_name = 'gallery'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Gallery.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gallery = self.object
        
        # Get all active photos for this gallery
        photos = gallery.photos.filter(is_active=True).order_by('ordering', 'created_at')
        context['photos'] = photos
        
        # Get related galleries from same category
        related_galleries = Gallery.objects.filter(
            is_active=True, 
            category=gallery.category
        ).exclude(id=gallery.id)[:4]
        context['related_galleries'] = related_galleries
        
        return context


def achievements_view(request):
    """Achievements view"""
    college_info = get_college_info()
    context = {
        'college_info': college_info,
    }
    return render(request, 'college_website/achievements.html', context)


class DynamicPageView(DetailView):
    """Dynamic CMS page view"""
    model = Page
    template_name = 'college_website/page_detail.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Page.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.object
        
        # Get all content blocks for this page
        rich_text_blocks = page.rich_text_blocks.filter(is_active=True).order_by('ordering')
        gallery_blocks = page.gallery_blocks.filter(is_active=True).order_by('ordering')
        video_blocks = page.video_blocks.filter(is_active=True).order_by('ordering')
        download_blocks = page.download_blocks.filter(is_active=True).order_by('ordering')
        table_blocks = page.table_blocks.filter(is_active=True).order_by('ordering')
        form_blocks = page.form_blocks.filter(is_active=True).order_by('ordering')
        
        # Combine all blocks and sort by ordering
        all_blocks = []
        for block in rich_text_blocks:
            all_blocks.append(('rich_text', block))
        for block in gallery_blocks:
            all_blocks.append(('gallery', block))
        for block in video_blocks:
            all_blocks.append(('video', block))
        for block in download_blocks:
            all_blocks.append(('downloads', block))
        for block in table_blocks:
            all_blocks.append(('table', block))
        for block in form_blocks:
            all_blocks.append(('form', block))
        
        # Sort by ordering field
        all_blocks.sort(key=lambda x: x[1].ordering)
        
        context['content_blocks'] = all_blocks
        return context


def search_view(request):
    """Search functionality"""
    form = SearchForm(request.GET or None)
    results = []
    query = None
    total_count = 0
    
    if form.is_valid():
        query = form.cleaned_data['q']
        category = form.cleaned_data.get('category', 'all')
        
        if query:
            # Search in different models based on category
            if category == 'all' or category == 'notice':
                notices = Notice.objects.filter(
                    Q(title__icontains=query) | Q(content__icontains=query),
                    is_active=True
                )
                for notice in notices:
                    results.append({
                        'type': 'notice',
                        'title': notice.title,
                        'content': notice.content[:200] + '...' if len(notice.content) > 200 else notice.content,
                        'url': notice.get_absolute_url(),
                        'date': notice.publish_date,
                    })
            
            if category == 'all' or category == 'event':
                events = Event.objects.filter(
                    Q(title__icontains=query) | Q(description__icontains=query),
                    is_active=True
                )
                for event in events:
                    results.append({
                        'type': 'event',
                        'title': event.title,
                        'content': event.description[:200] + '...' if len(event.description) > 200 else event.description,
                        'url': event.get_absolute_url(),
                        'date': event.date,
                    })
            
            if category == 'all' or category == 'program':
                programs = Program.objects.filter(
                    Q(name__icontains=query) | Q(description__icontains=query),
                    is_active=True
                )
                for program in programs:
                    results.append({
                        'type': 'program',
                        'title': program.name,
                        'content': program.description[:200] + '...' if len(program.description) > 200 else program.description,
                        'url': program.get_absolute_url(),
                        'date': program.created_at,
                    })
            
            if category == 'all' or category == 'page':
                pages = Page.objects.filter(
                    Q(title__icontains=query) | Q(meta_description__icontains=query),
                    is_active=True
                )
                for page in pages:
                    results.append({
                        'type': 'page',
                        'title': page.title,
                        'content': page.meta_description or 'Page content...',
                        'url': page.get_absolute_url(),
                        'date': page.created_at,
                    })
            
            total_count = len(results)
            
            # Sort results by date (newest first)
            results.sort(key=lambda x: x['date'], reverse=True)
            
            # Paginate results
            paginator = Paginator(results, 10)
            page_number = request.GET.get('page')
            results = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'results': results,
        'query': query,
        'total_count': total_count,
    }
    return render(request, 'college_website/search.html', context)


def test_navbar_view(request):
    """Test view to check navbar"""
    return render(request, 'test_navbar.html')


def director_message_view(request):
    """Director's message page view"""
    director_message = DirectorMessage.objects.filter(is_active=True).first()
    college_info = get_college_info()
    
    if not director_message:
        raise Http404("Director's message not found or not active.")
    
    context = {
        'director_message': director_message,
        'college_info': college_info,
    }
    return render(request, 'college_website/director_message.html', context)


def principal_message_view(request):
    """Principal's message page view"""
    principal_message = PrincipalMessage.objects.filter(is_active=True).first()
    college_info = get_college_info()
    
    if not principal_message:
        raise Http404("Principal's message not found or not active.")
    
    context = {
        'principal_message': principal_message,
        'college_info': college_info,
    }
    return render(request, 'college_website/principal_message.html', context)


def breadcrumb_context(request, page_title=None):
    """Helper function to generate breadcrumbs"""
    breadcrumbs = [{'title': 'Home', 'url': '/'}]
    
    path = request.path.strip('/')
    if path:
        path_parts = path.split('/')
        current_url = ''
        
        for part in path_parts[:-1]:
            current_url += f'/{part}'
            breadcrumbs.append({
                'title': part.replace('-', ' ').title(),
                'url': current_url
            })
        
        if page_title:
            breadcrumbs.append({'title': page_title, 'url': None})
    
    return breadcrumbs


# Academic Section Views

class AdmissionsListView(ListView):
    """List view for admissions"""
    model = AdmissionInfo
    template_name = 'college_website/admissions.html'
    context_object_name = 'admissions'
    paginate_by = 10
    
    def get_queryset(self):
        return AdmissionInfo.objects.filter(is_active=True).order_by('ordering', '-created_at')


class AdmissionDetailView(DetailView):
    """Detail view for admission"""
    model = AdmissionInfo
    template_name = 'college_website/admission_detail.html'
    context_object_name = 'admission'
    
    def get_queryset(self):
        return AdmissionInfo.objects.filter(is_active=True)


class ResultsListView(ListView):
    """List view for exam results"""
    model = ExamResult
    template_name = 'college_website/results.html'
    context_object_name = 'results'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = ExamResult.objects.filter(is_published=True)
        
        # Filter by result type
        result_type = self.request.GET.get('type')
        if result_type and result_type != 'all':
            queryset = queryset.filter(result_type=result_type)
        
        return queryset.order_by('-result_date', '-created_at')


class ResultDetailView(DetailView):
    """Detail view for exam result"""
    model = ExamResult
    template_name = 'college_website/result_detail.html'
    context_object_name = 'result'
    
    def get_queryset(self):
        return ExamResult.objects.filter(is_published=True)


class LibraryListView(ListView):
    """List view for library resources"""
    model = LibraryResource
    template_name = 'college_website/library.html'
    context_object_name = 'resources'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = LibraryResource.objects.all()
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(subject_category__icontains=query) |
                Q(isbn__icontains=query)
            )
        
        # Filter by resource type
        resource_type = self.request.GET.get('type')
        if resource_type and resource_type != 'all':
            queryset = queryset.filter(resource_type=resource_type)
        
        return queryset.order_by('-is_featured', 'title')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add some stats (you can replace these with actual database queries)
        context.update({
            'total_books': LibraryResource.objects.filter(resource_type='book').count(),
            'digital_resources': LibraryResource.objects.exclude(digital_copy='').count(),
            'journals': LibraryResource.objects.filter(resource_type='journal').count(),
            'active_users': 800,  # This could be calculated from user data
        })
        return context


class LibraryDetailView(DetailView):
    """Detail view for library resource"""
    model = LibraryResource
    template_name = 'college_website/library_detail.html'
    context_object_name = 'resource'


class ELearningListView(ListView):
    """List view for e-learning courses"""
    model = ELearningCourse
    template_name = 'college_website/elearning.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = ELearningCourse.objects.all()
        
        # Filter by difficulty level
        difficulty = self.request.GET.get('difficulty')
        if difficulty and difficulty != 'all':
            queryset = queryset.filter(difficulty_level=difficulty)
        
        # Filter by fee (free courses)
        fee_filter = self.request.GET.get('fee')
        if fee_filter == 'free':
            queryset = queryset.filter(enrollment_fee=0)
        
        return queryset.order_by('-is_featured', '-is_active', 'title')


class ELearningDetailView(DetailView):
    """Detail view for e-learning course"""
    model = ELearningCourse
    template_name = 'college_website/elearning_detail.html'
    context_object_name = 'course'


class PlacementsListView(ListView):
    """List view for placement records"""
    model = PlacementRecord
    template_name = 'college_website/placements.html'
    context_object_name = 'placements'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = PlacementRecord.objects.filter(is_published=True)
        
        # Filter by graduation year
        year = self.request.GET.get('year')
        if year and year != 'all':
            if '-' in year:
                # Handle year ranges like "2020-2024"
                start_year, end_year = year.split('-')
                queryset = queryset.filter(
                    graduation_year__gte=int(start_year),
                    graduation_year__lte=int(end_year)
                )
            else:
                queryset = queryset.filter(graduation_year=int(year))
        
        # Filter by job type
        job_type = self.request.GET.get('type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        
        # Filter featured placements
        if self.request.GET.get('featured') == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset.order_by('-is_featured', '-placement_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add placement statistics (replace with actual calculations)
        context.update({
            'placement_percentage': 95,
            'highest_package': 25,
            'average_package': 8.5,
            'total_companies': 150,
        })
        return context


class AlumniListView(ListView):
    """List view for alumni profiles"""
    model = AlumniProfile
    template_name = 'college_website/alumni.html'
    context_object_name = 'alumni_profiles'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = AlumniProfile.objects.filter(is_published=True)
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(current_company__icontains=query) |
                Q(current_position__icontains=query) |
                Q(course__icontains=query)
            )
        
        # Filter options
        filter_type = self.request.GET.get('filter')
        if filter_type == 'featured':
            queryset = queryset.filter(is_featured=True)
        elif filter_type == 'mentors':
            queryset = queryset.filter(willing_to_mentor=True)
        
        # Filter by graduation year ranges
        year_range = self.request.GET.get('year')
        if year_range:
            if '-' in year_range:
                start_year, end_year = year_range.split('-')
                queryset = queryset.filter(
                    graduation_year__gte=int(start_year),
                    graduation_year__lte=int(end_year)
                )
        
        return queryset.order_by('-is_featured', '-graduation_year', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add alumni statistics (replace with actual calculations)
        context.update({
            'total_alumni': AlumniProfile.objects.filter(is_published=True).count(),
            'countries': 25,  # This could be calculated from location data
            'mentors': AlumniProfile.objects.filter(willing_to_mentor=True, is_published=True).count(),
            'industries': 50,  # This could be calculated from company/position data
        })
        return context


class AlumniDetailView(DetailView):
    """Detail view for alumni profile"""
    model = AlumniProfile
    template_name = 'college_website/alumni_detail.html'
    context_object_name = 'alumni'
    
    def get_queryset(self):
        return AlumniProfile.objects.filter(is_published=True)


class DepartmentListView(ListView):
    """List view for departments with filtering by discipline"""
    model = Department
    template_name = 'college_website/departments_list.html'
    context_object_name = 'departments'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Department.objects.filter(is_active=True)
        discipline = self.request.GET.get('discipline')
        if discipline:
            queryset = queryset.filter(discipline=discipline)
        return queryset.order_by('ordering', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discipline = self.request.GET.get('discipline')
        
        context.update({
            'current_discipline': discipline,
            'discipline_choices': Department.DISCIPLINE_CHOICES,
            'total_departments': Department.objects.filter(is_active=True).count(),
            'science_count': Department.objects.filter(is_active=True, discipline='science').count(),
            'arts_count': Department.objects.filter(is_active=True, discipline='arts').count(),
            'commerce_count': Department.objects.filter(is_active=True, discipline='commerce').count(),
            'featured_departments': Department.objects.filter(is_active=True, is_featured=True)[:3],
        })
        return context


class DepartmentDetailView(DetailView):
    """Detail view for individual department"""
    model = Department
    template_name = 'college_website/department_detail.html'
    context_object_name = 'department'
    
    def get_queryset(self):
        return Department.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        
        # Get related programs
        related_programs = department.get_programs()
        
        # Get other departments in same discipline
        related_departments = Department.objects.filter(
            discipline=department.discipline,
            is_active=True
        ).exclude(pk=department.pk)[:4]
        
        context.update({
            'related_programs': related_programs,
            'related_departments': related_departments,
            'laboratories_list': [lab.strip() for lab in department.laboratories.split('\n') if lab.strip()] if department.laboratories else [],
            'research_areas_list': [area.strip() for area in department.research_areas.split('\n') if area.strip()] if department.research_areas else [],
            'programs_offered_list': [program.strip() for program in department.programs_offered.split('\n') if program.strip()] if department.programs_offered else [],
            'facilities_list': [facility.strip() for facility in department.facilities.split('\n') if facility.strip()] if department.facilities else [],
        })
        return context


def hero_banner_management(request):
    """View for managing hero banner content and styling"""
    from .forms import HeroBannerForm
    
    if request.method == 'POST':
        form = HeroBannerForm(request.POST, request.FILES)
        if form.is_valid():
            hero_banner = form.save()
            messages.success(request, f'Hero banner "{hero_banner.title}" has been saved successfully!')
            return redirect('college_website:hero_banner_management')
    else:
        # Try to get existing active hero banner or create new form
        try:
            hero_banner = HeroBanner.objects.filter(is_active=True).first()
            if hero_banner:
                form = HeroBannerForm(instance=hero_banner)
            else:
                form = HeroBannerForm()
        except:
            form = HeroBannerForm()
    
    # Get all hero banners for management
    all_hero_banners = HeroBanner.objects.all().order_by('order', '-created_at')
    
    context = {
        'form': form,
        'hero_banners': all_hero_banners,
        'active_banner': HeroBanner.objects.filter(is_active=True).first(),
    }

    return render(request, 'college_website/hero_banner_management.html', context)


# Program Management Views
@login_required
def program_list_view(request):
    """List all programs with management options"""
    college_info = get_college_info()
    programs = Program.objects.all().order_by('discipline', 'name')
    
    # Filter by discipline
    discipline = request.GET.get('discipline')
    if discipline:
        programs = programs.filter(discipline=discipline)
    
    # Filter by degree type
    degree_type = request.GET.get('degree_type')
    if degree_type:
        programs = programs.filter(degree_type=degree_type)
    
    # Filter by active status
    is_active = request.GET.get('is_active')
    if is_active is not None:
        programs = programs.filter(is_active=is_active == 'true')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        programs = programs.filter(
            Q(name__icontains=search_query) |
            Q(short_name__icontains=search_query) |
            Q(department__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(programs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'college_info': college_info,
        'programs': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'disciplines': Program.DISCIPLINE_CHOICES,
        'degree_types': Program.DEGREE_TYPE_CHOICES,
        'selected_discipline': discipline,
        'selected_degree_type': degree_type,
        'selected_is_active': is_active,
        'search_query': search_query,
    }
    return render(request, 'college_website/program_list.html', context)


@login_required
def program_create_view(request):
    """Create a new program"""
    college_info = get_college_info()
    
    if request.method == 'POST':
        form = ProgramCreateForm(request.POST, request.FILES)
        if form.is_valid():
            program = form.save()
            messages.success(request, f'Program "{program.name}" created successfully!')
            return redirect('college_website:program_detail', slug=program.slug)
    else:
        form = ProgramCreateForm()
    
    context = {
        'college_info': college_info,
        'form': form,
        'title': 'Create New Program',
    }
    return render(request, 'college_website/program_form.html', context)


@login_required
def program_update_view(request, slug):
    """Update an existing program"""
    college_info = get_college_info()
    
    try:
        program = Program.objects.get(slug=slug)
    except Program.DoesNotExist:
        messages.error(request, 'Program not found.')
        return redirect('college_website:program_list')
    
    if request.method == 'POST':
        form = ProgramUpdateForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            program = form.save()
            messages.success(request, f'Program "{program.name}" updated successfully!')
            return redirect('college_website:program_detail', slug=program.slug)
    else:
        form = ProgramUpdateForm(instance=program)
    
    context = {
        'college_info': college_info,
        'form': form,
        'program': program,
        'title': f'Update {program.name}',
    }
    return render(request, 'college_website/program_form.html', context)


@login_required
def program_quick_edit_view(request, slug):
    """Quick edit form for basic program information"""
    college_info = get_college_info()
    
    try:
        program = Program.objects.get(slug=slug)
    except Program.DoesNotExist:
        messages.error(request, 'Program not found.')
        return redirect('college_website:program_list')
    
    if request.method == 'POST':
        form = ProgramQuickEditForm(request.POST, instance=program)
        if form.is_valid():
            program = form.save()
            messages.success(request, f'Program "{program.name}" updated successfully!')
            return redirect('college_website:program_list')
    else:
        form = ProgramQuickEditForm(instance=program)
    
    context = {
        'college_info': college_info,
        'form': form,
        'program': program,
        'title': f'Quick Edit - {program.name}',
    }
    return render(request, 'college_website/program_quick_edit.html', context)


@login_required
def program_delete_view(request, slug):
    """Delete a program"""
    college_info = get_college_info()
    
    try:
        program = Program.objects.get(slug=slug)
    except Program.DoesNotExist:
        messages.error(request, 'Program not found.')
        return redirect('college_website:program_list')
    
    if request.method == 'POST':
        program_name = program.name
        program.delete()
        messages.success(request, f'Program "{program_name}" deleted successfully!')
        return redirect('college_website:program_list')
    
    context = {
        'college_info': college_info,
        'program': program,
    }
    return render(request, 'college_website/program_confirm_delete.html', context)


@login_required
def program_toggle_status_view(request, slug):
    """Toggle program active status"""
    try:
        program = Program.objects.get(slug=slug)
        program.is_active = not program.is_active
        program.save()
        
        status = "activated" if program.is_active else "deactivated"
        messages.success(request, f'Program "{program.name}" {status} successfully!')
    except Program.DoesNotExist:
        messages.error(request, 'Program not found.')
    
    return redirect('college_website:program_list')


@login_required
def program_toggle_featured_view(request, slug):
    """Toggle program featured status"""
    try:
        program = Program.objects.get(slug=slug)
        program.is_featured = not program.is_featured
        program.save()
        
        status = "featured" if program.is_featured else "unfeatured"
        messages.success(request, f'Program "{program.name}" {status} successfully!')
    except Program.DoesNotExist:
        messages.error(request, 'Program not found.')
    
    return redirect('college_website:program_list')


def program_detail_view(request, slug):
    """Detailed view of a specific program"""
    college_info = get_college_info()
    
    try:
        program = Program.objects.get(slug=slug, is_active=True)
    except Program.DoesNotExist:
        messages.error(request, 'Program not found or not available.')
        return redirect('college_website:programs')
    
    # Get related programs
    related_programs = Program.objects.filter(
        is_active=True,
        discipline=program.discipline
    ).exclude(id=program.id)[:4]
    
    context = {
        'college_info': college_info,
        'program': program,
        'related_programs': related_programs,
    }
    return render(request, 'college_website/program_detail.html', context)


# Question Paper Management Views
@login_required
def question_paper_list_view(request):
    """List all question papers with management options"""
    from .forms import QuestionPaperSearchForm
    
    # Get all question papers
    question_papers = QuestionPaper.objects.all().order_by('-academic_year', 'semester', 'subject')
    
    # Apply search and filters
    search_form = QuestionPaperSearchForm(request.GET)
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        subject = search_form.cleaned_data.get('subject')
        semester = search_form.cleaned_data.get('semester')
        degree_type = search_form.cleaned_data.get('degree_type')
        academic_year = search_form.cleaned_data.get('academic_year')
        is_featured = search_form.cleaned_data.get('is_featured')
        
        if search:
            question_papers = question_papers.filter(
                Q(title__icontains=search) |
                Q(subject__icontains=search) |
                Q(description__icontains=search)
            )
        if subject:
            question_papers = question_papers.filter(subject=subject)
        if semester:
            question_papers = question_papers.filter(semester=semester)
        if degree_type:
            question_papers = question_papers.filter(degree_type=degree_type)
        if academic_year:
            question_papers = question_papers.filter(academic_year__icontains=academic_year)
        if is_featured:
            question_papers = question_papers.filter(is_featured=True)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(question_papers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'question_papers': page_obj,
        'search_form': search_form,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'college_website/question_paper_list.html', context)


@login_required
def question_paper_create_view(request):
    """Create new question paper"""
    from .forms import QuestionPaperCreateForm
    
    if request.method == 'POST':
        form = QuestionPaperCreateForm(request.POST, request.FILES)
        if form.is_valid():
            question_paper = form.save()
            messages.success(request, f'Question paper "{question_paper.title}" created successfully!')
            return redirect('college_website:question_paper_list')
    else:
        form = QuestionPaperCreateForm()
    
    context = {
        'form': form,
        'title': 'Create Question Paper',
        'submit_text': 'Create Question Paper',
    }
    return render(request, 'college_website/question_paper_form.html', context)


@login_required
def question_paper_update_view(request, slug):
    """Update existing question paper"""
    from .forms import QuestionPaperUpdateForm
    
    try:
        question_paper = QuestionPaper.objects.get(slug=slug)
    except QuestionPaper.DoesNotExist:
        messages.error(request, 'Question paper not found.')
        return redirect('college_website:question_paper_list')
    
    if request.method == 'POST':
        form = QuestionPaperUpdateForm(request.POST, request.FILES, instance=question_paper)
        if form.is_valid():
            question_paper = form.save()
            messages.success(request, f'Question paper "{question_paper.title}" updated successfully!')
            return redirect('college_website:question_paper_list')
    else:
        form = QuestionPaperUpdateForm(instance=question_paper)
    
    context = {
        'form': form,
        'question_paper': question_paper,
        'title': 'Update Question Paper',
        'submit_text': 'Update Question Paper',
    }
    return render(request, 'college_website/question_paper_form.html', context)


@login_required
def question_paper_quick_edit_view(request, slug):
    """Quick edit for essential question paper fields"""
    from .forms import QuestionPaperQuickEditForm
    
    try:
        question_paper = QuestionPaper.objects.get(slug=slug)
    except QuestionPaper.DoesNotExist:
        messages.error(request, 'Question paper not found.')
        return redirect('college_website:question_paper_list')
    
    if request.method == 'POST':
        form = QuestionPaperQuickEditForm(request.POST, instance=question_paper)
        if form.is_valid():
            question_paper = form.save()
            messages.success(request, f'Question paper "{question_paper.title}" updated successfully!')
            return redirect('college_website:question_paper_list')
    else:
        form = QuestionPaperQuickEditForm(instance=question_paper)
    
    context = {
        'form': form,
        'question_paper': question_paper,
        'title': 'Quick Edit Question Paper',
        'submit_text': 'Update',
    }
    return render(request, 'college_website/question_paper_quick_edit.html', context)


@login_required
def question_paper_delete_view(request, slug):
    """Delete question paper"""
    try:
        question_paper = QuestionPaper.objects.get(slug=slug)
    except QuestionPaper.DoesNotExist:
        messages.error(request, 'Question paper not found.')
        return redirect('college_website:question_paper_list')
    
    if request.method == 'POST':
        title = question_paper.title
        question_paper.delete()
        messages.success(request, f'Question paper "{title}" deleted successfully!')
        return redirect('college_website:question_paper_list')
    
    context = {
        'question_paper': question_paper,
    }
    return render(request, 'college_website/question_paper_confirm_delete.html', context)


@login_required
def question_paper_toggle_status_view(request, slug):
    """Toggle active status of question paper"""
    try:
        question_paper = QuestionPaper.objects.get(slug=slug)
        question_paper.is_active = not question_paper.is_active
        question_paper.save()
        
        status = "activated" if question_paper.is_active else "deactivated"
        messages.success(request, f'Question paper "{question_paper.title}" {status} successfully!')
    except QuestionPaper.DoesNotExist:
        messages.error(request, 'Question paper not found.')
    
    return redirect('college_website:question_paper_list')


@login_required
def question_paper_toggle_featured_view(request, slug):
    """Toggle featured status of question paper"""
    try:
        question_paper = QuestionPaper.objects.get(slug=slug)
        question_paper.is_featured = not question_paper.is_featured
        question_paper.save()
        
        status = "featured" if question_paper.is_featured else "unfeatured"
        messages.success(request, f'Question paper "{question_paper.title}" {status} successfully!')
    except QuestionPaper.DoesNotExist:
        messages.error(request, 'Question paper not found.')
    
    return redirect('college_website:question_paper_list')


def question_paper_detail_view(request, slug):
    """Public view for question paper details"""
    try:
        question_paper = QuestionPaper.objects.get(slug=slug, is_active=True)
    except QuestionPaper.DoesNotExist:
        messages.error(request, 'Question paper not found.')
        return redirect('college_website:question_papers')
    
    # Get related question papers
    related_papers = QuestionPaper.objects.filter(
        is_active=True,
        subject=question_paper.subject
    ).exclude(id=question_paper.id)[:4]
    
    context = {
        'question_paper': question_paper,
        'related_papers': related_papers,
    }
    return render(request, 'college_website/question_paper_detail.html', context)


def question_paper_download_view(request, slug):
    """Handle question paper downloads"""
    try:
        question_paper = QuestionPaper.objects.get(slug=slug, is_active=True)
        
        # Increment download count
        question_paper.increment_download_count()
        
        # Return file response
        from django.http import FileResponse
        return FileResponse(
            question_paper.question_paper_file,
            as_attachment=True,
            filename=f"{question_paper.title}.pdf"
        )
    except QuestionPaper.DoesNotExist:
        messages.error(request, 'Question paper not found.')
        return redirect('college_website:question_papers')


def navigation_demo_view(request):
    """Navigation demo page to showcase the new navigation menu"""
    college_info = get_college_info()
    
    context = {
        'college_info': college_info,
        'page_title': 'Navigation Demo',
    }
    return render(request, 'college_website/navigation_demo.html', context)


def test_navigation_view(request):
    """Simple test page for navigation"""
    return render(request, 'test_navigation.html')


def simple_nav_test_view(request):
    """Ultra-simple navigation test page"""
    return render(request, 'simple_nav_test.html')
