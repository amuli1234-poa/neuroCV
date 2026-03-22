from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # <--- ADD THIS
from .models import Resume
import logging

# Set up logging
logger = logging.getLogger(__name__)

@login_required
def neuroCV(request):
    if request.method == 'POST':
        # 1. Capture data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        # New: Capture the manual summary from your form
        professional_summary = request.POST.get('professional_summary')
        
        university = request.POST.get('university')
        course = request.POST.get('course')
        score = request.POST.get('score')
        year = request.POST.get('year')
        company = request.POST.get('company')
        role = request.POST.get('role')
        duration = request.POST.get('duration')
        responsibilities = request.POST.get('responsibilities')
        skills = request.POST.get('skills')

        # 2. Create the object
        new_resume = Resume.objects.create(
            user=request.user, # Assign to the logged-in user
            full_name=full_name,
            email=email,
            phone=phone,
            university=university,
            course=course,
            score=score,
            year=year,
            company=company,
            role=role,
            duration=duration,
            responsibilities=responsibilities,
            skills=skills,
            # Use the captured summary here instead of repeating responsibilities
            ai_summary=professional_summary, 
            is_paid=False
        )

        return redirect('resume_detail', pk=new_resume.id)

    return render(request, 'neuroCV/neuroCV.html')

@login_required # <--- Protects the dashboard
def dashboard(request):
    # Fetch all resumes ordered by newest first
    resumes = Resume.objects.all().order_by('-id') 
    return render(request, 'neuroCV/dashboard.html', {'cvs': resumes})

@login_required # <--- Protects resume details
def resume_detail(request, pk):
    cv_data = get_object_or_404(Resume, pk=pk)
    return render(request, 'neuroCV/resume.html', {'cv': cv_data})

@login_required # <--- Protects delete function
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if request.method == "POST":
        resume.delete()
        return redirect('dashboard')
    return render(request, 'neuroCV/delete_confirm.html', {'resume': resume})

@login_required # <--- Protects edit function
def edit_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if request.method == "POST":
        resume.full_name = request.POST.get('full_name')
        resume.email = request.POST.get('email')
        resume.phone = request.POST.get('phone')
        resume.company = request.POST.get('company')
        resume.role = request.POST.get('role')
        # Add any other fields you want to be editable here
        resume.save()
        return redirect('dashboard')
    
    return render(request, 'neuroCV/edit_resume.html', {'resume': resume})