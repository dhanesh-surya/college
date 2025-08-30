#!/bin/bash

# Django College Website Deployment Script
# Choose your deployment method by uncommenting the relevant section

echo "🚀 Starting deployment process..."

# =============================================================================
# HEROKU DEPLOYMENT
# =============================================================================
deploy_to_heroku() {
    echo "📦 Deploying to Heroku..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI not found. Please install it first."
        echo "   Download from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Login to Heroku (if not already logged in)
    echo "🔐 Checking Heroku authentication..."
    heroku auth:whoami || heroku login
    
    # Create Heroku app (if it doesn't exist)
    read -p "Enter your Heroku app name: " APP_NAME
    heroku create $APP_NAME || echo "App might already exist, continuing..."
    
    # Set environment variables
    echo "⚙️ Setting environment variables..."
    heroku config:set DEBUG=False --app $APP_NAME
    heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())') --app $APP_NAME
    heroku config:set ALLOWED_HOSTS=$APP_NAME.herokuapp.com --app $APP_NAME
    
    # Add PostgreSQL addon
    echo "🗄️ Adding PostgreSQL database..."
    heroku addons:create heroku-postgresql:mini --app $APP_NAME || echo "Database addon might already exist"
    
    # Deploy
    echo "🚀 Deploying to Heroku..."
    git add .
    git commit -m "Deploy to Heroku" || echo "No changes to commit"
    git push heroku main
    
    # Run migrations
    echo "📊 Running database migrations..."
    heroku run python manage.py migrate --app $APP_NAME
    
    # Create superuser (optional)
    read -p "Create superuser? (y/n): " CREATE_SUPERUSER
    if [ "$CREATE_SUPERUSER" = "y" ]; then
        heroku run python manage.py createsuperuser --app $APP_NAME
    fi
    
    # Collect static files
    echo "📁 Collecting static files..."
    heroku run python manage.py collectstatic --noinput --app $APP_NAME
    
    echo "✅ Deployment complete! Your app is available at: https://$APP_NAME.herokuapp.com"
}

# =============================================================================
# PYTHONANYWHERE DEPLOYMENT
# =============================================================================
deploy_to_pythonanywhere() {
    echo "📦 Preparing for PythonAnywhere deployment..."
    
    # Create production requirements
    echo "📋 Creating production requirements..."
    pip freeze > requirements_production.txt
    
    # Create WSGI configuration
    cat > pythonanywhere_wsgi.py << 'EOF'
import os
import sys

# Add your project directory to Python path
path = '/home/yourusername/chaitanya-college-website'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'chaitanya_site.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
EOF
    
    echo "📝 Manual steps for PythonAnywhere:"
    echo "1. Upload your project files to PythonAnywhere"
    echo "2. Create a virtual environment: mkvirtualenv --python=/usr/bin/python3.11 mysite-virtualenv"
    echo "3. Install requirements: pip install -r requirements.txt"
    echo "4. Configure WSGI file using the generated pythonanywhere_wsgi.py"
    echo "5. Set environment variables in WSGI file or .env"
    echo "6. Run migrations: python manage.py migrate"
    echo "7. Collect static files: python manage.py collectstatic"
    echo "8. Configure static files mapping in PythonAnywhere dashboard"
}

# =============================================================================
# DIGITALOCEAN/VPS DEPLOYMENT
# =============================================================================
deploy_to_vps() {
    echo "📦 Preparing for VPS deployment..."
    
    # Create nginx configuration
    cat > nginx_config << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/chaitanya-college-website;
    }
    
    location /media/ {
        root /home/ubuntu/chaitanya-college-website;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF
    
    # Create systemd service
    cat > gunicorn.service << 'EOF'
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
User=ubuntu
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/home/ubuntu/chaitanya-college-website
ExecStart=/home/ubuntu/chaitanya-college-website/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          chaitanya_site.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
    
    echo "📝 Manual steps for VPS deployment:"
    echo "1. Set up Ubuntu server with Python 3.11"
    echo "2. Install nginx, postgresql, python3-pip, python3-venv"
    echo "3. Create database and user"
    echo "4. Upload project files and install requirements"
    echo "5. Configure nginx using the generated nginx_config"
    echo "6. Set up gunicorn service using the generated gunicorn.service"
    echo "7. Configure SSL with Let's Encrypt"
}

# =============================================================================
# MAIN MENU
# =============================================================================
echo "Choose your deployment platform:"
echo "1) Heroku (Recommended for beginners)"
echo "2) PythonAnywhere (Good for Django)"
echo "3) DigitalOcean/VPS (Advanced)"
echo "4) Exit"

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        deploy_to_heroku
        ;;
    2)
        deploy_to_pythonanywhere
        ;;
    3)
        deploy_to_vps
        ;;
    4)
        echo "👋 Deployment cancelled."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac