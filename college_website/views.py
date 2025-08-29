from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    CollegeInfo, Program, Event, Notice, SocialInitiative,
    StudentTestimonial, ImportantLink, ContactMessage, Page,
    Menu, MenuItem, BlockRichText, BlockImageGallery, BlockVideoEmbed,
    BlockDownloadList, BlockTableHTML, BlockForm, Gallery, GalleryPhoto,
    AdmissionInfo, ExamResult, LibraryResource, ELearningCourse, 
    PlacementRecord, AlumniProfile, DirectorMessage, PrincipalMessage,
    IQACInfo, IQACReport, NAACInfo, NIRFInfo, AccreditationInfo, 
    IQACFeedback, QualityInitiative, SideMenu, SideMenuItem
)
from .forms import ContactForm, SearchForm


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
    college_info = get_college_info()
    recent_notices = Notice.objects.filter(is_active=True)[:5]
    recent_events = Event.objects.filter(is_active=True)[:5]
    testimonials = StudentTestimonial.objects.filter(is_active=True)[:6]
    quick_links = ImportantLink.objects.filter(is_active=True, type='quick')[:6]
    
    # Get director's and principal's messages for homepage display
    director_message = DirectorMessage.objects.filter(is_active=True, show_on_homepage=True).first()
    principal_message = PrincipalMessage.objects.filter(is_active=True, show_on_homepage=True).first()
    
    context = {
        'college_info': college_info,
        'recent_notices': recent_notices,
        'recent_events': recent_events,
        'testimonials': testimonials,
        'quick_links': quick_links,
        'director_message': director_message,
        'principal_message': principal_message,
    }
    return render(request, 'college_website/home.html', context)


def about_view(request):
    """About page view"""
    college_info = get_college_info()
    context = {
        'college_info': college_info,
    }
    return render(request, 'college_website/about.html', context)


class ProgramsListView(ListView):
    """Programs listing view"""
    model = Program
    template_name = 'college_website/programs_list.html'
    context_object_name = 'programs'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Program.objects.filter(is_active=True)
        discipline = self.request.GET.get('discipline')
        if discipline:
            queryset = queryset.filter(discipline=discipline)
        return queryset.order_by('discipline', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disciplines'] = Program.DISCIPLINE_CHOICES
        context['selected_discipline'] = self.request.GET.get('discipline', '')
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
    college_info = get_college_info()
    context = {'college_info': college_info}
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
    """Academics main view"""
    college_info = get_college_info()
    programs = Program.objects.filter(is_active=True)
    context = {
        'college_info': college_info,
        'programs': programs,
    }
    return render(request, 'college_website/academics.html', context)

def faculties_view(request):
    """Faculties view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/faculties.html', context)

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
    """Programs main view"""
    college_info = get_college_info()
    programs = Program.objects.filter(is_active=True)
    context = {
        'college_info': college_info,
        'programs': programs,
    }
    return render(request, 'college_website/programs.html', context)

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
    """Courses Offered view"""
    college_info = get_college_info()
    programs = Program.objects.filter(is_active=True)
    context = {
        'college_info': college_info,
        'programs': programs,
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
    context = {'college_info': college_info}
    return render(request, 'college_website/exam_timetable.html', context)

def question_papers_view(request):
    """Question Papers view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
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
    """Revaluation view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/revaluation.html', context)

def exam_rules_view(request):
    """Exam Rules view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/exam_rules.html', context)

# Research Section Views
def research_view(request):
    """Research main view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/research.html', context)

def research_centers_view(request):
    """Research Centers view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/research_centers.html', context)

def publications_view(request):
    """Publications view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/publications.html', context)

def patents_projects_view(request):
    """Patents & Projects view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
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
    """Consultancy view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
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

def library_view(request):
    """Library view"""
    college_info = get_college_info()
    library_resources = LibraryResource.objects.filter(is_featured=True)[:10]
    context = {
        'college_info': college_info,
        'library_resources': library_resources,
    }
    return render(request, 'college_website/library.html', context)

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
    """NSS, NCC & Clubs view"""
    college_info = get_college_info()
    context = {'college_info': college_info}
    return render(request, 'college_website/nss_ncc_clubs.html', context)

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
    """Alumni view"""
    college_info = get_college_info()
    featured_alumni = AlumniProfile.objects.filter(is_featured=True, is_published=True)
    context = {
        'college_info': college_info,
        'alumni': featured_alumni,
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
