# tasks.py
from background_task import background
from django.utils import timezone
from .models import *

@background(schedule=10)  # Check every minute
def process_emi_payments():
    today = timezone.now().date()
    emis = EMI.objects.filter(next_payment_date=today)

    for emi in emis:
        # Update last payment date
        emi.last_payment_date = today
        emi.save()

        # Create an expense record
        default_category, created = Category.objects.get_or_create(
            name='EMI(Expense)',  
            category_type=Category.EXPENSE
        )

        Expense.objects.create(
            user=emi.user,
            amount=emi.amount,
            category=default_category,  
            description=emi.description,
            date=today,
            is_fixed=True
        )

        alert_message=f"EMI payment of {emi.amount} has been processed."

    
        # Update the next payment date based on the frequency
        if emi.next_payment_date < emi.end_date:
            if emi.frequency == 'monthly':
                emi.next_payment_date += timezone.timedelta(days=30)
            elif emi.frequency == 'weekly':
                emi.next_payment_date += timezone.timedelta(weeks=1)
            elif emi.frequency == 'yearly':
                emi.next_payment_date += timezone.timedelta(days=365)
            elif emi.frequency == 'quarterly':
                emi.next_payment_date += timezone.timedelta(days=90)
            elif emi.frequency == 'semi_annually':
                emi.next_payment_date += timezone.timedelta(days=182)
            elif emi.frequency == 'daily':
                emi.next_payment_date += timezone.timedelta(days=1)
            elif emi.frequency == 'bi_weekly':
                emi.next_payment_date += timezone.timedelta(weeks=2)

            emi.save()
