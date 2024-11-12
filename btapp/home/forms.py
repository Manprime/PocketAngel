from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Expense,Income

class ManualRegisterForm(UserCreationForm):
    #Manual Registartion form inherits from UserCreationForm,adds extra fields
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']



class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source','date']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('exp_name', 'category','amount' ,'date')