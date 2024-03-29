"""
Every day, remind people who were last reminded a week ago of their overdue invoice
"""

#Necessary imports
from wix_app.utilities import utilites
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from wix_app.models import *
import sys
import datetime
from wix_app.views.automatic_emails.EmailManager import email_manager
from celery import shared_task
import time
from datetime import datetime

#Daily Check and Email
@shared_task(name='send_automated_emails')
def send_automated_emails_time():
    #Get the starting time
    start = time.time()

    # Calculate the number of days since the last Sunday
    today = datetime.today()
    days_since_sunday = (today.weekday() + 1) % 7
    delta = timedelta(days=days_since_sunday)

    # Calculate the range of dates for overdue invoices
    start_date = today - delta - timedelta(days=7)
    end_date = today - delta

    # Query the Invoice model for overdue invoices
    overdue_invoices = Invoice.objects.filter(
        status='OVERDUE',
        due_date__range=(start_date, end_date)
    )

    #Using placeholder data
    email_manager.batch_send_reminders({"0": {"email": "awaikeai@gmail.com", "first_name":"Santosh", "product_name":"Guided Internship", "preview_link": "https://www.ai-camp.org//_api/invoice/ddb594b5-c2cc-4a38-b5a5-a7e33d9199e3:80de9344-4035-4810-8aa3-6d3abb2b9da6/view?token=5501d39a-a467-4d91-9483-b0a79b70822e", "issue_date": "11/3/23", "due_date": "11/10/23", "three_weeks_after_due_date": "12/1/23"}})

    #Get and log the time elapsed
    print("Time elapsed: " + str(time.time() - start))

@api_view(["GET", "POST"])
def send_automated_emails(request):
    #Get the starting time
    start = time.time()

    try:
        # Calculate the number of days since the last Sunday
        today = datetime.today()
        days_since_sunday = (today.weekday() + 1) % 7
        delta = timedelta(days=days_since_sunday)

        # Calculate the range of dates for overdue invoices
        start_date = today - delta - timedelta(days=7)
        end_date = today - delta

        # Query the Invoice model for overdue invoices
        overdue_invoices = Invoice.objects.filter(
            status='OVERDUE',
            due_date__range=(start_date, end_date)
        )
    except Exception as e:
        print(e)
        return

    #Using placeholder data
    email_manager.batch_send_reminders({"0": {"email": "awaikeai@gmail.com", "first_name":"Santosh", "product_name":"Guided Internship", "preview_link": "https://www.ai-camp.org//_api/invoice/ddb594b5-c2cc-4a38-b5a5-a7e33d9199e3:80de9344-4035-4810-8aa3-6d3abb2b9da6/view?token=5501d39a-a467-4d91-9483-b0a79b70822e", "issue_date": "11/3/23", "due_date": "11/10/23", "three_weeks_after_due_date": "12/1/23"}})

    #Get and log the time elapsed
    utilites.log("INFO", ("Time elapsed: " + str(time.time() - start)))