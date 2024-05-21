from django import forms
from .models import Income,Budget, Expense
from .categories import CATEGORY_CHOICES
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['description', 'amount', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date', 'tag']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount']
        widgets = {
            'category': forms.Select(choices=[
                ('Food', 'Food'),
                ('Clothing', 'Clothing'),
                ('Entertainment', 'Entertainment'),
                ('Fuel', 'Fuel'),
                ('Education', 'Education'),
                ('Monthly Bills', 'Monthly Bills'),
                ('Miscellaneous', 'Miscellaneous'),
            ])
        }