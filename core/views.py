from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(
        request,
        "core/dashboard.html",
    )

# Create your views here.
def home(request):
    return render(request, 'core/home.html')