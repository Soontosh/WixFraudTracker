# Generated by Django 4.2.7 on 2023-11-07 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wix_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestingLogs",
            fields=[
                ("key", models.AutoField(primary_key=True, serialize=False)),
                ("log", models.TextField()),
            ],
        ),
    ]
