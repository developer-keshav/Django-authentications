from django.contrib import admin

# Register your models here.
from .models import Hero,User

admin.site.register(Hero)
admin.site.register(User)
