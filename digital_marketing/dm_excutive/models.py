from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Lead(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('converted', 'Converted'),
        ('rejected', 'Rejected'),
    )

    lead_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    platform = models.CharField(max_length=150)
    is_verified = models.BooleanField(default=False)
    is_assigned = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

class LeadAssignment(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    executive = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'dm_executive'})
    assigned_at = models.DateTimeField(auto_now_add=True)
