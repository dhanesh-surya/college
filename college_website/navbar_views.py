from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from .models import NavbarInfo
from .forms import NavbarInfoForm

@staff_member_required
def navbar_config_view(request):
    """View to manage navbar configuration"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    
    if request.method == 'POST':
        form = NavbarInfoForm(request.POST, request.FILES, instance=navbar_config)
        if form.is_valid():
            # Deactivate other configurations
            NavbarInfo.objects.filter(is_active=True).update(is_active=False)
            
            # Save new configuration
            navbar_config = form.save(commit=False)
            navbar_config.is_active = True
            navbar_config.save()
            
            messages.success(request, 'Navbar configuration updated successfully!')
            return redirect('navbar_config')
    else:
        form = NavbarInfoForm(instance=navbar_config)
    
    context = {
        'form': form,
        'navbar_config': navbar_config,
        'title': 'Navbar Configuration'
    }
    
    return render(request, 'admin/navbar_config.html', context)

@staff_member_required
@require_http_methods(["POST"])
def navbar_config_reset(request):
    """Reset navbar configuration to defaults"""
    # Deactivate current configuration
    NavbarInfo.objects.filter(is_active=True).update(is_active=False)
    
    # Create new default configuration
    navbar_config = NavbarInfo.objects.create(
        brand_name="Chaitanya Science and Arts College",
        brand_subtitle="Shaheed Nandkumar Patel Vishwavidyalaya, Raigarh",
        show_logo=True,
        show_brand_text=True,
        
        # Navbar styling
        navbar_background_color="#dc2626",
        navbar_text_color="#ffffff",
        navbar_hover_color="#7c3aed",
        navbar_border_color="#e5e7eb",
        
        # Search functionality
        enable_search=True,
        search_placeholder="Search...",
        
        # Navbar behavior
        is_sticky=False,
        show_below_header=True,
        
        # Navbar dimensions and spacing
        navbar_height=40,
        navbar_padding_top=0.1,
        navbar_padding_bottom=0.1,
        navbar_padding_horizontal=0.5,
        
        # Menu item spacing
        menu_item_padding_vertical=0.15,
        menu_item_padding_horizontal=0.2,
        menu_item_margin=0.005,
        menu_item_gap=0.005,
        menu_item_border_radius=2.0,
        
        # Font settings
        brand_font_size=0.75,
        menu_font_size=0.65,
        menu_line_height=1.1,
        
        # Logo settings
        logo_height=28,
        
        # Responsive breakpoints
        mobile_breakpoint=992,
        tablet_breakpoint=768,
        
        # Mobile specific settings
        mobile_navbar_height=35,
        mobile_padding_horizontal=0.1,
        mobile_menu_font_size=0.65,
        mobile_brand_font_size=0.7,
        mobile_logo_height=20,
        
        # Dropdown settings
        dropdown_padding=0.8,
        dropdown_item_padding_vertical=0.3,
        dropdown_item_padding_horizontal=0.8,
        dropdown_item_font_size=0.75,
        dropdown_item_margin=0.15,
        
        # Mega menu settings
        mega_menu_padding=0.8,
        mega_menu_columns=4,
        mega_menu_width="auto",
        
        # Animation settings
        transition_duration=0.3,
        hover_scale=1.05,
        
        # Shadow and border settings
        box_shadow="0 1px 3px -1px rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.06)",
        border_radius=0.0,
        
        is_active=True
    )
    
    messages.success(request, 'Navbar configuration reset to defaults!')
    return redirect('navbar_config')

@staff_member_required
def navbar_preview(request):
    """Preview navbar configuration"""
    navbar_config = NavbarInfo.objects.filter(is_active=True).first()
    
    context = {
        'navbar_config': navbar_config,
        'title': 'Navbar Preview'
    }
    
    return render(request, 'admin/navbar_preview.html', context)
