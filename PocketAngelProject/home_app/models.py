from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
    verbose_name="Email Address",
    max_length=255,
    unique=True,
    )
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","phone"]

    def __str__(self):
        return self.email
    

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
     # Simplest possible answer: Yes, always
        return True
    

    @property
    def is_staff(self):
        "Is the user a member of staff?"
    # Simplest possible answer: All admins are staff
        return self.is_admin
    
    def total_income(self):
        return sum([income.amount for income in self.income.all()]) if self.income.all() else 0
    def total_expense(self):
        return sum([expense.amount for expense in self.expenses.all()]) if self.expenses.all() else 0
    def total_savings(self):
        return self.total_income() - self.total_expense() if self.income.all() and self.expenses.all() else self.total_income()
    


class Category(models.Model):
    INCOME = 'Income'
    EXPENSE = 'Expense'
    CATEGORY_TYPES = [
    (INCOME, 'Income'),
    (EXPENSE, 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
    null=True,related_name='categories')
    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ({self.category_type})"
    

class Income(models.Model):
    user = models.ForeignKey(User,
    on_delete=models.CASCADE,related_name='income')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
    limit_choices_to={'category_type': 'Income'},related_name='income')
    description = models.TextField(blank=True, null=True,max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Idate: {self.date} - Name: {self.user.name} - Category: {self.category.name} - IAmount: {self.amount}  -  Description :{self.description}"
    
class Expense(models.Model):
    user = models.ForeignKey(User,
    on_delete=models.CASCADE,related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
    limit_choices_to={'category_type': 'Expense'},related_name='expenses')
    description = models.TextField(blank=True, null=True,max_length=100)
    date = models.DateField()
    is_fixed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Edate: {self.date} - Name: {self.user.name} - Category: {self.category.name} - EAmount: {self.amount}  - IsFixed:{self.is_fixed} -  Description :{self.description}"
    

class EMI(models.Model):
    #frequency added
    FREQUENCY_CHOICES = [
        ('one_time', 'One-Time'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('quarterly', 'Quarterly'),
        ('bi_weekly', 'Bi-Weekly'),
        ('semi_annually', 'Semi-Annually'),
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
        
    ]
    user = models.ForeignKey(User,
    on_delete=models.CASCADE,related_name='emis')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(help_text = "Please use the following format: <em>YYYY-MM-DD</em>.")
    frequency = models.CharField(max_length=20,choices=FREQUENCY_CHOICES) 
    # e.g., "Monthly"
    description = models.TextField(blank=True, null=True,max_length=100)
    next_payment_date = models.DateField()
    def __str__(self):
        return f"{self.user.name} - Amount {self.amount} - Frequency {self.frequency}- Start{self.start_date} - End{self.end_date}- NextPay{self.next_payment_date}- description{self.description}"
    

class Budget(models.Model):
    user = models.ForeignKey(User,
    on_delete=models.CASCADE,related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return f"{self.user.name} - {self.category.name} Budget {self.amount_limit}"
    

class Alert(models.Model):
    user = models.ForeignKey(User,
    on_delete=models.CASCADE,related_name='alerts')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Alert for {self.user.name}: {self.message[:30]}"
    

class Report(models.Model):
    user = models.ForeignKey(User,
    on_delete=models.CASCADE,related_name='reports')
    report_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    file_path = models.FileField(upload_to='reports/', blank=True,
    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Report for {self.user.name} - {self.report_type}"