from django.urls import path, include
from . import views
from . import navbar_views

app_name = 'college_website'

urlpatterns = [
    # Homepage
    path('', views.home_view, name='home'),
    
    # Menu Test (for debugging)
    path('menu-test/', views.menu_test_view, name='menu_test'),
    
<<<<<<< HEAD
    # Navbar Configuration
    path('admin/navbar-config/', navbar_views.navbar_config_view, name='navbar_config'),
    path('admin/navbar-config/reset/', navbar_views.navbar_config_reset, name='navbar_config_reset'),
    path('admin/navbar-preview/', navbar_views.navbar_preview, name='navbar_preview'),
    
=======
>>>>>>> a11168e (Fix)
    # Home Section
    path('home/', include([
        path('', views.home_view, name='home_index'),
        path('about-institution/', views.about_institution_view, name='about_institution'),
        path('history/', views.history_view, name='history'),
        path('principal-message/', views.principal_message_view, name='principal_message'),
        path('governing-body/', views.governing_body_view, name='governing_body'),
    ])),
    
    # About Section
    path('about/', include([
        path('', views.about_view, name='about'),
        path('history/', views.history_view, name='history'),
        path('vision-mission/', views.vision_mission_view, name='vision_mission'),
        path('overview/', views.about_overview_view, name='about_overview'),
        path('administration/', views.administration_view, name='administration'),
        path('organizational-structure/', views.organizational_structure_view, name='organizational_structure'),
        path('statutory-approvals/', views.statutory_approvals_view, name='statutory_approvals'),
        path('infrastructure/', views.infrastructure_view, name='infrastructure'),
        path('policies/', include([
            path('', views.policies_view, name='policies'),
            path('anti-ragging/', views.anti_ragging_policy_view, name='anti_ragging_policy'),
            path('grievance-redressal/', views.grievance_redressal_policy_view, name='grievance_redressal_policy'),
            path('code-of-conduct/', views.code_of_conduct_policy_view, name='code_of_conduct_policy'),
        ])),
    ])),
    
    # Academics Section
    path('academics/', include([
        path('', views.academics_view, name='academics'),
        path('faculties/', views.faculties_view, name='faculties'),
        path('academic-faculties/', views.academic_faculties_view, name='academic_faculties'),
        path('non-academic-faculties/', views.non_academic_faculties_view, name='non_academic_faculties'),
        path('faculty/<slug:dept_slug>/<slug:slug>/', views.faculty_detail_view, name='faculty_detail'),
        path('staff/<slug:dept_slug>/<slug:slug>/', views.staff_detail_view, name='staff_detail'),
        path('departments/', include([
            path('', views.DepartmentListView.as_view(), name='departments_list'),
            path('<slug:slug>/', views.DepartmentDetailView.as_view(), name='department_detail'),
        ])),
        path('programs/', include([
            path('', views.programs_view, name='programs'),
            path('ug/', views.ug_programs_view, name='ug_programs'),
            path('pg/', views.pg_programs_view, name='pg_programs'),
            path('diploma-certificate/', views.diploma_certificate_view, name='diploma_certificate'),
            path('phd-research/', views.phd_research_view, name='phd_research'),
        ])),
        path('academic-calendar/', views.academic_calendar_view, name='academic_calendar'),
        path('academic-calendar/<str:year>/pdf/', views.academic_calendar_pdf_view, name='academic_calendar_pdf'),
        path('syllabus-curriculum/', views.syllabus_curriculum_view, name='syllabus_curriculum'),
        path('teaching-learning-resources/', views.teaching_learning_resources_view, name='teaching_learning_resources'),
        path('library/', views.LibraryListView.as_view(), name='academics_library'),
        path('library/<slug:slug>/', views.LibraryDetailView.as_view(), name='academics_library_detail'),
    ])),
    
    # Admissions Section
    path('admissions/', include([
        path('', views.admissions_view, name='admissions'),
        path('guidelines/', views.admission_guidelines_view, name='admission_guidelines'),
        path('eligibility/', views.admission_eligibility_view, name='admission_eligibility'),
        path('courses-offered/', views.courses_offered_view, name='courses_offered'),
        path('fee-structure/', views.fee_structure_view, name='fee_structure'),
        path('online-application/', views.online_application_view, name='online_application'),
        path('prospectus/', views.prospectus_view, name='prospectus'),
        path('scholarships/', views.scholarships_view, name='scholarships'),
        path('<slug:slug>/', views.AdmissionDetailView.as_view(), name='admission_detail'),
    ])),
    
    # Examinations Section
    path('examinations/', include([
        path('', views.examinations_view, name='examinations'),
        path('notices/', views.exam_notices_view, name='exam_notices'),
        path('timetable/', views.exam_timetable_view, name='exam_timetable'),
        path('question-papers/', views.question_papers_view, name='question_papers'),
        path('question-papers/<slug:slug>/', views.question_paper_detail_view, name='question_paper_detail'),
        path('question-papers/<slug:slug>/download/', views.question_paper_download_view, name='question_paper_download'),
        path('results/', views.exam_results_view, name='exam_results'),
        path('results/<slug:slug>/', views.ResultDetailView.as_view(), name='result_detail'),
        path('revaluation/', views.revaluation_view, name='revaluation'),
        path('rules/', views.exam_rules_view, name='exam_rules'),
        # Exam Timetable Management (Staff Only)
        path('timetable/manage/', views.exam_timetable_manage, name='exam_timetable_manage'),
        path('timetable/create/', views.exam_timetable_create, name='exam_timetable_create'),
        path('timetable/<int:timetable_id>/edit/', views.exam_timetable_edit, name='exam_timetable_edit'),
        path('timetable/<int:timetable_id>/weeks/', views.exam_timetable_week_manage, name='exam_timetable_week_manage'),
        path('timetable/week/<int:week_id>/exams/', views.exam_timetable_exam_manage, name='exam_timetable_exam_manage'),
    ])),
    
    # Research Section
    path('research/', include([
        path('', views.research_view, name='research'),
        path('research-centers/', views.research_centers_view, name='research_centers'),
        path('publications/', views.publications_view, name='publications'),
        path('patents-projects/', views.patents_projects_view, name='patents_projects'),
        path('collaborations-mous/', views.collaborations_mous_view, name='collaborations_mous'),
        path('innovation-incubation/', views.innovation_incubation_view, name='innovation_incubation'),
        path('consultancy/', views.consultancy_view, name='consultancy'),
    ])),
    
    # Student Support Section
    path('student-support/', include([
        path('', views.student_support_view, name='student_support'),
        path('portal/', views.student_portal_view, name='student_portal'),
        path('register/', views.student_register_view, name='student_register'),
        path('login/', views.student_login_view, name='student_login'),
        path('library/', views.library_view, name='library'),
        path('library/<slug:slug>/', views.LibraryDetailView.as_view(), name='library_detail'),
        path('hostel/', views.hostel_view, name='hostel'),
        path('sports-cultural/', views.sports_cultural_view, name='sports_cultural'),
        path('nss-ncc-clubs/', views.nss_ncc_clubs_view, name='nss_ncc_clubs'),
        path('nss-ncc-notices/', views.nss_ncc_notices_view, name='nss_ncc_notices'),
        path('placement-cell/', views.placement_cell_view, name='placement_cell'),
        path('alumni/', views.alumni_view, name='alumni'),
        path('alumni/<slug:slug>/', views.AlumniDetailView.as_view(), name='alumni_detail'),
    ])),
    
    # IQAC Section
    path('iqac/', include([
        path('', views.iqac_view, name='iqac'),
        path('reports/', views.iqac_reports_view, name='iqac_reports'),
        path('naac/', views.naac_view, name='naac'),
        path('nirf/', views.nirf_view, name='nirf'),
        path('accreditation/', views.accreditation_view, name='accreditation'),
        path('feedback/', views.iqac_feedback_view, name='iqac_feedback'),
    ])),
    
    # Events Section
    path('events/', include([
        path('', views.events_view, name='events'),
        path('news-announcements/', views.news_announcements_view, name='news_announcements'),
        path('academic-events/', views.academic_events_view, name='academic_events'),
        path('extracurricular-events/', views.extracurricular_events_view, name='extracurricular_events'),
        path('gallery/', views.events_gallery_view, name='events_gallery'),
        path('annual-reports/', views.annual_reports_view, name='annual_reports'),
        path('<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
    ])),
    
    # Mandatory Disclosure Section
    path('mandatory-disclosure/', include([
        path('', views.mandatory_disclosure_view, name='mandatory_disclosure'),
        path('rti/', views.rti_view, name='rti'),
        path('institutional-policies/', views.institutional_policies_view, name='institutional_policies'),
        path('audit-reports/', views.audit_reports_view, name='audit_reports'),
        path('statutory-committees/', include([
            path('', views.statutory_committees_view, name='statutory_committees'),
            path('grievance-cell/', views.grievance_cell_view, name='grievance_cell'),
            path('anti-ragging/', views.anti_ragging_committee_view, name='anti_ragging_committee'),
            path('icc/', views.icc_view, name='icc'),
        ])),
    ])),
    
    # Contact Section
    path('contact/', include([
        path('', views.contact_view, name='contact'),
        path('contact-info/', views.contact_info_view, name='contact_info'),
        path('campus-map/', views.campus_map_view, name='campus_map'),
        path('enquiry-form/', views.enquiry_form_view, name='enquiry_form'),
        path('social-media/', views.social_media_view, name='social_media'),
    ])),
    
    # Program Management URLs (must come before legacy URLs to avoid conflicts)
    path('admin/programs/', include([
        path('', views.program_list_view, name='program_list'),
        path('create/', views.program_create_view, name='program_create'),
        path('<slug:slug>/', include([
            path('', views.program_detail_view, name='program_detail_public'),
            path('edit/', views.program_update_view, name='program_update'),
            path('quick-edit/', views.program_quick_edit_view, name='program_quick_edit'),
            path('delete/', views.program_delete_view, name='program_delete'),
            path('toggle-status/', views.program_toggle_status_view, name='program_toggle_status'),
            path('toggle-featured/', views.program_toggle_featured_view, name='program_toggle_featured'),
        ])),
    ])),
    
    # Question Paper Management URLs
    path('admin/question-papers/', include([
        path('', views.question_paper_list_view, name='question_paper_list'),
        path('create/', views.question_paper_create_view, name='question_paper_create'),
        path('<slug:slug>/', include([
            path('edit/', views.question_paper_update_view, name='question_paper_update'),
            path('quick-edit/', views.question_paper_quick_edit_view, name='question_paper_quick_edit'),
            path('delete/', views.question_paper_delete_view, name='question_paper_delete'),
            path('toggle-status/', views.question_paper_toggle_status_view, name='question_paper_toggle_status'),
            path('toggle-featured/', views.question_paper_toggle_featured_view, name='question_paper_toggle_featured'),
        ])),
    ])),
    
    # Legacy URLs for backward compatibility
    path('programs/', views.programs_view, name='programs_list'),
    path('programs/<slug:slug>/', views.ProgramDetailView.as_view(), name='program_detail'),
    path('notices/', views.NoticesListView.as_view(), name='notices_list'),
    path('notices/<slug:slug>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    path('social-impact/', views.SocialImpactView.as_view(), name='social_impact'),
    path('social-impact/<slug:slug>/', views.SocialInitiativeDetailView.as_view(), name='social_initiative_detail'),
    path('student-corner/', views.student_corner_view, name='student_corner'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('gallery/<slug:slug>/', views.GalleryDetailView.as_view(), name='gallery_detail'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('search/', views.search_view, name='search'),
    path('e-learning/', views.ELearningListView.as_view(), name='elearning'),
    path('e-learning/<slug:slug>/', views.ELearningDetailView.as_view(), name='elearning_detail'),
    path('placements/', views.PlacementsListView.as_view(), name='placements'),
    path('placement/', views.PlacementsListView.as_view(), name='placement'),
    path('alumni/', views.alumni_view, name='alumni_list'),
    path('alumni/<slug:slug>/', views.AlumniDetailView.as_view(), name='alumni_profile_detail'),
    path('leadership/director/', views.director_message_view, name='director_message'),
    path('test-navbar/', views.test_navbar_view, name='test_navbar'),
    path('navigation-demo/', views.navigation_demo_view, name='navigation_demo'),
    path('test-nav/', views.test_navigation_view, name='test_navigation'),
    path('simple-nav-test/', views.simple_nav_test_view, name='simple_nav_test'),
    
    # Hero Banner Management
    path('hero-banner/', views.hero_banner_management, name='hero_banner_management'),
    
    # Hero Banner Management
    path('hero-banner/', views.hero_banner_management, name='hero_banner_management'),
    
    # Dynamic CMS Pages (must be last to avoid conflicts)
    path('p/<slug:slug>/', views.DynamicPageView.as_view(), name='page_detail'),
]
