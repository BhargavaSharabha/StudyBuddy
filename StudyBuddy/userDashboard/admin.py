from django.contrib import admin
from .models import StudyGroup, GroupMembership, GroupMessage

class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 1

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'host', 'meeting_date', 'meeting_time', 'current_member_count', 'max_members')
    list_filter = ('subject', 'meeting_date')
    search_fields = ('title', 'description', 'host__username')
    date_hierarchy = 'meeting_date'
    inlines = [GroupMembershipInline]

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'date_joined', 'is_active')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('user__username', 'group__title')

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'timestamp')
    list_filter = ('timestamp', 'group')
    search_fields = ('content', 'user__username', 'group__title')
