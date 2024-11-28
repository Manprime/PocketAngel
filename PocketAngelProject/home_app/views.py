from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserCreationForm
from .forms import *
from .models import *
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
 
# Create views here.
def indexfunc(request):
    return render(request,'index.html')

@login_required(login_url='signin')
def dashboard(request):
    # Call the method to add due EMIs to expenses and create alerts
    add_due_emis_to_expenses()
    
    # Fetch alerts for the user
    alerts = Alert.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'alerts': alerts})


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
    return render(request, 'add_forms.html', {'category_form': form, 'form_type': 'category'})






@login_required(login_url='signin')
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST,user=request.user)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Set the logged-in user
            income.save()
            return redirect('income_list') 
         # Redirect to the income list view/dashboard 
         # here income_list is the name value from urls.py of app
    else:
        form = IncomeForm(user=request.user)
    return render(request, 'add_forms.html', {'income_form': form, 'form_type': 'income'})

@login_required(login_url='signin')
def income_list(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    #gives user specific incomes only
    #print(incomes)  # Debugging line to check the incomes queryset

    return render(request, 'income_list.html', {'incomes': incomes})



@login_required(login_url='signin')
def expense_list(request):
    #expenses = Expense.objects.all().order_by('-date')
    #this will give all expenses for all users so not used.
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expense_list.html', {'expenses': expenses})



@login_required(login_url='signin')
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST,user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  
            # Set the logged-in user, necessary to add object to specific user
            expense.save()
            return redirect('expense_list')  
           # Redirect to the Expense list view/ sow the list
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'add_forms.html',{'expense_form': form, 'form_type': 'expense'})









@login_required(login_url='signin')
def EMI_Form(request):
    if request.method == 'POST':
        form = EMIForm(request.POST)
        if form.is_valid():
            emi = form.save(commit=False)
            emi.user = request.user
            emi.save()
            return redirect('emi_list')
    else:
        form = EMIForm()

    return render(request, 'add_forms.html', {'add_emi': form, 'form_type': 'add_emi'})





@login_required(login_url='signin')
def emi_list(request):
    #expenses = Expense.objects.all().order_by('-date')
    #this will give all expenses for all users
    emi_lt = EMI.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'emi_list.html', {'emi_lst': emi_lt})
#'emi_lst' is varialble used in html template to access
# whereas 'emi_lt' contains all data objects









@login_required(login_url='signin')
def update_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)  # Ensure the user owns the income
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income updated successfully.')
            return redirect('income_list')  # Redirect to the income list view
    else:
        form = IncomeForm(instance=income)
    return render(request, 'add_forms.html', {'income_form': form, 'form_type': 'update_income'})

@login_required(login_url='signin')
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)  # Ensure the user owns the income
    income.delete()
    messages.success(request, 'Income deleted successfully.')
    return redirect('income_list') 


@login_required(login_url='signin')
def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)  
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('expense_list') 
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'add_forms.html', {'expense_form': form, 'form_type': 'update_expense'})

@login_required(login_url='signin')
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)  
    expense.delete()
    messages.success(request, 'Expense deleted successfully.')
    return redirect('expense_list') 



@login_required(login_url='signin')
def update_emi(request, emi_id):
    emi = get_object_or_404(EMI, id=emi_id, user=request.user)  
    if request.method == 'POST':
        form = EMIForm(request.POST, instance=emi)
        if form.is_valid():
            form.save()
            messages.success(request, 'EMI updated successfully.')
            return redirect('emi_list')  
    else:
        form = EMIForm(instance=emi)
    return render(request, 'add_forms.html', {'emi_form': form, 'form_type': 'update_emi'})

@login_required(login_url='signin')
def delete_emi(request,emi_id):
    emi = get_object_or_404(EMI, id=emi_id, user=request.user)  
    # Ensure the user owns the emi
    emi.delete()
    messages.success(request, 'Emi deleted successfully.')
    return redirect('emi_list') 



#function for adding emi to expense
def add_due_emis_to_expenses():
    today = timezone.now().date()
    due_emis = EMI.objects.filter(next_payment_date=today)

    # Create a default category for EMIs
    default_category, created = Category.objects.get_or_create(
        name='EMI(Expense)',  
        category_type=Category.EXPENSE  
    )

    for emi in due_emis:
        # Create an Expense object for each due EMI
        Expense.objects.create(
            user=emi.user,
            amount=emi.amount,
            category=default_category,  
            description=emi.description,
            date=today,
            is_fixed=True  
        )
        
        # Create an alert for the user
        Alert.objects.create(
            user=emi.user,
            message=f"Your EMI of {emi.amount} is due today."
        )

        # Update the next payment date for the EMI
        if emi.frequency == 'monthly':
            emi.next_payment_date += timezone.timedelta(days=30)
        elif emi.frequency == 'weekly':
            emi.next_payment_date += timezone.timedelta(weeks=1)
        elif emi.frequency == 'yearly':
            emi.next_payment_date += timezone.timedelta(days=365)
       
        emi.save()



@login_required(login_url='signin')
def alerts_list(request):
    alerts = Alert.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'alerts_list.html', {'alerts': alerts})


@login_required(login_url='signin')
def mark_alert_as_read(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id, user=request.user)
    alert.is_read = True
    alert.save()
    messages.success(request, 'Alert marked as read.')
    return redirect('alerts_list')
