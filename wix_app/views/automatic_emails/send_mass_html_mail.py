"""
Create a custom function to handle sending mass HTML messages with Django. 
Need to create custom function as Django does not support mass HTML messages.
"""
from django.core.mail import get_connection, EmailMultiAlternatives
from celery import shared_task
from wix_app.models import EventLog
import datetime
from pytz import UTC

#Soft times out after 960 seconds, times out after 1000 seconds
@shared_task(time_limit=1000, soft_time_limit=960)
def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, 
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
        event_log = EventLog(timestamp=datetime.datetime.now(UTC), event_type = "EMAIL_SENT") #need to add more detailed logs(later)
        event_log.save()
    return connection.send_messages(messages)