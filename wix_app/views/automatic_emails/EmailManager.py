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

#Email Manager class
class EmailManager:
    def __init__(self) -> None:
        pass

    def batch_send_reminders(self, data: dict) -> None:
        """
        Loops through given dictionary to send reminder emails

        ### Fields:
            data ```dict```: Dictionary containing all customers to email. All keys have nested dictionaries containg more information.
        
        ### Handles and Logs:
        \u200bAll logging and error handling is handled by the \"create_reminder_email\" function.
        """

        #Variable to keep track of the amount of errors that took place in the loop
        err_count = 0

        #Tuple to store all emails
        email_tuple = ()

        #Loop through data, send email for each piece of data
        for key in data.keys():
            try:
                #Get email data and add to tuple
                email_tuple += (self.create_reminder_email(data[key]),)
            except Exception as e:
                #Increment err_count
                err_count += 1

                #Save event log to database
                event_log = EventLog(timestamp=datetime.datetime.now(UTC), event_type = "EMAIL_SENT", error = True, error_type = f"{type(e).__name__}", error_message = e, line_number = inspect.currentframe().f_back.f_lineno)
                event_log.save()

                #Log unhandled exception
                utilites.log("ERROR", f"Unhandled exception of type {type(e).__name__}: '{e}', in function '{sys._getframe().f_code.co_name}. Associated event log ID: {event_log.id}. Line number: {inspect.currentframe().f_back.f_lineno}'")

        #Mass email using stored tuples
        try:
            #Run asyncronously
            send_mass_html_mail.delay(email_tuple, fail_silently=False)
        except Exception as e:
            #type(ex).__name__
            #Save event log to database
            event_log = EventLog(timestamp=datetime.datetime.now(UTC), event_type = "EMAIL_SENT", error = True, error_type = f"{type(e).__name__}", error_message = e, line_number = inspect.currentframe().f_back.f_lineno)
            event_log.save()

            #Log unhandled exception
            print(email_tuple)
            print(f"length: {len(email_tuple)}")
            utilites.log("ERROR", f"Unhandled exception of type {type(e).__name__}: '{traceback.format_exc()}', in function '{sys._getframe().f_code.co_name}. Associated event log ID: {event_log.id}. Called line number: {inspect.currentframe().f_back.f_lineno}'")


    def create_reminder_email(self, data: dict) -> tuple:
        """
        Sends reminder email using given data. Seperating this function from ```batch_send_reminders``` allows for easier error handling.

        ### Fields:
            data ```dict```: Dictionary containing information pertaining to the customer
        
        ### Handles and Logs:
        \u200b```None```

        ### Returns:
        A tuple containing necessary information about the email
        """

        #Extract data to variables that will be used in email. Throw KeyError if unable to find key
        try:
            email = data["email"] #Extract customer email
            first_name = data["first_name"] #Customer's first name
            product_name = data["product_name"] #The product's name
            preview_link = data["preview_link"] #The preview link
            issue_date = data["issue_date"] #The date this invoice was issued
            due_date = data["due_date"] #This invoice's due date
            three_weeks_after_due_date = data["three_weeks_after_due_date"] #Three weeks after the due date

            #Attempt to extract the student's name. If it is not available, keep it as a default value
            try:
                student_name = data["student_name"]
            except KeyError:
                #Default value
                student_name = "your student"
        except KeyError as invalid_key:
            #Save event log to database
            event_log = EventLog(timestamp=datetime.datetime.now(UTC), event_type = "EMAIL_SENT", error = True, error_type = "Key Error", error_message = invalid_key, json_data = data, line_number = inspect.currentframe().f_back.f_lineno)
            event_log.save()

            #Log error with information regarding the invalid key
            utilites.log("ERROR", f"Unable to find key {invalid_key} in paramter of type dict \"data\" at function '{sys._getframe().f_code.co_name}. Associated event log ID: {event_log.id}. Line number: {inspect.currentframe().f_back.f_lineno}'")

        try:
            #Load the contents of the email
            template = open(f"{os.path.dirname(os.path.realpath(__file__))}\\template.txt", "r", encoding="utf-8").read()
            template = template.format(first_name = first_name, product_name = product_name, issue_date = issue_date, due_date = due_date, three_weeks_after_due_date = three_weeks_after_due_date, student_name = student_name, url = preview_link)
        
            text_template = open(f"{os.path.dirname(os.path.realpath(__file__))}\\text_template.txt", "r", encoding="utf-8").read()
            text_template = template.format(first_name = first_name, product_name = product_name, issue_date = issue_date, due_date = due_date, three_weeks_after_due_date = three_weeks_after_due_date, student_name = student_name, url = preview_link)
        except IndexError as index_error:
            #Means we passed too many variables into our template

            #Save event log to database
            event_log = EventLog(timestamp=datetime.datetime.now(UTC), event_type = "EMAIL_SENT", error = True, error_type = "Index Error", error_message = index_error, line_number = inspect.currentframe().f_back.f_lineno)
            event_log.save()

            #Log error with information regarding the invalid key
            utilites.log("ERROR", f"{index_error} at '{sys._getframe().f_code.co_name}. Associated event log ID: {event_log.id}'")
        except KeyError as invalid_key:
            #Means we tried to format an argument that didn't exist

            #Save event log to database
            event_log = EventLog(timestamp=datetime.datetime.now(UTC), event_type = "EMAIL_SENT", error = True, error_type = "Key Error", error_message = invalid_key, json_data = data, line_number = inspect.currentframe().f_back.f_lineno)
            event_log.save()

            #Log error with information regarding the invalid key
            utilites.log("ERROR", f"Unable to find key {invalid_key} in email template at function '{sys._getframe().f_code.co_name}. Associated event log ID: {event_log.id}. Line number: {inspect.currentframe().f_back.f_lineno}'")
        except Exception as unhandled_error_obj:
            #Save event log to database
            event_log = EventLog(timestamp=datetime.datetime.now(UTC), event_type = "EMAIL_SENT", error = True, error_type = f"{type(unhandled_error_obj).__name__}", error_message = unhandled_error_obj, line_number = inspect.currentframe().f_back.f_lineno)
            event_log.save()

            #Log unhandled exception
            utilites.log("ERROR", f"Unhandled exception of type {type(unhandled_error_obj).__name__}: '{unhandled_error_obj}', in function '{sys._getframe().f_code.co_name}, in event of type EMAIL_SENT while trying to format email template. Associated event log ID: {event_log.id}'. Line number: {inspect.currentframe().f_back.f_lineno}")


        message = ( #Create tuple w/ message data
            f"Urgent: Overdue Invoice Reminder for {first_name}",
            text_template,
            template,
            "testing.emailf9@gmail.com",
            [email],
        )
        return message

#Create instance
email_manager = EmailManager()