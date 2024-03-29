from wix_app.utilities import utilites
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from wix_app.models import *
import sys
import datetime
from django.http import HttpRequest
import re
from pytz import UTC
import cv2
import urllib.request
import numpy as np
from wix_app.views.automatic_emails.send_mass_html_mail import send_mass_html_mail
import inspect
import traceback
from django.core.mail import send_mail

#also set the related invoice row to be suspended
class action_utilities:
    def __init__(self) -> None:
        pass

    def notify_parent(self, parent_email: str, parent_name: str, invoice_link: str, student_name: str, invoice_num: int, product_name: str = "product") -> None:
        template = open(f"{os.path.dirname(os.path.realpath(__file__))}/email_templates/parent/html_template.txt", "r", encoding="utf-8").read()
        template = template.format(parent_name = parent_name, student_name = student_name, program_name = product_name, preview_link = invoice_link)
        self.suspend_invoice(invoice_num)

        text_template = open(f"{os.path.dirname(os.path.realpath(__file__))}/email_templates/parent/text_template.txt", "r", encoding="utf-8").read()
        text_template = text_template.format(parent_name = parent_name, student_name = student_name, program_name = product_name, preview_link = invoice_link)
        send_mail("Urgent: Notice of Program Suspension - Action Required", text_template, "testing.emailf9@gmail.com", [parent_email], html_message=template)

    def notify_student(self, student_email: str, student_name: str, product_name: str = "product") -> None:
        template = open(f"{os.path.dirname(os.path.realpath(__file__))}/email_templates/student/html_template.txt", "r", encoding="utf-8").read()
        template = template.format(student_name = student_name, program_name = product_name)
        
        text_template = open(f"{os.path.dirname(os.path.realpath(__file__))}/email_templates/student/text_template.txt", "r", encoding="utf-8").read()
        text_template = template.format(student_name = student_name, program_name = product_name)
        send_mail("Notice of Program Suspension", text_template, "testing.emailf9@gmail.com", [student_email], html_message=template)
    
    def suspend_invoice(self, invoice_num: int) -> None:
        invoice_row = Invoice.objects.get(invoice_number=invoice_num)
        invoice_row.status = "SUSPENDED"
        invoice_row.save()