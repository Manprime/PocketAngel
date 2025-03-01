from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from home_app import views as user_views

urlpatterns = [
    path('',user_views.indexfunc,name='home'),
    path('aboutus',user_views.about,name='aboutpage'),
    path('dashboard',user_views.dashboard,name='dashboard'),
   

    
    path('register',user_views.register,name='register'),
    path('signin',user_views.signin,name='signin'),
    path('signout',user_views.signout,name='signout'),



    path('mark_as_read/<int:alert_id>/', user_views.mark_alert_as_read, name='mark_alert_as_read'),
    path('alerts_list',user_views.alerts_list, name='alerts_list'),
    path('alerts_delete/<int:alert_id>',user_views.delete_alert, name='delete_alert'),
    
    path('report_delete/<int:report_id>',user_views.delete_report, name='delete_report'),
    
    path('reports',user_views.reports_list, name='reports'),
    path('generate_report', user_views.generate_report, name='generate_report'),



    path('income_list', user_views.income_list, name='income_list'),
    path('add_income', user_views.add_income, name='add_income'),
    #in LOGIN_REDIRECT_URL or in any URL specify the 'name' value in this path("") to call the path



    path('add_category', user_views.add_category, name='add_category'),
    

    path('expense_list', user_views.expense_list, name='expense_list'),
    path('add_expense', user_views.add_expense, name='add_expense'),


    
    path('add_emi', user_views.EMI_Form, name='add_emi'),
    path('emi_list', user_views.emi_list, name='emi_list'),
    path('confirm_emi/<int:emi_id>/',user_views.confirm_emi_payment,name='confirm_emi_pay'),




    path('set_budget', user_views.set_budget, name='set_budget'),
    path('set_overall_budget', user_views.set_overall_budget, name='set_overall_budget'),
    path('budgetlist', user_views.get_budget, name='budgetlist'),
    path('overallbudgetlist', user_views.get_overall_budget, name='overallbudgetlist'),

    path('update_overall_budget/<int:overall_budget_id>/', user_views.update_overall_budget, name='update_overall_budget'),
    path('delete_overall_budget/<int:overall_budget_id>/', user_views.delete_overall_budget, name='delete_overall_budget'),

    path('update_budget/<int:budget_id>/', user_views.update_budget, name='update_budget'),
    path('delete_budget/<int:budget_id>/', user_views.delete_budget, name='delete_budget'),


    path('update_income/<int:income_id>/', user_views.update_income, name='update_income'),
    path('delete_income/<int:income_id>/', user_views.delete_income, name='delete_income'),

    path('update_expense/<int:expense_id>/', user_views.update_expense, name='update_expense'),
    path('delete_expense/<int:expense_id>/', user_views.delete_expense, name='delete_expense'),

    path('update_emi/<int:emi_id>/', user_views.update_emi, name='update_emi'),
    path('delete_emi/<int:emi_id>/', user_views.delete_emi, name='delete_emi'),




    path('goal_list', user_views.goal_list, name='goal_list'),
    path('add_goal', user_views.add_goal, name='add_goal'),
    path('update_goal/<int:goal_id>/', user_views.update_goal, name='update_goal'),
    path('delete_goal/<int:goal_id>/', user_views.delete_goal, name='delete_goal'),

]