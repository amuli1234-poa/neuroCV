from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    # This controls which columns show up in the list view
    list_display = ('full_name', 'email', 'phone', 'is_paid', 'created_at')
    
    # This adds a sidebar to filter by payment status or date
    list_filter = ('is_paid', 'created_at', 'university')
    
    # This adds a search bar at the top
    search_fields = ('full_name', 'email', 'phone', 'company')
    
    # This organizes the "Edit" page inside the admin panel into sections
    fieldsets = (
        ('Personal Details', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Education', {
            'fields': ('university', 'course', 'score', 'year')
        }),
        ('Work Experience', {
            'fields': ('company', 'role', 'duration', 'responsibilities', 'ai_content')
        }),
        ('Skills', {
            'fields': ('skills',)
        }),
        ('Referees', {
            'fields': (('ref1_name', 'ref1_job', 'ref1_contact'), ('ref2_name', 'ref2_job', 'ref2_contact'))
        }),
        ('Payment Info', {
            'fields': ('is_paid', 'checkout_request_id')
        }),
    )