from django.contrib import admin
from . import models

admin.site.register(models.Post)
admin.site.register(models.User)
admin.site.register(models.Genre)

# Register your models here.