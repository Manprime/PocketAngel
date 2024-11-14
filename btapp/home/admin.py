from django.contrib import admin
from .models import *


#Manual change in Django Admin Header Text
admin.site.site_header = "Pocket Angel Administration"
admin.site.site_title = "Pocket Angel Admin Portal"
admin.site.index_title = "Welcome to Pocket Angel!"



# Register models to be visible in Administration
admin.site.register(UserProfile)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Goals)
