from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('reset-balance/', views.reset_balance, name='reset_balance'),
     
    path('set_budget/', views.set_budget, name='set_budget'),
    path('view_budgets/', views.view_budgets, name='view_budgets'),
    path('edit_budget/<int:budget_id>/', views.edit_budget, name='edit_budget'),
    path('delete_budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),
]
