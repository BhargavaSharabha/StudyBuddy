from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('create_group', views.create_group, name='create_group'),
    path('group_details', views.group_details, name='group_details'),
]
