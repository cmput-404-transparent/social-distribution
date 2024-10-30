from django.contrib import admin
from .models import *

class AuthorAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Hash the password if it has been set or changed
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        
        # Save the object first to get the ID
        super().save_model(request, obj, form, change)

        # Automatically set the host and page fields if they are not provided
        if not obj.host:
            obj.host = f"http://localhost:3000/api"
        if not obj.page:
            obj.page = f"{obj.host}/authors/{obj.id}"
        
        # Save again to update the host and page fields
        obj.save()

admin.site.register(Author, AuthorAdmin)
admin.site.register(Follow)
