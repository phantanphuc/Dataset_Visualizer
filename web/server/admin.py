from django.contrib import admin

from .models import BoundingBox, Image
# Register your models here.
admin.site.register(BoundingBox)
admin.site.register(Image)