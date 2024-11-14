from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **other_fields)




#models
class UserProfile(AbstractUser):
    #used for custom user model
    email = models.EmailField(unique=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

   



class Income(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source=models.CharField(max_length=50)
    date = models.DateField()
    
    def __str__(self):
        return f'{self.user.email}: {self.source} - {self.amount} - {self.date}'
    

class Expense(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    exp_name=models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
       return f'{self.user.email}: {self.exp_name} - {self.category} - {self.amount} - {self.date}'
    
class Goals(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    goal_name=models.CharField(max_length=50)
    g_amount=models.DecimalField(max_digits=10, decimal_places=2)
    g_category=models.CharField(max_length=50)
    g_creationDate = models.DateField()
    g_deadline=models.DateField()
    
    def __str__(self):
        #to return instances as string
        return f'{self.user.email}: {self.goal_name} - {self.g_category} - {self.g_amount} - {self.g_creationDate} - {self.g_deadline}'

