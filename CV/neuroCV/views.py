from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # <--- ADD THIS
from .models import Resume
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .mpesa import trigger_stk_push # The file we created earlier

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

@login_required
def dashboard(request):
    # Filter resumes so users only see their own
    resumes = Resume.objects.filter(user=request.user) 
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


@csrf_exempt
def mpesa_callback(request, resume_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        result_code = data['Body']['stkCallback']['ResultCode']
        
        # ResultCode 0 means the transaction was successful
        if result_code == 0:
            try:
                resume = Resume.objects.get(id=resume_id)
                resume.is_paid = True # Unlock the PDF
                resume.save()
                return JsonResponse({"status": "Success"}, status=200)
            except Resume.DoesNotExist:
                return JsonResponse({"status": "Resume not found"}, status=404)
        
        return JsonResponse({"status": "Payment Failed or Cancelled"}, status=200)
   


@login_required
def initiate_payment(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    
    # In a real app, you might have a 'phone' field in a UserProfile model
    # For now, we can use the phone number attached to the CV
    phone_number = resume.phone 
    
    # Clean the phone number (Safaricom needs 2547XXXXXXXX)
    # This logic assumes the user entered 07... or +254...
    clean_phone = phone_number.replace("+", "").replace(" ", "")
    if clean_phone.startswith("0"):
        clean_phone = "254" + clean_phone[1:]
    
    amount = 50 # Your price in KES
    
    # Trigger the M-Pesa Prompt
    response = trigger_stk_push(clean_phone, amount, resume.id)
    
    if response.get("ResponseCode") == "0":
        # Successfully sent the prompt to the phone
        return render(request, 'neuroCV/payment_pending.html', {'resume': resume})
    else:
        # Something went wrong (e.g., Daraja is down)
        return render(request, 'neuroCV/payment_failed.html', {'error': response.get("ResponseDescription")})