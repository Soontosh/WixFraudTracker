# Generated by Django 4.2.7 on 2023-11-05 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "invoice_number",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("subscription_id", models.CharField(max_length=250)),
                ("contact_id", models.CharField(max_length=250)),
                ("cycle", models.IntegerField()),
                ("title", models.TextField()),
                ("issue_date", models.DateField()),
                ("due_date", models.DateField()),
                ("total", models.FloatField()),
                ("currency", models.CharField(max_length=50)),
                ("preview_link", models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Email",
            fields=[
                ("email_id", models.AutoField(primary_key=True, serialize=False)),
                ("contact_id", models.CharField(max_length=250)),
                ("recipient_email", models.CharField(max_length=320)),
                ("email_contents", models.TextField()),
                ("send_date", models.DateTimeField()),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=models.SET("deleted"), to="wix_app.invoice"
                    ),
                ),
            ],
        ),
    ]
