from django.shortcuts import render

# Create your views here.
def ba_home(request):
    return render(request, 'business_analyst/ba_home.html')