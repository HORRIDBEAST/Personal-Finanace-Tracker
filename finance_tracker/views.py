from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Income, Expense, Balance, Budget
from .forms import IncomeForm, ExpenseForm, BudgetForm
from django.db.models import Sum
from django.http import JsonResponse
import json
from decimal import Decimal


def serialize_transactions(transactions):
    serialized_transactions = []
    for transaction in transactions:
        if isinstance(transaction, Income):
            serialized_transactions.append({
                'description': transaction.description,
                'transaction_type': 'Income',
                'date': transaction.date.isoformat(),
                'amount': float(transaction.amount),  # Convert Decimal to float
                'tag': ''  # or any default value if Income does not have a tag
            })
        elif isinstance(transaction, Expense):
            serialized_transactions.append({
                'description': transaction.description,
                'transaction_type': 'Expense',
                'date': transaction.date.isoformat(),
                'amount': float(transaction.amount),  # Convert Decimal to float
                'tag': transaction.tag
            })
    return serialized_transactions

@login_required
def dashboard(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or Decimal(0)

    spending_data = []
    for expense in expenses:
        category = expense.tag
        found = False
        for i, (cat, amt) in enumerate(spending_data):
            if cat == category:
                spending_data[i] = (cat, float(amt) + float(expense.amount))  # Convert Decimal to float
                found = True
                break
        if not found:
            spending_data.append((category, float(expense.amount)))  # Convert Decimal to float

    transactions = list(incomes) + list(expenses)
    budgets = Budget.objects.filter(user=request.user)

    budget_data = []
    for budget in budgets:
        spent = expenses.filter(tag=budget.category).aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
        budget_data.append({
            'category': budget.category,
            'budget': float(budget.amount),  # Convert Decimal to float
            'actual': float(spent)  # Convert Decimal to float
        })

    context = {
        'balance': float(total_income - total_expenses),  # Convert Decimal to float
        'total_income': float(total_income),  # Convert Decimal to float
        'total_expenses': float(total_expenses),  # Convert Decimal to float
        'incomes': incomes,
        'expenses': expenses,
        'spending_data': json.dumps(spending_data),
        'transactions': json.dumps(serialize_transactions(transactions)),
        'budgets': budgets,
        'budget_data': json.dumps(budget_data)
    }

    return render(request, 'finance_tracker/dashboard.html', context)

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            balance, created = Balance.objects.get_or_create(user=request.user)
            balance.amount += Decimal(str(income.amount)) # Convert float to Decimal
            balance.save()
            messages.success(request, 'Income added successfully')
            return redirect('dashboard')
    else:
        form = IncomeForm()

    return render(request, 'finance_tracker/add_income.html', {'form': form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            balance, created = Balance.objects.get_or_create(user=request.user)
            balance.amount -= Decimal(str(expense.amount))
            balance.save()
            messages.success(request, 'Expense added successfully')
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'finance_tracker/add_expense.html', {'form': form})

@login_required
def reset_balance(request):
    balance, created = Balance.objects.get_or_create(user=request.user)
    balance.amount = 0
    balance.save()
    Income.objects.filter(user=request.user).delete()
    Expense.objects.filter(user=request.user).delete()
    messages.success(request, 'Balance reset successfully')
    return redirect('dashboard')

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    budget_progress = []
    for budget in budgets:
        spent = expenses.filter(tag=budget.category).aggregate(Sum('amount'))['amount__sum'] or 0
        progress = (spent / budget.amount) * 100 if budget.amount > 0 else 0
        budget_progress.append({
            'id': budget.id,
            'category': budget.category,
            'budget': budget.amount,
            'spent': spent,
            'progress': progress
        })

    context = {
        'budgets': budgets,
        'budget_progress': budget_progress
    }
    return render(request, 'finance_tracker/budget_list.html', context)

@login_required
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget added successfully')
            return redirect('dashboard')
    else:
        form = BudgetForm()
    return render(request, 'finance_tracker/set_budget.html', {'form': form})

@login_required
def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully')
            return redirect('view_budgets')
    else:
        form = BudgetForm(instance=budget)
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'finance_tracker/edit_budget.html', {'form': form})

def view_budgets(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'finance_tracker/view_budgets.html', {'budgets': budgets})


@login_required
def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully')
        return redirect('view_budgets')  # Redirect to budget_list view
    else:
        return redirect('view_budgets')  # Redirect to budget_list view



