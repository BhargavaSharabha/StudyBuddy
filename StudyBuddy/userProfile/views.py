from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def profile(request):
    return render(request, 'userProfile/profile.html')

@login_required
def profile_setup(request):
    return render(request, 'userProfile/profile_setup.html')


