from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import ScheduleEvent, Notification, CustomUser


class Command(BaseCommand):
    help = 'Scan for schedule events that are due and create notifications for users.'

    def handle(self, *args, **options):
        now = timezone.now()
        due = ScheduleEvent.objects.filter(datetime__lte=now, notified=False)
        created = 0
        for ev in due:
            try:
                # simple policy: notify all users except the creator
                recipients = CustomUser.objects.exclude(pk=ev.created_by.pk)
                msg = f"Event starting: {ev.title}"
                for u in recipients:
                    Notification.objects.create(user=u, message=msg, url=f"/schedule/{ev.id}/")
                ev.notified = True
                ev.save()
                created += recipients.count()
            except Exception as e:
                # continue on errors to avoid stopping the sweeper
                self.stderr.write(str(e))
        self.stdout.write(f"Created {created} notifications for {due.count()} events.")
