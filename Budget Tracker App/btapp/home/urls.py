from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from home import views as user_views

urlpatterns = [
    path('',user_views.indexfunc,name='home'),

    path('aboutus',user_views.about,name='aboutpage'),

    


    path('income_list', user_views.income_list, name='income_list'),

    path('add_income', user_views.add_income, name='add_income'),
    #in LOGIN_REDIRECT_URL or in any URL specify the 'name' value in path

    path('expense_list', user_views.expense_list, name='expense_list'),

    path('add_expense', user_views.add_expense, name='add_expense'),


    path('register',user_views.register,name='register'),

    path('signin',user_views.CustomeLoginView.as_view(),name='signin'),
    #template_name is an attribute of as_view from LoginView class, so it cannot be changed
    
   #path('signout',auth_views.LogoutView.as_view(template_name='signout.html'),name='signout'),
   
   
   path('signout',user_views.signout,name='signout'),
]