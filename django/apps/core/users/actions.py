from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import User

def _send_email_registrations(
    registration_subject, text_content, html_content, from_email, email_list, bcc_email
):
    if not settings.EMAIL_SEND: return "mocking email sending"
    msg = EmailMultiAlternatives(
        registration_subject, text_content, from_email, email_list, bcc=bcc_email
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


def _check_user_if_in_platform(email):
    return User.objects.filter(email=email).exists()

def invite_user_to_subscription(email):
    if not _check_user_if_in_platform(email):
        print("adding user to platform")
    if settings.EMAIL_SEND:
        print("mocking email")
    return True