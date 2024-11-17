from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from home_app import views as user_views

urlpatterns = [
    path('',user_views.indexfunc,name='home'),

    path('aboutus',user_views.about,name='aboutpage'),

    
    path('register',user_views.register,name='register'),

    path('signin',user_views.signin,name='signin'),

    
    path('signout',user_views.signout,name='signout'),

    path('income_list', user_views.income_list, name='income_list'),

    path('add_income', user_views.add_income, name='add_income'),
    #in LOGIN_REDIRECT_URL or in any URL specify the 'name' value in path

    path('add_category', user_views.add_category, name='add_category'),

    path('expense_list', user_views.expense_list, name='expense_list'),

    path('add_expense', user_views.add_expense, name='add_expense'),

]

