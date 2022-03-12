from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from .models import Profile

logger = get_task_logger(__name__)

def send_email_registrations(registration_subject, text_content, html_content, from_email, email_list, bcc_email):
    msg = EmailMultiAlternatives(registration_subject, text_content, from_email, email_list, bcc=bcc_email)
    msg.attach_alternative(html_content, "text/html")
    return msg.send()

@shared_task
def send_registration_email(first_name, account_expiry, user_email):
    logger.info(f'sending registration email to {user_email}')
    from_email = settings.DEFAULT_FROM_EMAIL
    bcc_email = [settings.EMAIL_REGISTRATION_BCC]
    registration_subject = settings.EMAIL_REGISTRATION_SUBJECT
    registration_template = settings.EMAIL_REGISTRATION_TEMPLATE
    site_url = settings.SITE_URL
    target_email_list = [user_email]
    config_message = {'email': user_email, 'first_name': first_name, 'account_expiry': account_expiry, 'site_url': site_url}
    text_content = get_template(f"{registration_template}.txt").render(config_message)
    html_content = get_template(f"{registration_template}.html").render(config_message)
    send_email_registrations(registration_subject, text_content, html_content, from_email, target_email_list, bcc_email)
    return user_email

@shared_task
def check_expiry():
    logger.info('checking expired accounts!')
    for p in Profile.objects.filter(user__is_active=True, user__is_staff=False):
        if p.is_expired:
            p.user.is_active = False
            p.user.save()
    logger.info('checking expired accounts done!')
