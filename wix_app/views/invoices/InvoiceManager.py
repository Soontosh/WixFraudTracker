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
import inspect

class InvoiceManager:
    """
    Class to manage invoices and use common functions
    """
    def __init__(self) -> None:

        #The status corresponding to each invoice
        self.statusDict = {
            "INVOICE_SENT": "PENDING",
            "INVOICE_PAID": "PAID",
            "INVOICE_OVERDUE": "OVERDUE"
        }
        return
    
    def extract_invoice_info(self, request: HttpRequest, eventType: str):
        """
            Recieves automated webhooks sent by Wix regarding invoices. Saves data to database and logs data accordingly

            ### Fields:
            request ```djang.https.HttpRequest```: The request object of the view from which this function is being called
            eventType ```str```: The type of event that is taking place. This can be "INVOICE_SENT", "INVOICE_PAID", or "INVOICE_OVERDUE". The function will return an error if the parameter is not one of these

            ### Handles and Logs:
                A ```json.JSONDecodeError``` if request does not contain JSON data or properly formatted JSON data\n
                A ```KeyError``` if request does not contain "data" key\n
                A ```KeyError``` if ```jsonData``` variable does not contain a key needed for database\n
        """
        #Ensure the event type is valid by checking if it is in status dictionary
        if eventType not in self.statusDict.keys():
            #Save event log to database
            eventLog = EventLog(timestamp=datetime.datetime.now(UTC), event_type = eventType, error = True, error_type = "Invalid Event Type", error_message = "Invalid Event Type", line_number = inspect.currentframe().f_back.f_lineno)
            eventLog.save()

            #Log error if request does not contain JSON data and/or does not contain properly formatted JSON data
            utilites.log("ERROR", f"Invalid event type at '{sys._getframe().f_code.co_name}. Associated event log ID: {eventLog.id}'. Line number: {inspect.currentframe().f_back.f_lineno}")
            return Response("Error", status=400)

        #Extract JSON data from request. Throw errors if unable to decode data or find key
        try:
            jsonData = request.data["data"]
        except json.JSONDecodeError as e:
            #Save event log to database
            eventLog = EventLog(timestamp=datetime.datetime.now(UTC), event_type = eventType, error = True, error_type = "json.JSONDecodeError", error_message = e, line_number = inspect.currentframe().f_back.f_lineno)
            eventLog.save()

            #Log error if request does not contain JSON data and/or does not contain properly formatted JSON data
            utilites.log("ERROR", f"Unable to decode JSON data in function '{sys._getframe().f_code.co_name}. Associated event log ID: {eventLog.id}'. Line number: {inspect.currentframe().f_back.f_lineno}")
            return Response("Malformed Data", status=400)
        except KeyError as e:
            #Save event log to database
            eventLog = EventLog(timestamp=datetime.datetime.now(UTC), event_type = eventType, error = True, error_type = "KeyError", error_message = e, json_data = str(request.json()), line_number = inspect.currentframe().f_back.f_lineno)
            eventLog.save()

            #Log error if request JSON data does not contain "data" key
            utilites.log("ERROR", f"Unable to find key \"data\" in function '{sys._getframe().f_code.co_name}. Associated event log ID: {eventLog.id}'. Line number: {inspect.currentframe().f_back.f_lineno}")
            return Response("Malformed Data", status=400)
        except Exception as e:
            #Save event log to database
            eventLog = EventLog(timestamp=datetime.datetime.now(UTC), event_type = eventType, error = True, error_type = f"{type(e).__name__}", error_message = e, line_number = inspect.currentframe().f_back.f_lineno)
            eventLog.save()

            #Log unhandled exception
            utilites.log("ERROR", f"Unhandled exception of type {type(e).__name__}: '{e}', in function '{sys._getframe().f_code.co_name} while extracting JSON data from request. Associated event log ID: {eventLog.id}'. Line number: {inspect.currentframe().f_back.f_lineno}")
            return Response("Error", status=400)
        
        #Declare all nullable rows as null
        contact_phone_number = None
        student_name = None
        student_email = None

        #Extract data to variables that will be saved to database. Throw KeyError if unable to find key
        try:
            
            invoice_number = jsonData["_context"]["invoice_number"] #Primary Key - The invoice tracking number and unique identifier given by Wix
            preview_link = jsonData["_context"]["preview_link"] #Link to preview the invoice

            #Convert issue_date from a string to to a 'date' object that can be used w/ Django models
            issue_date = datetime.datetime.strptime(jsonData["_context"]["issue_date"], "%Y-%m-%dT%H:%M:%S.%fZ").date() #Date at which the invoice was issued

            #Convert due_date from a string to to a 'date' object that can be used w/ Django models
            due_date = datetime.datetime.strptime(jsonData["_context"]["due_date"], "%Y-%m-%dT%H:%M:%S.%fZ").date() #Due date of the invoice

            total = jsonData["_context"]["total"] #Total cost of the invoice
            currency = jsonData["_context"]["currency"] #Currency in which the invoice is priced
            contact_name = jsonData["customer_name"] #The customer's name
            contact_email = jsonData["customer_email"] #The customer's email

            #Attempt to get nullable data, if it is not available, do nothing. Variables with null value are already defined above
            try:
                contact_phone_number = jsonData["_context"]["contact"]["phone"]
            except KeyError:
                pass #Do nothing

            try:
                #From the ordered product's name, check if the student's name is available
                name_match = re.search(r'(?i)name: ([^,]+)', jsonData["_context"]["item_1"])
                if name_match:
                    student_name = name_match.group(1).strip() #if there is a match, extract the student's name
            except KeyError:
                pass #Do nothing

            try:
                #From the ordered product's name, extract the student's email
                email_match = re.search(r'(?i)email: ([^)]+)', jsonData["_context"]["item_1"])
                if email_match:
                    student_email = email_match.group(1).strip() #if there is a match, extract the student's email
            except KeyError:
                pass #Do nothing

        except KeyError as invalidKey:
            #Save event log to database
            eventLog = EventLog(timestamp=datetime.datetime.now(UTC), event_type = eventType, error = True, error_type = "Key Error", error_message = invalidKey, json_data = jsonData, line_number = inspect.currentframe().f_back.f_lineno)
            eventLog.save()

            #Log error with information regarding the invalid key
            utilites.log("ERROR", f"Unable to find key {invalidKey} in variable \"jsonData\" at function '{sys._getframe().f_code.co_name}. Associated event log ID: {eventLog.id}'. Line number: {inspect.currentframe().f_back.f_lineno}")
            return Response(f"Invalid Key(s)", status=400)
        except Exception as e:
            #Save event log to database
            eventLog = EventLog(timestamp=datetime.datetime.now(UTC), event_type = eventType, error = True, error_type = f"{type(e).__name__}", error_message = invalidKey, json_data = jsonData, line_number = inspect.currentframe().f_back.f_lineno)
            eventLog.save()

            #Log unhandled exception
            utilites.log("ERROR", f"Unhandled exception of type {type(e).__name__}: '{e}', in function '{sys._getframe().f_code.co_name}, in event of type {eventType}, while assigning necessary variables. Associated event log ID: {eventLog.id}. Line number: {inspect.currentframe().f_back.f_lineno}'")
            return Response("Error", status=400)
        
        #Set the status based on the eventType
        status = self.statusDict[eventType]

        #Save data to database
        invoice = Invoice(invoice_number=invoice_number, preview_link=preview_link, issue_date=issue_date, due_date=due_date, total=total, currency=currency, contact_name=contact_name, contact_email=contact_email, contact_phone_number=contact_phone_number, student_name=student_name, student_email=student_email, status="PENDING")
        invoice.save()

        #Save data to Event Logs
        eventLog = EventLog(timestamp=datetime.datetime.now(UTC), event_type = eventType, associated_invoice = invoice, line_number = inspect.currentframe().f_back.f_lineno)
        eventLog.save()

        return Response("success", status=200)

#Create instance
invoiceManager = InvoiceManager()