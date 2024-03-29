"""
    Recieves automated webhooks sent by Wix regarding invoices being paid. Saves and logs data accordingly
"""

from wix_app.utilities import utilites
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from wix_app.models import *
import sys
import datetime
from wix_app.views.invoices.InvoiceManager import invoiceManager

@api_view(["POST"])
def invoice_paid(request):
    response = invoiceManager.extract_invoice_info(request, "INVOICE_PAID")
    return response