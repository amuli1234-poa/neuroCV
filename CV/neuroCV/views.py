from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume
from google.genai import Client
import logging

# Set up logging
logger = logging.getLogger(__name__)

# 1. Setup the Client
API_KEY = "AIzaSyDjlCTjDFv3oqxtRXRiM10G-D918BjG0hM"
client = Client(api_key=API_KEY)

def neuroCV(request):
    if request.method == 'POST':
        # 1. Capture data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        university = request.POST.get('university')
        course = request.POST.get('course')
        score = request.POST.get('score')
        year = request.POST.get('year')
        company = request.POST.get('company')
        role = request.POST.get('role')
        duration = request.POST.get('duration')
        responsibilities = request.POST.get('responsibilities')
        skills = request.POST.get('skills')

        # 2. AI Integration (with safety fallback)
        ai_content = "AI was busy, but your data is saved! Please edit to add details."
        try:
            prompt = f"Rewrite into 3 bullet points: {responsibilities}"
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            if response and response.text:
                ai_content = response.text
        except Exception as e:
            print(f"--- AI ERROR: {e} ---")

        # 3. Create the object
        new_resume = Resume.objects.create(
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
            ai_bullet=ai_content,
            is_paid=False
        )

        # IMPORTANT: This must be indented INSIDE the 'if POST' block
        return redirect('resume_detail', pk=new_resume.id)

    # This handles the initial GET request
    return render(request, 'neuroCV/neuroCV.html')
def dashboard(request):
    # Fetch all resumes ordered by newest first
    resumes = Resume.objects.all().order_by('-id') 
    return render(request, 'neuroCV/dashboard.html', {'cvs': resumes})

def resume_detail(request, pk):
    cv_data = get_object_or_404(Resume, pk=pk)
    return render(request, 'neuroCV/resume.html', {'cv': cv_data})

def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if request.method == "POST":
        resume.delete()
        return redirect('dashboard')
    # If your template is in neuroCV folder, keep the prefix
    return render(request, 'neuroCV/delete_confirm.html', {'resume': resume})

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