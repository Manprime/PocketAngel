from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source=models.CharField(max_length=50)
    date = models.DateField()
    
    def __str__(self):
        return self.user

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exp_name=models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
        return self.user
    
class Goals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_name=models.CharField(max_length=50)
    g_amount=models.DecimalField(max_digits=10, decimal_places=2)
    g_category=models.CharField(max_length=50)
    g_creationDate = models.DateField()
    g_deadline=models.DateField()
    
    def __str__(self):
        return self.user

