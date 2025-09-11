from django.core.management.base import BaseCommand
from college_website.models import Menu, MenuItem


class Command(BaseCommand):
    help = 'Create hierarchical menu structure for college website'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating hierarchical menu structure...'))

        # Create Main Navigation Menu
        main_menu, created = Menu.objects.get_or_create(
            title='Main Navigation',
            defaults={
                'slug': 'main-navigation',
                'is_active': True,
                'ordering': 1
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created Main Navigation menu'))

        # Clear existing menu items if they exist
        main_menu.items.all().delete()

        # Define the menu structure
        menu_structure = [
            {
                'title': 'Home',
                'path_type': 'named_url',
                'named_url': 'college_website:home',
                'icon_class': 'fas fa-home',
                'ordering': 1,
                'children': [
                    {
                        'title': 'About Institution',
                        'path_type': 'named_url',
                        'named_url': 'college_website:about_institution',
                        'ordering': 1
                    },
                    {
                        'title': 'History',
                        'path_type': 'named_url',
                        'named_url': 'college_website:history',
                        'ordering': 2
                    },
                    {
                        'title': "Principal's Message",
                        'path_type': 'named_url',
                        'named_url': 'college_website:principal_message',
                        'ordering': 3
                    },
                    {
                        'title': 'Governing Body',
                        'path_type': 'named_url',
                        'named_url': 'college_website:governing_body',
                        'ordering': 4
                    }
                ]
            },
            {
                'title': 'About',
                'path_type': 'named_url',
                'named_url': 'college_website:about',
                'icon_class': 'fas fa-info-circle',
                'ordering': 2,
                'children': [
                    {
                        'title': 'Overview',
                        'path_type': 'named_url',
                        'named_url': 'college_website:about_overview',
                        'ordering': 1
                    },
                    {
                        'title': 'Administration',
                        'path_type': 'named_url',
                        'named_url': 'college_website:administration',
                        'ordering': 2
                    },
                    {
                        'title': 'Organizational Structure',
                        'path_type': 'named_url',
                        'named_url': 'college_website:organizational_structure',
                        'ordering': 3
                    },
                    {
                        'title': 'Statutory Approvals',
                        'path_type': 'named_url',
                        'named_url': 'college_website:statutory_approvals',
                        'ordering': 4
                    },
                    {
                        'title': 'Infrastructure',
                        'path_type': 'named_url',
                        'named_url': 'college_website:infrastructure',
                        'ordering': 5
                    },
                    {
                        'title': 'Policies',
                        'path_type': 'named_url',
                        'named_url': 'college_website:policies',
                        'ordering': 6,
                        'children': [
                            {
                                'title': 'Anti-Ragging Policy',
                                'path_type': 'named_url',
                                'named_url': 'college_website:anti_ragging_policy',
                                'ordering': 1
                            },
                            {
                                'title': 'Grievance Redressal',
                                'path_type': 'named_url',
                                'named_url': 'college_website:grievance_redressal_policy',
                                'ordering': 2
                            },
                            {
                                'title': 'Code of Conduct',
                                'path_type': 'named_url',
                                'named_url': 'college_website:code_of_conduct_policy',
                                'ordering': 3
                            }
                        ]
                    }
                ]
            },
            {
                'title': 'Academics',
                'path_type': 'named_url',
                'named_url': 'college_website:academics',
                'icon_class': 'fas fa-graduation-cap',
                'ordering': 3,
                'children': [
                    {
                        'title': 'Faculties',
                        'path_type': 'named_url',
                        'named_url': 'college_website:faculties',
                        'ordering': 1
                    },
                    {
                        'title': 'Departments',
                        'path_type': 'named_url',
                        'named_url': 'college_website:departments',
                        'ordering': 2,
                        'children': [
                            {
                                'title': 'Arts',
                                'path_type': 'named_url',
                                'named_url': 'college_website:arts_department',
                                'ordering': 1
                            },
                            {
                                'title': 'Science',
                                'path_type': 'named_url',
                                'named_url': 'college_website:science_department',
                                'ordering': 2
                            },
                            {
                                'title': 'Commerce',
                                'path_type': 'named_url',
                                'named_url': 'college_website:commerce_department',
                                'ordering': 3
                            },
                            {
                                'title': 'Management',
                                'path_type': 'named_url',
                                'named_url': 'college_website:management_department',
                                'ordering': 4
                            }
                        ]
                    },
                    {
                        'title': 'Programs',
                        'path_type': 'named_url',
                        'named_url': 'college_website:programs',
                        'ordering': 3,
                        'children': [
                            {
                                'title': 'Undergraduate',
                                'path_type': 'named_url',
                                'named_url': 'college_website:ug_programs',
                                'ordering': 1
                            },
                            {
                                'title': 'Postgraduate',
                                'path_type': 'named_url',
                                'named_url': 'college_website:pg_programs',
                                'ordering': 2
                            },
                            {
                                'title': 'Diploma & Certificate',
                                'path_type': 'named_url',
                                'named_url': 'college_website:diploma_certificate',
                                'ordering': 3
                            },
                            {
                                'title': 'PhD & Research',
                                'path_type': 'named_url',
                                'named_url': 'college_website:phd_research',
                                'ordering': 4
                            }
                        ]
                    },
                    {
                        'title': 'Academic Calendar',
                        'path_type': 'named_url',
                        'named_url': 'college_website:academic_calendar',
                        'ordering': 4
                    },
                    {
                        'title': 'Syllabus & Curriculum',
                        'path_type': 'named_url',
                        'named_url': 'college_website:syllabus_curriculum',
                        'ordering': 5
                    },
                    {
                        'title': 'Teaching Learning Resources',
                        'path_type': 'named_url',
                        'named_url': 'college_website:teaching_learning_resources',
                        'ordering': 6
                    }
                ]
            },
            {
                'title': 'Admissions',
                'path_type': 'named_url',
                'named_url': 'college_website:admissions',
                'icon_class': 'fas fa-user-plus',
                'ordering': 4,
                'children': [
                    {
                        'title': 'Guidelines',
                        'path_type': 'named_url',
                        'named_url': 'college_website:admission_guidelines',
                        'ordering': 1
                    },
                    {
                        'title': 'Eligibility',
                        'path_type': 'named_url',
                        'named_url': 'college_website:admission_eligibility',
                        'ordering': 2
                    },
                    {
                        'title': 'Courses Offered',
                        'path_type': 'named_url',
                        'named_url': 'college_website:courses_offered',
                        'ordering': 3
                    },
                    {
                        'title': 'Fee Structure',
                        'path_type': 'named_url',
                        'named_url': 'college_website:fee_structure',
                        'ordering': 4
                    },
                    {
                        'title': 'Online Application',
                        'path_type': 'named_url',
                        'named_url': 'college_website:online_application',
                        'ordering': 5
                    },
                    {
                        'title': 'Prospectus',
                        'path_type': 'named_url',
                        'named_url': 'college_website:prospectus',
                        'ordering': 6
                    },
                    {
                        'title': 'Scholarships',
                        'path_type': 'named_url',
                        'named_url': 'college_website:scholarships',
                        'ordering': 7
                    }
                ]
            },
            {
                'title': 'Examinations',
                'path_type': 'named_url',
                'named_url': 'college_website:examinations',
                'icon_class': 'fas fa-clipboard-list',
                'ordering': 5,
                'children': [
                    {
                        'title': 'Notices',
                        'path_type': 'named_url',
                        'named_url': 'college_website:exam_notices',
                        'ordering': 1
                    },
                    {
                        'title': 'Timetable',
                        'path_type': 'named_url',
                        'named_url': 'college_website:exam_timetable',
                        'ordering': 2
                    },
                    {
                        'title': 'Question Papers',
                        'path_type': 'named_url',
                        'named_url': 'college_website:question_papers',
                        'ordering': 3
                    },
                    {
                        'title': 'Results',
                        'path_type': 'named_url',
                        'named_url': 'college_website:exam_results',
                        'ordering': 4
                    },
                    {
                        'title': 'Revaluation',
                        'path_type': 'named_url',
                        'named_url': 'college_website:revaluation',
                        'ordering': 5
                    },
                    {
                        'title': 'Rules',
                        'path_type': 'named_url',
                        'named_url': 'college_website:exam_rules',
                        'ordering': 6
                    }
                ]
            },
            {
                'title': 'Research',
                'path_type': 'named_url',
                'named_url': 'college_website:research',
                'icon_class': 'fas fa-microscope',
                'ordering': 6,
                'children': [
                    {
                        'title': 'Research Centers',
                        'path_type': 'named_url',
                        'named_url': 'college_website:research_centers',
                        'ordering': 1
                    },
                    {
                        'title': 'Publications',
                        'path_type': 'named_url',
                        'named_url': 'college_website:publications',
                        'ordering': 2
                    },
                    {
                        'title': 'Patents & Projects',
                        'path_type': 'named_url',
                        'named_url': 'college_website:patents_projects',
                        'ordering': 3
                    },
                    {
                        'title': 'Collaborations & MOUs',
                        'path_type': 'named_url',
                        'named_url': 'college_website:collaborations_mous',
                        'ordering': 4
                    },
                    {
                        'title': 'Innovation & Incubation',
                        'path_type': 'named_url',
                        'named_url': 'college_website:innovation_incubation',
                        'ordering': 5
                    },
                    {
                        'title': 'Consultancy',
                        'path_type': 'named_url',
                        'named_url': 'college_website:consultancy',
                        'ordering': 6
                    }
                ]
            },
            # Student Portal moved to main nav level
            {
                'title': 'Student Portal',
                'path_type': 'named_url',
                'named_url': 'college_website:student_portal',
                'icon_class': 'fas fa-user-graduate',
                'ordering': 7
            },
            # Library moved to main nav level
            {
                'title': 'Library',
                'path_type': 'named_url',
                'named_url': 'college_website:library',
                'icon_class': 'fas fa-book-reader',
                'ordering': 8
            },
            # Sports & Cultural moved to main nav level
            {
                'title': 'Sports & Cultural',
                'path_type': 'named_url',
                'named_url': 'college_website:sports_cultural',
                'icon_class': 'fas fa-running',
                'ordering': 9
            },
            # NSS, NCC & Clubs moved to main nav level
            {
                'title': 'NSS, NCC & Clubs',
                'path_type': 'named_url',
                'named_url': 'college_website:nss_ncc_clubs',
                'icon_class': 'fas fa-users',
                'ordering': 10
            },
            # Placement Cell moved to main nav level
            {
                'title': 'Placement Cell',
                'path_type': 'named_url',
                'named_url': 'college_website:placement_cell',
                'icon_class': 'fas fa-briefcase',
                'ordering': 11
            },
            # Alumni moved to main nav level
            {
                'title': 'Alumni',
                'path_type': 'named_url',
                'named_url': 'college_website:alumni',
                'icon_class': 'fas fa-user-tie',
                'ordering': 12
            },
            # Student Support with only Hostel remaining
            {
                'title': 'Student Support',
                'path_type': 'named_url',
                'named_url': 'college_website:student_support',
                'icon_class': 'fas fa-user-friends',
                'ordering': 13,
                'children': [
                    {
                        'title': 'Hostel',
                        'path_type': 'named_url',
                        'named_url': 'college_website:hostel',
                        'ordering': 1
                    }
                ]
            },
            {
                'title': 'IQAC',
                'path_type': 'named_url',
                'named_url': 'college_website:iqac',
                'icon_class': 'fas fa-award',
                'ordering': 14,
                'children': [
                    {
                        'title': 'Reports',
                        'path_type': 'named_url',
                        'named_url': 'college_website:iqac_reports',
                        'ordering': 1
                    },
                    {
                        'title': 'NAAC',
                        'path_type': 'named_url',
                        'named_url': 'college_website:naac',
                        'ordering': 2
                    },
                    {
                        'title': 'NIRF',
                        'path_type': 'named_url',
                        'named_url': 'college_website:nirf',
                        'ordering': 3
                    },
                    {
                        'title': 'Accreditation',
                        'path_type': 'named_url',
                        'named_url': 'college_website:accreditation',
                        'ordering': 4
                    },
                    {
                        'title': 'Feedback',
                        'path_type': 'named_url',
                        'named_url': 'college_website:iqac_feedback',
                        'ordering': 5
                    }
                ]
            },
            {
                'title': 'Events',
                'path_type': 'named_url',
                'named_url': 'college_website:events',
                'icon_class': 'fas fa-calendar-alt',
                'ordering': 15,
                'children': [
                    {
                        'title': 'News & Announcements',
                        'path_type': 'named_url',
                        'named_url': 'college_website:news_announcements',
                        'ordering': 1
                    },
                    {
                        'title': 'Academic Events',
                        'path_type': 'named_url',
                        'named_url': 'college_website:academic_events',
                        'ordering': 2
                    },
                    {
                        'title': 'Extracurricular Events',
                        'path_type': 'named_url',
                        'named_url': 'college_website:extracurricular_events',
                        'ordering': 3
                    },
                    {
                        'title': 'Gallery',
                        'path_type': 'named_url',
                        'named_url': 'college_website:events_gallery',
                        'ordering': 4
                    },
                    {
                        'title': 'Annual Reports',
                        'path_type': 'named_url',
                        'named_url': 'college_website:annual_reports',
                        'ordering': 5
                    }
                ]
            },
            {
                'title': 'Mandatory Disclosure',
                'path_type': 'named_url',
                'named_url': 'college_website:mandatory_disclosure',
                'icon_class': 'fas fa-file-alt',
                'ordering': 16,
                'children': [
                    {
                        'title': 'RTI',
                        'path_type': 'named_url',
                        'named_url': 'college_website:rti',
                        'ordering': 1
                    },
                    {
                        'title': 'Institutional Policies',
                        'path_type': 'named_url',
                        'named_url': 'college_website:institutional_policies',
                        'ordering': 2
                    },
                    {
                        'title': 'Audit Reports',
                        'path_type': 'named_url',
                        'named_url': 'college_website:audit_reports',
                        'ordering': 3
                    },
                    {
                        'title': 'Statutory Committees',
                        'path_type': 'named_url',
                        'named_url': 'college_website:statutory_committees',
                        'ordering': 4,
                        'children': [
                            {
                                'title': 'Grievance Cell',
                                'path_type': 'named_url',
                                'named_url': 'college_website:grievance_cell',
                                'ordering': 1
                            },
                            {
                                'title': 'Anti-Ragging Committee',
                                'path_type': 'named_url',
                                'named_url': 'college_website:anti_ragging_committee',
                                'ordering': 2
                            },
                            {
                                'title': 'ICC',
                                'path_type': 'named_url',
                                'named_url': 'college_website:icc',
                                'ordering': 3
                            }
                        ]
                    }
                ]
            },
            {
                'title': 'Contact',
                'path_type': 'named_url',
                'named_url': 'college_website:contact',
                'icon_class': 'fas fa-envelope',
                'ordering': 17,
                'children': [
                    {
                        'title': 'Contact Info',
                        'path_type': 'named_url',
                        'named_url': 'college_website:contact_info',
                        'ordering': 1
                    },
                    {
                        'title': 'Campus Map',
                        'path_type': 'named_url',
                        'named_url': 'college_website:campus_map',
                        'ordering': 2
                    },
                    {
                        'title': 'Enquiry Form',
                        'path_type': 'named_url',
                        'named_url': 'college_website:enquiry_form',
                        'ordering': 3
                    },
                    {
                        'title': 'Social Media',
                        'path_type': 'named_url',
                        'named_url': 'college_website:social_media',
                        'ordering': 4
                    }
                ]
            }
        ]

        # Create menu items
        created_items = self.create_menu_items(main_menu, menu_structure)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_items} menu items for hierarchical navigation!'
            )
        )

    def create_menu_items(self, menu, items, parent=None):
        """Recursively create menu items"""
        created_count = 0
        
        for item_data in items:
            # Create the menu item
            menu_item = MenuItem.objects.create(
                menu=menu,
                parent=parent,
                title=item_data['title'],
                path_type=item_data.get('path_type', 'named_url'),
                named_url=item_data.get('named_url', ''),
                external_url=item_data.get('external_url', ''),
                icon_class=item_data.get('icon_class', ''),
                description=item_data.get('description', ''),
                ordering=item_data.get('ordering', 0),
                is_active=True
            )
            
            created_count += 1
            self.stdout.write(f'Created menu item: {menu_item.title}')
            
            # Create children if they exist
            if 'children' in item_data:
                child_count = self.create_menu_items(menu, item_data['children'], menu_item)
                created_count += child_count
                
        return created_count
