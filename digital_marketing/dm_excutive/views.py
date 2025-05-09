from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.models import CustomUser, Attendance, LeaveRequest
from dm_excutive.models import Lead, LeadAssignment


from accounts.models import Attendance
from datetime import date, timedelta

# Create your views here.
def exc_home(request):
    return render(request, 'dm_excutive/exc_home.html')


def view_leads(request):
    assigned_leads = LeadAssignment.objects.filter(executive=request.user).values_list('lead_id', flat=True)
    leads = Lead.objects.filter(id__in=assigned_leads)
    return render(request, 'dm_excutive/view_assigned_leads.html', {'leads': leads})


def mark_attendance_and_apply_leave(request):
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

def exc_change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirmation do not match.')
            return redirect('change_password')

        if (len(new_password) < 8 or
            not any(char.isupper() for char in new_password) or
            not any(char.isdigit() for char in new_password) or
            not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in new_password)):
            messages.error(request, 'Password must be at least 8 characters long and contain at least one uppercase letter, one digit, and one special character.')
            return redirect('exc_change_password')
        
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'Password changed successfully. Please log in again.')
        return redirect('login_fn')

    return render(request, 'dm_excutive/change_password.html')


def exc_attendance_leave_summary(request):

    user = request.user
    attendance_records = Attendance.objects.filter(user=user)
    leave_requests = LeaveRequest.objects.filter(user=user)
    first_attendance = attendance_records.order_by('date').first()
    first_leave = leave_requests.order_by('from_date').first()

    if first_attendance and first_leave:
        start_date = min(first_attendance.date, first_leave.from_date)
    elif first_attendance:
        start_date = first_attendance.date
    elif first_leave:
        start_date = first_leave.from_date
    else:
        start_date = date.today()

    today = date.today()

    all_dates = []
    current_date = start_date
    while current_date <= today:
        all_dates.append(current_date)
        current_date += timedelta(days=1)

    records = []
    for d in all_dates:
        attendance = attendance_records.filter(date=d).first()
        leave = leave_requests.filter(from_date__lte=d, to_date__gte=d).first()
        records.append({
            'date': d,
            'status': attendance.status if attendance else None,
            'leave': leave,
        })

    context = {
        'records': records,
        'leave_requests': leave_requests,
    }

    return render(request, 'dm_excutive/exc_attendance_summary.html', context)
