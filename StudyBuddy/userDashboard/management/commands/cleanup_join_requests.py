from django.core.management.base import BaseCommand
from userDashboard.models import GroupJoinRequest, GroupMembership
from django.db.models import Count


class Command(BaseCommand):
    help = 'Clean up duplicate or problematic join request records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be cleaned up without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        # Find users who are members but have approved join requests
        # These approved requests can be safely removed as they're redundant
        redundant_approved = []
        approved_requests = GroupJoinRequest.objects.filter(status='approved')
        
        for request in approved_requests:
            if GroupMembership.objects.filter(user=request.user, group=request.group, is_active=True).exists():
                redundant_approved.append(request)
        
        self.stdout.write(f'Found {len(redundant_approved)} redundant approved requests')
        
        if redundant_approved:
            for request in redundant_approved:
                self.stdout.write(f'  - {request.user.username} -> {request.group.title} (approved on {request.responded_at})')
            
            if not dry_run:
                count = len(redundant_approved)
                for request in redundant_approved:
                    request.delete()
                self.stdout.write(self.style.SUCCESS(f'Deleted {count} redundant approved requests'))
        
        # Find duplicate requests (shouldn't exist due to unique constraint, but check anyway)
        duplicates = GroupJoinRequest.objects.values('user', 'group').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        if duplicates:
            self.stdout.write(f'Found {len(duplicates)} sets of duplicate requests')
            for dup in duplicates:
                requests = GroupJoinRequest.objects.filter(
                    user_id=dup['user'], 
                    group_id=dup['group']
                ).order_by('-requested_at')
                
                # Keep the most recent one, delete the rest
                to_keep = requests.first()
                to_delete = requests.exclude(id=to_keep.id)
                
                self.stdout.write(f'  - User {to_keep.user.username} -> Group {to_keep.group.title}: keeping {to_keep.status} request from {to_keep.requested_at}, deleting {to_delete.count()} older requests')
                
                if not dry_run:
                    to_delete.delete()
        
        if not dry_run:
            self.stdout.write(self.style.SUCCESS('Cleanup completed successfully'))
        else:
            self.stdout.write(self.style.WARNING('Dry run completed - use without --dry-run to apply changes')) 