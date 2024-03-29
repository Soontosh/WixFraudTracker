from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from wix_app.views.discord_REST.REST_utilities import rest_utilities
import json
from wix_app.models import *
from django.http import JsonResponse
from datetime import datetime, timedelta
from wix_app.views.discord_REST.encode_jwt import encode_jwt

@api_view(["GET"])
def generate_report(request):
    # Calculate the date one week ago from the current date
    one_week_ago = datetime.now() - timedelta(days=7)

    # Get the number of emails sent in the last week
    emails_count = EventLog.objects.filter(
        timestamp__gte=one_week_ago,
        timestamp__lte=datetime.now(),
        event_type="EMAIL_SENT",
        error=False
    ).count()


    # Get the number of invoices that went overdue in the last week
    overdue_count = EventLog.objects.filter(
        timestamp__gte=one_week_ago,
        timestamp__lte=datetime.now(),
        event_type="INVOICE_OVERDUE",
        error=False
    ).count()

    # Get the total number of overdue invoices
    total_overdue_count = Invoice.objects.filter(
        status="OVERDUE"
    ).count()

    # Get the total number of fraudsters detected in the last week
    fraudsters_last_week = Invoice.objects.filter(
        #timestamp__gte=one_week_ago,
        #timestamp__lte=datetime.now(),
        status="OVERDUE",
        offenses=3
    ).count()

    # Get the total number of cancellations from past week
    cancellation_count = CancellationLogs.objects.filter(
        timestamp__gte=one_week_ago,
        timestamp__lte=datetime.now(),
    ).count()

    # Get all Discord IDs to ping
    ping_ids = [id[0] for id in list(Ping.objects.all().values_list('id'))]

    compiled_json_data = {
        "emails_count": emails_count,
        "overdue_count": overdue_count,
        "detected_fraudsters": fraudsters_last_week,
        "total_overdue_count": total_overdue_count,
        "cancellation_count": cancellation_count,
        "ping_ids": ping_ids
    }

    return Response(encode_jwt(compiled_json_data), status=200)