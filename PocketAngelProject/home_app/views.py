from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from .models import *
from .signal import budget_alert_signal
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from decimal import Decimal # Using  Decimal for the float value to avaid error while comparing in budgets

#for pdf report generation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch

# Create views here.
User = get_user_model()
def indexfunc(request):
    return render(request,'index.html')

@login_required(login_url='signin')
def dashboard(request):
    check_emi_login(request)

    checkoverallbudget(request)
    checkbudget(request)
    new_alerts = Alert.objects.filter(user=request.user, is_read=False)  
    has_new_alerts = new_alerts.exists() 
    new_alert_count =new_alerts.count()
    if has_new_alerts==True:
        messages.info(request, f"You have {new_alert_count} new alerts.")
    return render(request, 'dashboard.html')


def about(request):
    return render(request,'about.html')

"""class CustomeLoginView(LoginView):
    template_name = 'signin.html'"""

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
                return redirect('dashboard')
            
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
#when user is not logged in it will redirect to login_url='signin' i.e signinpage
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  
            # Set the logged-in user
            category.save()
            messages.success(request,"New Category Created.")
            Alert.objects.create(user=request.user,message=f"New Category '{category}'created.")
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
            messages.success(request, 'Income has been added.')
            return redirect('income_list') 
         # Redirect to the income list view/dashboard 
         # here income_list is the name value from urls.py of app
    else:
        form = IncomeForm(user=request.user)
    return render(request, 'add_forms.html', {'income_form': form, 'form_type': 'income'})



@login_required(login_url='signin')
def update_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)  # Ensure the user owns the income
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            checkoverallbudget(request)
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
def income_list(request):
    user = request.user
    incomes = Income.objects.filter(user=user)
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_id = request.GET.get('category')
    
    if start_date:
        incomes = incomes.filter(date__gte=start_date)  
        #  __gte  is for greater than or equal to
    if end_date:
        incomes = incomes.filter(date__lte=end_date)   
         # __lte  is for less than or equal to
    if category_id:
        incomes = incomes.filter(category_id=category_id)

    categories = Category.objects.filter(user=user,category_type='Income')

    return render(request, 'income_list.html', {
        'incomes': incomes,
        'categories': categories,
    })






@login_required(login_url='signin')
def expense_list(request):
    user = request.user
    expenses = Expense.objects.filter(user=user)

   
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_id = request.GET.get('category')

    
    if start_date:
        expenses = expenses.filter(date__gte=start_date)  
        
    if end_date:
        expenses = expenses.filter(date__lte=end_date)   
      
    if category_id:
        expenses = expenses.filter(category_id=category_id)

   
    categories = Category.objects.filter(user=user, category_type='Expense')

   
    return render(request, 'expense_list.html', {
        'expenses': expenses,
        'categories': categories,
    })


@login_required(login_url='signin')
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST,user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  
            # Set the logged-in user, necessary to add object to specific user
            expense.save()
            checkbudget(request)
            messages.success(request, 'Expense has been added.')
            return redirect('expense_list')  
           # Redirect to the Expense list view/ sow the list
            

    
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'add_forms.html',{'expense_form': form, 'form_type': 'expense'})


@login_required(login_url='signin')
def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)  
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            checkbudget(request)
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


@login_required(login_url='login')
def check_emi_login(request):
    today = timezone.now().date()  
    em_is_due = EMI.objects.filter(user=request.user, next_payment_date__lte=today)

    for emi in em_is_due:
        if emi.next_payment_date <= today and emi.next_payment_date <= emi.end_date:
            alert_messg=f"Your EMI is for {emi.amount} is pending. Today,is the payment day for next installment."
            messages.warning(request,alert_messg)
            if  not Alert.objects.filter(user=request.user, message=alert_messg).exists():
                Alert.objects.create(
                user=emi.user,
                message=alert_messg
                              )

            emi.save()

    return redirect('emi_list')



