from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Personal Info
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Education
    university = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    score = models.CharField(max_length=100)
    year = models.CharField(max_length=50) # Changed to CharField for flexibility (e.g., "2022-2026")
    
    # Experience
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    responsibilities = models.TextField()
    
    # AI Fields - Keeping them separate makes your HTML template much cleaner!
    ai_summary = models.TextField(blank=True, null=True)
    ai_bullet = models.TextField(blank=True, null=True)
    
    # Skills
    skills = models.TextField()
    
    # Referees
    ref1_name = models.CharField(max_length=255, blank=True)
    ref1_job = models.CharField(max_length=255, blank=True)
    ref1_contact = models.CharField(max_length=255, blank=True)
    
    ref2_name = models.CharField(max_length=255, blank=True)
    ref2_job = models.CharField(max_length=255, blank=True)
    ref2_contact = models.CharField(max_length=255, blank=True)

    # Payment Status
    is_paid = models.BooleanField(default=False)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Shows newest resumes first in the dashboard

    def __str__(self):
        return f"{self.full_name} - {self.role}"