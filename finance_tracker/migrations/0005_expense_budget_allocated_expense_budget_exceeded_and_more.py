# Generated by Django 5.0.6 on 2024-05-21 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance_tracker", "0004_alter_income_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="budget_allocated",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name="expense",
            name="budget_exceeded",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name="expense",
            name="budget_left",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
