from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('business_analyst', 'Business Analyst'),
        ('dm_analyst', 'DM Analyst'),
        ('dm_executive', 'DM Executive'),
    )
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    company_name = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    status = models.IntegerField(default=0,
        choices=(
            (0, 'Pending'),
            (1, 'Approved'),
            (2, 'Disapproved'),
        )
    )


class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    STATUS_CHOICES = (('present', 'Present'), ('absent', 'Absent'))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    reason = models.TextField(null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = (
        ('full', 'Full Day'),
        ('half', 'Half Day'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES, default='full')
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')), default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)