from django.shortcuts import redirect, render
from .models import CustomUser

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

def index(request):
    return render(request, 'home.html')

def login_fn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id

            if user.is_superuser:
                return redirect('admin_home')
            elif user.role == 'business_analyst':
                return redirect('ba_home')
            elif user.role == 'dm_analyst':
                return redirect('dma_home')
            elif user.role == 'dm_executive':
                return redirect('dme_home')
            else:
                messages.error(request, "User role is undefined.")
                return redirect('login_fn')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login_fn')

    return render(request, 'accounts/login.html')

def logout_fn(request):
    logout(request)
    return redirect('index')

def register_fn(request):
    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        company_name = request.POST.get('company_name')
        profile_image = request.FILES.get('profile_image')


        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register_fn')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register_fn')
        if CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already registered.')
            return redirect('register_fn')
        
        if not all([first_name, last_name, username, email, phone, gender, role, company_name, profile_image]):
            messages.error(request, 'All fields are required.')
            return redirect('register_fn')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            gender=gender,
            role=role,
            company_name=company_name,
            profile_image=profile_image,
            is_approved=False,
            status=0,
        )
        user.save()

        messages.success(request, 'Registration successful! Please wait for approval.')
        return redirect('login_fn')

    return render(request, 'accounts/register.html')



def verify_field(request):
    field = request.GET.get('field')
    value = request.GET.get('value')
    exclude_id = request.GET.get('exclude_id')

    if not field or not value:
        return JsonResponse({'error': 'Missing field or value'}, status=400)

    filter_data = {field: value}

    if exclude_id:
        exists = CustomUser.objects.exclude(id=exclude_id).filter(**filter_data).exists()
    else:
        exists = CustomUser.objects.filter(**filter_data).exists()

    return JsonResponse({'available': not exists})