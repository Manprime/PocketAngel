from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserCreationForm
from .forms import *
from .models import Income,Expense
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def indexfunc(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

class CustomeLoginView(LoginView):
    template_name = 'signin.html'

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in.')
                return redirect('home')  # Redirect to the dashboard view
    else:
        form = LoginForm()

    return render(request, 'signin.html', {'form': form})



def signout(request):
    logout(request)
    context = {'message': 'Hello, world!'}
    return render(request, 'signout.html', context)
# Redirect to the login page after logout


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)

            return redirect('home')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)



@login_required(login_url='signin')
#when user is not logged in it will redirect to login_url='name'
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  # Set the logged-in user
            category.save()
            return redirect('add_category') 
         # Redirect to the income list view/dashboard 
         # here income_list is the name value from urls.py of app
    else:
        form = CategoryForm()
    return render(request, 'add_inc_exp.html', {'category_form': form, 'form_type': 'category'})


@login_required(login_url='signin')
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Set the logged-in user
            income.save()
            return redirect('income_list') 
         # Redirect to the income list view/dashboard 
         # here income_list is the name value from urls.py of app
    else:
        form = IncomeForm()
    return render(request, 'add_inc_exp.html', {'income_form': form, 'form_type': 'income'})

@login_required(login_url='signin')
def income_list(request):
    incomes = Income.objects.filter(user=request.user)
    #gives user specific incomes only
    return render(request, 'income_list.html', {'incomes': incomes})


@login_required(login_url='signin')
def expense_list(request):
    #expenses = Expense.objects.all().order_by('-date')
    #this will give all expenses for all users
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expense_list.html', {'expenses': expenses})

@login_required(login_url='signin')
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Set the logged-in user
            expense.save()
            return redirect('expense_list')  # Redirect to the Expense list view
    else:
        form = ExpenseForm()
    return render(request, 'add_inc_exp.html',{'expense_form': form, 'form_type': 'expense'})