def confirm_emi_payment(request, emi_id):
    today = timezone.now().date()
    emi = get_object_or_404(EMI, id=emi_id)
    
    emi.last_payment_date = today
    
    default_category, created = Category.objects.get_or_create(
    name='EMI(Expense)',  
    category_type=Category.EXPENSE  )

    #expense oibject created
    Expense.objects.create(
        user=emi.user,
        amount=emi.amount,
        category=default_category,  
        description=emi.description,
        date=timezone.now().date(),
        is_fixed=True )
    alert_message=None

    
    

    if emi.end_date<today:
        alert_message=f"EMI payment of {emi.amount} ended on {emi.end_date}."
        messages.info(request,f"EMI payment of {emi.amount} ended on {emi.end_date}.")
    if emi.next_payment_date!= None:
        if emi.next_payment_date==emi.end_date:
            alert_message=f"The last installment of EMI amount {emi.amount} for {emi.description} ends on {emi.end_date}."
            messages.info(request,alert_message)
    if emi.next_payment_date < emi.end_date:
        messages.info(request,f"EMI payment of {emi.amount} added to Expense List.")
        if emi.frequency == 'monthly':
            emi.next_payment_date += timezone.timedelta(days=31)
        elif emi.frequency == 'weekly':
            emi.next_payment_date += timezone.timedelta(weeks=1)
        elif emi.frequency == 'yearly':
            emi.next_payment_date += timezone.timedelta(days=365)
        elif emi.frequency == 'quaterly':
            emi.next_payment_date += timezone.timedelta(days=90)
        elif emi.frequency == 'semi_annually':
            emi.next_payment_date += timezone.timedelta(days=182)
        elif emi.frequency == 'daily':
            emi.next_payment_date += timezone.timedelta(days=1)
        elif emi.frequency == 'bi_weekly':
            emi.next_payment_date += timezone.timedelta(weeks=2)
        else:
            pass

    
    if emi.end_date<emi.next_payment_date:
        alert_message=f"EMI payment of {emi.amount} has been paid. No more dues left."
        messages.info(request,f"EMI payment of {emi.amount} has no more dues left.")
        emi.next_payment_date=None

    if alert_message and not Alert.objects.filter(user=request.user, message=alert_message).exists():
        Alert.objects.create(
            user=emi.user,
            message=alert_message
        )

    emi.save()

    return redirect('emi_list')

    



@login_required(login_url='signin')
def EMI_Form(request):
    if request.method == 'POST':
        form = EMIForm(request.POST)
        if form.is_valid():
            emi = form.save(commit=False)
            emi.user = request.user
            emi.save()
            messages.success(request, 'EMI has been added.')
            return redirect('emi_list')
    else:
        form = EMIForm()

    return render(request, 'add_forms.html', {'add_emi': form, 'form_type': 'add_emi'})


@login_required(login_url='signin')
def emi_list(request):
    emi_lt = EMI.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'emi_list.html', {'emi_lst': emi_lt})
#'emi_lst' is varialble used in html template to access
# whereas 'emi_lt' contains all data objects


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






@login_required(login_url='signin')
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user  
            # Set the logged-in user
            budget.save()
            checkbudget(request)
            messages.success(request, 'Budget has been added.')
            return redirect('budgetlist') 
         # Redirect to the budgetlist in urls.py ->path 
         
    else:
        form = BudgetForm()
    return render(request, 'add_forms.html', {'budget_form': form, 'form_type': 'budget_form'})

@login_required(login_url='signin')
def get_budget(request):
    budget=Budget.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'budgets.html', {
        'getbudget': budget       
    })
    


@login_required(login_url='signin')
def update_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)  
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully.')
            checkbudget(request)
            return redirect('budgetlist')  
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'add_forms.html', {'budget_form': form, 'form_type': 'update_budget'})

@login_required(login_url='signin')
def delete_budget(request,budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)  
    # Ensure the user created the budget 
    budget.delete()
    messages.success(request, 'Budget deleted successfully.')
    return redirect('budgetlist') 



@login_required(login_url='signin')
def set_overall_budget(request):
    if request.method == 'POST':
        form = OverallBudgetForm(request.POST)
        if form.is_valid():
            overall_budget = form.save(commit=False)
            overall_budget.user = request.user  # Set the logged-in user
            overall_budget.save()
            #print(overall_budget)debug
            messages.success(request, 'OverallBudget has been added.')
            return redirect('overallbudgetlist') 
         # Redirect to the budget list view/dashboard 

         
    else:
        form =OverallBudgetForm()
    return render(request, 'add_forms.html', {'overall_budget': form, 'form_type': 'overall_budget'})


@login_required(login_url='signin')
def get_overall_budget(request):
    overall_budget=OverallBudget.objects.filter(user=request.user).order_by('-start_date')
    #print(overall_budget)
    return render(request,'budgets.html',{'get_overall_budget':overall_budget})


