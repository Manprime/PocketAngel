from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
class HomeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home_app'
    def ready(self):
        import home_app.signal
        # Connect the post_migrate signal to the schedule_task function
        post_migrate.connect(schedule_task)

@receiver(post_migrate)
def schedule_task(sender, **kwargs):
    if sender.name == 'home_app':  # Ensure this runs only for your app
        from .tasks import my_background_task
        my_background_task()  # Schedule the background task
        
        
        

