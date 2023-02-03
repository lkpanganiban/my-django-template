from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import User

def _send_email_registrations(
    registration_subject:str, text_content:str, html_content:str, from_email:str, email_list:list, bcc_email:str
) -> None:
    """
    send email registration notification
    """
    if not settings.EMAIL_SEND: return "mocking email sending"
    msg = EmailMultiAlternatives(
        registration_subject, text_content, from_email, email_list, bcc=bcc_email
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def _check_user_if_in_platform(email: str) -> bool:
    """
    checks if user exists
    """
    return User.objects.filter(email=email).exists()

def invite_user_to_subscription(email: str) -> bool:
    """
    invite user to be added to a subscription
    """
    if not _check_user_if_in_platform(email):
        print("adding user to platform")
    if settings.EMAIL_SEND:
        print("mocking email")
    return True