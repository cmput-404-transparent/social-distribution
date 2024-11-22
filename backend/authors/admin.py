from django.contrib import admin
from .models import *
from django import forms

def approve_users(modeladmin, request, queryset):
    for author in queryset:
        if not author.is_approved:
            author.is_approved = True
            author.save()
            
approve_users.short_description = "Approve selected users"

class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ['require_user_approval']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_approved', 'is_staff', 'is_active']
    actions = [approve_users]

    '''
    source: ChatGPT (OpenAI)
    prompt: "in django is there a way for when the form data is pulled, to clear the password
            field of Author model so you can't see the password?"
    date: October 30, 2024
    '''
    def get_form(self, request, obj=None, **kwargs):
        # Get the default form
        form = super().get_form(request, obj, **kwargs)

        # Use PasswordInput and clear the initial password field
        if obj and request.method == "GET":  # Only hide if editing an existing author
            form.base_fields['password'].widget = forms.PasswordInput(render_value=False)
        
            # Clear password field on display
            form.base_fields['password'].initial = None

        form.base_fields['password'].required = False
        form.base_fields['password'].help_text = "Leave blank unless changing the password."

        return form
    
    def save_model(self, request, obj, form, change):

        if not change:
            super().save_model(request, obj, form, change)

        # If password is provided, hash it; otherwise, retain the old password
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        elif change:  # For editing an existing user, preserve the old password
            obj.password = Author.objects.get(id=obj.id).password

        # Automatically set the host and page fields if they are not provided
        if not obj.host:
            obj.host = "http://localhost:8000/api"
        if not obj.page:
            obj.page = f"{obj.host}/authors/{obj.id}"
        
        # Save the changes
        obj.save()

# Register RemoteNode in the admin panel
# class RemoteNodeAdmin(admin.ModelAdmin):
#     list_display = ['url', 'username', 'password']

admin.site.register(Author, AuthorAdmin)
admin.site.register(Follow)
admin.site.register(SiteConfiguration, SiteConfigurationAdmin)
admin.site.register(RemoteNode)  
