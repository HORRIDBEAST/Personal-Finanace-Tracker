# Generated by Django 5.0.6 on 2024-05-21 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "finance_tracker",
            "0005_expense_budget_allocated_expense_budget_exceeded_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="expense",
            name="budget_allocated",
        ),
        migrations.RemoveField(
            model_name="expense",
            name="budget_exceeded",
        ),
        migrations.RemoveField(
            model_name="expense",
            name="budget_left",
        ),
    ]