@login_required(login_url='signin')
def update_overall_budget(request, overall_budget_id):
    overall_budget = get_object_or_404(OverallBudget, id=overall_budget_id, user=request.user)  
    if request.method == 'POST':
        form = OverallBudgetForm(request.POST, instance=overall_budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Overall Budget updated successfully.')
            return redirect('budgetlist')  
    else:
        form = OverallBudgetForm(instance=overall_budget)
    return render(request, 'add_forms.html', {'overall_budget': form, 'form_type': 'update_overall_budget'})

@login_required(login_url='signin')
def delete_overall_budget(request,overall_budget_id):
    overall_budget = get_object_or_404(OverallBudget, id=overall_budget_id, user=request.user)  
    # Ensure the user created the budget 
    overall_budget.delete()
    messages.success(request, 'Overall_Budget deleted successfully.')
    return redirect('budgetlist') 




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


@login_required(login_url='signin')
# it is a function to check so return statement is avoided
def checkbudget(request):
    expenses = Expense.objects.filter(user=request.user).select_related('category').order_by('-date')
    budgets = Budget.objects.filter(user=request.user).select_related('category').order_by('-start_date')

    # dictionary holds budget limits by category
    budget_limits = {}
    for bud in budgets:
        budget_limits[(bud.category.id, bud.start_date, bud.end_date)] = bud.amount_limit

    # Iterates expenses and checks against budget limits
    for exp in expenses:
        key = (exp.category.id, exp.date, exp.date)  
        #a key for the current expense
        for (cat_id, start_date, end_date), amount_limit in budget_limits.items():
            if cat_id == exp.category.id and start_date <= exp.date <= end_date:
               
                alert_message = ""
                if exp.amount == amount_limit:
                    alert_message = f"*Expense of {exp.amount} for category '{exp.category}' having date '{exp.date}' has reached the budget limit of {amount_limit}.\nThis budget limit ends on {end_date}."
                elif exp.amount > amount_limit:
                    alert_message = f"*Expense of {exp.amount} for category '{exp.category}' exceeds the budget limit of {amount_limit}.\nThis budget limit ends on {end_date}."
                elif exp.amount >= amount_limit * Decimal('0.9'):
                    alert_message = f"*Expense of {exp.amount} for category '{exp.category}' has reached 90% of the budget limit of {amount_limit}.\nThis budget limit ends on {end_date}."

                # Create alert if message is not empty and does not already exist
                if alert_message:
                    if not Alert.objects.filter(user=request.user, message=alert_message).exists():
                        Alert.objects.create(user=request.user, message=alert_message)
                        messages.error(request,alert_message)
                        budget_alert_signal.send(sender=checkbudget, user=request.user, message=alert_message)

    



@login_required(login_url='signin')
def delete_alert(request,alert_id):
    alert = get_object_or_404(Alert, id=alert_id, user=request.user)  
    alert.delete()
    messages.success(request, 'Alert deleted.')
    return redirect('alerts_list')






@login_required(login_url='signin')
# it is a function to check so return statement is avoided
def checkoverallbudget(request):
    # Get all expenses and incomes for the user
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)  

    # Get all budgets for the user
    budgets = OverallBudget.objects.filter(user=request.user).order_by('-start_date')

    # Create a dictionary to hold budget limits by category
    budget_limits = {}
    for bud in budgets:
        budget_limits[(bud.category, bud.start_date, bud.end_date)] = bud.amount_limit

   
    # Check against budget limits
    for (cat, start_date, end_date), amount_limit in budget_limits.items():
        if start_date <= timezone.now().date() <= end_date: 
            
            if cat == 'Expense':
                total_amount = User.total_income(request.user)
            elif cat == 'Income':
                total_amount = User.total_income(request.user)
            else:
                continue  

           
            alert_message = ""
            if total_amount == amount_limit:
                alert_message = f"*Total {cat} of {total_amount} has reached the budget limit of {amount_limit}.\nThis limit ends on {end_date}."
            elif total_amount > amount_limit:
                alert_message = f"*Total {cat} of {total_amount} exceeds the budget limit of {amount_limit}.\nThis limit ends on {end_date}."
            elif total_amount >= (amount_limit * 0.9):
                alert_message = f"*Total {cat} of {total_amount} has reached 90% of the budget limit of {amount_limit}.\nThis limit ends on {end_date}."

            # Create alert if message is not empty and does not already exist
            if alert_message:
                if not Alert.objects.filter(user=request.user, message=alert_message).exists():
                    Alert.objects.create(user=request.user, message=alert_message)
                    messages.error(request,alert_message)
    




