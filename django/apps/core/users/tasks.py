from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Profile

logger = get_task_logger(__name__)

@shared_task
def send_email(user_info):
    print('sending user info')

@shared_task
def check_expiry():
    print('checking expired accounts!')
    for p in Profile.objects.filter(user__is_active=True, user__is_staff=False):
        if p.is_expired:
            p.user.is_active = False
            p.user.save()
    print('checking expired accounts done!')
