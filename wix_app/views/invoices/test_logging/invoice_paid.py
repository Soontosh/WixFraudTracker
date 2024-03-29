"""
    Recieves automated webhooks sent by Wix regarding invoices being paid. this is a test file used for logging
"""

from django.shortcuts import render
from wix_app.utilities import utilites
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from wix_app.models import *

@api_view(["POST", "GET"])
def invoice_paid_loggging(request):
    try:
        """Recieves webhooks regarding an invoice being paid for

        ### Raises:
        """
        utilites.log("INFO", str(request.body)) #Logs request body

        logRow = TestingLogs(log = str(request.body), type = "PAID")
        logRow.save()
        return Response("Success", status=200)
    except Exception as e:
        print(f"FATAL ERROR... {Exception}")
        print(F"REQUEST DATA: {str(request.body)}")
        return Response("Success", status=400)