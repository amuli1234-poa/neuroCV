from django.db import models
from django.contrib.auth.models import User # For Phase 2 (Logins)

class Resume(models.Model):
    # Link to a user (optional for now, but good for the future)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Personal Info
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Education
    university = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    score = models.CharField(max_length=100)
    year = models.IntegerField()
    
    # Experience
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    responsibilities = models.TextField()
    ai_content = models.TextField(blank=True, null=True) # Store the AI polished version
    
    # Skills
    skills = models.TextField()
    
    # Referees
    ref1_name = models.CharField(max_length=255, blank=True)
    ref1_job = models.CharField(max_length=255, blank=True)
    ref1_contact = models.CharField(max_length=255, blank=True)
    
    ref2_name = models.CharField(max_length=255, blank=True)
    ref2_job = models.CharField(max_length=255, blank=True)
    ref2_contact = models.CharField(max_length=255, blank=True)

    # Payment Status (For M-Pesa Phase)
    is_paid = models.BooleanField(default=False)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name}'s Resume"