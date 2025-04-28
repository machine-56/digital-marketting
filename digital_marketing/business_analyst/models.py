from django.db import models
from accounts.models import CustomUser

# Create your models here.
class LeadTask(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    target_count = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    file = models.FileField(upload_to='lead_task_files/', null=True, blank=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'business_analyst'})
    progress_percentage = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    submitted_on = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=(('in_progress', 'In Progress'), ('completed', 'Completed')), default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)


class DailyReport(models.Model):
    task = models.ForeignKey(LeadTask, on_delete=models.CASCADE, related_name='reports')
    report_text = models.TextField()
    report_file = models.FileField(upload_to='daily_reports/', null=True, blank=True)
    lead_count = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
