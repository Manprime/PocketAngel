from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Expense,Income,UserProfile
from django.contrib.auth import get_user_model
User=get_user_model()

class ManualRegisterForm(UserCreationForm):
    #Manual Registartion form inherits from UserCreationForm,adds extra fields
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    

    class Meta:
        model = UserProfile
        fields = [ 'email', 'username', 'first_name', 'last_name', 'password1', 'password2']

class ManualAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))




class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source','date']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('exp_name', 'category','amount' ,'date')









