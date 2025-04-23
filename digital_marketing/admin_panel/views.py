from django.shortcuts import redirect, render
from accounts.models import CustomUser
from django.contrib import messages

from django.core.mail import send_mail
from django.utils.crypto import get_random_string

# Create your views here.

def admin_home(request):
    new_count = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False).count()

    return render(request, 'admin_panel/admin_home.html', {'new_count' : new_count})

def approve_users(request):
    unapproved_users = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False)
    new_count = CustomUser.objects.filter(is_approved=False, status=0, is_superuser=False).count()

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
                from_email=None,  # Use DEFAULT_FROM_EMAIL from settings
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
    return render(request, 'admin_panel/approve_users.html', {'unapproved_users': unapproved_users, 'new_count' : new_count})