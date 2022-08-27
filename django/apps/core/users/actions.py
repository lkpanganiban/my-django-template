from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def _send_email_registrations(
    registration_subject, text_content, html_content, from_email, email_list, bcc_email
):
    if not settings.EMAIL_SEND: return "mocking email sending"
    msg = EmailMultiAlternatives(
        registration_subject, text_content, from_email, email_list, bcc=bcc_email
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()

def invite_user_to_subscription(self, email):
    if settings.EMAIL_SEND:
        print("mocking email")
    return True