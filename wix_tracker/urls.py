"""
URL configuration for wix_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from wix_app.views.invoices.test_logging.invoice_sent import invoice_sent_logging
from wix_app.views.invoices.test_logging.invoice_paid import invoice_paid_loggging
from wix_app.views.invoices.test_logging.invoice_overdue import invoice_overdue
from wix_app.views.invoices.invoice_paid import invoice_paid
from wix_app.views.invoices.invoice_sent import invoice_sent
from wix_app.views.automatic_emails.automatic_emails import send_automated_emails
from wix_app.views.discord_REST.reports.get_events import get_events
from wix_app.views.discord_REST.reports.get_event_data import get_event_data
from wix_app.views.discord_REST.reports.recieve_cancellation_webhook import recieve_cancellation_webhook
from wix_app.views.discord_REST.get_fraudulent_students import get_fraudulent_students
from wix_app.views.discord_REST.get_student_discord_ids import get_student_discord_ids
from wix_app.views.discord_REST.get_student_info import get_student_info
from wix_app.views.discord_REST.action_taken.email_parent import email_parent
from wix_app.views.discord_REST.action_taken.email_student import email_student
from wix_app.views.discord_REST.reports.get_report import generate_report
from wix_app.views.discord_REST.log_event import log_event
from wix_app.views.discord_REST.reports.ping_me import ping_me

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/invoice_sent", invoice_sent_logging),
    path("api/invoice_paid", invoice_paid_loggging),
    path("api/invoice_overdue", invoice_overdue),
    path("api/demo/invoice_paid", invoice_paid),
    path("api/demo/invoice_sent", invoice_sent),
    path("api/demo/send_automated_emails", send_automated_emails),

    #Discord URLs
    path("discord/rest/get_events", get_events),
    path("discord/rest/get_event_data", get_event_data),
    path("discord/rest/get_fraudulent_students", get_fraudulent_students),
    path("discord/rest/get_student_discord_ids", get_student_discord_ids),
    path("discord/rest/get_student_info", get_student_info),
    path("discord/rest/action/email_parent", email_parent),
    path("discord/rest/action/email_student", email_student),
    path("discord/rest/action/recieve_cancellation_webhook", recieve_cancellation_webhook),
    path("discord/rest/report/generate_report", generate_report),
    path("discord/rest/log_discord_event", log_event),
    path("discord/rest/reports/ping_me", ping_me),
]

