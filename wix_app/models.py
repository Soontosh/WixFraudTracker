from django.db import models
import django.core.exceptions
from datetime import datetime, timedelta

# Create your models here.
class Invoice(models.Model):
    """
    Table for invoices that have either been sent

    ### Fields:
        invoice_number ```Integer Field```: The invoice tracking number and unique identifier given by Wix\n
        preview_link ```Text Field```: Link to preview the invoice\n
        issue_date ```Date Field```: Date at which the invoice was issued\n
        due_date ```Date Field```: Due date of the invoice\n
        total ```Float Field```: Total cost of the invoice\n
        currency ```Char Field```: Currency in which the invoice is priced\n
        contact_name ```Text Field```: The customer's name\n
        contact_email ```Email Field```: The customer's email\n
        contact_phone_number ```Char Field```: The customer's nullable phone number\n
        student_name ```Text Field```: The student's nullable name\n
        student_email ```Text Field```: The student's nullable email\n
        status ```Char Field```: The invoice's current status. This can be of either \"FULLY_PAID\", \"PENDING\", \"OVERDUE\", \"SUSPENDED\"
    """

    invoice_number = models.IntegerField(primary_key=True)
    preview_link = models.TextField()
    product_name = models.TextField() #Still need to add functionality for this! Should be short
    offenses = models.IntegerField() #Still need to add functionality for this!
    issue_date = models.DateField()
    due_date = models.DateField()
    total = models.FloatField()
    currency = models.CharField(max_length=50)
    contact_name = models.TextField()
    contact_email = models.EmailField()
    contact_phone_number = models.CharField(max_length=30, null=True)
    student_name = models.TextField(null=True)
    student_email = models.TextField(null=True)
    status = models.CharField(choices=[("PAID","PAID"), ("PENDING","PENDING"), ("OVERDUE", "OVERDUE"), ("SUSPENDED", "SUSPENDED")])

class Email(models.Model): 
    """
    Table for emails sent regarding overdue invoices

    ### Fields:
        email_id ```Auto Field```: Automatically generated ID for row, unrelated to Wix \n
        invoice ```Foreign Key```: Foreign Key corresponding to invoice table, sets self to "deleted" on foreign row deletion\n
        contact_id ```Char Field```: Contact ID of customer, allows us to get their contact information\n
        recipient_email ```Char Field```: Email of the recipient\n
        email_contents ```Text Field```: Contents of the email\n
        send_date ```Date & Time Field```: Date and time at which email was sent\n
    """

    email_id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET("deleted"))
    contact_id = models.CharField(max_length=250)
    recipient_email = models.CharField(max_length=320)
    email_contents = models.TextField()
    send_date = models.DateTimeField()

class EventLog(models.Model):
    """
    Table to record logs. Records both logs of events and logs of errors

    ### Fields:
        id ```Auto Field```: Automatically generated ID for row, unrelated to wix \n
        timestamp ```Date Time Field```: When this event was logged \n
        event_type ```Char Field```: The type of event that took place. (```INVOICE SENT```, ```INVOICE PAID```, ```INVOICE OVERDUE```, ```EMAIL SENT```, ```EMAIL OPENED```) \n
        error ```Boolean Field```: Whether or not an error took place during this event. Defaults to ```False```\n
        error_message ```Text Field```: Error message associated with the log. Defaults to ```null``` if not present\n
        json_data ```Text Field```: JSON Data associated with the log, useful when dealing with errors. Defaults to ```null``` if not available\n
        associated_invoice ```Foreign Key```: The invoice associated with this event. Sets self to "deleted" on foreign row deletion \n
        associated_invoice_id ```Integer Field```: The invoice id associated with this event. Useful when dealing with invoices that do not exist on our database, but exist on Wix database \n
        associated_email ```Foreign Key```: The email associated with the event. If this event did not involve an email, this is null. Sets self to "deleted" on foreign row deletion \n
        note ```Text Field```: A note associated with the row. Useful when trying to locate error, especially in case of unhandled exception \n
        line_number ```Integer Field``` The line at which this error took place.
    """
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    event_type = models.CharField(max_length=50, choices=[("INVOICE_SENT", "INVOICE_SENT"), ("INVOICE_PAID", "INVOICE_PAID"), ("INVOICE_OVERDUE", "INVOICE_OVERDUE"), ("EMAIL_SENT", "EMAIL_SENT"), ("EMAIL_OPENED", "EMAIL_OPENED"), ("DISCORD_BOT", "DISCORD_BOT")])
    error = models.BooleanField(default=False)
    error_type = models.CharField(max_length=250)
    error_message = models.TextField(null=True)
    json_data = models.TextField(null=True)
    associated_invoice = models.ForeignKey(Invoice, on_delete=models.SET("deleted"), null=True)
    associated_email = models.ForeignKey(Email, on_delete=models.SET("deleted"), null=True)
    line_number = models.IntegerField(default=-1) #Deprecate

    def save(self, *args, **kwargs):
        if self.error and not self.error_message: #Check if 'error' is True while error_message is null
            raise django.core.exceptions.ValidationError("Error message cannot be null if error is true") #Throw error
        super().save(*args, **kwargs) #Save row if no errors occur

class CancellationLogs(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    json_data = models.TextField()

class Ping(models.Model):
    #Discord ID
    id = models.TextField(primary_key=True)

class TestingLogs(models.Model):
    """
    TEMPORARY LOGGING
    """
    key = models.AutoField(primary_key=True)
    log = models.TextField()
    type = models.CharField(max_length=50)