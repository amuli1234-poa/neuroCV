import google.generativeai as genai
from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume
# from django_daraja.mpesa.core import MpesaClient
# from django.http import HttpResponse
# import json
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse

# 1. Setup your API Key
# Replace the string below with your actual API key from Google AI Studio
genai.configure(api_key="AIzaSyBcmd7naXxewOQjwk-xQG_bxnfCl5tHpRs")

from django.shortcuts import render, redirect
from .models import Resume
import google.generativeai as genai

def neuroCV(request):
    if request.method == 'POST':
        # 1. Capture all data from your form fields
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

        # 2. AI Integration using 'gemini-pro'
        ai_content = ""
        try:
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"""
            You are an expert Executive Resume Writer. 
            Rewrite the following "Responsibilities" into 3 professional, 
            high-impact bullet points starting with strong action verbs.
            
            Role: {role}
            Company: {company}
            Input: {responsibilities}
            
            Also, provide a 2-line professional summary for this person.
            """
            response = model.generate_content(prompt)
            ai_content = response.text
        except Exception as e:
            print(f"AI Error: {e}")
            ai_content = "Professional summary will be available soon."

        # 3. CRITICAL STEP: Save to Database
        # This makes the data appear in the Dashboard and Admin Panel
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
            ai_content=ai_content  # Saving the AI result too!
        )

        # 4. Redirect to the Preview page using the NEW ID
        # It's better to redirect to a 'resume_preview' view so the URL is clean
        return redirect('resume', pk=new_resume.id)

    return render(request, 'neuroCV/neuroCV.html')

# 5. Add a view to show the specific Resume after saving
def resume(request, pk):
    resume = Resume.objects.get(pk= pk)
    
    return render(request, 'neuroCV/resume.html', {'cv': resume})

def dashboard(request):
    resumes = Resume.objects.all().order_by('-created_at')
    return render(request, 'neuroCV/dashboard.html', {'resumes': resumes})
# 2. DELETE
def delete_cv(request, cv_id):
    cv = get_object_or_404(Resume, id=cv_id)
    cv.delete()
    return redirect('dashboard')

# 3. UPDATE (Edit an existing CV)
def edit_cv(request, cv_id):
    cv = get_object_or_404(Resume, id=cv_id)
    
    if request.method == 'POST':
        # Update the existing object with new data from the form
        cv.full_name = request.POST.get('full_name')
        cv.email = request.POST.get('email')
        cv.phone = request.POST.get('phone')
        cv.university = request.POST.get('university')
        cv.course = request.POST.get('course')
        cv.score = request.POST.get('score')
        cv.year = request.POST.get('year')
        cv.company = request.POST.get('company')
        cv.role = request.POST.get('role')
        cv.duration = request.POST.get('duration')
        cv.responsibilities = request.POST.get('responsibilities')
        cv.skills = request.POST.get('skills')
        cv.save()
        return redirect('dashboard')
        
    return render(request, 'neuroCV/edit_cv.html', {'cv': cv})


# def initiate_stk_push(request, cv_id):
#     # 1. Get the Resume record
#     resume = get_object_or_404(Resume, id=cv_id)
    
#     # 2. Format Phone Number (Daraja needs 2547XXXXXXXX)
#     phone = resume.phone.replace("+", "")
#     if phone.startswith("0"):
#         phone = "254" + phone[1:]
    
#     # 3. Initialize Mpesa Client
#     cl = MpesaClient()
#     amount = 1  # Amount in KES (Use 1 for testing)
#     account_reference = 'NeuroCV_Ref'
#     transaction_desc = f'Payment for {resume.full_name} CV'
    
#     # 4. Set Callback URL (Safaricom sends the result here)
#     # Note: Use your Ngrok URL here during local testing
#     callback_url = 'https://your-domain.com/mpesa/callback/'
    
#     # 5. Send Request
#     response = cl.stk_push(phone, amount, account_reference, transaction_desc, callback_url)
    
#     if response.response_code == "0":
#         # Save the CheckoutRequestID to identify this transaction later
#         resume.checkout_request_id = response.checkout_request_id
#         resume.save()
#         return HttpResponse("Check your phone for the M-Pesa PIN prompt!")
#     else:
#         return HttpResponse(f"Error: {response.response_description}")

# @csrf_exempt
# def mpesa_callback(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         stk_callback = data['Body']['stkCallback']
#         result_code = stk_callback['ResultCode']
#         checkout_request_id = stk_callback['CheckoutRequestID']

#         # ResultCode 0 means the user entered the PIN and payment was successful
#         if result_code == 0:
#             try:
#                 resume = Resume.objects.get(checkout_request_id=checkout_request_id)
#                 resume.is_paid = True
#                 resume.save()
#                 print(f"Payment Successful for {resume.full_name}")
#             except Resume.DoesNotExist:
#                 print("Error: Resume with this ID not found.")

#         return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})