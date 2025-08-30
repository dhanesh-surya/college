# PythonAnywhere Deployment Guide

## Why PythonAnywhere?
- ✅ **No credit card required** for free tier
- ✅ **3 months free** trial
- ✅ **Django optimized** hosting
- ✅ **Easy file upload** via web interface

## Step-by-Step Setup

### 1. Create Account
- Go to [pythonanywhere.com](https://www.pythonanywhere.com)
- Sign up for free account
- Choose "Beginner" plan (free for 3 months)

### 2. Upload Your Project
**Option A: Via Web Interface**
- Go to Files tab in dashboard
- Create folder: `/home/yourusername/chaitanya-college-website`
- Upload all project files

**Option B: Via Git (Recommended)**
```bash
# In PythonAnywhere console
git clone https://github.com/yourusername/chaitanya-college-website.git
cd chaitanya-college-website
```

### 3. Set Up Virtual Environment
```bash
# In PythonAnywhere console
mkvirtualenv --python=/usr/bin/python3.11 college-env
pip install -r requirements.txt
```

### 4. Configure Web App
- Go to Web tab in dashboard
- Click "Add a new web app"
- Choose "Manual configuration"
- Select Python 3.11
- Set source code path: `/home/yourusername/chaitanya-college-website`
- Set virtualenv path: `/home/yourusername/.virtualenvs/college-env`

### 5. Configure WSGI File
Replace WSGI file content with:
```python
import os
import sys

# Add your project directory to Python path
path = '/home/yourusername/chaitanya-college-website'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'chaitanya_site.settings'
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'your-production-secret-key-here'
os.environ['ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 6. Configure Static Files
In Web tab, add static files mapping:
- URL: `/static/`
- Directory: `/home/yourusername/chaitanya-college-website/staticfiles/`

Add media files mapping:
- URL: `/media/`
- Directory: `/home/yourusername/chaitanya-college-website/media/`

### 7. Run Django Commands
```bash
# In PythonAnywhere console
cd chaitanya-college-website
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 8. Reload Web App
- Go to Web tab
- Click "Reload yourusername.pythonanywhere.com"
- Visit your site: `https://yourusername.pythonanywhere.com`

## Troubleshooting

### Common Issues:
1. **Import errors**: Check virtualenv activation
2. **Static files not loading**: Verify static files mapping
3. **Database errors**: Run migrations in console
4. **500 errors**: Check error logs in Web tab

### Useful Commands:
```bash
# Activate virtual environment
workon college-env

# Check Django version
python -m django --version

# Test Django setup
python manage.py check

# View error logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log
```
