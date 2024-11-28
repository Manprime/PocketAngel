from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth import authenticate
from django.forms.widgets import SelectDateWidget
from datetime import datetime


class CustomSelectDateWidget(SelectDateWidget):
    def __init__(self, *args, **kwargs):
        # Set the range of years (e.g., from the current year to 20 years in the future)
        current_year = datetime.now().year
        self.years = range(current_year, current_year + 21)  # Adjust the range as needed
        super().__init__(*args, **kwargs)

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label="Password",
    widget=forms.PasswordInput)
    password2 = forms.CharField(
    label="Password confirmation", widget=forms.PasswordInput
    )


    class Meta:
        model = User
        fields = ["name","email", "phone"]
        widgets = {
            'phone': forms.NumberInput,
        
        }
       

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    



class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ["name","email", "password", "phone", "is_active",
        "is_admin"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','category_type']


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'description','category','date']
        
        widgets = {
            'date':forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Adjust rows and cols as needed
            
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        # Get the user from kwargs
        super().__init__(*args, **kwargs)  
        # Call the parent class's __init__ method
        if user:
            # Filter categories to only include those of type 'Income'
            self.fields['category'].queryset = Category.objects.filter(user=user, category_type=Category.INCOME)


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ( 'category','amount' ,'date','description','is_fixed')
        widgets = {
            'date':forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Adjust rows and cols as needed
        }
        # same in income ,thi shows userspecific category
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)  # Call the parent class's __init__ method
        if user:
            # Filter categories to only include those of type 'Expense'
            self.fields['category'].queryset = Category.objects.filter(user=user, category_type=Category.EXPENSE)





class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                self.add_error('email', 'Invalid email or password')
                self.add_error('password', 'Invalid email or password')




class EMIForm(forms.ModelForm):
    class Meta:
        model = EMI
        fields = ('amount', 'start_date', 'end_date', 'frequency', 'description', 'next_payment_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'}),
            'end_date': forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'}),
            'next_payment_date': forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        next_payment_date = cleaned_data.get('next_payment_date')

        # Check if next_payment_date is provided and it should
        #be within end_date
        if next_payment_date and start_date and end_date:
            if next_payment_date < start_date or next_payment_date > end_date:
                raise ValidationError("Next payment date must be between the start date and end date.")

        return cleaned_data



