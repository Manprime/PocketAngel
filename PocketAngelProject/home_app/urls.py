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
    path('alerts/mark_as_read/<int:alert_id>/', user_views.mark_alert_as_read, name='mark_alert_as_read'),

    path('alerts_list',user_views.alerts_list, name='alerts_list'),
    path('signout',user_views.signout,name='signout'),

    path('income_list', user_views.income_list, name='income_list'),

    path('add_income', user_views.add_income, name='add_income'),
    #in LOGIN_REDIRECT_URL or in any URL specify the 'name' value in path

    path('add_category', user_views.add_category, name='add_category'),
    

    path('expense_list', user_views.expense_list, name='expense_list'),

    path('add_expense', user_views.add_expense, name='add_expense'),
    
    path('add_emi', user_views.EMI_Form, name='add_emi'),
    path('emi_list', user_views.emi_list, name='emi_list'),
   
    path('update_income/<int:income_id>/', user_views.update_income, name='update_income'),
    path('delete_income/<int:income_id>/', user_views.delete_income, name='delete_income'),

    path('update_expense/<int:expense_id>/', user_views.update_expense, name='update_expense'),
    path('delete_expense/<int:expense_id>/', user_views.delete_expense, name='delete_expense'),

    path('update_emi/<int:emi_id>/', user_views.update_emi, name='update_emi'),
    path('delete_emi/<int:emi_id>/', user_views.delete_emi, name='delete_emi'),

]