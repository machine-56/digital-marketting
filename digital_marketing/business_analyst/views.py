from django.shortcuts import redirect, render
from .models import LeadTask,DailyReport
from django.utils import timezone

# Create your views here.
def ba_home(request):
    return render(request, 'business_analyst/ba_home.html')


def ba_task_list(request):
    tasks = LeadTask.objects.filter(assigned_to=request.user)
    return render(request, 'business_analyst/task_list.html', {'tasks': tasks})


def ba_task_detail(request, task_id):
    task = LeadTask.objects.get(id=task_id, assigned_to=request.user)   
    reports = task.reports.order_by('-submitted_at')
    return render(request, 'business_analyst/task_detail.html', {'task': task, 'reports': reports})



def add_daily_report(request, task_id):
    task = LeadTask.objects.get(id=task_id, assigned_to=request.user)
    reports = task.reports.order_by('-submitted_at')
    
    if request.method == 'POST':
        report_text = request.POST.get('report_text')
        lead_count = request.POST.get('lead_count')
        report_file = request.FILES.get('report_file')
        # progress_percentage = request.POST.get('progress_percentage')

        if report_text and lead_count and lead_count.isdigit():
        # if report_text and lead_count and lead_count.isdigit() and progress_percentage.isdigit():
            lead_count = int(lead_count)
            # progress_percentage = int(progress_percentage)

            report = DailyReport(
                task=task,
                report_text=report_text,
                lead_count=lead_count,
                report_file=report_file
            )
            report.save()

            # task.progress_percentage = progress_percentage
            total_leads = sum(r.lead_count for r in task.reports.all())
            task.progress_percentage = min(100, int((total_leads / task.target_count) * 100))

            task.save()

            return redirect('ba_task_detail', task_id=task.id)
        else:
            error = "Please fill in all fields correctly."
            return render(request, 'business_analyst/add_report.html', {'task': task, 'error': error})
    
    return render(request, 'business_analyst/add_report.html', {'task': task, 'reports': reports})




def submit_task(request, task_id):
    task = LeadTask.objects.get(id=task_id, assigned_to=request.user)
    if request.method == 'POST':
        file_upload = request.FILES.get('file_upload')

        if file_upload:
            task.file = file_upload
            task.is_completed = True
            task.status = 'completed'
            task.submitted_on = timezone.now().date()
            task.progress_percentage = 100
            task.save()

            return redirect('ba_task_detail', task_id=task.id)
        else:
            error = "Please upload a file before submitting."
            return render(request, 'business_analyst/submit_task.html', {'task': task, 'error': error})

    return render(request, 'business_analyst/submit_task.html', {'task': task})