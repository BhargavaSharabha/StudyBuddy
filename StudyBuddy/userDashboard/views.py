from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'userDashboard/dashboard.html')

@login_required
def create_group(request):
    return render(request, 'userDashboard/create_group.html')

@login_required
def group_details(request):
    return render(request, 'userDashboard/group_detail.html')
