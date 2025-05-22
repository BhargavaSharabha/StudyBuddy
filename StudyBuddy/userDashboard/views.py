from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudyGroup, GroupMembership, GroupMessage
from userProfile.models import Subject
from django.utils import timezone
import datetime

# Create your views here.

@login_required
def dashboard(request):
    # Get all study groups ordered by creation date (newest first)
    study_groups = StudyGroup.objects.all().order_by('-created_at')
    
    # Get filter parameters from GET request
    subject_filter = request.GET.get('subject')
    search_query = request.GET.get('search')
    
    # Apply filters if they exist
    if subject_filter:
        study_groups = study_groups.filter(subject_id=subject_filter)
    
    if search_query:
        study_groups = study_groups.filter(title__icontains=search_query)
    
    # Get all subjects for filter dropdown
    subjects = Subject.objects.all().order_by('name')
    
    context = {
        'study_groups': study_groups,
        'subjects': subjects,
        'selected_subject': subject_filter,
        'search_query': search_query
    }
    
    return render(request, 'userDashboard/dashboard.html', context)

@login_required
def create_group(request):
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('group_title')
        subject_id = request.POST.get('subject')
        description = request.POST.get('description')
        meeting_date_str = request.POST.get('meeting_date')
        meeting_time_str = request.POST.get('meeting_time')
        max_members = request.POST.get('max_members')
        location = request.POST.get('location', '')
        
        # Parse date and time
        try:
            # This assumes the datepicker returns date in MM/DD/YYYY format
            month, day, year = meeting_date_str.split('/')
            meeting_date = datetime.date(int(year), int(month), int(day))
            
            # This assumes the timepicker returns time in HH:MM AM/PM format
            time_parts = meeting_time_str.split(' ')
            hour, minute = time_parts[0].split(':')
            hour = int(hour)
            minute = int(minute)
            
            # Adjust for PM
            if time_parts[1] == 'PM' and hour < 12:
                hour += 12
            # Adjust for 12 AM
            if time_parts[1] == 'AM' and hour == 12:
                hour = 0
                
            meeting_time = datetime.time(hour, minute)
        except (ValueError, IndexError):
            messages.error(request, "Invalid date or time format. Please try again.")
            return render(request, 'userDashboard/create_group.html')
        
        try:
            # Get the subject
            subject = Subject.objects.get(id=subject_id)
            
            # Create the study group
            study_group = StudyGroup.objects.create(
                title=title,
                description=description,
                subject=subject,
                host=request.user,
                max_members=max_members,
                meeting_date=meeting_date,
                meeting_time=meeting_time,
                meeting_location=location
            )
            
            # Add the creator as a member
            GroupMembership.objects.create(
                user=request.user,
                group=study_group
            )
            
            messages.success(request, f"Study group '{title}' has been created successfully!")
            return redirect('group_details', group_id=study_group.id)
        
        except Subject.DoesNotExist:
            messages.error(request, "Selected subject doesn't exist. Please try again.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    # GET request
    subjects = Subject.objects.all().order_by('name')
    return render(request, 'userDashboard/create_group.html', {'subjects': subjects})

@login_required
def group_details(request, group_id=None):
    if group_id:
        try:
            group = StudyGroup.objects.get(id=group_id)
            
            # Check if user is a member of this group
            is_member = group.members.filter(id=request.user.id).exists()
            is_host = group.host == request.user
            
            # Get all messages for this group
            messages_list = group.messages.all().order_by('timestamp')
            
            # Handle message posting
            if request.method == 'POST' and (is_member or is_host):
                message_content = request.POST.get('message')
                if message_content:
                    # Create the message
                    GroupMessage.objects.create(
                        group=group,
                        user=request.user,
                        content=message_content
                    )
                    return redirect('group_details', group_id=group.id)
            
            context = {
                'group': group,
                'is_member': is_member,
                'is_host': is_host,
                'messages_list': messages_list
            }
            return render(request, 'userDashboard/group_detail.html', context)
        except StudyGroup.DoesNotExist:
            messages.error(request, "Study group not found.")
            return redirect('dashboard')
    return render(request, 'userDashboard/group_detail.html')

@login_required
def join_group(request, group_id):
    try:
        group = StudyGroup.objects.get(id=group_id)
        
        # Check if the user is already a member
        if group.members.filter(id=request.user.id).exists():
            messages.warning(request, "You are already a member of this group.")
        elif group.is_full:
            messages.error(request, "This group is already full.")
        else:
            # Add the user to the group
            GroupMembership.objects.create(
                user=request.user,
                group=group
            )
            messages.success(request, f"You have successfully joined {group.title}!")
    except StudyGroup.DoesNotExist:
        messages.error(request, "Study group not found.")
    
    return redirect('group_details', group_id=group_id)

@login_required
def leave_group(request, group_id):
    try:
        group = StudyGroup.objects.get(id=group_id)
        
        # Check if the user is the host
        if group.host == request.user:
            messages.warning(request, "As the host, you cannot leave the group. You can delete it instead.")
        else:
            # Check if the user is a member
            membership = GroupMembership.objects.filter(
                user=request.user,
                group=group
            ).first()
            
            if membership:
                membership.delete()
                messages.success(request, f"You have left {group.title}.")
            else:
                messages.warning(request, "You are not a member of this group.")
    except StudyGroup.DoesNotExist:
        messages.error(request, "Study group not found.")
    
    return redirect('dashboard')

@login_required
def edit_group(request, group_id):
    try:
        group = StudyGroup.objects.get(id=group_id)
        
        # Check if the user is the host
        if group.host != request.user:
            messages.error(request, "Only the host can edit the group details.")
            return redirect('group_details', group_id=group_id)
        
        if request.method == 'POST':
            # Get form data
            title = request.POST.get('group_title')
            subject_id = request.POST.get('subject')
            description = request.POST.get('description')
            meeting_date_str = request.POST.get('meeting_date')
            meeting_time_str = request.POST.get('meeting_time')
            max_members = request.POST.get('max_members')
            location = request.POST.get('location', '')
            
            # Parse date and time
            try:
                # This assumes the datepicker returns date in MM/DD/YYYY format
                month, day, year = meeting_date_str.split('/')
                meeting_date = datetime.date(int(year), int(month), int(day))
                
                # This assumes the timepicker returns time in HH:MM AM/PM format
                time_parts = meeting_time_str.split(' ')
                hour, minute = time_parts[0].split(':')
                hour = int(hour)
                minute = int(minute)
                
                # Adjust for PM
                if time_parts[1] == 'PM' and hour < 12:
                    hour += 12
                # Adjust for 12 AM
                if time_parts[1] == 'AM' and hour == 12:
                    hour = 0
                    
                meeting_time = datetime.time(hour, minute)
            except (ValueError, IndexError):
                messages.error(request, "Invalid date or time format. Please try again.")
                return render(request, 'userDashboard/edit_group.html', {'group': group})
            
            try:
                # Get the subject
                subject = Subject.objects.get(id=subject_id)
                
                # Update the group
                group.title = title
                group.description = description
                group.subject = subject
                group.max_members = max_members
                group.meeting_date = meeting_date
                group.meeting_time = meeting_time
                group.meeting_location = location
                group.save()
                
                messages.success(request, f"Study group '{title}' has been updated successfully!")
                return redirect('group_details', group_id=group.id)
            
            except Subject.DoesNotExist:
                messages.error(request, "Selected subject doesn't exist. Please try again.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        
        # GET request
        subjects = Subject.objects.all().order_by('name')
        return render(request, 'userDashboard/edit_group.html', {
            'group': group,
            'subjects': subjects
        })
    except StudyGroup.DoesNotExist:
        messages.error(request, "Study group not found.")
        return redirect('dashboard')
