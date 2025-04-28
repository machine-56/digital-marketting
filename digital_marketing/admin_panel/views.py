from django.shortcuts import redirect, render
from accounts.models import CustomUser, Attendance, LeaveRequest
from business_analyst.models import LeadTask, DailyReport
from django.contrib import messages

from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.http import JsonResponse

from datetime import date
from django.db.models import Q

# Create your views here.

def admin_home(request):
    new_count = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False).count()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()

    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()
    return render(request, 'admin_panel/admin_home.html', {'new_count' :new_count, 'leave_count' : leave_count})

def validate_user_field(request):
    field = request.GET.get('field')
    value = request.GET.get('value')
    exclude_id = request.GET.get('exclude_id')

    filters = {field: value}
    queryset = CustomUser.objects.filter(**filters)

    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)

    available = not queryset.exists()
    return JsonResponse({'available': available})

def approve_users(request):
    unapproved_users = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False)
    new_count = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False).count()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = CustomUser.objects.get(id=user_id)

        if action == 'approve':

            password = get_random_string(length=12)
            user.set_password(password)
            user.is_approved = True
            user.status = 1
            user.save()

            subject = 'Account Approved – Welcome to Digital Marketing Portal'
            message = (
                f"Dear {user.first_name},\n\n"
                f"Your registration has been approved.\n"
                f"Here are your login credentials:\n\n"
                f"Username: {user.username}\n"
                f"Password: {password}\n\n"
                f"You can now log in and access your account.\n\n"
                f"Best regards,\n"
                f"The Digital Marketing Team"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(request, f"{user.username} has been approved and credentials sent.")

        elif action == 'disapprove':
            user.is_approved = False
            user.status = 2
            user.save()

            subject = 'Account Disapproval – Digital Marketing Portal'
            message = (
                f"Dear {user.first_name},\n\n"
                f"We regret to inform you that your registration request has been disapproved.\n"
                f"If you believe this was a mistake or have any questions, please contact our support team.\n\n"
                f"Best regards,\n"
                f"The Digital Marketing Team"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.error(request, f"{user.username} has been disapproved and notified.")

        return redirect('approve_users')
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()
    return render(request, 'admin_panel/approve_users.html', {'unapproved_users': unapproved_users, 'new_count' : new_count, 'leave_count' : leave_count })

def admin_view_users(request):
    role_filter = request.GET.get('role')
    new_count = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False).count()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()

    users = CustomUser.objects.filter(role__in=['business_analyst', 'dm_analyst', 'dm_executive'], is_superuser=False)

    if role_filter:
        users = users.filter(role=role_filter)

    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()
    return render(request, 'admin_panel/manage_users.html', {'users': users, 'role_filter': role_filter, 'new_count' : new_count, 'leave_count' : leave_count })

def admin_edit_user(request, id):
    user = CustomUser.objects.get(id=id)
    new_count = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False).count()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        gender = request.POST.get('gender')
        company_name = request.POST.get('company_name')

        if not all([first_name, last_name, username, email, phone, role, gender, company_name]):
            messages.error(request, 'All fields are required.')
            return redirect('admin_edit_user', id=id)


        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.phone = phone
        user.role = role
        user.gender = gender
        user.company_name = company_name
        user.save()

        messages.success(request, 'User updated successfully.')
        return redirect('admin_view_users')
    
    return render(request, 'admin_panel/edit_user.html', {'user': user, 'new_count': new_count, 'leave_count' : leave_count})

def admin_delete_user(request, id):
    user = CustomUser.objects.get(id=id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('admin_view_users')

def admin_task_overview(request):
    new_count = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False).count()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()

    tasks = LeadTask.objects.select_related('assigned_to').all()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()
    return render(request, 'admin_panel/task_overview.html', {'tasks': tasks, 'new_count' : new_count, 'leave_count' : leave_count })

def admin_task_detail(request, id):
    new_count = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False).count()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()

    task = LeadTask.objects.get(id=id)
    reports = DailyReport.objects.filter(task=task).order_by('-submitted_at')

    lead_data = list(DailyReport.objects.filter(task=task)
    .annotate(date=TruncDate('submitted_at'))
    .values('date')
    .annotate(total_leads=Sum('lead_count'))
    .order_by('date'))

    return render(request, 'admin_panel/task_detail.html', {
        'task': task,
        'reports': reports,
        'lead_data': list(lead_data),
        'new_count': new_count
    })

def assign_lead_task(request):

    new_count = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False).count()
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()
    business_analysts = CustomUser.objects.filter(role='business_analyst', is_approved=True)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        target_count = request.POST.get('target_count')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        assigned_to_id = request.POST.get('assigned_to')
        file = request.FILES.get('file')

        assigned_to = CustomUser.objects.get(id=assigned_to_id)

        lead_task = LeadTask(
            name=name,
            description=description,
            target_count=target_count,
            start_date=start_date,
            end_date=end_date,
            assigned_to=assigned_to,
            file=file
        )
        lead_task.save()

        messages.success(request, 'Lead task assigned successfully.')
        return redirect('assign_lead_task')
    return render(request, 'admin_panel/assign_lead_task.html', {'business_analysts': business_analysts, 'new_count' : new_count, 'leave_count' : leave_count })


def leave_approval(request):
    leaves = LeaveRequest.objects.filter(status='pending').select_related('user')
    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()
    new_count = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False).count()
    return render(request, 'admin_panel/leave_approval.html', {'new_count' : new_count, 'leaves': leaves, 'leave_count': leave_count})

def approve_leave(request, id, action):
    leave = LeaveRequest.objects.get(id=id)
    if action == 'approve':
        leave.status = 'approved'
    elif action == 'reject':
        leave.status = 'rejected'
    leave.save()
    messages.success(request, f"Leave {leave.status} successfully.")
    return redirect('leave_approval')

def attendance_overview(request):
    today = date.today()

    leave_count = LeaveRequest.objects.filter(status='pending').select_related('user').count()
    new_count = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False).count()
    role_filter = request.GET.get('role')
    attendance_records = Attendance.objects.filter(date__lte=today)

    if role_filter:
        attendance_records = attendance_records.filter(user__role=role_filter)

    leaves = LeaveRequest.objects.filter(
        status='approved',
        from_date__lte=today
    ).exclude(to_date__lt=today)

    if role_filter:
        leaves = leaves.filter(user__role=role_filter)

    roles = CustomUser.ROLE_CHOICES

    return render(request, 'admin_panel/attendance_overview.html', {
        'attendance_records': attendance_records,
        'leaves': leaves,
        'roles': roles,
        'role_filter': role_filter,
        'leave_count': leave_count,
        'new_count': new_count,
    })