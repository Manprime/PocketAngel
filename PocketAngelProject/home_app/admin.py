from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import *

# Register your models here.
User=get_user_model()
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model
    # These override the definitions on the base UserAdmin
# that reference specific fields on auth.User.
    list_display = ["name","email", "phone", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
    (None, {"fields": ["email", "password"]}),
    ("Personal info", {"fields": ["name","phone"]}),
    ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
    (
    None,
    {
    "classes": ["wide"],
    "fields": ["email", "phone", "password1", "password2"],
    },
    ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []






# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(Category)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(EMI)
admin.site.register(Budget)
admin.site.register(Alert)
admin.site.register(Report)






#Manual change in Django Admin Header Text
admin.site.site_header = "Pocket Angel Administration"
admin.site.site_title = "Pocket Angel Admin Portal"
admin.site.index_title = "Welcome to Pocket Angel!"
