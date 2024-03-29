# Generated by Django 4.2.7 on 2023-11-18 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wix_app", "0013_alter_eventlog_line_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ping",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name="eventlog",
            name="event_type",
            field=models.CharField(
                choices=[
                    ("INVOICE_SENT", "INVOICE_SENT"),
                    ("INVOICE_PAID", "INVOICE_PAID"),
                    ("INVOICE_OVERDUE", "INVOICE_OVERDUE"),
                    ("EMAIL_SENT", "EMAIL_SENT"),
                    ("EMAIL_OPENED", "EMAIL_OPENED"),
                    ("DISCORD_BOT", "DISCORD_BOT"),
                ],
                max_length=50,
            ),
        ),
    ]
