from django.apps import AppConfig


class CollegeWebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'college_website'
    
    def ready(self):
        """Import signal handlers when the app is ready"""
        import college_website.signals