@login_required(login_url='signin')
def generate_report(request):
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
    #a response object and the content type to PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="financial_report.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    def add_table(title, data):
        styles = getSampleStyleSheet()
        heading = Paragraph('PocketAngel', styles['Title'])
        elements.append(heading)
        title_paragraph = Paragraph(title, styles['Title'])
        elements.append(title_paragraph)

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        elements.append(Paragraph("<br/>", styles['Normal']))
        elements.append(PageBreak())  


    # Income
    income_data = [["Date", "Amount", "Category", "Description"]]
    incs=Income.objects.filter(user=request.user)
    for income in incs:
        income_data.append([income.date.strftime('%d-%m-%Y'), income.amount, income.category, income.description])

    # Expense
    expense_data = [["Date", "Amount","Category","Is Fixed", "Description"]]  # Table header
    for expense in Expense.objects.filter(user=request.user):
        expense_data.append([expense.date.strftime('%d-%m-%Y'), expense.amount, expense.category ,expense.is_fixed, expense.description])

    # Budget
    budget_data = [["Category", "Amount Limit","Start Date","End Date"]]  # Table header
    for budget in Budget.objects.filter(user=request.user):
        budget_data.append([budget.category.name, budget.amount_limit,budget.start_date.strftime('%d-%m-%Y'),budget.end_date.strftime('%d-%m-%Y')])

    # EMI Section
    emi_data = [["Amount", "Frequency", "Start Date","Ends On", "Last Paid On","Next Payment On","Description"]]  # Table header
    for emi in EMI.objects.filter(user=request.user):
        emi_data.append([emi.amount, emi.frequency, emi.start_date.strftime('%d-%m-%Y'),emi.end_date.strftime('%d-%m-%Y'),emi.last_payment_date,emi.next_payment_date.strftime('%d-%m-%Y'),emi.description])

    # Overall Budget Section
    overall_budget_data = [["Category", "Amount Limit", 'Start Date',"Ends on"]]  # Table header
    for overall_budget in OverallBudget.objects.filter(user=request.user):
        overall_budget_data.append([overall_budget.category, overall_budget.amount_limit, overall_budget.start_date.strftime('%d-%m-%Y'), overall_budget.end_date.strftime('%d-%m-%Y')])

    
    if report_type == "i":
        add_table("Your Income List", income_data)
    elif report_type == "ex":
        add_table("Expenses", expense_data)
    elif report_type == "em":
        add_table("EMIs", emi_data)
    elif report_type == "bud":
        add_table("Budgets", budget_data)
    elif report_type == "overbud":
        add_table("Overall Budgets", overall_budget_data)
    elif report_type == "Monthly":
        time = timezone.now()
        current_month = time.month-1
        current_year = time.year

        income_current_month = Income.objects.filter(user=request.user, date__month=current_month, date__year=current_year)
        expense_current_month = Expense.objects.filter(user=request.user, date__month=current_month, date__year=current_year)

        inc_data = [["Date", "Amount", "Category", "Description"]]
        for income in income_current_month:
            inc_data.append([income.date.strftime('%d-%m-%Y'), income.amount, income.category, income.description])
        
      
        exp_data = [["Date", "Amount", "Category", "Is Fixed", "Description"]]  # Table header
        for expense in expense_current_month:
            exp_data.append([expense.date.strftime('%d-%m-%Y'), expense.amount, expense.category, expense.is_fixed, expense.description])
        
        e_data = [["Amount", "Frequency", "Start Date","Ends On", "Last Paid On","Next Payment On","Description"]]  # Table header
        for emi in EMI.objects.filter(user=request.user,end_date__month=current_month, end_date__year=current_year):
            e_data.append([emi.amount, emi.frequency, emi.start_date.strftime('%d-%m-%Y'),emi.end_date.strftime('%d-%m-%Y'),emi.last_payment_date,emi.next_payment_date.strftime('%d-%m-%Y'),emi.description])
        
        add_table("Your Income for last Month", inc_data)
        add_table("Your Expenses for last Month", exp_data)
        add_table("Your EMI for last Month", e_data)


    elif report_type == "Yearly":
        time = timezone.now()
        last_year = time.year-1

        income_last_year = Income.objects.filter(user=request.user, date__year=last_year)
        expense_last_year = Expense.objects.filter(user=request.user, date__year=last_year)

        incy_data = [["Date", "Amount", "Category", "Description"]]
        for income in income_last_year:
            incy_data.append([income.date.strftime('%d-%m-%Y'), income.amount, income.category, income.description])
        
      
        expy_data = [["Date", "Amount", "Category", "Is Fixed", "Description"]]  # Table header
        for expense in expense_last_year:
            expy_data.append([expense.date.strftime('%d-%m-%Y'), expense.amount, expense.category, expense.is_fixed, expense.description])
        
        ey_data = [["Amount", "Frequency", "Start Date","Ends On", "Last Paid On","Next Payment On","Description"]]  # Table header
        for emi in EMI.objects.filter(user=request.user, start_date__year=last_year):
            ey_data.append([emi.amount, emi.frequency, emi.start_date.strftime('%d-%m-%Y'),emi.end_date.strftime('%d-%m-%Y'),emi.last_payment_date,emi.next_payment_date.strftime('%d-%m-%Y'),emi.description])
        
        add_table(f"Your Income for {last_year} ", incy_data)
        add_table(f"Your Expenses for {last_year}", expy_data)
        add_table(f"Your EMI for last {last_year}", ey_data)

    else:
        add_table("Your Overall Budgets", overall_budget_data)
        add_table("Your Income List", income_data)
        add_table("Your Expenses", expense_data)
        add_table("Your EMIs", emi_data)
        add_table("Your Budgets", budget_data)

    # Build the PDF
    pdf.build(elements)

    return response