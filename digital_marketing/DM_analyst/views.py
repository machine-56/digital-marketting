from django.shortcuts import render

# Create your views here.
def dma_home(request):
    return render(request, 'DM_analyst/dma_home.html')