from django.dispatch import Signal
from django.dispatch import receiver
from .models import Alert

budget_alert_signal = Signal()

@receiver(budget_alert_signal)
def create_alert(sender, user, message, **kwargs):
    Alert.objects.create(user=user, message=message)