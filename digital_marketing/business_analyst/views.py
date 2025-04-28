from django.shortcuts import redirect, render
from .models import LeadTask,DailyReport
from accounts.models import Attendance, LeaveRequest


from django.utils import timezone
from django.contrib import messages
from datetime import date

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


def ba_mark_attendance_and_apply_leave(request):
    today = date.today()

    leaves_today = LeaveRequest.objects.filter(
        user=request.user, 
        from_date__lte=today, 
        to_date__gte=today,
        status='approved'
    )

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'attendance':
            status = request.POST.get('status')

            leave_conflict = LeaveRequest.objects.filter(
                user=request.user, 
                from_date__lte=today, 
                to_date__gte=today, 
                status='approved'
            )

            if leave_conflict.exists():
                messages.error(request, 'You cannot mark attendance during approved leave.')
            elif Attendance.objects.filter(user=request.user, date=today).exists():
                messages.warning(request, 'Attendance already marked for today.')
            else:
                Attendance.objects.create(user=request.user, date=today, status=status)
                messages.success(request, f'Attendance marked as {status.title()} for today.')

        elif form_type == 'leave':
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            leave_type = request.POST.get('leave_type')
            reason = request.POST.get('reason')

            LeaveRequest.objects.create(
                user=request.user,
                from_date=from_date,
                to_date=to_date,
                leave_type=leave_type,
                reason=reason
            )

            messages.success(request, 'Leave request submitted successfully.')

        return redirect('mark_attendance_and_apply_leave')

    return render(request, 'dm_excutive/attendance.html', {
        'today': today,
        'leaves_today': leaves_today
    })


def ba_change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('ba_change_password')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirmation do not match.')
            return redirect('ba_change_password')

        if (len(new_password) < 8 or
            not any(char.isupper() for char in new_password) or
            not any(char.isdigit() for char in new_password) or
            not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in new_password)):
            messages.error(request, 'Password must be at least 8 characters long and contain at least one uppercase letter, one digit, and one special character.')
            return redirect('ba_change_password')
        
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'Password changed successfully. Please log in again.')
        return redirect('login_fn')

    return render(request, 'business_analyst/change_password.html')

