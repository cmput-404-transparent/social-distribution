from django.contrib import admin
from .models import Friend
from .models import *

# Register your models here.
admin.site.register(Friend)
admin.site.register(Post)