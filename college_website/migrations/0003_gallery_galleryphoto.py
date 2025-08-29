# Generated migration for Gallery models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college_website', '0002_gallery_headerinfo_navbarinfo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('campus', 'Campus'), ('events', 'Events'), ('cultural', 'Cultural'), ('sports', 'Sports'), ('academic', 'Academic'), ('facilities', 'Facilities'), ('achievements', 'Achievements')], default='campus', max_length=20)),
                ('cover_image', models.ImageField(blank=True, upload_to='gallery/covers/')),
                ('is_featured', models.BooleanField(default=False, help_text='Show on homepage')),
                ('is_active', models.BooleanField(default=True)),
                ('ordering', models.IntegerField(default=0)),
                ('meta_description', models.TextField(blank=True, max_length=160)),
            ],
            options={
                'verbose_name_plural': 'Galleries',
                'ordering': ['ordering', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GalleryPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='gallery/photos/')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('caption', models.TextField(blank=True)),
                ('photographer', models.CharField(blank=True, max_length=100)),
                ('date_taken', models.DateField(blank=True, null=True)),
                ('ordering', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='college_website.gallery')),
            ],
            options={
                'ordering': ['ordering', '-created_at'],
            },
        ),
    ]
