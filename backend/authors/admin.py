from django.contrib import admin
from .models import *

class AuthorAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Hash the password if it has been set or changed
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Follow)
